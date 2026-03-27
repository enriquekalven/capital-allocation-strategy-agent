# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for the Loan Decision Agent — mock decision finalization."""

from google.adk.tools.tool_context import ToolContext
from capital_allocation_strategy_agent.shared_libraries.logging_config import get_logger

logger = get_logger(__name__)


def finalize_loan_decision(tool_context: ToolContext) -> dict:
    """
    Finalize the loan decision and generate a decision letter reference.

    In production, this would record the decision in Cymbal Bank's loan origination
    system and trigger generation of official decision letters.

    Args:
        tool_context: The tool context with access to session state.

    Returns:
        dict: Final decision details.
    """
    try:
        loan_request_id = tool_context.state.get("loan_request_id")
        application_data = tool_context.state.get("MarketIntelligenceAgent_output")
        pricing_data = tool_context.state.get("CapitalStructureAgent_output")

        if not loan_request_id:
            loan_request_id = "STRAT-2026-00142"


        if not application_data:
            application_data = {"loan_amount_requested": "$1,000,000", "loan_term_months": "60"}

        if not pricing_data:
            pricing_data = {"interest_rate": "7.5%"}


        strategy_directive_id = tool_context.state.get("strategy_directive_id")
        if not strategy_directive_id:
            strategy_directive_id = tool_context.state.get("loan_request_id")
            if not strategy_directive_id:
                strategy_directive_id = "STRAT-2026-00142"

        logger.info(f"Finalizing governance decision for: {strategy_directive_id}")

        # Generate decision letter ID
        decision_letter_id = f"DL-{strategy_directive_id.replace('STRAT-', '')}-001"

        # Extract approved terms from pricing
        approved_rate = pricing_data.get("interest_rate", "N/A") if isinstance(pricing_data, dict) else "N/A"

        return {
            "status": "success",
            "decision": "STRATEGY_APPROVED",
            "decision_letter_id": decision_letter_id,
            "approved_amount": "N/A",
            "approved_rate": approved_rate,
            "approved_term": "N/A",
            "conditions": [
                "Board sign-off required for allocation shifts > 30 bps",
                "Internal audit verification of stress tests complete",
            ],
            "message": (
                f"Capital Allocation Strategy {strategy_directive_id} has been approved by Governance. "
                f"Decision directive {decision_letter_id} has been generated. "
                "The target interest simulation maintains compliance within Tier 1 constraints."
            ),
        }


    except Exception as e:
        logger.error(f"Error finalizing loan decision: {e}")
        return {"status": "error", "message": f"Error: {e!s}"}
