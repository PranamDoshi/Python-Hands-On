#!/usr/bin/env python3
"""Script to start the Main Scheduler."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from schedulers.main_scheduler import MainScheduler

if __name__ == "__main__":
    scheduler = MainScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
