from fastapi import APIRouter, HTTPException, status

from schemas.models import (
    RobotCommandRequest,
    RobotCommandResponse,
    RabbitMQSendResponse,
    JobStatusResponse
)
from api.dependencies import RabbitMQClientDep
from api.dependencies.common import RequestIdDep
from core.config import Exchanges, JobStatus


router = APIRouter(prefix="/robot", tags=["robot"])

ROBOT_COMMAND_EXPECTED_MESSAGES = 1


@router.post(
    "/command",
    response_model=RabbitMQSendResponse,
    summary="Send a command to the robot"
)
async def send_robot_command(
    request: RobotCommandRequest,
    request_id: RequestIdDep,
    rabbitmq: RabbitMQClientDep,
):
    """
    Send a text command to the robot for execution.
    
    This is an asynchronous API that returns a job ID. Check the job status using the
    status endpoint and retrieve results using the results endpoint once the job is complete.
    """
    try:
        job_id = request_id
        message_body = request.model_dump()
        job_id = await rabbitmq.send_message(
            exchange=Exchanges.ROBOT_COMMAND, body=message_body, message_id=job_id
        )

        return RabbitMQSendResponse(
            job_id=job_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/command/status",
    response_model=JobStatusResponse,
    summary="Get robot command status"
)
async def get_robot_command_status(job_id: str, rabbitmq_client: RabbitMQClientDep):
    """Get the status of a robot command job"""
    processed = await rabbitmq_client.check_queue_messages_were_processed(
        job_id, ROBOT_COMMAND_EXPECTED_MESSAGES
    )
    if processed is None:
        return JobStatusResponse(
            status=JobStatus.FAILED,
            total_records=ROBOT_COMMAND_EXPECTED_MESSAGES,
            description="Job was already retrieved or wrong message id.",
        )

    if not processed:
        return JobStatusResponse(
            status=JobStatus.PENDING,
            total_records=ROBOT_COMMAND_EXPECTED_MESSAGES,
            description="Robot command is in progress. Please check back later for results.",
        )

    return JobStatusResponse(
        status=JobStatus.COMPLETED,
        total_records=ROBOT_COMMAND_EXPECTED_MESSAGES,
        description="Robot command is completed. Please check the results.",
    )


@router.get(
    "/command/results",
    summary="Get robot command results",
    description="""
    Retrieve the results of a completed robot command job.

    Results are only available for completed jobs.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Results returned successfully",
            "content": {
                "application/json": {
                    "example": {
                        "result": "Robot successfully moved to position X and performed the requested action.",
                        "token_usage": {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150},
                        "cost": 0.0005
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Job not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Job not found",
                        "message": "Job with id 550e8400-e29b-41d4-a716-446655440000 already retrieved or wrong message id.",
                        "request_id": "550e8400-e29b-41d4-a716-446655440000",
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Job not completed",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Job not completed",
                        "message": "Robot command with id 550e8400-e29b-41d4-a716-446655440000 is in progress. Please check back later for results.",
                        "request_id": "550e8400-e29b-41d4-a716-446655440000",
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Internal server error",
                        "message": "Error retrieving job results for id 550e8400-e29b-41d4-a716-446655440000: Some error",
                        "request_id": "550e8400-e29b-41d4-a716-446655440000",
                    }
                }
            },
        },
    },
    response_model=RobotCommandResponse,
)
async def get_robot_command_results(
    job_id: str,
    request_id: RequestIdDep,
    rabbitmq_client: RabbitMQClientDep,
):
    """
    Get the results of a completed robot command job.

    Args:
        job_id (str): The unique identifier of the job
        request_id (str): Unique request identifier
        rabbitmq_client (RabbitMQClient): RabbitMQ client for retrieving results

    Returns:
        RobotCommandResponse: Results of the robot command execution

    Raises:
        HTTPException: If the job is not found or not completed
    """
    try:
        processed = await rabbitmq_client.check_queue_messages_were_processed(
            job_id, ROBOT_COMMAND_EXPECTED_MESSAGES
        )

        if processed is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Job not found",
                    "message": f"Robot command with id {job_id} was already retrieved or wrong message id.",
                    "request_id": request_id,
                },
            )

        if not processed:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Job not completed",
                    "message": f"Robot command with id {job_id} is in progress. Please check back later for results.",
                    "request_id": request_id,
                },
            )

        results = await rabbitmq_client.get_messages(job_id)

        result = results[0]
        if "headers" in result and "error" in result["headers"]:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Message processing error",
                    "message": f"Message processing error for id {job_id}: {result}",
                    "request_id": request_id,
                },
            )

        return RobotCommandResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": f"Error retrieving job results for id {job_id}: {str(e)}",
                "request_id": request_id,
            },
        ) 
