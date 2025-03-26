"""Example usage of dumb-datasets package."""

import os
from pathlib import Path
from typing import Any

from datasets import disable_progress_bar
from loguru import logger

from dumb_datasets import (
    dataset_schema,
    load_dataset,
    merge_intermediate_data,
    push_intermediate_data,
    save_dataset_sample,
    set_api_token,
    set_cache_dir,
)


def basic_example() -> None:
    """Basic usage example."""
    # disable progress bars for cleaner output
    disable_progress_bar()

    # set up cache dir if needed
    if "DUMB_DATASETS_CACHE_DIR" in os.environ:
        set_cache_dir(os.environ["DUMB_DATASETS_CACHE_DIR"])

    # load a dataset (using squad as example)
    logger.info("Loading dataset...")
    dataset = load_dataset("squad", split="train")

    # get dataset info
    info = dataset.info()
    logger.info(f"Dataset has {info['num_rows']} examples")
    logger.info(f"Features: {list(info['features'].keys())}")

    # save a sample to inspect
    output_dir = Path("examples")
    output_dir.mkdir(exist_ok=True)
    save_dataset_sample(dataset, output_dir / "squad_samples.json", num_examples=5)

    # transform some fields
    logger.info("Transforming dataset...")
    processed = dataset.map_columns(lambda x: x.lower(), ["question", "context"])

    # access raw underlying dataset
    raw_dataset = processed.raw
    logger.info(f"First example question: {raw_dataset[0]['question']}")


def multiple_splits_example() -> None:
    """Example with multiple splits."""
    # load a dataset with multiple splits
    logger.info("Loading multi-split dataset...")
    dataset = load_dataset("glue", name="mnli")

    # get schema for all splits
    schema = dataset_schema(dataset)
    for split_name, split_info in schema.items():
        logger.info(f"Split '{split_name}' has {split_info['num_rows']} examples")

    # save samples from validation split
    output_dir = Path("examples")
    output_dir.mkdir(exist_ok=True)
    save_dataset_sample(
        dataset, output_dir / "mnli_validation_samples.json", num_examples=3, split="validation_matched"
    )


def intermediate_data_example() -> None:
    """example demonstrating the distributed intermediate data upload and merge functionality.

    this shows how to:
    1. push partial data files from multiple workers
    2. merge and deduplicate those files in a central aggregator
    """
    import json
    import os
    import tempfile

    # setup auth token - in real usage, this would be from env var
    set_api_token("YOUR_HF_TOKEN")

    # example repo id - replace with your actual repo
    repo_id = "your-username/your-dataset"

    # --- worker process simulation ---

    # worker 1: generate and upload some data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        # write some sample data rows
        json.dump({"id": 1, "text": "sample text 1"}, f)
        f.write("\n")
        json.dump({"id": 2, "text": "sample text 2"}, f)
        f.write("\n")
        worker1_file = f.name

    # push the data file to intermediates branch
    # this auto-organizes by date and worker id
    worker1_url = push_intermediate_data(
        local_path=worker1_file,
        repo_id=repo_id,
        # these are default values, shown for clarity
        prefix="intermediates",
        date_folder=True,
    )
    print(f"worker 1 uploaded data: {worker1_url}")

    # clean up temporary file
    os.unlink(worker1_file)

    # worker 2: generate and upload different data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        # write some sample data rows (note: id 2 is duplicate)
        json.dump({"id": 2, "text": "sample text 2"}, f)
        f.write("\n")
        json.dump({"id": 3, "text": "sample text 3"}, f)
        f.write("\n")
        worker2_file = f.name

    # push the data file to intermediates branch
    # auto-generates a different worker id
    worker2_url = push_intermediate_data(
        local_path=worker2_file,
        repo_id=repo_id,
    )
    print(f"worker 2 uploaded data: {worker2_url}")

    # clean up temporary file
    os.unlink(worker2_file)

    # --- aggregator process simulation ---

    # custom deduplication function (optional)
    # this extracts the "id" field to use as the dedup key
    def dedup_by_id(row: dict) -> Any:
        return row.get("id")

    # merge the intermediate data files
    result = merge_intermediate_data(
        repo_id=repo_id,
        # optional params shown with their defaults
        prefix="intermediates",
        aggregator_branch="aggregator_output",
        push_to_main=True,
        deduplicate=True,
        dedup_key=dedup_by_id,  # custom deduplication function
        remember_merged=True,
    )

    # print merge results
    print("\nMerge results:")
    print(f"Files processed: {result['files_processed']}")
    print(f"Rows processed: {result['rows_processed']}")
    print(f"Rows after deduplication: {result['rows_after_dedup']}")
    print(f"Output file: {result['output_file']}")

    # the final merged dataset is now available in:
    # - aggregator_branch as {result['output_file']}
    # - main branch (if push_to_main=True) as {result['output_file']}

    # subsequent merges will only process new files
    # thanks to the remember_merged=True option


if __name__ == "__main__":
    logger.info("Running dumb-datasets examples")
    basic_example()
    logger.info("---")
    multiple_splits_example()
    logger.info("Examples completed")

    # this would run the example if executed directly
    # intermediate_data_example()
