# dumb-datasets

[![Release](https://img.shields.io/github/v/release/nlile/dumb-datasets)](https://pypi.org/project/dumb-datasets/)
[![Build status](https://img.shields.io/github/actions/workflow/status/nlile/dumb-datasets/master.yml?branch=master)](https://github.com/nlile/dumb-datasets/actions/workflows/master.yml?query=branch%3Amaster)
[![codecov](https://codecov.io/gh/nlile/dumb-datasets/branch/master/graph/badge.svg)](https://codecov.io/gh/nlile/dumb-datasets)
[![Commit activity](https://img.shields.io/github/commit-activity/m/nlile/dumb-datasets)](https://img.shields.io/github/commit-activity/m/nlile/dumb-datasets)
[![License](https://img.shields.io/github/license/nlile/dumb-datasets)](https://img.shields.io/github/license/nlile/dumb-datasets)

A lightweight wrapper around HuggingFace datasets.

## Features

- 🔄 Complete wrapper around HuggingFace datasets with extended functionality
- 🚀 Cached dataset loading with smart retries and error handling
- 🛠️ Rich helper functions for common dataset operations
- 📊 Streamlined data processing pipelines with fluent API
- 🔍 Type validation with Pydantic models
- 🔌 Extension points via hooks and adapters
- 📋 Feature definition and inference utilities
- ⚡ Ultra-fast downloads with HF Transfer enabled by default
- 🔗 Integrated HuggingFace Hub API for repository interactions

## Installation

```bash
pip install dumb-datasets
```

Or with Poetry:

```bash
poetry add dumb-datasets
```

## Usage

### Loading Datasets

```python
from dumb_datasets import load_dataset, set_api_token

# Optionally set your HuggingFace API token for private datasets
set_api_token("your_hf_token")

# Load a dataset
dataset = load_dataset("squad", split="train")

# Access information about the dataset
info = dataset.info()
print(f"Number of rows: {info['num_rows']}")
```

### Fast Downloads with HF Transfer

dumb-datasets enables HF Transfer by default for ultra-fast downloads:

```python
from dumb_datasets import load_dataset, enable_hf_transfer, download_file, download_repository

# HF Transfer is enabled by default, but you can control it:
enable_hf_transfer(True)  # Enable explicitly
# enable_hf_transfer(False)  # Disable if needed

# Download a specific file
file_path = download_file(
    repo_id="google/fleurs",
    filename="README.md",
    repo_type="dataset"
)

# Download an entire repository
repo_path = download_repository(
    repo_id="google/fleurs",
    repo_type="dataset"
)
```

### Hub API Integration

```python
from dumb_datasets import HubAPI

# Create a Hub API instance
hub = HubAPI(token="your_hf_token")  # Token is optional

# List available datasets
datasets = hub.list_datasets()
for ds in datasets[:5]:
    print(f"Dataset: {ds['id']}")

# Upload a file to a repository
url = hub.upload_file(
    path_or_fileobj="path/to/file.csv",
    path_in_repo="data/file.csv",
    repo_id="your-username/your-repo",
    repo_type="dataset"
)
```

### Using Sessions

Sessions help manage configuration across multiple operations:

```python
from dumb_datasets import Session

# Create a session with your preferences
session = Session(
    cache_dir="/path/to/cache",
    api_token="your_hf_token",
    force_hf_transfer=True  # Enable HF Transfer (default)
)

# Use the session to load datasets and interact with the Hub
dataset = session.get_dataset("squad", split="train")
file_path = session.download_file("google/fleurs", "README.md")
```

## Quick Usage

```python
from dumb_datasets import load_dataset, Features, Value

# Load a dataset with automatic caching and error handling
dataset = load_dataset("squad")

# Get dataset info
info = dataset.info()
print(f"Dataset has {info['num_rows']} rows with features: {info['features']}")

# Apply transformations with a fluent API
processed = (dataset
    .filter(lambda x: len(x["question"]) > 10)
    .map_columns(lambda x: x.lower(), ["question", "context"])
    .shuffle(seed=42))

# Define custom features
features = Features({
    "text": Value("string"),
    "label": Value("int64")
})

# Use session for consistent settings
from dumb_datasets import Session
session = Session(cache_dir="/tmp/datasets", api_token="YOUR_HF_TOKEN")
new_dataset = session.get_dataset("glue", name="mnli")
```

## Advanced Usage

```python
from dumb_datasets import (
    Dataset,
    ClassLabel,
    infer_features_from_dict,
    save_dataset_sample
)

# Infer features from examples
example = {"text": "Hello world", "score": 0.95, "labels": ["positive", "greeting"]}
features = infer_features_from_dict(example)

# Save samples for inspection
save_dataset_sample(dataset, "samples.json", num_examples=5)

# Register an adapter for custom dataset loading
from dumb_datasets import register_adapter
register_adapter("my_format", my_custom_loader_function)

# Use hooks for custom processing
from dumb_datasets import add_hook
add_hook("after_load", lambda ds: print(f"Loaded dataset with {len(ds)} examples"))
```

## Distributed Data Generation

The library provides an opinionated API for distributed data generation workflows:

```python
from dumb_datasets import push_intermediate_data, merge_intermediate_data

# === WORKER PROCESS ===
# Push partial data to a "intermediates" branch with date-based organization
url = push_intermediate_data(
    local_path="worker_data.jsonl",  # Local JSONL file to upload
    repo_id="your-username/your-dataset",
    # Optional params with defaults shown:
    prefix="intermediates",  # Folder within the branch
    date_folder=True,       # Create YYYYMMDD subfolder
)
print(f"Uploaded intermediate data: {url}")
# Each worker gets a stable ID and files are named to avoid collisions

# === AGGREGATOR PROCESS ===
# Define custom deduplication function (optional)
def dedup_by_id(row):
    return row.get("id")  # Use id field as deduplication key

# Merge all intermediate data files
result = merge_intermediate_data(
    repo_id="your-username/your-dataset",
    # Optional params with defaults shown:
    prefix="intermediates",
    aggregator_branch="aggregator_output",  # Branch for merged results
    push_to_main=True,       # Also push to main branch
    deduplicate=True,        # Remove duplicate rows
    dedup_key=dedup_by_id,   # Custom key function (default: entire row)
    remember_merged=True,    # Track processed files to avoid reprocessing
)

print(f"Merged {result['files_processed']} files with {result['rows_processed']} rows")
print(f"Output file: {result['output_file']}")
```

This API standardizes how distributed data generation processes can:
1. Push partial files from multiple workers to a single branch
2. Organize uploads by date and worker ID to prevent collisions
3. Merge and deduplicate data in a separate aggregator process
4. Track which files have been processed to enable incremental merges
