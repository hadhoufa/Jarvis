"""Core Spider Engine."""

import logging

import aiohttp

from .frontier import Frontier
from .parser import parse_html

logger = logging.getLogger("spider")


class Spider:
    def __init__(self, start_urls, max_pages=50):
        self.start_urls = start_urls
        self.max_pages = max_pages
        self.frontier = Frontier()
        self.results = []

    async def crawl(self):
        for u in self.start_urls:
            self.frontier.add(u)
        async with aiohttp.ClientSession(
            headers={"User-Agent": "SpiderBot/2.0"}
        ) as session:
            while len(self.frontier) > 0 and len(self.results) < self.max_pages:
                url = self.frontier.pop()
                try:
                    async with session.get(url, timeout=10) as resp:
                        if resp.status == 200 and "text/html" in resp.headers.get(
                            "Content-Type", ""
                        ):
                            html = await resp.text(errors="ignore")
                            data = parse_html(html, str(resp.url))
                            self.results.append(data)
                            logger.info(f"✓ {resp.status} {url} ({len(html)} bytes)")
                            for link in data["links"]:
                                self.frontier.add(link)
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logger.error(f"✗ {url} -> {e}")
        return self.results
