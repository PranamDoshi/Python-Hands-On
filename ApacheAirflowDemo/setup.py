"""Setup script for the project."""
from setuptools import setup, find_packages

setup(
    name="apache-airflow-demo",
    version="1.0.0",
    description="Apache Airflow Web Crawling Pipeline",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.12.5",
        "pydantic-settings>=2.6.1",
        "fastapi>=0.128.0",
        "uvicorn>=0.34.0",
        "apache-airflow>=2.10.0",
        "pymongo>=4.10.1",
        "psycopg2-binary>=2.9.10",
        "sqlalchemy>=2.0.36",
        "redis>=5.2.1",
        "playwright>=1.57.0",
        "beautifulsoup4>=4.12.3",
        "lxml>=6.0.2",
        "python-dotenv>=1.0.1",
    ],
)
