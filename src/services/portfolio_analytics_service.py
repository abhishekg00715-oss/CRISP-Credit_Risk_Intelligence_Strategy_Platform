"""
portfolio_analytics_service.py

Provides a unified analytical interface for Portfolio Intelligence.

Responsibilities
----------------
- Orchestrate portfolio analytical services.
- Provide a single entry point for portfolio analytics.
- Combine KPI, segmentation, risk and exposure analytics.
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

    # --------------------------------------------------------------
    # Portfolio Overview
    # --------------------------------------------------------------

    def get_portfolio_overview(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio overview.

        Combines the primary KPI, risk, exposure and segmentation
        views into a single analytical response.
        """

        return {
            "kpis": self.kpi_service.get_portfolio_kpis(),
            "risk": self.risk_service.analyze_risk_distribution(),
            "exposure": self.exposure_service.analyze_exposure(),
            "segmentation": (
                self.segment_service.analyze_segments()
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

        return {
            "kpis": kpis,

            "risk": {
                "dominant_risk_band": dominant_risk,
            },

            "exposure": {
                "highest_exposure_category": highest_exposure,
                "concentration": concentration,
            },
        }
