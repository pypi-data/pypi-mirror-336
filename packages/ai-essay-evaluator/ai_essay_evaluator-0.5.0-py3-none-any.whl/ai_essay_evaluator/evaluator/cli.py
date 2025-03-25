import asyncio
import time
from pathlib import Path

import typer

from .processor import process_csv

evaluator_app = typer.Typer(help="CLI for grading student responses.")


@evaluator_app.command()
def grader(
    input_file: Path = typer.Option(..., help="Path to input CSV"),
    export_folder: Path = typer.Option(..., help="Folder to export results"),
    export_file_name: str = typer.Option(..., help="Base file name for output"),
    scoring_format: str = typer.Option(..., help="Scoring format: extended, item-specific, short"),
    story_folder: Path = typer.Option(..., help="Folder containing story text files"),
    rubric_folder: Path = typer.Option(..., help="Folder containing rubric text files"),
    question_file: Path = typer.Option(..., help="Path to question text file"),
    api_key: str = typer.Option(..., help="OpenAI API Key"),
    openai_project: str = typer.Option(None, help="OpenAI project ID"),
    ai_model: str = typer.Option(None, help="Custom AI model to use"),
    log: bool = typer.Option(True, help="Enable logging"),
    cost_analysis: bool = typer.Option(True, help="Perform cost analysis"),
    passes: int = typer.Option(1, help="Number of times to process the CSV"),
    merge_results: bool = typer.Option(True, help="Merge results if multiple passes"),
    show_progress: bool = typer.Option(True, help="Display progress during processing"),
    calculate_totals: bool = typer.Option(True, help="Calculate scoring totals for each student"),
):
    start_time = time.time()

    # Determine the AI model if not provided
    if ai_model is None:
        model_mapping = {
            "extended": "ft:gpt-4o-mini-2024-07-18:securehst::B6YDFKyO",
            "item-specific": "ft:gpt-4o-mini-2024-07-18:securehst::B72LJHWZ",
            "short": "ft:gpt-4o-mini-2024-07-18:securehst::B79Kzt5H",
        }
        ai_model = model_mapping.get(scoring_format)

    typer.echo(f"Starting essay evaluation with {scoring_format} format...")

    asyncio.run(
        process_csv(
            input_file,
            export_folder,
            export_file_name,
            scoring_format,
            openai_project,
            api_key,
            ai_model,
            log,
            cost_analysis,
            passes,
            merge_results,
            story_folder,
            rubric_folder,
            question_file,
            start_time,
            show_progress,
            calculate_totals,
        )
    )

    duration = time.time() - start_time
    typer.echo(f"Processing completed in {duration:.2f} seconds.")
