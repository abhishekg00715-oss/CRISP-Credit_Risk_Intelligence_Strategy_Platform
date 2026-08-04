"""
portfolio_queries.py

Reusable SQL queries for the Portfolio Data Generation pipeline.

Responsibilities
----------------
- Retrieve operational customer data required by the Portfolio
  Data Generators.
- Provide a single source of truth for SQL statements.
- Keep business calculations outside SQL.


# ================================================================
# Portfolio Summary
# ================================================================

GET_CUSTOMER_PORTFOLIO_DATA = """
SELECT
    cm.customer_id,
    cm.customer_segment,
    cm.state,
    cb.credit_score,
    cb.credit_utilisation,
    cb.debt_to_income_ratio,
    cb.default_history
FROM customer_master cm
INNER JOIN credit_bureau cb
    ON cm.customer_id = cb.customer_id
"""

# ================================================================
# Portfolio Risk
# ================================================================

GET_CUSTOMER_RISK_DATA = """
SELECT
    customer_id,
    credit_score,
    credit_utilisation,
    debt_to_income_ratio,
    default_history
FROM credit_bureau
"""

# ================================================================
# Portfolio Exposure
# ================================================================

GET_LOAN_EXPOSURE_DATA = """
SELECT
    customer_id,
    loan_type,
    outstanding_balance,
    loan_status
FROM loan_accounts
"""

GET_CARD_EXPOSURE_DATA = """
SELECT
    customer_id,
    card_type,
    credit_limit,
    current_balance
FROM credit_card_accounts
"""

# ================================================================
# Portfolio Segmentation
# ================================================================

GET_SEGMENTATION_DATA = """
SELECT
    cm.customer_id,
    cm.customer_segment,
    cm.region,
    cb.credit_score,
    cb.credit_utilisation
FROM customer_master cm
INNER JOIN credit_bureau cb
    ON cm.customer_id = cb.customer_id
"""

# ================================================================
# Portfolio Trend Analysis
# ================================================================

GET_TRANSACTION_TRENDS = """
SELECT
    customer_id,
    transaction_date,
    transaction_amount,
    transaction_type
FROM transactions
ORDER BY transaction_date
"""

GET_DIGITAL_ACTIVITY = """
SELECT
    customer_id,
    login_date,
    login_count
FROM digital_behavior
ORDER BY login_date
"""

# ================================================================
# Portfolio Opportunity Analysis
# ================================================================

GET_OPPORTUNITY_DATA = """
SELECT
    cm.customer_id,
    cm.customer_segment,
    cb.credit_score,
    cb.credit_utilisation,
    cb.default_history,
    cc.credit_limit,
    cc.current_balance
FROM customer_master cm

INNER JOIN credit_bureau cb
    ON cm.customer_id = cb.customer_id

LEFT JOIN credit_card_accounts cc
    ON cm.customer_id = cc.customer_id
"""
