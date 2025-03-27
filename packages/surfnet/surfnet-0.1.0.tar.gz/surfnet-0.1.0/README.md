# Surfnet

A powerful Python web scraping package with integrated search capabilities, advanced captcha handling, and parallel processing.

## Features

- 🔍 **Integrated Search**: Built-in DuckDuckGo search functionality
- 🚀 **Parallel Processing**: Scrape multiple URLs simultaneously for faster results
- ⚡ **JavaScript Support**: Handle JavaScript-heavy websites with Playwright
- 🤖 **Captcha Bypassing**: Intelligent captcha detection and solving capabilities
- 🛡️ **Smart Detection**: Automatically avoids login/authentication pages
- 📊 **Content Extraction**: Target specific HTML tags for precise data collection
- 🧠 **Human-like Behavior**: Simulates natural browsing patterns to avoid detection

## Installation

```bash
pip install surfnet
```

Or install from source:

```bash
git clone https://github.com/yourusername/surfnet.git
cd surfnet
pip install -e .
```

## Dependencies

Surfnet requires the following main dependencies:

- `duckduckgo-search`: For search functionality
- `beautifulsoup4`: For HTML parsing
- `requests`: For HTTP requests
- `playwright`: For JavaScript-heavy websites
- `concurrent-futures-extra`: For parallel processing
- `fake-useragent`: For rotating user agents
- `pydub`: For audio processing (captcha solving)
- `SpeechRecognition`: For audio captcha solving

## Usage Examples

### Basic Usage

```python
from surfnet import Surfnet

# Initialize the scraper
scraper = Surfnet()

# Search for content
results = scraper.search("Python programming", max_results=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result.get('snippet', '')}")
    print("---")

# Scrape a single URL
data = scraper.scrapeurl("https://example.com", tags=["p", "h1", "article"])
print(f"Title: {data['title']}")
print(f"Content: {data['content'][:200]}...")
```

### Advanced Usage

```python
from surfnet import Surfnet

# Initialize with parallel processing capabilities
scraper = Surfnet(max_workers=4)

# Scrape multiple URLs in parallel
urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]
results = scraper.scrape_urls_parallel(urls, tags=["article", "p", "h1", "h2"])

# Crawl a website (max 5 pages)
site_data = scraper.crawlwebsite("https://example.com", max_pages=5)

# Handle JavaScript-heavy websites using Playwright
js_site_data = scraper.scrapeurl("https://dynamic-site.com", use_playwright=True)
```

### Captcha Handling

```python
from surfnet import Surfnet

# Initialize with captcha handling
scraper = Surfnet()

# The scraper will automatically detect and handle common captchas
result = scraper.scrapeurl("https://site-with-captcha.com", use_playwright=True)

# You can also explicitly crawl sites with captcha protection
results = scraper.crawlwebsite("https://protected-site.com", max_pages=3)
```

## License

MIT