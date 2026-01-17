"""Main DAG for orchestrating crawl workflow - Airflow DAG file."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from dags.main_dag import dag

# Export the DAG
__all__ = ["dag"]
