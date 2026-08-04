"""
portfolio_config.py

Configuration settings for the Portfolio Analytical Repository.

This module centralises configuration used across the Portfolio
Data Foundation components.

"""

from pathlib import Path

# ------------------------------------------------------------------
# Repository Configuration
# ------------------------------------------------------------------

DATABASE_DIRECTORY = Path("src/database")

DATABASE_NAME = "portfolio_analytics.db"

DATABASE_PATH = DATABASE_DIRECTORY / DATABASE_NAME
PORTFOLIO_DATABASE_PATH = DATABASE_PATH


# ------------------------------------------------------------------
# Snapshot Configuration
# ------------------------------------------------------------------

DEFAULT_REPORTING_PERIOD = "Monthly"

DEFAULT_DATE_FORMAT = "%Y-%m-%d"


# ------------------------------------------------------------------
# Generator Configuration
# ------------------------------------------------------------------

ENABLE_DATABASE_RESET = False

DEFAULT_BATCH_SIZE = 100
