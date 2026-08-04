"""
portfolio_schema.py

Defines the physical database schema for the Portfolio Analytical Repository.

The Portfolio Repository stores analytically prepared portfolio datasets
used by the Portfolio Analytics Service. It intentionally contains
derived analytical information rather than operational customer data.


"""

# ------------------------------------------------------------------
# Table Names
# ------------------------------------------------------------------

PORTFOLIO_SUMMARY = "portfolio_summary"
PORTFOLIO_RISK = "portfolio_risk"
PORTFOLIO_EXPOSURE = "portfolio_exposure"
PORTFOLIO_SEGMENTATION = "portfolio_segmentation"
PORTFOLIO_TRENDS = "portfolio_trends"
PORTFOLIO_OPPORTUNITIES = "portfolio_opportunities"

# ------------------------------------------------------------------
# Portfolio Summary
# ------------------------------------------------------------------

CREATE_PORTFOLIO_SUMMARY_TABLE = f"""
CREATE TABLE IF NOT EXISTS {PORTFOLIO_SUMMARY} (

    snapshot_date              TEXT PRIMARY KEY,

    active_customers           INTEGER,
    total_portfolio_value      REAL,
    total_credit_exposure      REAL,

    average_credit_score       REAL,
    average_utilisation        REAL,

    portfolio_health_score     REAL,

    default_rate               REAL,
    delinquency_rate           REAL,

    created_at                 TEXT
);
"""

# ------------------------------------------------------------------
# Portfolio Risk
# ------------------------------------------------------------------

CREATE_PORTFOLIO_RISK_TABLE = f"""
CREATE TABLE IF NOT EXISTS {PORTFOLIO_RISK} (

    snapshot_date              TEXT,

    risk_band                  TEXT,

    customer_count             INTEGER,

    exposure_amount            REAL,

    average_credit_score       REAL,

    default_rate               REAL,

    delinquency_rate           REAL,

    PRIMARY KEY (
        snapshot_date,
        risk_band
    )
);
"""

# ------------------------------------------------------------------
# Portfolio Exposure
# ------------------------------------------------------------------

CREATE_PORTFOLIO_EXPOSURE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {PORTFOLIO_EXPOSURE} (

    snapshot_date              TEXT,

    product_type               TEXT,

    state                     TEXT,

    exposure_amount            REAL,

    concentration_percentage   REAL,

    PRIMARY KEY (
        snapshot_date,
        product_type,
        state
    )
);
"""

# ------------------------------------------------------------------
# Portfolio Segmentation
# ------------------------------------------------------------------

CREATE_PORTFOLIO_SEGMENTATION_TABLE = f"""
CREATE TABLE IF NOT EXISTS portfolio_segmentation (

    snapshot_date              TEXT,

    customer_segment           TEXT,

    state                      TEXT,

    employment_type            TEXT,

    occupation                 TEXT,

    customer_count             INTEGER,

    average_credit_score       REAL,

    average_utilisation        REAL,

    PRIMARY KEY (
        snapshot_date,
        customer_segment,
        state,
        employment_type,
        occupation
    )
);
"""

# ------------------------------------------------------------------
# Portfolio Trends
# ------------------------------------------------------------------

CREATE_PORTFOLIO_TRENDS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {PORTFOLIO_TRENDS} (

    snapshot_date              TEXT,

    metric_name                TEXT,

    metric_value               REAL,

    reporting_period           TEXT,

    PRIMARY KEY (
        snapshot_date,
        metric_name
    )
);
"""

# ------------------------------------------------------------------
# Portfolio Opportunities
# ------------------------------------------------------------------

CREATE_PORTFOLIO_OPPORTUNITIES_TABLE = f"""
CREATE TABLE IF NOT EXISTS {PORTFOLIO_OPPORTUNITIES} (

    snapshot_date              TEXT,

    opportunity_type           TEXT,

    eligible_customers         INTEGER,

    estimated_value            REAL,

    confidence_score           REAL,

    PRIMARY KEY (
        snapshot_date,
        opportunity_type
    )
);
"""

# ------------------------------------------------------------------
# Schema Definition
# ------------------------------------------------------------------

SCHEMA_DEFINITION = [

    CREATE_PORTFOLIO_SUMMARY_TABLE,

    CREATE_PORTFOLIO_RISK_TABLE,

    CREATE_PORTFOLIO_EXPOSURE_TABLE,

    CREATE_PORTFOLIO_SEGMENTATION_TABLE,

    CREATE_PORTFOLIO_TRENDS_TABLE,

    CREATE_PORTFOLIO_OPPORTUNITIES_TABLE,
]
