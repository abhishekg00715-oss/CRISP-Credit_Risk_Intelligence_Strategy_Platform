"""
portfolio_analytics_service.py

Provides a unified analytical interface for Portfolio Intelligence.

Responsibilities
----------------
- Orchestrate portfolio analytical services.
- Provide a single entry point for portfolio analytics.
- Combine KPI, segmentation, risk, exposure, trend and
  opportunity analytics.
- Support reusable analytical operations for downstream agents
  and presentation services.

This service is intentionally an orchestration/facade layer.

Business calculations remain within the specialised analytics
services. Database access remains encapsulated by
PortfolioRepository.

The Portfolio Agent should consume this service rather than
directly accessing the repository.
"""

from typing import Any, Dict, Optional

from src.services.portfolio_kpi_service import (
    PortfolioKPIService,
)

from src.services.portfolio_segment_service import (
    PortfolioSegmentService,
)

from src.services.portfolio_risk_service import (
    PortfolioRiskService,
)

from src.services.portfolio_exposure_service import (
    PortfolioExposureService,
)

from src.services.portfolio_trend_service import (
    PortfolioTrendService,
)

from src.services.portfolio_opportunity_service import (
    PortfolioOpportunityService,
)


class PortfolioAnalyticsService:
    """
    Unified service for Portfolio Analytics.

    Acts as a facade over the specialised portfolio analytics
    services.
    """

    def __init__(
        self,
        kpi_service: Optional[PortfolioKPIService] = None,
        segment_service: Optional[PortfolioSegmentService] = None,
        risk_service: Optional[PortfolioRiskService] = None,
        exposure_service: Optional[PortfolioExposureService] = None,
        trend_service: Optional[PortfolioTrendService] = None,
        opportunity_service: Optional[
            PortfolioOpportunityService
        ] = None,
    ) -> None:

        self.kpi_service = (
            kpi_service
            if kpi_service is not None
            else PortfolioKPIService()
        )

        self.segment_service = (
            segment_service
            if segment_service is not None
            else PortfolioSegmentService()
        )

        self.risk_service = (
            risk_service
            if risk_service is not None
            else PortfolioRiskService()
        )

        self.exposure_service = (
            exposure_service
            if exposure_service is not None
            else PortfolioExposureService()
        )

        self.trend_service = (
            trend_service
            if trend_service is not None
            else PortfolioTrendService()
        )

        self.opportunity_service = (
            opportunity_service
            if opportunity_service is not None
            else PortfolioOpportunityService()
        )

    # --------------------------------------------------------------
    # Portfolio Overview
    # --------------------------------------------------------------

    def get_portfolio_overview(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio overview.

        Combines the primary KPI, risk, exposure, segmentation,
        trend and opportunity views into a single analytical
        response.
        """

        return {
            "kpis": self.kpi_service.get_portfolio_kpis(),

            "risk": self.risk_service.analyze_risk_distribution(),

            "exposure": self.exposure_service.analyze_exposure(),

            "segmentation": (
                self.segment_service.analyze_segments()
            ),

            "trends": (
                self.trend_service.analyze_trends()
            ),

            "opportunities": (
                self.opportunity_service.analyze_opportunities()
            ),
        }

    # --------------------------------------------------------------
    # Portfolio KPIs
    # --------------------------------------------------------------

    def get_kpis(self) -> Dict[str, Any]:
        """
        Return portfolio-level KPI metrics.
        """

        return self.kpi_service.get_portfolio_kpis()

    # --------------------------------------------------------------
    # Risk Analytics
    # --------------------------------------------------------------

    def get_risk_analysis(self) -> Dict[str, Any]:
        """
        Return portfolio risk distribution analytics.
        """

        return self.risk_service.analyze_risk_distribution()

    def get_risk_distribution(self) -> list[dict]:
        """
        Return customer distribution across risk bands.
        """

        return self.risk_service.get_customer_distribution()

    def get_risk_exposure_distribution(
        self,
    ) -> list[dict]:
        """
        Return portfolio exposure distributed across risk bands.
        """

        return self.risk_service.get_exposure_distribution()

    # --------------------------------------------------------------
    # Exposure Analytics
    # --------------------------------------------------------------

    def get_exposure_analysis(self) -> Dict[str, Any]:
        """
        Return consolidated portfolio exposure analytics.
        """

        return self.exposure_service.analyze_exposure()

    def get_product_exposure(self) -> list[dict]:
        """
        Return portfolio exposure aggregated by product type.
        """

        return self.exposure_service.get_product_exposure()

    def get_geographic_exposure(self) -> list[dict]:
        """
        Return portfolio exposure aggregated by state.
        """

        return self.exposure_service.get_geographic_exposure()

    def get_exposure_concentration(self) -> Dict[str, Any]:
        """
        Return portfolio exposure concentration metrics.
        """

        return self.exposure_service.get_exposure_concentration()

    # --------------------------------------------------------------
    # Segmentation Analytics
    # --------------------------------------------------------------

    def get_segmentation_analysis(self) -> Dict[str, Any]:
        """
        Return portfolio segmentation analytics.
        """

        return self.segment_service.analyze_segments()

    def get_segment_distribution(self) -> list[dict]:
        """
        Return customer distribution across portfolio segments.
        """

        return self.segment_service.get_segment_distribution()

    # --------------------------------------------------------------
    # Trend Analytics
    # --------------------------------------------------------------

    def get_trend_analysis(self) -> Dict[str, Any]:
        """
        Return consolidated portfolio trend analytics.
        """

        return self.trend_service.analyze_trends()

    def get_latest_trends(self) -> list[dict]:
        """
        Return the latest available value for each portfolio
        trend metric.
        """

        return self.trend_service.get_latest_trends()

    def get_improving_trends(self) -> list[dict]:
        """
        Return portfolio metrics showing an increasing movement.
        """

        return self.trend_service.get_improving_trends()

    def get_deteriorating_trends(self) -> list[dict]:
        """
        Return portfolio metrics showing a decreasing movement.
        """

        return self.trend_service.get_deteriorating_trends()

    # --------------------------------------------------------------
    # Opportunity Analytics
    # --------------------------------------------------------------

    def get_opportunity_analysis(self) -> Dict[str, Any]:
        """
        Return consolidated portfolio opportunity analytics.
        """

        return self.opportunity_service.analyze_opportunities()

    def get_opportunity_distribution(
        self,
    ) -> list[dict]:
        """
        Return opportunity distribution by opportunity type.
        """

        return (
            self.opportunity_service
            .get_opportunity_distribution()
        )

    def get_customer_opportunity_distribution(
        self,
    ) -> list[dict]:
        """
        Return opportunities ranked by eligible customer count.
        """

        return (
            self.opportunity_service
            .get_customer_opportunity_distribution()
        )

    def get_opportunity_value_distribution(
        self,
    ) -> list[dict]:
        """
        Return opportunities ranked by estimated value.
        """

        return (
            self.opportunity_service
            .get_value_distribution()
        )

    def get_opportunity_confidence_distribution(
        self,
    ) -> list[dict]:
        """
        Return opportunities ranked by confidence score.
        """

        return (
            self.opportunity_service
            .get_confidence_distribution()
        )

    def get_highest_value_opportunity(
        self,
    ) -> Dict[str, Any]:
        """
        Return the highest-value portfolio opportunity.
        """

        return (
            self.opportunity_service
            .get_highest_value_opportunity()
        )

    def get_highest_confidence_opportunity(
        self,
    ) -> Dict[str, Any]:
        """
        Return the highest-confidence portfolio opportunity.
        """

        return (
            self.opportunity_service
            .get_highest_confidence_opportunity()
        )

    def get_high_confidence_opportunities(
        self,
        threshold: float = 0.70,
    ) -> list[dict]:
        """
        Return opportunities meeting the supplied confidence
        threshold.
        """

        return (
            self.opportunity_service
            .get_high_confidence_opportunities(
                threshold=threshold
            )
        )

    # --------------------------------------------------------------
    # Executive Analytical Snapshot
    # --------------------------------------------------------------

    def get_analytical_snapshot(self) -> Dict[str, Any]:
        """
        Return a compact analytical snapshot suitable for
        downstream summary or narrative generation.

        This method intentionally returns structured analytical
        facts rather than natural-language interpretation.
        """

        kpis = self.get_kpis()

        dominant_risk = (
            self.risk_service.get_dominant_risk_band()
        )

        highest_exposure = (
            self.exposure_service.get_highest_exposure_category()
        )

        concentration = (
            self.exposure_service.get_exposure_concentration()
        )

        trend_analysis = (
            self.trend_service.analyze_trends()
        )

        opportunity_analysis = (
            self.opportunity_service.analyze_opportunities()
        )

        return {
            "kpis": kpis,

            "risk": {
                "dominant_risk_band": dominant_risk,
            },

            "exposure": {
                "highest_exposure_category": highest_exposure,
                "concentration": concentration,
            },

            "trends": {
                "analysis": trend_analysis,
            },

            "opportunities": {
                "analysis": opportunity_analysis,
            },
        }
