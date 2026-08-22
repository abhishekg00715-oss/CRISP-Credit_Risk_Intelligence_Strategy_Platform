"""
portfolio_analytics_service_smoke_test.py

Purpose
-------
Smoke test for the Portfolio Analytics Service.

Responsibilities
----------------
- Validate PortfolioAnalyticsService initialization.
- Validate integration with specialised portfolio analytics services.
- Verify that analytical methods execute successfully.
- Verify basic response structure.
- Confirm that the CRA-13 analytical service layer is operational.

This is intentionally a lightweight integration smoke test rather
than a detailed unit-test suite.

Expected Architecture
---------------------
Portfolio Analytical Repository
            |
            v
    PortfolioRepository
            |
            v
+-----------------------------------+
|   Portfolio Analytics Services    |
|                                   |
| KPI | Segment | Risk | Exposure   |
+-----------------------------------+
            |
            v
  PortfolioAnalyticsService
"""

from pathlib import Path
import sys


# ------------------------------------------------------------------
# Repository Root
# ------------------------------------------------------------------

REPO_ROOT = str(
    Path(__file__).resolve().parents[2]
)

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


# ------------------------------------------------------------------
# Service Import
# ------------------------------------------------------------------

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


# ------------------------------------------------------------------
# Test Helpers
# ------------------------------------------------------------------

def print_result(
    test_name: str,
    passed: bool,
) -> None:

    status = "PASS" if passed else "FAIL"

    print(
        f"{test_name:<50} [{status}]"
    )


def validate_dict_response(
    response,
    required_keys=None,
) -> bool:
    """
    Validate that a service response is a dictionary and,
    optionally, contains the expected keys.
    """

    if not isinstance(response, dict):
        return False

    if required_keys:

        return all(
            key in response
            for key in required_keys
        )

    return True


def validate_list_response(
    response,
) -> bool:
    """
    Validate that a service response is a list.
    """

    return isinstance(response, list)


# ------------------------------------------------------------------
# Main Smoke Test
# ------------------------------------------------------------------

def run_smoke_test() -> bool:

    print()

    print("=" * 70)

    print(
        "Portfolio Analytics Service : Smoke Test"
    )

    print("=" * 70)

    all_passed = True

    try:

        # ----------------------------------------------------------
        # Service Initialization
        # ----------------------------------------------------------

        analytics_service = (
            PortfolioAnalyticsService()
        )

        print_result(
            "PortfolioAnalyticsService initialization",
            True,
        )

        # ----------------------------------------------------------
        # KPI Analytics
        # ----------------------------------------------------------

        kpis = (
            analytics_service.get_kpis()
        )

        passed = validate_dict_response(
            kpis
        )

        print_result(
            "Portfolio KPI analytics",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Risk Analysis
        # ----------------------------------------------------------

        risk_analysis = (
            analytics_service.get_risk_analysis()
        )

        passed = validate_dict_response(
            risk_analysis
        )

        print_result(
            "Portfolio risk analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Risk Distribution
        # ----------------------------------------------------------

        risk_distribution = (
            analytics_service.get_risk_distribution()
        )

        passed = validate_list_response(
            risk_distribution
        )

        print_result(
            "Risk customer distribution",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Risk Exposure Distribution
        # ----------------------------------------------------------

        risk_exposure = (
            analytics_service
            .get_risk_exposure_distribution()
        )

        passed = validate_list_response(
            risk_exposure
        )

        print_result(
            "Risk exposure distribution",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Exposure Analysis
        # ----------------------------------------------------------

        exposure_analysis = (
            analytics_service
            .get_exposure_analysis()
        )

        passed = validate_dict_response(
            exposure_analysis
        )

        print_result(
            "Portfolio exposure analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Product Exposure
        # ----------------------------------------------------------

        product_exposure = (
            analytics_service
            .get_product_exposure()
        )

        passed = validate_list_response(
            product_exposure
        )

        print_result(
            "Product exposure analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Geographic Exposure
        # ----------------------------------------------------------

        geographic_exposure = (
            analytics_service
            .get_geographic_exposure()
        )

        passed = validate_list_response(
            geographic_exposure
        )

        print_result(
            "Geographic exposure analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Exposure Concentration
        # ----------------------------------------------------------

        concentration = (
            analytics_service
            .get_exposure_concentration()
        )

        passed = validate_dict_response(
            concentration
        )

        print_result(
            "Exposure concentration analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Segmentation Analysis
        # ----------------------------------------------------------

        segmentation = (
            analytics_service
            .get_segmentation_analysis()
        )

        passed = validate_dict_response(
            segmentation
        )

        print_result(
            "Portfolio segmentation analysis",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Segment Distribution
        # ----------------------------------------------------------

        segment_distribution = (
            analytics_service
            .get_segment_distribution()
        )

        passed = validate_list_response(
            segment_distribution
        )

        print_result(
            "Portfolio segment distribution",
            passed,
        )

        all_passed &= passed

        # ----------------------------------------------------------
        # Analytical Snapshot
        # ----------------------------------------------------------

        snapshot = (
            analytics_service
            .get_analytical_snapshot()
        )

        passed = validate_dict_response(
            snapshot,
            required_keys=[
                "kpis",
                "risk",
                "exposure",
            ],
        )

        print_result(
            "Consolidated analytical snapshot",
            passed,
        )

        all_passed &= passed

    except Exception as exc:

        all_passed = False

        print()

        print(
            f"Smoke test execution failed: {exc}"
        )

    # --------------------------------------------------------------
    # Final Result
    # --------------------------------------------------------------

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

    sys.exit(
        0 if success else 1
    )
