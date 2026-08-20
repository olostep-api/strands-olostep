"""Tests for the Olostep tools."""

import pytest

from strands_olostep import (
    olostep_answers,
    olostep_crawl,
    olostep_get_crawl_results,
    olostep_map,
    olostep_scrape,
    olostep_search,
)
from strands_olostep._client import OlostepError, _api_key, error, ok

ALL_TOOLS = [
    (olostep_search, "olostep_search"),
    (olostep_scrape, "olostep_scrape"),
    (olostep_answers, "olostep_answers"),
    (olostep_map, "olostep_map"),
    (olostep_crawl, "olostep_crawl"),
    (olostep_get_crawl_results, "olostep_get_crawl_results"),
]


@pytest.mark.parametrize(("fn", "name"), ALL_TOOLS)
def test_tools_are_registered(fn, name):
    """The @tool decorator exposes each function under its tool name."""
    assert fn.tool_name == name


def test_missing_api_key_raises(monkeypatch):
    """A missing API key produces a clear, actionable error."""
    monkeypatch.delenv("OLOSTEP_API_KEY", raising=False)
    with pytest.raises(OlostepError, match="OLOSTEP_API_KEY"):
        _api_key()


def test_tools_return_error_shape_without_key(monkeypatch):
    """Tools degrade to an error result rather than raising into the agent loop."""
    monkeypatch.delenv("OLOSTEP_API_KEY", raising=False)
    result = olostep_search("test query")
    assert result["status"] == "error"
    assert "OLOSTEP_API_KEY" in result["content"][0]["text"]


def test_crawl_results_error_without_key(monkeypatch):
    """The crawl results tool also degrades gracefully."""
    monkeypatch.delenv("OLOSTEP_API_KEY", raising=False)
    result = olostep_get_crawl_results("crawl_does_not_exist")
    assert result["status"] == "error"


def test_result_wrappers():
    """The success and error wrappers produce the expected tool result shape."""
    assert ok({"a": 1}) == {"status": "success", "content": [{"json": {"a": 1}}]}
    assert error("boom") == {"status": "error", "content": [{"text": "boom"}]}
