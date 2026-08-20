# strands-olostep

[Olostep](https://olostep.com) tools for [Strands Agents](https://strandsagents.com) — give your agents live web search, scraping, crawling, and cited AI answers.

## Installation

```bash
pip install strands-olostep
```

## Configuration

Set your Olostep API key as an environment variable. Get one from the [Olostep dashboard](https://www.olostep.com/dashboard/api-keys) — the free tier includes 500 credits.

```bash
export OLOSTEP_API_KEY="your-api-key"
```

| Variable | Required | Description |
|----------|----------|-------------|
| `OLOSTEP_API_KEY` | Yes | Your Olostep API key |
| `OLOSTEP_BASE_URL` | No | Override the API base URL (defaults to `https://api.olostep.com/v1`) |

## Usage

```python
from strands import Agent
from strands_olostep import (
    olostep_answers,
    olostep_crawl,
    olostep_get_crawl_results,
    olostep_map,
    olostep_scrape,
    olostep_search,
)

agent = Agent(
    tools=[
        olostep_search,
        olostep_scrape,
        olostep_answers,
        olostep_map,
        olostep_crawl,
        olostep_get_crawl_results,
    ]
)

agent("Find the three most recent posts on the Olostep blog and summarize each one.")
```

Import only the tools you need — an agent that just answers questions may only want `olostep_answers`.

## Tools

| Tool | What it does |
|------|--------------|
| `olostep_search` | Search the live web; returns deduplicated links with titles and descriptions |
| `olostep_scrape` | Fetch a single page as clean markdown, HTML, JSON, or text |
| `olostep_answers` | Ask a question and get an AI-synthesized answer with citations |
| `olostep_map` | Discover the URLs on a site, optionally ranked by a query |
| `olostep_crawl` | Start an async crawl that follows links from a start URL |
| `olostep_get_crawl_results` | Poll a crawl and fetch its page content |

### Picking the right tool

- **Want a synthesized answer?** Use `olostep_answers`. It searches, reads, and cross-validates, returning sources with the answer.
- **Want a list of links to explore?** Use `olostep_search`, then `olostep_scrape` the ones worth reading.
- **Know the exact page?** Go straight to `olostep_scrape`.
- **Want a whole site or section?** Use `olostep_crawl`, then `olostep_get_crawl_results`. Crawl both discovers and scrapes.
- **Just want to see what URLs exist?** Use `olostep_map` — discovery only, no scraping.

### Notes

`olostep_crawl` is asynchronous. It returns a crawl id immediately and the job runs in the background — you must call `olostep_get_crawl_results` with that id to fetch pages. While the crawl is running, that tool reports progress so the agent knows to call again.

For JavaScript-heavy pages, pass `wait_before_scraping` (in milliseconds) to `olostep_scrape`:

```python
olostep_scrape("https://example.com", wait_before_scraping=3000)
```

For geo-targeted content, pass a two-letter `country` code:

```python
olostep_scrape("https://example.com", country="GB")
```

## Error handling

Tools return an error result rather than raising, so a failed call doesn't break the agent loop:

```python
{"status": "error", "content": [{"text": "Olostep API Error: 401 ..."}]}
```

A missing `OLOSTEP_API_KEY` produces a clear message pointing at the dashboard.

## Development

```bash
pip install -e ".[dev]"
hatch run prepare   # format, lint, typecheck, test
```

## Links

- [Olostep documentation](https://docs.olostep.com)
- [Olostep API reference](https://docs.olostep.com/api-reference/common/object-oriented)
- [Strands Agents documentation](https://strandsagents.com)
- [Issues](https://github.com/olostep-api/strands-olostep/issues)

## License

Apache 2.0 — see [LICENSE](LICENSE).
