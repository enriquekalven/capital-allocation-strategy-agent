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

"""Tools for the Underwriting Agent — mock internal data lookup."""

import json

from google.adk.tools.tool_context import ToolContext

from capital_allocation_strategy_agent.shared_libraries.logging_config import get_logger

logger = get_logger(__name__)

# Mock C-Suite Strategic Portfolio records (simulates Cymbal Bank's internal database)
# In production, this would query the bank's actual data warehouse or stress-cube API
MOCK_INTERNAL_RECORDS = {
    "STRAT-2026-00142": {
        "scenario_name": "Artisan Segment Churn Counter-Offensive",
        "segment_name": "Artisan SMB (High Balance solopreneurs)",
        "current_churn": "4.2% MoM (High-Value attrition)",
        "competitor_yield": "Circle & Solid: 4.5% yield-on-cash",
        "current_tier_1_ratio": "13.2%",
        "regulatory_floor": "12.5% (+30bps buffer threshold)",
        "internal_concentration_limits": "Max unsecured creation credit: $850M_Cap",
        "estimated_retention_lift": "72% Recovery within 90 days",
    },
    "STRAT-2026-00143": {
        "scenario_name": "High-Growth B2B Retail Micro-Merchant expansion",
        "segment_name": "B2B Solopreneurs / Micro-merchants (> $2M revenue, < 5 emp)",
        "current_churn": "1.8% MoM (Rising risk)",
        "competitor_yield": "Square & Stripe: Standard yields",
        "current_tier_1_ratio": "12.9%",
        "regulatory_floor": "12.5%",
        "internal_concentration_limits": "$500M_Cap",
    },
    "STRAT-2026-00144": {
        "scenario_name": "Liquidity Deployment - Small Scale Manufacturing",
        "segment_name": "Small Scale Manufacturing",
        "deployment_amount": "$200M",
        "current_tier_1_ratio": "13.2%",
        "regulatory_floor": "10.5% (Stress test limit for manufacturing concentration)",
        "internal_concentration_limits": "$2B_Cap",
    },
}


def get_internal_business_data(tool_context: ToolContext) -> dict:
    """
    Retrieve Cymbal Bank's internal business records for underwriting validation.

    In production, this would query Cymbal Bank's internal systems.
    For this demo, returns mock data matching the sample loan applications.

    Args:
        tool_context: The tool context with access to session state.

    Returns:
        dict: Internal business data for the given loan request.
    """
    try:
        loan_request_id = tool_context.state.get("loan_request_id")

        if not loan_request_id:
            return {
                "status": "error",
                "message": "loan_request_id not found in session state",
            }

        logger.info(f"Fetching internal records for: {loan_request_id}")

        internal_data = MOCK_INTERNAL_RECORDS.get(loan_request_id)

        if not internal_data:
            # Fall back to default mock record for any loan ID (demo purposes)
            default_record = next(iter(MOCK_INTERNAL_RECORDS.values()))
            internal_data = {**default_record}
            logger.info(f"No exact match for {loan_request_id}, using default mock record")

        return {
            "status": "success",
            "loan_request_id": loan_request_id,
            "internal_data": json.dumps(internal_data),
        }

    except Exception as e:
        logger.error(f"Error fetching internal business data: {e}")
        return {"status": "error", "message": f"Error: {e!s}"}
