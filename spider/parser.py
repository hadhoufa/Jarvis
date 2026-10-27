"""HTML Parser."""

from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    links = [
        urljoin(base_url, a["href"])
        for a in soup.find_all("a", href=True)
        if not a["href"].startswith(("javascript:", "mailto:", "#"))
    ]
    text = soup.get_text(separator=" ", strip=True)[:2000]
    return {"url": base_url, "title": title, "links": links, "text": text}
