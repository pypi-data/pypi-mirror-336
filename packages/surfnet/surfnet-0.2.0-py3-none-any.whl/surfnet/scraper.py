import re
import time
import random
from datetime import datetime
from typing import List, Dict, Optional, Union, Set
from urllib.parse import urljoin, urlparse
import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.async_api import async_playwright, Browser, Page, TimeoutError, Response

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from tqdm import tqdm
from fake_useragent import UserAgent

# Import the enhanced captcha solver
from .captcha_solver import CaptchaSolver
from .system_profiler import SystemProfiler, initialize_ray_if_available

class Surfnet:
    """Web scraping tool with parallel processing and captcha handling."""
    
    def __init__(self, max_workers: Optional[int] = None, auto_optimize: bool = True, 
                 use_gpu: Optional[bool] = None, use_ray: bool = False):
        """
        Initialize the Surfnet scraper.
        
        Args:
            max_workers: Maximum number of parallel workers (default: auto-detected)
            auto_optimize: Whether to automatically optimize settings for hardware (default: True)
            use_gpu: Whether to use GPU acceleration if available (default: auto-detected)
            use_ray: Whether to use Ray for distributed processing (default: False)
        """
        # Initialize system profiler if auto-optimizing
        self.auto_optimize = auto_optimize
        if self.auto_optimize:
            self.profiler = SystemProfiler()
            recommended_workers = self.profiler.get_recommended_workers()
            self.use_gpu = use_gpu if use_gpu is not None else self.profiler.should_use_gpu()
            self.use_ray = use_ray or self.profiler.should_use_ray()
            self.max_parallel_requests = self.profiler.get_max_parallel_requests()
            self.estimated_throughput = self.profiler.get_estimated_throughput()
        else:
            recommended_workers = os.cpu_count() - 1 if os.cpu_count() else 4
            self.use_gpu = use_gpu if use_gpu is not None else False
            self.use_ray = use_ray
            self.max_parallel_requests = 10
            self.estimated_throughput = 0
            
        # Set max workers
        self.max_workers = max_workers if max_workers is not None else recommended_workers
        
        # Initialize Ray if requested
        if self.use_ray:
            self.ray_initialized = initialize_ray_if_available(self.max_workers)
        else:
            self.ray_initialized = False
            
        # Print system report if auto-optimizing
        if self.auto_optimize:
            self.profiler.print_system_report()
            
        # Setup user agent rotation
        self.user_agent = UserAgent()
        
        # Initialize captcha solver
        self.captcha_solver = CaptchaSolver()
        
        # Initialize Playwright browser
        self.browser = None
        self.playwright = None
        
        # Auth and login page patterns
        self.auth_patterns = [
            r'/login', r'/signin', r'/auth', r'/account/login', 
            r'login\.', r'signin\.', r'auth\.', r'authenticate',
            r'/register', r'/signup', r'register\.', r'signup\.'
        ]

    def _rotate_user_agent(self):
        """Rotate the user agent to avoid detection."""
        self.user_agent = self.user_agent.random
        return self.user_agent

    async def init_browser(self, stealth_mode: bool = False, gpu_acceleration: bool = None):
        """Initialize Playwright browser with optional GPU acceleration and stealth mode."""
        if self.browser is None:
            # Use class-level setting if not specified
            if gpu_acceleration is None:
                gpu_acceleration = self.use_gpu
            
            self.playwright = await async_playwright().start()
            
            # Configure browser options
            browser_args = []
            
            # Add GPU acceleration if requested and available
            if gpu_acceleration:
                browser_args.extend([
                    "--enable-gpu",
                    "--enable-webgl",
                    "--ignore-gpu-blocklist",
                    "--enable-accelerated-2d-canvas"
                ])
            else:
                browser_args.append("--disable-gpu")
            
            # Add stealth mode options
            if stealth_mode:
                browser_args.extend([
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-site-isolation-trials"
                ])
            
            # Launch with configured options
            try:
                if stealth_mode:
                    # Try undetected Playwright if available and in stealth mode
                    try:
                        import undetected_playwright
                        self.browser = await undetected_playwright.stealth_async().launch(
                            headless=True, args=browser_args
                        )
                    except ImportError:
                        # Fall back to regular Playwright with stealth args
                        self.browser = await self.playwright.chromium.launch(
                            headless=True, args=browser_args
                        )
                else:
                    # Standard Playwright
                    self.browser = await self.playwright.chromium.launch(
                        headless=True, args=browser_args
                    )
            except Exception as e:
                print(f"Error launching browser with GPU acceleration, retrying without: {str(e)}")
                # Retry without GPU acceleration if it fails
                browser_args = [arg for arg in browser_args if not arg.startswith("--enable-")]
                browser_args.append("--disable-gpu")
                self.browser = await self.playwright.chromium.launch(
                    headless=True, args=browser_args
                )

    async def close_browser(self):
        """Close the browser properly."""
        if self.browser:
            try:
                await self.browser.close()
            except Exception as e:
                print(f"Error closing browser: {str(e)}")
            finally:
                self.browser = None
                
    def __del__(self):
        """Ensure browser resources are cleaned up."""
        if self.browser:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close_browser())
                else:
                    # Create a new loop if necessary
                    try:
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        new_loop.run_until_complete(self.close_browser())
                        new_loop.close()
                    except Exception as e:
                        print(f"Error during browser cleanup: {str(e)}")
            except Exception as e:
                print(f"Error getting event loop: {str(e)}")
            finally:
                self.browser = None

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search using DuckDuckGo."""
        try:
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=max_results))
            return [{
                'title': r.get('title', ''),
                'url': r.get('link', r.get('url', '')),
                'snippet': r.get('body', r.get('snippet', ''))
            } for r in results]
        except Exception as e:
            print(f"Error searching: {str(e)}")
            return []

    def isauthpage(self, url: str) -> bool:
        """
        Check if the URL is likely an authentication page.
        
        Args:
            url: URL to check
            
        Returns:
            Boolean indicating if it's an auth page
        """
        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in self.auth_patterns)

    def extractcontent(self, soup: BeautifulSoup, tags: List[str] = None) -> str:
        """
        Extract content from specified HTML tags.
        
        Args:
            soup: BeautifulSoup object
            tags: List of HTML tags to extract content from
            
        Returns:
            Extracted content as string
        """
        content = []
        if tags is None:
            # Default tags if none specified
            tags = ['article', 'main', 'div', 'p', 'section']
            
        for tag in tags:
            elements = soup.find_all(tag)
            for element in elements:
                # Remove script and style elements
                for script in element.find_all(['script', 'style']):
                    script.decompose()
                content.append(element.get_text(strip=True))
        return '\n'.join(content)

    def detect_captcha(self, html_content: str) -> bool:
        """
        Detect if a page contains a captcha.
        
        Args:
            html_content: HTML content of the page
            
        Returns:
            Boolean indicating if a captcha was detected
        """
        # Use the enhanced captcha detector
        captcha_type = self.captcha_solver.detect_captcha(html_content)
        return captcha_type is not None

    async def handle_captcha(self, page: Page) -> bool:
        """
        Handle captcha using enhanced captcha solver.
        
        Args:
            page: Playwright Page object
            
        Returns:
            Boolean indicating if captcha was bypassed
        """
        try:
            # Get the page content to identify captcha type
            content = await page.content()
            captcha_type = self.captcha_solver.detect_captcha(content)
            
            if not captcha_type:
                return True  # No captcha detected
                
            print(f"Detected {captcha_type} captcha, attempting to solve...")
            # Use the enhanced solver with specific captcha type
            return await self.captcha_solver.solve_captcha(page, captcha_type)
            
        except Exception as e:
            print(f"Error handling captcha: {str(e)}")
            return False

    async def _simulate_human_behavior(self, page: Page):
        """Use the enhanced human behavior simulation from captcha solver."""
        await self.captcha_solver._simulate_advanced_human_behavior(page)

    async def scrapeurl_playwright(self, url: str, tags: List[str] = None) -> Optional[Dict]:
        """
        Scrape a single URL using Playwright for JavaScript-heavy websites.
        
        Args:
            url: URL to scrape
            tags: List of HTML tags to extract content from (optional)
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        if self.isauthpage(url):
            return None

        try:
            await self.init_browser(stealth_mode=True)
            context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=self.user_agent.random
            )
            
            # Set extra HTTP headers with random user agent
            await context.set_extra_http_headers({
                'User-Agent': self.user_agent.random,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            })
            
            page = await context.new_page()
            
            # Add random delay before navigation
            await asyncio.sleep(random.uniform(1, 3))
            
            # Navigate to the page and wait for network idle
            response = await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Check for captcha with enhanced detection
            content = await page.content()
            if self.detect_captcha(content):
                print(f"Captcha detected on {url}, attempting to bypass with enhanced solver...")
                captcha_bypassed = await self.handle_captcha(page)
                if not captcha_bypassed:
                    print(f"Failed to bypass captcha on {url}")
                    await page.close()
                    await context.close()
                    return None
            
            # Wait for content to load
            await page.wait_for_load_state('domcontentloaded')
            
            # Get the page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else url
            
            # Extract content from specified tags
            extracted_content = self.extractcontent(soup, tags)
            
            if not extracted_content:
                return None
                
            await page.close()
            await context.close()
            return {
                'url': url,
                'title': title,
                'content': extracted_content,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'tags': tags,
                    'scraped_with': 'playwright'
                }
            }
            
        except Exception as e:
            print(f"Error scraping {url} with Playwright: {str(e)}")
            return None

    def scrapeurl(self, url: str, tags: List[str] = None, use_playwright: bool = False) -> Optional[Dict]:
        """
        Scrape a single URL and extract content from specified tags.
        
        Args:
            url: URL to scrape
            tags: List of HTML tags to extract content from (optional)
            use_playwright: Whether to use Playwright for JavaScript-heavy websites
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        if use_playwright:
            return asyncio.run(self.scrapeurl_playwright(url, tags))
            
        if self.isauthpage(url):
            return None

        try:
            # Rotate user agent
            user_agent = self._rotate_user_agent()
            
            # Add random delay
            time.sleep(random.uniform(0.5, 2))
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Check for captcha with enhanced detection
            if self.detect_captcha(response.text):
                print(f"Captcha detected on {url}, switching to Playwright mode with enhanced solver...")
                return asyncio.run(self.scrapeurl_playwright(url, tags))
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else url
            
            # Extract content from specified tags
            content = self.extractcontent(soup, tags)
            
            if not content:
                return None
                
            return {
                'url': url,
                'title': title,
                'content': content,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'tags': tags,
                    'scraped_with': 'requests'
                }
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    async def scrape_urls_parallel_async(self, urls: List[str], tags: List[str] = None) -> List[Dict]:
        """
        Scrape multiple URLs in parallel using Playwright.
        
        Args:
            urls: List of URLs to scrape
            tags: List of HTML tags to extract content from (optional)
            
        Returns:
            List of dictionaries containing scraped content
        """
        await self.init_browser(stealth_mode=True)
        results = []
        
        # Create a semaphore to limit concurrent tabs
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async def scrape_with_semaphore(url):
            async with semaphore:
                return await self._scrape_single_url_async(url, tags)
        
        # Create tasks for all URLs
        tasks = [scrape_with_semaphore(url) for url in urls]
        
        # Execute all tasks concurrently and collect results
        for result in await asyncio.gather(*tasks):
            if result:
                results.append(result)
                
        return results
    
    async def _scrape_single_url_async(self, url: str, tags: List[str] = None) -> Optional[Dict]:
        """Helper method to scrape a single URL asynchronously."""
        if self.isauthpage(url):
            return None
        
        try:
            context = await self.browser.new_context(user_agent=self.user_agent.random)
            page = await context.new_page()
            
            # Navigate to the page
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Check for captcha with enhanced detection
            content = await page.content()
            captcha_type = self.captcha_solver.detect_captcha(content)
            if captcha_type:
                print(f"Captcha ({captcha_type}) detected on {url} during parallel processing, attempting to solve...")
                captcha_bypassed = await self.captcha_solver.solve_captcha(page, captcha_type)
                if not captcha_bypassed:
                    await page.close()
                    await context.close()
                    return None
            
            # Get content and extract information
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            title = soup.title.string if soup.title else url
            extracted_content = self.extractcontent(soup, tags)
            
            await page.close()
            await context.close()
            
            if not extracted_content:
                return None
                
            return {
                'url': url,
                'title': title,
                'content': extracted_content,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'tags': tags,
                    'scraped_with': 'playwright-parallel'
                }
            }
            
        except Exception as e:
            print(f"Error scraping {url} in parallel: {str(e)}")
            return None

    def scrape_urls_parallel(self, urls: List[str], tags: List[str] = None, use_playwright: bool = False) -> List[Dict]:
        """
        Scrape multiple URLs in parallel.
        
        Args:
            urls: List of URLs to scrape
            tags: HTML tags to extract content from (default: all tags)
            use_playwright: Whether to use Playwright for JS-heavy sites
            
        Returns:
            List of dictionaries containing scraped data
        """
        if not urls:
            return []
            
        # Filter out auth pages
        filtered_urls = [url for url in urls if not self.isauthpage(url)]
        
        # Use Ray for distributed processing if available
        if self.ray_initialized:
            try:
                import ray
                
                @ray.remote
                def ray_scrape_url(url, tags, use_playwright):
                    # Create an isolated Surfnet instance for this Ray worker
                    local_scraper = Surfnet(max_workers=1, auto_optimize=False, 
                                           use_gpu=self.use_gpu, use_ray=False)
                    if use_playwright:
                        # For async operations in Ray, we need a special approach
                        return local_scraper._run_async_scrape(url, tags)
                    else:
                        return local_scraper.scrapeurl(url, tags)
                
                # Submit jobs to Ray
                ray_jobs = [ray_scrape_url.remote(url, tags, use_playwright) for url in filtered_urls]
                
                # Get results with progress bar
                results = []
                with tqdm(total=len(ray_jobs), desc="Scraping URLs with Ray") as pbar:
                    remaining = ray_jobs
                    while remaining:
                        # Use ray.wait to get completed tasks
                        finished, remaining = ray.wait(remaining, timeout=0.5)
                        if finished:
                            for result_id in finished:
                                result = ray.get(result_id)
                                if result:
                                    results.append(result)
                            pbar.update(len(finished))
                
                return results
                
            except Exception as e:
                print(f"Ray processing failed, falling back to ThreadPoolExecutor: {str(e)}")
        
        # Fall back to ThreadPoolExecutor if Ray is not available
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if use_playwright:
                # For Playwright, we need to use async scraping
                future_to_url = {
                    executor.submit(self._run_async_scrape, url, tags): url 
                    for url in filtered_urls
                }
            else:
                # For regular scraping, use the normal scrapeurl method
                future_to_url = {
                    executor.submit(self.scrapeurl, url, tags): url 
                    for url in filtered_urls
                }
            
            # Process results as they complete
            results = []
            with tqdm(total=len(filtered_urls), desc="Scraping URLs in parallel") as pbar:
                for future in concurrent.futures.as_completed(future_to_url):
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception as e:
                        url = future_to_url[future]
                        print(f"Error scraping {url}: {str(e)}")
                    finally:
                        pbar.update(1)
        
        return results
    
    def _run_async_scrape(self, url: str, tags: List[str] = None) -> Dict:
        """Run the async scrape in a sync context for parallel processing."""
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async scrape
            result = loop.run_until_complete(self.scrapeurl_playwright(url, tags))
            
            # Clean up
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            
            return result
        except Exception as e:
            print(f"Error in async scrape: {str(e)}")
            return None

    async def crawlwebsite_playwright(self, start_url: str, max_pages: int = 3, tags: List[str] = None) -> List[Dict]:
        """
        Crawl a website using Playwright for JavaScript-heavy websites.
        
        Args:
            start_url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl
            tags: List of HTML tags to extract content from (optional)
            
        Returns:
            List of dictionaries containing scraped content from all pages
        """
        if tags is None:
            tags = ['article', 'main', 'div']
            
        results = []
        visited = set()
        to_visit = {start_url}
        all_urls = set()
        
        # First, collect all URLs to crawl (BFS approach)
        try:
            await self.init_browser(stealth_mode=True)
            context = await self.browser.new_context(user_agent=self.user_agent.random)
            page = await context.new_page()
            
            # Add random delay before first navigation
            await asyncio.sleep(random.uniform(1, 3))
            
            with tqdm(total=max_pages, desc="Discovering pages") as pbar:
                while to_visit and len(visited) < max_pages:
                    url = to_visit.pop()
                    
                    if url in visited or self.isauthpage(url):
                        continue
                    
                    try:
                        # Navigate to the page and wait for network idle
                        await page.goto(url, wait_until='networkidle', timeout=60000)
                        
                        # Check for captcha with enhanced detection
                        content = await page.content()
                        captcha_type = self.captcha_solver.detect_captcha(content)
                        if captcha_type:
                            print(f"Captcha ({captcha_type}) detected on {url} during crawling, attempting to solve...")
                            captcha_bypassed = await self.captcha_solver.solve_captcha(page, captcha_type)
                            if not captcha_bypassed:
                                visited.add(url)
                                pbar.update(1)
                                continue
                        
                        # Get the page content
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Add this URL to the pages we'll actually scrape
                        all_urls.add(url)
                        
                        # Find new links to visit
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(url, href)
                            
                            # Only follow links from the same domain
                            if (urlparse(full_url).netloc == urlparse(start_url).netloc 
                                and full_url not in visited 
                                and len(all_urls) < max_pages):
                                to_visit.add(full_url)
                        
                        visited.add(url)
                        pbar.update(1)
                        
                        # Add small delay between requests
                        await asyncio.sleep(random.uniform(0.5, 2))
                        
                    except Exception as e:
                        print(f"Error discovering {url}: {str(e)}")
                        visited.add(url)
                        pbar.update(1)
                        continue
            
            await page.close()
            await context.close()
                
            # Now scrape all discovered URLs in parallel
            if all_urls:
                print(f"Scraping {len(all_urls)} discovered URLs in parallel...")
                results = await self.scrape_urls_parallel_async(list(all_urls), tags)
                
            return results
            
        finally:
            await self.close_browser()

    def crawlwebsite(self, start_url: str, max_pages: int = 3, tags: List[str] = None, 
                    use_playwright: bool = False) -> List[Dict]:
        """
        Crawl a website starting from the given URL and scrape content from discovered pages.
        
        Args:
            start_url: Starting URL for the crawl
            max_pages: Maximum number of pages to crawl
            tags: HTML tags to extract content from (optional)
            use_playwright: Whether to use Playwright for JavaScript-heavy websites
            
        Returns:
            List of dictionaries containing scraped content
        """
        # Use Playwright for advanced crawling if requested or GPU is available
        if use_playwright or self.use_gpu:
            return asyncio.run(self.crawlwebsite_playwright(start_url, max_pages, tags))
        
        # Standard crawling implementation
        discovered_urls = set([start_url])
        scraped_urls = set()
        results = []
        
        with tqdm(total=max_pages, desc="Discovering pages") as pbar:
            while discovered_urls and len(scraped_urls) < max_pages:
                # Get the next URL to crawl
                url = discovered_urls.pop()
                if url in scraped_urls or self.isauthpage(url):
                    continue
                
                # Scrape the page
                try:
                    response = requests.get(url, timeout=15)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find all links on the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith(('http://', 'https://')):
                            full_url = href
                        else:
                            full_url = urljoin(url, href)
                        
                        # Only add URLs from the same domain
                        if urlparse(full_url).netloc == urlparse(start_url).netloc:
                            discovered_urls.add(full_url)
                    
                    # Mark as scraped
                    scraped_urls.add(url)
                    pbar.update(1)
                
                except Exception as e:
                    print(f"Error discovering links in {url}: {str(e)}")
            
            # Scrape the discovered URLs
            to_scrape = list(scraped_urls)[:max_pages]
            print(f"Scraping {len(to_scrape)} discovered URLs in parallel...")
            results = self.scrape_urls_parallel(to_scrape, tags, use_playwright=False)
        
        return results 