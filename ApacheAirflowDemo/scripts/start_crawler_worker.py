#!/usr/bin/env python3
"""Script to start the Crawler Worker."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from workers.crawler.crawler_worker import CrawlerWorker

if __name__ == "__main__":
    worker = CrawlerWorker()
    try:
        worker.run()
    except KeyboardInterrupt:
        worker.stop()
