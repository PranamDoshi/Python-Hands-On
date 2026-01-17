#!/usr/bin/env python3
"""Script to start the PDP Crawling Scheduler."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from schedulers.pdp_crawling_scheduler import PDPCrawlingScheduler

if __name__ == "__main__":
    scheduler = PDPCrawlingScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
