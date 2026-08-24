"""
portfolio_analytics_service_smoke_test.py

Smoke test for the Portfolio Analytics Service.

Responsibilities
----------------
- Validate PortfolioAnalyticsService initialization.
- Validate existing KPI, risk, exposure and segmentation
  analytics.
- Validate newly added trend analytics.
- Validate newly added opportunity analytics.
- Validate integration of all analytical services through
  PortfolioAnalyticsService.
- Validate the consolidated analytical snapshot.

This is a lightweight integration smoke test and is not intended
to replace detailed unit tests.
"""

from pathlib import Path
import sys


# ------------------------------------------------------------------
# Repository Root
# ------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(REPO_ROOT)
    )


# ------------------------------------------------------------------
# Service Import
# ------------------------------------------------------------------

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


# ------------------------------------------------------------------
# Test Utilities
# ------------------------------------------------------------------

PASS = "[PASS]"
FAIL = "[FAIL]"


def check(
    test_name: str,
    condition: bool,
) -> bool:

    status = PASS if condition else FAIL

    print(
        f"{test_name:<50} {status}"
    )

    return condition


# ------------------------------------------------------------------
# Smoke Test
# ------------------------------------------------------------------

def run_smoke_test() -> bool:

    print()
    print("=" * 70)
    print("Portfolio Analytics Service : Smoke Test")
    print("=" * 70)

    all_passed = True

    # --------------------------------------------------------------
    # Initialization
    # --------------------------------------------------------------

    try:

        analytics_service = (
            PortfolioAnalyticsService()
        )

        all_passed &= check(
            "PortfolioAnalyticsService initialization",
            analytics_service is not None,
        )

    except Exception as exc:

        print(
            f"{FAIL} PortfolioAnalyticsService initialization"
        )

        print(
            f"      Error: {exc}"
        )

        return False

    # --------------------------------------------------------------
    # KPI Analytics
    # --------------------------------------------------------------

    try:

        result = analytics_service.get_kpis()

        all_passed &= check(
            "Portfolio KPI analytics",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio KPI analytics"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Risk Analytics
    # --------------------------------------------------------------

    try:

        result = analytics_service.get_risk_analysis()

        all_passed &= check(
            "Portfolio risk analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio risk analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Risk Customer Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_risk_distribution()
        )

        all_passed &= check(
            "Risk customer distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Risk customer distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Risk Exposure Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_risk_exposure_distribution()
        )

        all_passed &= check(
            "Risk exposure distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Risk exposure distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Exposure Analytics
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_exposure_analysis()
        )

        all_passed &= check(
            "Portfolio exposure analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio exposure analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Product Exposure
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_product_exposure()
        )

        all_passed &= check(
            "Product exposure analysis",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Product exposure analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Geographic Exposure
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_geographic_exposure()
        )

        all_passed &= check(
            "Geographic exposure analysis",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Geographic exposure analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Exposure Concentration
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_exposure_concentration()
        )

        all_passed &= check(
            "Exposure concentration analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Exposure concentration analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Segmentation Analytics
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_segmentation_analysis()
        )

        all_passed &= check(
            "Portfolio segmentation analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio segmentation analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Segment Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_segment_distribution()
        )

        all_passed &= check(
            "Portfolio segment distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio segment distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # ==============================================================
    # NEW : Trend Analytics
    # ==============================================================

    try:

        result = (
            analytics_service
            .get_trend_analysis()
        )

        all_passed &= check(
            "Portfolio trend analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio trend analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Latest Trends
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_latest_trends()
        )

        all_passed &= check(
            "Latest portfolio trends",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Latest portfolio trends"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Improving Trends
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_improving_trends()
        )

        all_passed &= check(
            "Improving portfolio trends",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Improving portfolio trends"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Deteriorating Trends
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_deteriorating_trends()
        )

        all_passed &= check(
            "Deteriorating portfolio trends",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Deteriorating portfolio trends"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # ==============================================================
    # NEW : Opportunity Analytics
    # ==============================================================

    try:

        result = (
            analytics_service
            .get_opportunity_analysis()
        )

        all_passed &= check(
            "Portfolio opportunity analysis",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Portfolio opportunity analysis"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Opportunity Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_opportunity_distribution()
        )

        all_passed &= check(
            "Opportunity distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Opportunity distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Customer Opportunity Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_customer_opportunity_distribution()
        )

        all_passed &= check(
            "Customer opportunity distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Customer opportunity distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Opportunity Value Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_opportunity_value_distribution()
        )

        all_passed &= check(
            "Opportunity value distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Opportunity value distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Opportunity Confidence Distribution
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_opportunity_confidence_distribution()
        )

        all_passed &= check(
            "Opportunity confidence distribution",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} Opportunity confidence distribution"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Highest Value Opportunity
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_highest_value_opportunity()
        )

        all_passed &= check(
            "Highest value opportunity",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Highest value opportunity"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # Highest Confidence Opportunity
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_highest_confidence_opportunity()
        )

        all_passed &= check(
            "Highest confidence opportunity",
            isinstance(result, dict)
            and len(result) > 0,
        )

    except Exception as exc:

        print(
            f"{FAIL} Highest confidence opportunity"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # --------------------------------------------------------------
    # High Confidence Opportunities
    # --------------------------------------------------------------

    try:

        result = (
            analytics_service
            .get_high_confidence_opportunities()
        )

        all_passed &= check(
            "High confidence opportunities",
            isinstance(result, list),
        )

    except Exception as exc:

        print(
            f"{FAIL} High confidence opportunities"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # ==============================================================
    # Consolidated Portfolio Overview
    # ==============================================================

    try:

        result = (
            analytics_service
            .get_portfolio_overview()
        )

        required_sections = {
            "kpis",
            "risk",
            "exposure",
            "segmentation",
            "trends",
            "opportunities",
        }

        all_passed &= check(
            "Consolidated portfolio overview",
            isinstance(result, dict)
            and required_sections.issubset(
                result.keys()
            ),
        )

    except Exception as exc:

        print(
            f"{FAIL} Consolidated portfolio overview"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # ==============================================================
    # Executive Analytical Snapshot
    # ==============================================================

    try:

        result = (
            analytics_service
            .get_analytical_snapshot()
        )

        required_sections = {
            "kpis",
            "risk",
            "exposure",
            "trends",
            "opportunities",
        }

        all_passed &= check(
            "Consolidated analytical snapshot",
            isinstance(result, dict)
            and required_sections.issubset(
                result.keys()
            ),
        )

    except Exception as exc:

        print(
            f"{FAIL} Consolidated analytical snapshot"
        )

        print(
            f"      Error: {exc}"
        )

        all_passed = False

    # ==============================================================
    # Final Result
    # ==============================================================

    print()
    print("=" * 70)

    if all_passed:

        print(
            "Portfolio Analytics Service : PASSED"
        )

    else:

        print(
            "Portfolio Analytics Service : FAILED"
        )

    print("=" * 70)

    return all_passed


# ------------------------------------------------------------------
# Local Execution
# ------------------------------------------------------------------

if __name__ == "__main__":

    success = run_smoke_test()

    if not success:

        sys.exit(1)
