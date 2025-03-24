import os
import pytest
from src.llm_summarizer.summarizer import LLMSummarizer

class TestLLMSummarizer:
    def setup_method(self):
        os.environ["OPENAI_API_KEY"] = "test_api_key"
        self.summarizer = LLMSummarizer()

    def test_create_summary(self):
        data = {
            "first_name": "Lewis",
            "last_name": "Hamilton",
            "occupation": "Driver",
            "wins": 100,
            "points": 1000
        }
        context = {
            "first_name": "Named after Olympic sprinter Carl Lewis",
            "occupation": "Formula 1 racing driver"
        }
        excluded_keys = ["email"]

        summary = self.summarizer.create_summary(data, context, excluded_keys)
        assert isinstance(summary, str)
        assert len(summary) > 0

    def test_remove_excluded_keys(self):
        data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        excluded_keys = ["key1"]
        cleaned_data = self.summarizer._remove_excluded_keys(data, excluded_keys)
        assert "key1" not in cleaned_data
        assert "key2" in cleaned_data
        assert "key3" in cleaned_data