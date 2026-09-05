
from typing import Any, Dict


class ResponseFormattingService:
    """
    Formats Coordinator responses for channel/UI consumption while
    preserving orchestration and routing metadata.

    Architectural responsibility:
        - Transform response presentation.
        - Preserve execution/routing metadata.
        - Do not infer or reconstruct routing decisions.
        - Do not contain agent-specific orchestration logic.
    """

    def format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a successful Coordinator response while preserving
        orchestration metadata.

        Failed responses are returned unchanged.
        """
        if not response["success"]:
            return response

        agents = response.get("agents_invoked", [])

        if agents == ["policy"]:
            return self._format_policy_response(response)

        if agents == ["customer"]:
            return self._format_customer_response(response)

        if "policy" in agents and "customer" in agents:
            return self._format_policy_customer_response(response)

        return response

    def _format_policy_response(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format a policy-only response while preserving routing metadata.
        """
        formatted_response = {
            "success": True,
            "response_type": "policy",
            "title": "Policy Response",
            "sections": [
                {
                    "heading": "Answer",
                    "type": "text",
                    "content": response["responses"]["policy"],
                }
            ],
        }

        return self._with_metadata(formatted_response, response)

    def _format_customer_response(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format a customer-only response while preserving routing metadata.
        """
        formatted_response = {
            "success": True,
            "response_type": "customer",
            "title": "Customer Assessment",
            "sections": [
                {
                    "heading": "Assessment",
                    "type": "customer",
                    "content": response["responses"]["customer"],
                }
            ],
        }

        return self._with_metadata(formatted_response, response)

    def _format_policy_customer_response(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format a combined policy + customer response while preserving
        routing metadata.
        """
        formatted_response = {
            "success": True,
            "response_type": "policy_customer",
            "title": "Customer Policy Assessment",
            "sections": [
                {
                    "heading": "Applicable Policy",
                    "type": "text",
                    "content": response["responses"]["policy"],
                },
                {
                    "heading": "Customer Assessment",
                    "type": "customer",
                    "content": response["responses"]["customer"],
                },
            ],
        }

        return self._with_metadata(formatted_response, response)

    @staticmethod
    def _with_metadata(
        formatted_response: Dict[str, Any],
        original_response: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Preserve Coordinator-owned metadata in the formatted response.

        The formatter must never infer these values from response_type,
        sections, or response content. The original Coordinator response
        remains the source of truth.
        """
        formatted_response["agents_invoked"] = original_response.get(
            "agents_invoked",
            []
        )

        formatted_response["routing"] = original_response.get(
            "routing"
        )

        return formatted_response

