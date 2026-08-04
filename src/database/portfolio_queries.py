"""
portfolio_queries.py

Reusable SQL queries for the Portfolio Data Generation pipeline.

Responsibilities
----------------
- Retrieve operational customer data required by the Portfolio
  Data Generators.
- Provide a single source of truth for SQL statements.
- Keep business calculations outside SQL.


"""

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
    cm.customer_id,
    cm.state,
    cm.customer_segment,
    la.loan_type,
    la.outstanding_balance,
    la.loan_status
FROM loan_accounts la
INNER JOIN customer_master cm
    ON la.customer_id = cm.customer_id
"""

GET_CARD_EXPOSURE_DATA = """
SELECT
    cm.customer_id,
    cm.state,
    cm.customer_segment,
    cc.card_type,
    cc.credit_limit,
    cc.current_balance
FROM credit_card_accounts cc
INNER JOIN customer_master cm
    ON cc.customer_id = cm.customer_id
"""

# ================================================================
# Portfolio Segmentation
# ================================================================

GET_SEGMENTATION_DATA = """
SELECT
    cm.customer_id,
    cm.customer_segment,
    cm.state,
    cm.employment_type,
    cm.occupation,
    cb.credit_score,
    cb.credit_utilisation,
    cb.debt_to_income_ratio,
    cb.default_history
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
    cm.state,
    cm.annual_income,
    cb.credit_score,
    cb.credit_utilisation,
    cb.default_history,
    cc.card_type,
    cc.credit_limit,
    cc.current_balance
FROM customer_master cm
INNER JOIN credit_bureau cb
    ON cm.customer_id = cb.customer_id
LEFT JOIN credit_card_accounts cc
    ON cm.customer_id = cc.customer_id
"""
