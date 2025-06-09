from typing import Dict
from pydantic import BaseModel, ConfigDict, Field
from core.config import JobStatus

class RabbitMQSendResponse(BaseModel):
    job_id: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }
    )


class JobStatusResponse(BaseModel):
    status: JobStatus
    total_records: int
    description: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": JobStatus.PENDING,
                "total_records": 1,
                "description": "The job is in progress",
            }
        }
    )

class RobotCommandRequest(BaseModel):
    text: str = Field(..., description="Text command for the robot to execute")


class RobotCommandResponse(BaseModel):
    command_result: dict = Field(..., description="Result of the robot command execution")
    token_usage: Dict[str, int] = Field(..., description="Token usage statistics")
    cost: float = Field(..., description="Cost of the command execution in USD")
