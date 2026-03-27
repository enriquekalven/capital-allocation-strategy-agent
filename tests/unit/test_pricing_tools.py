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

"""Unit tests for the Pricing/Capital Structure Agent tools."""

import pytest
from unittest.mock import MagicMock
from capital_allocation_strategy_agent.sub_agents.pricing.tools import calculate_loan_pricing


class TestCalculateLoanPricing:
    def test_calculate_with_missing_state_uses_fallback(self):
        # Create a mock ToolContext with an empty state dictionary
        mock_context = MagicMock()
        mock_context.state = {}

        result = calculate_loan_pricing(mock_context)

        # It should fallback to a success simulation rather than failing!
        assert result["status"] == "success"
        assert result["projected_irr"] == "14.2% (Target: 12.0%)"
        assert "interest_rate" in result

    def test_calculate_with_real_state(self):
        mock_context = MagicMock()
        mock_context.state = {
            "DocumentExtractionAgent_output": {
                "loan_amount_requested": "$500,000",
                "loan_term_months": "36"
            },
            "UnderwritingAgent_output": {
                "eligibility_status": "ELIGIBLE",
                "risk_flags": []
            },
            "loan_request_id": "REQ-123"
        }

        result = calculate_loan_pricing(mock_context)

        assert result["status"] == "success"
        # Since Eligible and no risk flags -> Tier 1 (6.5%)
        assert result["interest_rate"] == "6.5%"
        assert result["risk_tier"] == "Tier 1 - Low Risk"
