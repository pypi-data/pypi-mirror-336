import asyncio
import atexit
import json
import logging
import os
import re
from datetime import datetime

import openai
import pandas as pd
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# Configure logging to file with timestamp
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_directory, f"ai_evaluator_{timestamp}.log")

# Create file handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler],
)

# Set httpx logger to WARNING level to suppress INFO messages
logging.getLogger("httpx").setLevel(logging.WARNING)

# Get your application logger
logger = logging.getLogger(__name__)


# Function to close the log handlers properly
def close_logging_handlers():
    """Close all logging handlers to ensure files are properly closed."""
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
    for logger_name in logging.Logger.manager.loggerDict:
        logger_obj = logging.getLogger(logger_name)
        for handler in logger_obj.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()


# Register the function to run at exit
atexit.register(close_logging_handlers)

# Retry settings for handling OpenAI API errors & Pydantic validation failures
RETRY_SETTINGS = {
    "stop": stop_after_attempt(5),
    "wait": wait_exponential(multiplier=1, min=2, max=10),
    "retry": retry_if_exception_type((openai.OpenAIError, ValidationError)),
}


class ExtendedScoringResponse(BaseModel):
    idea_development_score: int
    idea_development_feedback: str
    language_conventions_score: int
    language_conventions_feedback: str


class StandardScoringResponse(BaseModel):
    score: int
    feedback: str


def parse_reset_time(reset_str: str) -> int:
    """
    Parses a reset time string (e.g. "1s" or "6m0s") and returns the number of seconds.
    """
    minutes = 0
    seconds = 0
    m_match = re.search(r"(\d+)m", reset_str)
    if m_match:
        minutes = int(m_match.group(1))
    s_match = re.search(r"(\d+)s", reset_str)
    if s_match:
        seconds = int(s_match.group(1))
    return minutes * 60 + seconds


@retry(**RETRY_SETTINGS)
async def call_openai_parse(messages: list[dict[str, str]], model: str, client: AsyncOpenAI, scoring_format: str):
    response_format = ExtendedScoringResponse if scoring_format == "extended" else StandardScoringResponse
    max_completion_tokens = 2000

    response = await client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        temperature=0,
        response_format=response_format,
        max_tokens=max_completion_tokens,
    )

    # Rate limiting check based on request limits:
    headers = getattr(response, "headers", {})  # Assume headers are available on the response
    remaining_requests = int(headers.get("x-ratelimit-remaining-requests", 1))
    if remaining_requests <= 0:
        reset_str = headers.get("x-ratelimit-reset-requests", "1s")
        wait_time = parse_reset_time(reset_str)
        logger.info(f"Rate limit for requests exhausted. Sleeping for {wait_time} seconds...")
        await asyncio.sleep(wait_time)

    # You can add similar checks for tokens using x-ratelimit-remaining-tokens if needed.

    structured = extract_structured_response(response, scoring_format)
    usage = response.usage
    return structured, usage


async def process_with_openai(
    df, ai_model, api_key, stories, rubrics, question, scoring_format, openai_project, progress_callback=None
):
    client = AsyncOpenAI(
        api_key=api_key,
        project=openai_project,
        timeout=30,
        max_retries=3,
    )
    semaphore = asyncio.Semaphore(100)

    async def async_log(level, msg):
        await asyncio.to_thread(logger.log, level, msg)

    async def process_row(index, row):
        async with semaphore:
            prompt = generate_prompt(row, scoring_format, stories, rubrics, question)
            try:
                result = await call_openai_parse(prompt, ai_model, client, scoring_format)
                if progress_callback:
                    await progress_callback()
                return index, result
            except ValidationError as e:
                await async_log(
                    logging.ERROR,
                    f"Validation failed for row index {index}, "
                    f"Local Student ID {row.get('Local Student ID', 'N/A')}: {e}. "
                    f"Row content: {row.to_dict()}",
                )
                if progress_callback:
                    await progress_callback()
                return index, (get_default_response(scoring_format), {})
            except Exception as e:
                await async_log(
                    logging.ERROR,
                    f"Error processing row index {index}, "
                    f"Local Student ID {row.get('Local Student ID', 'N/A')}: {e}. "
                    f"Row content: {row.to_dict()}",
                )
                if progress_callback:
                    await progress_callback()
                return index, (get_default_response(scoring_format), {})

    batch_size = 500
    results = []
    for start in range(0, len(df), batch_size):
        batch = df.iloc[start : start + batch_size]
        tasks = [process_row(idx, row) for idx, row in batch.iterrows()]
        for coro in asyncio.as_completed(tasks):
            idx, res = await coro
            results.append((idx, res))

    # Build a dictionary mapping each original index to its structured result and gather usage details
    structured_results_dict = {}
    usage_list = []
    for idx, (structured, usage) in results:
        structured_results_dict[idx] = structured
        if usage:
            usage_list.append(usage)

    # Create a DataFrame from the structured results and reindex it to match the original DataFrame order
    structured_df = pd.DataFrame.from_dict(structured_results_dict, orient="index")
    structured_df = structured_df.reindex(df.index)

    return pd.concat([df, structured_df], axis=1), usage_list


def generate_prompt(row, scoring_format, story_dict, rubric_text, question_text):
    student_response = row["Student Constructed Response"]
    if scoring_format == "extended":
        extended_system_content = (
            "four keys: 'idea_development_score' (an integer), 'idea_development_feedback' (a string), "
            "'language_conventions_score' (an integer), and 'language_conventions_feedback' (a string)"
        )
    else:
        extended_system_content = "two keys: 'score' (an integer) and 'feedback' (a string)"

    # Normalize language format
    tested_language = row["Tested Language"].strip().lower()
    grade_level = row["Enrolled Grade Level"]

    # Language instructions
    if tested_language == "spanish":
        language_instruction = (
            "El estudiante ha realizado la prueba en español. "
            "Proporcione la retroalimentación y la evaluación en español."
        )
    else:
        language_instruction = "The student has taken the test in English. Provide feedback and evaluation in English."

    # Structured prompt to reduce token usage
    user_prompt = {
        "grade_level": f"Grade {grade_level}",
        "language": tested_language.capitalize(),
        "stories": story_dict,
        "question": question_text,
        "rubric": rubric_text,
        "evaluation_guidance": (
            f"Analyze the student's response in a grade-appropriate manner. "
            f"Ensure feedback aligns with expectations for Grade {grade_level}. "
            f"{language_instruction}"
        ),
        "student_response": student_response,
    }

    user_message = {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)}

    messages = [
        {
            "role": "system",
            "content": (
                f"AI Grader: Evaluate student responses based on rubric. "
                f"Your task is to assess the student's answer using the provided story, question, and rubric. "
                f"If the student's response is a verbatim or near-verbatim copy of the provided story or prompt, "
                f"assign a score of 0 and provide feedback indicating that copying occurred. "
                f"Return your evaluation strictly as a JSON object with exactly {extended_system_content}. "
                f"Do not include any additional text or commentary. Ensure that the JSON output is valid and parsable."
            ),
        },
        user_message,
    ]
    return messages


@retry(**RETRY_SETTINGS)
def extract_structured_response(response, scoring_format):
    response_text = response.choices[0].message.content.strip()

    try:
        structured_output = json.loads(response_text)
        if scoring_format == "extended":
            return ExtendedScoringResponse(**structured_output).model_dump()
        else:
            return StandardScoringResponse(**structured_output).model_dump()
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        return get_default_response(scoring_format)


def get_default_response(scoring_format):
    if scoring_format == "extended":
        return {
            "idea_development_score": 0,
            "idea_development_feedback": "Invalid response",
            "language_conventions_score": 0,
            "language_conventions_feedback": "Invalid response",
        }
    else:
        return {"score": 0, "feedback": "Invalid response"}
