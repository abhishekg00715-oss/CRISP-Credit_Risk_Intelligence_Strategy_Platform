
from src.initialization.application_startup import (
    ApplicationStartup,
)


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


if __name__ == "__main__":
    test_portfolio_summary()

    print(
        "Portfolio Summary Service smoke test [PASS]"
    )

