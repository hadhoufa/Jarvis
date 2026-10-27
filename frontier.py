"""Frontier: URL queue with dedup."""

from collections import deque
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def canonicalize(url):
    parts = urlsplit(url.strip())
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", query, "")
    )


class Frontier:
    def __init__(self, max_queue=10000):
        self.queue = deque()
        self.seen = set()
        self.max_queue = max_queue

    def add(self, url):
        canon = canonicalize(url)
        if canon in self.seen or len(self.queue) >= self.max_queue:
            return False
        self.seen.add(canon)
        self.queue.append(canon)
        return True

    def pop(self):
        return self.queue.popleft() if self.queue else None

    def __len__(self):
        return len(self.queue)
