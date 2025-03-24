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

## Installation

```bash
pip install dumb-datasets
```

Or with Poetry:

```bash
poetry add dumb-datasets
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

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b master
git add .
git commit -m "init .gitignore"
git remote add origin git@github.com:nlile/dumb-datasets.git
git push -u origin master
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to master, or when you create a new release.

To finalize the set-up for publishing to PyPI or Artifactory, see [here](https://nlile.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://nlile.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://nlile.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/nlile/dumb-datasets/settings/secrets/actions/new).
- Create a [new release](https://github.com/nlile/dumb-datasets/releases/new) on Github.
- Create a new tag in the form `*.*.*`.
- For more details, see [here](https://nlile.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [nlile/cookiecutter-poetry](https://github.com/nlile/cookiecutter-poetry).
