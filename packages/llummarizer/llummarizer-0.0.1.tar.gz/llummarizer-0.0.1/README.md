# LLM Summarizer

LLummarizer is a Python library that provides an interface to the OpenAI GPT-4 model for generating summaries from structured data. This library allows developers to easily integrate summarization capabilities into their applications.

## Installation

You can install the LLM Summarizer library using pip:

```sh
pip install llummarizer
```

## Usage

Here is a simple example of how to use the `LLMSummarizer` class:

```python
from llummarizer import LLMSummarizer

# Create an instance of the summarizer
summarizer = LLMSummarizer()

# Define the data to summarize
data = {
    "first_name": "Lewis",
    "last_name": "Hamilton",
    "occupation": "Driver",
    "wins": 100,
    "points": 1000
}

# Optionally, define context and excluded keys
context = {
    "first_name": "Named after Olympic sprinter Carl Lewis",
    "occupation": "Formula 1 racing driver"
}
excluded_keys = ["email"]

# Generate the summary in English (default)
summary_en = summarizer.create_summary(data, context=context, excluded_keys=excluded_keys)

# Generate the summary in Spanish
summary_es = summarizer.create_summary(data, context=context, excluded_keys=excluded_keys, language="spanish")

print("English summary:", summary_en)
print("Spanish summary:", summary_es)
```

## Features

- Generate summaries from structured data
- Customize summaries with additional context
- Exclude specific keys from summarization
- Support for multiple output languages
- Powered by OpenAI's GPT-4 model

## Requirements

- Python 3.12 or higher
- OpenAI API key (set as an environment variable `OPENAI_API_KEY`)

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
