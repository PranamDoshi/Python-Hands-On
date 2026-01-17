#!/usr/bin/env python3
"""Script to start the Extractor Worker."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from workers.extractor.extractor_worker import ExtractorWorker

if __name__ == "__main__":
    worker = ExtractorWorker()
    try:
        worker.run()
    except KeyboardInterrupt:
        worker.stop()
