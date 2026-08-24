"""
portfolio_trend_service.py

Provides portfolio trend analytics.

Responsibilities
----------------
- Retrieve portfolio trend data from PortfolioRepository.
- Analyse metric movements across reporting periods.
- Calculate absolute and percentage changes.
- Identify improving and deteriorating trends.
- Provide reusable trend analytics for downstream services.

Business calculations are implemented within this service, while
database access remains encapsulated by PortfolioRepository.

The service operates on the analytical portfolio repository and
does not access operational customer data directly.
"""

from typing import Any, Dict, List, Optional

from src.database.portfolio_repository import (
    PortfolioRepository,
)


class PortfolioTrendService:
    """
    Service responsible for portfolio trend analysis.
    """

    def __init__(
        self,
        repository: Optional[PortfolioRepository] = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else PortfolioRepository()
        )

    # --------------------------------------------------------------
    # Trend Analysis
    # --------------------------------------------------------------

    def analyze_trends(self) -> Dict[str, Any]:
        """
        Analyse the available portfolio trend metrics.

        Returns
        -------
        dict
            Consolidated trend analysis.

        Raises
        ------
        ValueError
            If no portfolio trend data is available.
        """

        rows = self.repository.get_portfolio_trends()

        if not rows:
            raise ValueError(
                "No portfolio trend data is available."
            )

        metrics = self._group_by_metric(rows)

        trend_results = []

        for metric_name, metric_rows in metrics.items():

            ordered_rows = self._sort_by_period(
                metric_rows
            )

            analysis = self._calculate_metric_trend(
                ordered_rows
            )

            trend_results.append(
                analysis
            )

        return {
            "metric_count": len(trend_results),
            "metrics": trend_results,
        }

    # --------------------------------------------------------------
    # Metric Trends
    # --------------------------------------------------------------

    def get_metric_trend(
        self,
        metric_name: str,
    ) -> Dict[str, Any]:
        """
        Analyse a specific portfolio metric.

        Parameters
        ----------
        metric_name:
            Name of the portfolio metric.

        Returns
        -------
        dict
            Trend analysis for the requested metric.
        """

        rows = self.repository.get_portfolio_trends()

        if not rows:
            raise ValueError(
                "No portfolio trend data is available."
            )

        metric_rows = [
            row
            for row in rows
            if row["metric_name"] == metric_name
        ]

        if not metric_rows:
            raise ValueError(
                f"No trend data found for metric "
                f"'{metric_name}'."
            )

        ordered_rows = self._sort_by_period(
            metric_rows
        )

        return self._calculate_metric_trend(
            ordered_rows
        )

    # --------------------------------------------------------------
    # Latest Trend Values
    # --------------------------------------------------------------

    def get_latest_trends(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return the latest available value for each portfolio metric.

        Returns
        -------
        list[dict]
            Latest metric values.
        """

        rows = self.repository.get_portfolio_trends()

        if not rows:
            raise ValueError(
                "No portfolio trend data is available."
            )

        metrics = self._group_by_metric(rows)

        latest_values = []

        for metric_name, metric_rows in metrics.items():

            latest_row = max(
                metric_rows,
                key=lambda row: row["snapshot_date"],
            )

            latest_values.append(
                dict(latest_row)
            )

        return latest_values

    # --------------------------------------------------------------
    # Improving Trends
    # --------------------------------------------------------------

    def get_improving_trends(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return metrics whose latest value increased relative
        to the previous reporting period.

        Note
        ----
        An increase is treated as a mathematical movement only.
        Whether an increase is positive or negative from a
        business perspective depends on the metric.
        """

        trend_analysis = self.analyze_trends()

        return [
            metric
            for metric in trend_analysis["metrics"]
            if metric["direction"] == "increasing"
        ]

    # --------------------------------------------------------------
    # Deteriorating Trends
    # --------------------------------------------------------------

    def get_deteriorating_trends(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return metrics whose latest value decreased relative
        to the previous reporting period.

        Business interpretation of deterioration remains outside
        this service because metric semantics may differ.
        """

        trend_analysis = self.analyze_trends()

        return [
            metric
            for metric in trend_analysis["metrics"]
            if metric["direction"] == "decreasing"
        ]

    # --------------------------------------------------------------
    # Period Change
    # --------------------------------------------------------------

    def calculate_period_change(
        self,
        metric_name: str,
    ) -> Dict[str, Any]:
        """
        Calculate the latest period-over-period change for a
        specific metric.

        Returns
        -------
        dict
            Absolute and percentage change.
        """

        metric_analysis = self.get_metric_trend(
            metric_name
        )

        return {
            "metric_name": metric_name,
            "current_value": metric_analysis[
                "current_value"
            ],
            "previous_value": metric_analysis[
                "previous_value"
            ],
            "absolute_change": metric_analysis[
                "absolute_change"
            ],
            "percentage_change": metric_analysis[
                "percentage_change"
            ],
            "direction": metric_analysis[
                "direction"
            ],
        }

    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    @staticmethod
    def _group_by_metric(
        rows: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group trend records by metric name.
        """

        grouped: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

        for row in rows:

            metric_name = row["metric_name"]

            grouped.setdefault(
                metric_name,
                [],
            ).append(row)

        return grouped

    @staticmethod
    def _sort_by_period(
        rows: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Sort metric records chronologically.

        The reporting_period is used when available. Snapshot
        date provides the fallback ordering mechanism.
        """

        return sorted(
            rows,
            key=lambda row: (
                row.get("reporting_period") or "",
                row.get("snapshot_date") or "",
            ),
        )

    @staticmethod
    def _calculate_metric_trend(
        rows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate trend information for one metric.
        """

        latest = rows[-1]

        current_value = latest["metric_value"]

        if len(rows) < 2:

            return {
                "metric_name": latest["metric_name"],
                "reporting_period": latest[
                    "reporting_period"
                ],
                "current_value": current_value,
                "previous_value": None,
                "absolute_change": None,
                "percentage_change": None,
                "direction": "insufficient_history",
            }

        previous = rows[-2]

        previous_value = previous["metric_value"]

        absolute_change = (
            current_value - previous_value
        )

        if previous_value == 0:

            percentage_change = None

        else:

            percentage_change = (
                absolute_change
                / abs(previous_value)
                * 100
            )

        if absolute_change > 0:

            direction = "increasing"

        elif absolute_change < 0:

            direction = "decreasing"

        else:

            direction = "stable"

        return {
            "metric_name": latest["metric_name"],
            "reporting_period": latest[
                "reporting_period"
            ],
            "current_value": round(
                current_value,
                2,
            ),
            "previous_value": round(
                previous_value,
                2,
            ),
            "absolute_change": round(
                absolute_change,
                2,
            ),
            "percentage_change": (
                round(
                    percentage_change,
                    2,
                )
                if percentage_change is not None
                else None
            ),
            "direction": direction,
        }
