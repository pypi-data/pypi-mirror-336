"""Example usage of dumb-datasets package."""

import os
from pathlib import Path

from loguru import logger
from datasets import disable_progress_bar

from dumb_datasets import (
    load_dataset,
    set_cache_dir,
    set_api_token,
    save_dataset_sample,
    dataset_schema,
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
        dataset,
        output_dir / "mnli_validation_samples.json",
        num_examples=3,
        split="validation_matched"
    )


if __name__ == "__main__":
    logger.info("Running dumb-datasets examples")
    basic_example()
    logger.info("---")
    multiple_splits_example()
    logger.info("Examples completed")