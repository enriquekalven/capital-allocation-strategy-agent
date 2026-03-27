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

"""Underwriting Agent definition."""

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig, HttpOptions, HttpRetryOptions
from capital_allocation_strategy_agent.shared_libraries.firestore_utils.state_callbacks import (
    after_agent_callback_with_state_logging,
    before_agent_callback_with_state_check,
)
from capital_allocation_strategy_agent.sub_agents.underwriting.models import StrategyBoardBriefing
from capital_allocation_strategy_agent.sub_agents.underwriting.prompt import UNDERWRITING_PROMPT
from capital_allocation_strategy_agent.sub_agents.underwriting.tools import (
    get_internal_business_data,
)

MODEL_NAME = "gemini-2.5-flash"


underwriting_agent = LlmAgent(
    name="PortfolioRiskAgent",
    model=MODEL_NAME,
    generate_content_config=GenerateContentConfig(
        http_options=HttpOptions(
            retry_options=HttpRetryOptions(initial_delay=1, attempts=2),
        ),
    ),
    instruction=UNDERWRITING_PROMPT,
    description="Validates internal Q1 risk datasets and Tier 1 capital ratios",
    before_agent_callback=before_agent_callback_with_state_check,
    tools=[get_internal_business_data],
    after_agent_callback=after_agent_callback_with_state_logging,
    output_schema=StrategyBoardBriefing,
    output_key="PortfolioRiskAgent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
