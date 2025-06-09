from core.config import FilterType


def match_industry_icp_prompt(company_description: str, items: list, items_count: int):
    formatted_items = "\n".join(f"- {item}" for item in items)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE INDUSTRIES LIST:
    {formatted_items}

    TASK:
    You are a business analyst specializing in company classification. Analyze the COMPANY DESCRIPTION above and identify UP TO {items_count} industries from the AVAILABLE INDUSTRIES LIST that MOST ACCURATELY DESCRIBE WHAT THIS COMPANY DOES.

    ANALYSIS INSTRUCTIONS:
    1. First, understand the company's core products, services, and business model.
    2. Then, identify which industries from the list BEST MATCH the company's PRIMARY ACTIVITIES (not their customers).
    3. Focus on what the company itself does - its actual operations, products, and services.
    4. Pay close attention to specific technologies, domains, and market sectors mentioned in the description.
    5. Look for industries that directly describe the company's primary business function.
    6. BE HIGHLY CRITICAL - only include industries with clear evidence or very strong inference from the description.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select industries EXCLUSIVELY from the 'AVAILABLE INDUSTRIES LIST' provided above. Do not invent, modify, or suggest any industries not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {items_count} industries, but ONLY include industries that genuinely match. If fewer than {items_count} industries match, return fewer. If none match well, return an empty array.
    3. **EXACT COPY:** Copy the selected industries precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **COMPANY FOCUS:** Select industries that describe WHAT THE COMPANY ITSELF DOES, not who its customers are.
    5. **CONFIDENCE THRESHOLD:** Only include industries with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of accurately describing the company.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {items_count} strings.
    - Example with matches: ["item from list 1", "item from list 2", "item from list 3"]
    - Example with no good matches: []
    """


def match_country_icp_prompt(
    company_description: str, countries: list, countries_count: int
):
    formatted_countries = "\n".join(f"- {country}" for country in countries)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE COUNTRIES LIST:
    {formatted_countries}

    TASK:
    You are a global business analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {countries_count} countries from the AVAILABLE COUNTRIES LIST that are EXPLICITLY MENTIONED or DIRECTLY RELEVANT to this company's operations, headquarters, or primary markets.

    ANALYSIS APPROACH:
    1. First, identify any countries or regions EXPLICITLY MENTIONED in the description.
    2. Then, look for geographic information that strongly implies specific countries:
       - Headquarters location
       - Primary market regions mentioned (like "Europe" or "North America")
       - Specific country/regional offices mentioned
       - Founder or company origin information
    3. Only include countries that have DIRECT EVIDENCE or VERY STRONG INFERENCE in the description.
    4. Do NOT include countries just because they might be potential markets without explicit evidence.
    5. BE HIGHLY CRITICAL - prefer returning fewer or no countries rather than making tenuous connections.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select countries EXCLUSIVELY from the 'AVAILABLE COUNTRIES LIST' provided above. Do not invent, modify, or suggest any countries not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {countries_count} countries, but ONLY include countries with substantial evidence. If fewer than {countries_count} countries have evidence, return fewer. If none have strong evidence, return an empty array.
    3. **EXACT COPY:** Copy the selected countries precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **EVIDENCE REQUIRED:** Only select countries with direct evidence or very strong inference. Do not select additional countries simply to reach the count limit.
    5. **CONFIDENCE THRESHOLD:** Only include countries with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being directly relevant.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {countries_count} strings.
    - Example with matches: ["united states", "united kingdom", "germany"]
    - Example with no good matches: []
    """


def match_technology_icp_prompt(
    company_description: str, technologies: list, technologies_count: int
):
    formatted_technologies = "\n".join(f"- {tech}" for tech in technologies)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE TECHNOLOGIES LIST:
    {formatted_technologies}

    TASK:
    You are a technology analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {technologies_count} technologies from the AVAILABLE TECHNOLOGIES LIST that the company MOST LIKELY USES OR DEVELOPS as part of its core products and services.

    ANALYSIS APPROACH:
    1. First, identify what technology products or services this company likely creates, maintains, or heavily utilizes.
    2. Look for technologies that:
       - Are explicitly mentioned in the description
       - Would be essential to deliver the company's core products/services
       - Align with the company's described technical focus
       - Are fundamental to the company's industry sector
    3. For software companies, prioritize their core development technologies and platforms.
    4. For hardware companies, prioritize key hardware technologies and relevant software systems.
    5. Focus on technologies the company itself would use, not what their customers might use.
    6. BE HIGHLY CRITICAL - only include technologies with clear evidence or very strong inference.

    SELECTION CRITERIA:
    1. Direct Evidence: Technologies explicitly mentioned in the description
    2. Core Functionality: Technologies essential to the company's main products/services
    3. Industry Standard: Technologies standard in the company's sector
    4. Technical Domain: Technologies aligned with the company's technical domain
    5. Development Focus: Technologies central to the company's development work

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select technologies EXCLUSIVELY from the 'AVAILABLE TECHNOLOGIES LIST' provided above. Do not invent, modify, or suggest any technologies not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {technologies_count} technologies, but ONLY include technologies with substantial evidence. If fewer than {technologies_count} technologies have good evidence, return fewer. If none have strong evidence, return an empty array.
    3. **EXACT COPY:** Copy the selected technologies precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **COMPANY USAGE:** Identify technologies that the COMPANY ITSELF would use or develop, not technologies their customers would use.
    5. **CONFIDENCE THRESHOLD:** Only include technologies with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {technologies_count} strings.
    - Example with matches: ["technology from list 1", "technology from list 2"]
    - Example with no good matches: []
    """


def match_job_title_prompt(company_description: str, jobs: list, jobs_count: int):
    formatted_jobs = "\n".join(f"- {job}" for job in jobs)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE JOB TITLES LIST:
    {formatted_jobs}

    TASK:
    You are an organizational structure analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {jobs_count} job titles from the AVAILABLE JOB TITLES LIST that are MOST RELEVANT to the company's CORE BUSINESS FUNCTIONS and LEADERSHIP NEEDS.

    ANALYSIS INSTRUCTIONS:
    1. First, understand the company's primary business domain, technical focus, and operational model.
    2. Identify job titles that would be ESSENTIAL for a company with this specific business profile.
    3. Prioritize executive and leadership roles that align with the company's industry and scale.
    4. Consider technical leadership roles that match the company's technological focus.
    5. Include specialized roles only if they are central to the company's core business (not for every potential department).
    6. BE HIGHLY CRITICAL - only include job titles with clear relevance to the company's specific business model.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select job titles EXCLUSIVELY from the 'AVAILABLE JOB TITLES LIST' provided above. Do not invent, modify, or suggest any job titles not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {jobs_count} job titles, but ONLY include roles with substantial relevance. If fewer than {jobs_count} job titles are clearly relevant, return fewer. If none are strongly relevant, return an empty array.
    3. **EXACT COPY:** Copy the selected job titles precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **BUSINESS ALIGNMENT:** Focus on roles that align with the company's specific business model and industry, not generic roles.
    5. **CONFIDENCE THRESHOLD:** Only include job titles with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being essential to the company.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {jobs_count} strings.
    - Example with matches: ["job title from list 1", "job title from list 2"]
    - Example with no good matches: []
    """


def match_state_prompt(company_description: str, states: list, states_count: int):
    formatted_states = "\n".join(f"- {state}" for state in states)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE STATES LIST:
    {formatted_states}

    TASK:
    You are a location analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {states_count} states/provinces from the AVAILABLE STATES LIST that are EXPLICITLY MENTIONED or have DIRECT EVIDENCE of being relevant to the company's operations.

    ANALYSIS INSTRUCTIONS:
    1. First, identify any states/provinces EXPLICITLY MENTIONED in the description.
    2. Look for location-specific information that strongly implies certain states/provinces:
       - Headquarters location details
       - Office location information
       - Regional operation centers mentioned
       - Specific markets highlighted at the state/province level
    3. Only include states/provinces with DIRECT EVIDENCE in the description.
    4. Do NOT include states/provinces simply because they might be potential markets without explicit evidence.
    5. BE HIGHLY CRITICAL - prefer returning fewer or no states rather than making tenuous connections.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select states/provinces EXCLUSIVELY from the 'AVAILABLE STATES LIST' provided above. Do not invent, modify, or suggest any locations not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {states_count} states/provinces, but ONLY include locations with substantial evidence. If fewer than {states_count} states have evidence, return fewer. If none have strong evidence, return an empty array.
    3. **EXACT COPY:** Copy the selected states/provinces precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **EVIDENCE REQUIRED:** Only select states/provinces with direct evidence or very strong inference. Do not select additional states simply to reach the count limit.
    5. **CONFIDENCE THRESHOLD:** Only include states with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being relevant.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {states_count} strings.
    - Example with matches: ["state from list 1", "state from list 2"]
    - Example with no good matches: []
    """


def match_city_prompt(company_description: str, cities: list, cities_count: int):
    formatted_cities = "\n".join(f"- {city}" for city in cities)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE CITIES LIST:
    {formatted_cities}

    TASK:
    You are a corporate location analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {cities_count} cities from the AVAILABLE CITIES LIST that are EXPLICITLY MENTIONED or have STRONG EVIDENCE of being relevant to the company's operations or headquarters.

    ANALYSIS INSTRUCTIONS:
    1. First, identify any cities EXPLICITLY MENTIONED in the company description.
    2. Look for location-specific information that strongly implies certain cities:
       - Headquarters location details
       - Office location information
       - Founding location information
       - Major operation centers mentioned
    3. Only include cities with DIRECT EVIDENCE or VERY STRONG IMPLICATION in the description.
    4. Do NOT include cities just because they might be potential markets without explicit evidence.
    5. BE HIGHLY CRITICAL - prefer returning fewer or no cities rather than making tenuous connections.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select cities EXCLUSIVELY from the 'AVAILABLE CITIES LIST' provided above. Do not invent, modify, or suggest any cities not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {cities_count} cities, but ONLY include cities with substantial evidence. If fewer than {cities_count} cities have evidence, return fewer. If none have strong evidence, return an empty array.
    3. **EXACT COPY:** Copy the selected cities precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **EVIDENCE REQUIRED:** Only select cities with direct evidence or very strong implication. Do not select additional cities simply to reach the count limit.
    5. **CONFIDENCE THRESHOLD:** Only include cities with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being relevant locations.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {cities_count} strings.
    - Example with matches: ["city from list 1", "city from list 2"]
    - Example with no good matches: []
    """


def match_fundings_prompt(
    company_description: str, fundings: list, fundings_count: int
):
    formatted_fundings = "\n".join(f"- {funding}" for funding in fundings)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE FUNDING TYPES LIST:
    {formatted_fundings}

    TASK:
    You are a venture capital and funding analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {fundings_count} funding types from the AVAILABLE FUNDING TYPES LIST that are MOST APPROPRIATE for this company's current stage and business model.

    ANALYSIS INSTRUCTIONS:
    1. First, assess the company's current stage of development and maturity level.
    2. Consider key indicators such as:
       - Product development stage
       - Market traction and customer base
       - Revenue status and business model maturity
       - Team size and organizational structure
       - Industry sector and growth potential
    3. Match these indicators to appropriate funding types that align with the company's needs.
    4. Consider the natural progression of funding stages (e.g., seed → series A → series B).
    5. Include alternative funding types (grants, debt, etc.) if they align with the company's profile.
    6. BE HIGHLY CRITICAL - only include funding types with clear relevance to the company's stage.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select funding types EXCLUSIVELY from the 'AVAILABLE FUNDING TYPES LIST' provided above. Do not invent, modify, or suggest any funding types not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {fundings_count} funding types, but ONLY include types with substantial relevance. If fewer than {fundings_count} funding types are clearly relevant, return fewer. If none are strongly relevant, return an empty array.
    3. **EXACT COPY:** Copy the selected funding types precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **STAGE ALIGNMENT:** Focus on funding types that align with the company's current stage, not potential future stages.
    5. **CONFIDENCE THRESHOLD:** Only include funding types with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being appropriate for the company.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {fundings_count} strings.
    - Example with matches: ["seed", "series a", "venture capital"]
    - Example with no good matches: []
    """


def match_employees_prompt(
    company_description: str, employee_ranges: list, ranges_count: int
):
    formatted_ranges = "\n".join(f"- {range}" for range in employee_ranges)

    return f"""
    COMPANY DESCRIPTION:
    '{company_description}'

    AVAILABLE EMPLOYEE RANGES LIST:
    {formatted_ranges}

    TASK:
    You are a company size and growth analyst. Analyze the COMPANY DESCRIPTION above and identify UP TO {ranges_count} employee ranges from the AVAILABLE EMPLOYEE RANGES LIST that MOST ACCURATELY REFLECT the company's current size and scale.

    ANALYSIS INSTRUCTIONS:
    1. First, assess the company's current stage and scale of operations.
    2. Consider key indicators such as:
       - Product/service complexity and scope
       - Market presence and customer base size
       - Revenue scale and business model maturity
       - Team structure and organizational complexity
       - Industry sector and typical company sizes
    3. Look for explicit mentions of team size, departments, or organizational structure.
    4. Consider the company's stage of development and typical employee counts for that stage.
    5. Evaluate the scope of operations and required workforce to support it.
    6. BE HIGHLY CRITICAL - only include ranges with clear evidence or very strong inference.

    CRITICAL RULES (MUST Follow):
    1. **MANDATORY SOURCE:** Select employee ranges EXCLUSIVELY from the 'AVAILABLE EMPLOYEE RANGES LIST' provided above. Do not invent, modify, or suggest any ranges not present in that exact list.
    2. **QUALITY OVER QUANTITY:** Return UP TO {ranges_count} ranges, but ONLY include ranges with substantial evidence. If fewer than {ranges_count} ranges are clearly relevant, return fewer. If none are strongly relevant, return an empty array.
    3. **EXACT COPY:** Copy the selected ranges precisely as they appear in the list, including spelling, capitalization, and spacing. Do NOT alter them in any way.
    4. **CURRENT SIZE:** Focus on the company's CURRENT size, not potential future growth.
    5. **CONFIDENCE THRESHOLD:** Only include ranges with a confidence level of 7/10 or higher.
    6. **CONFIDENCE RANKING:** Order your selections from highest to lowest confidence of being appropriate for the company's current size.

    RESPONSE FORMAT:
    - Return ONLY a single JSON array containing 0 to {ranges_count} strings.
    - Example with matches: ["11-50", "51-200"]
    - Example with no good matches: []
    """


def match_prompt(
    company_description: str, items: list, items_count: int, matcher_type: FilterType
):
    """
    Selects the appropriate prompt based on the matcher type.

    Args:
        company_description: Description of the company
        items: List of available items (industries, countries, technologies)
        items_count: Number of items to include in the result
        matcher_type: Type of the matcher ('industries', 'countries', 'technologies')

    Returns:
        The formatted prompt string for the specific matcher type
    """
    if matcher_type == FilterType.INDUSTRIES:
        return match_industry_icp_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.COUNTRIES:
        return match_country_icp_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.TECHNOLOGIES:
        return match_technology_icp_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.JOB_TITLE:
        return match_job_title_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.STATE:
        return match_state_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.CITY:
        return match_city_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.FUNDINGS:
        return match_fundings_prompt(company_description, items, items_count)
    elif matcher_type == FilterType.EMPLOYEES:
        return match_employees_prompt(company_description, items, items_count)
    else:
        raise ValueError(f"Unknown matcher type: {matcher_type}")
