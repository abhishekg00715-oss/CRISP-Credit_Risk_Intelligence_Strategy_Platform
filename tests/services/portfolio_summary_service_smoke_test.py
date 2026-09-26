from typing import Any, Dict

from src.initialization.application_startup import (
    ApplicationStartup,
)

from src.services.portfolio_summary_service import (
    PortfolioSummaryService,
)


# ------------------------------------------------------------------
# Application Startup
# ------------------------------------------------------------------

def create_summary_service():
    """
    Create PortfolioSummaryService through the application
    startup lifecycle.
    """

    startup = (
        ApplicationStartup()
        .initialize()
    )

    return startup.portfolio_summary_service


# ------------------------------------------------------------------
# Existing Application-Level Smoke Test
# ------------------------------------------------------------------

def test_portfolio_summary() -> None:
    """
    Validate that PortfolioSummaryService returns the complete
    consolidated analytical summary.
    """

    summary_service = (
        create_summary_service()
    )

    response = (
        summary_service
        .get_summary()
    )

    assert isinstance(
        response,
        dict,
    )

    assert (
        "summary"
        in response
    )

    assert (
        "evidence"
        in response
    )

    summary = (
        response["summary"]
    )

    assert (
        "kpis"
        in summary
    )

    assert (
        "risk"
        in summary
    )

    assert (
        "exposure"
        in summary
    )

    assert (
        "trends"
        in summary
    )

    assert (
        "opportunities"
        in summary
    )

    evidence = (
        response["evidence"]
    )

    assert (
        evidence["source"]
        == "PortfolioSummaryService"
    )

    assert (
        evidence["upstream_source"]
        == "PortfolioAnalyticsService"
    )


# ------------------------------------------------------------------
# Deterministic Analytics Stub
# ------------------------------------------------------------------

class FakePortfolioAnalyticsService:
    """
    Minimal analytics-service substitute used to isolate
    PortfolioSummaryService.

    No database, repository, or LLM is involved.
    """

    def __init__(
        self,
        snapshot: Dict[str, Any],
    ) -> None:

        self.snapshot = snapshot
        self.call_count = 0

    def get_analytical_snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Return the deterministic analytical snapshot.
        """

        self.call_count += 1

        return self.snapshot


def create_test_snapshot() -> Dict[str, Any]:
    """
    Create deterministic analytical data.

    Values are intentionally synthetic because this test validates
    CRA-14 behaviour rather than portfolio calculations.
    """

    return {
        "kpis": {
            "total_customers": 1000,
            "average_credit_score": 742.5,
        },

        "risk": {
            "dominant_risk_band": "medium",
        },

        "exposure": {
            "highest_exposure_category": "credit_card",
            "concentration": {
                "top_category_share": 0.42,
            },
        },

        "trends": {
            "analysis": {
                "direction": "stable",
            },
        },

        "opportunities": {
            "analysis": {
                "high_confidence_count": 12,
            },
        },
    }


# ------------------------------------------------------------------
# Isolation Test 1
# ------------------------------------------------------------------

def test_summary_delegates_to_analytics_snapshot() -> None:
    """
    Verify that PortfolioSummaryService obtains its analytical
    data through PortfolioAnalyticsService.
    """

    analytics_service = (
        FakePortfolioAnalyticsService(
            create_test_snapshot()
        )
    )

    summary_service = (
        PortfolioSummaryService(
            analytics_service=analytics_service
        )
    )

    summary_service.get_summary()

    assert (
        analytics_service.call_count
        == 1
    )


# ------------------------------------------------------------------
# Isolation Test 2
# ------------------------------------------------------------------

def test_summary_preserves_analytical_content() -> None:
    """
    Verify that PortfolioSummaryService preserves the analytical
    domains supplied by PortfolioAnalyticsService.
    """

    snapshot = (
        create_test_snapshot()
    )

    analytics_service = (
        FakePortfolioAnalyticsService(
            snapshot
        )
    )

    summary_service = (
        PortfolioSummaryService(
            analytics_service=analytics_service
        )
    )

    response = (
        summary_service
        .get_summary()
    )

    summary = (
        response["summary"]
    )

    assert (
        summary["kpis"]
        == snapshot["kpis"]
    )

    assert (
        summary["risk"]
        == snapshot["risk"]
    )

    assert (
        summary["exposure"]
        == snapshot["exposure"]
    )

    assert (
        summary["trends"]
        == snapshot["trends"]
    )

    assert (
        summary["opportunities"]
        == snapshot["opportunities"]
    )


# ------------------------------------------------------------------
# Isolation Test 3
# ------------------------------------------------------------------

def test_summary_propagates_analytics_failure() -> None:
    """
    Verify that PortfolioSummaryService does not silently hide
    failures from PortfolioAnalyticsService.
    """

    class FailingAnalyticsService:

        def get_analytical_snapshot(
            self,
        ) -> Dict[str, Any]:

            raise RuntimeError(
                "Analytics snapshot unavailable"
            )

    summary_service = (
        PortfolioSummaryService(
            analytics_service=(
                FailingAnalyticsService()
            )
        )
    )

    try:

        summary_service.get_summary()

        assert False, (
            "Expected analytics failure "
            "to propagate."
        )

    except RuntimeError as exc:

        assert (
            str(exc)
            == "Analytics snapshot unavailable"
        )


# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

def main() -> None:
    """
    Execute CRA-14 PortfolioSummaryService smoke tests.
    """

    test_portfolio_summary()

    print(
        "Portfolio Summary Service "
        "application smoke test       [PASS]"
    )

    test_summary_delegates_to_analytics_snapshot()

    print(
        "Portfolio Summary Service "
        "delegation test               [PASS]"
    )

    test_summary_preserves_analytical_content()

    print(
        "Portfolio Summary Service "
        "content preservation test     [PASS]"
    )

    test_summary_propagates_analytics_failure()

    print(
        "Portfolio Summary Service "
        "failure handling test         [PASS]"
    )

    print()
    print(
        "Portfolio Summary Service "
        "CRA-14 isolated testing       [PASS]"
    )


if __name__ == "__main__":
    main()
