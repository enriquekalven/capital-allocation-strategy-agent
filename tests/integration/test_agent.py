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

"""Smoke tests for the Small Business Loan Agent."""

import dotenv
import pytest
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from capital_allocation_strategy_agent.agent import root_agent

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


async def _run_agent(user_input: str) -> str:
    """Helper to run the agent and return the final response text."""
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="test_user")
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text
    return response


REGRESSION_QUESTIONS = [
    "We are losing 4% MoM in the 'Artisan' segment to Square/Stripe. Analyze our Q1 risk data and external market comps. Identify the 'High-Growth' segment we can win back and propose a proactive capital structure that beats the competition while staying within our Tier 1 capital ratios.",
    "What is the fastest way to win back the 'B2B Retail / Micro-Merchant' segment? Analyze competing rates from Square and run a capital simulation to find the exact interest rate we should offer to maintain a 12%+ IRR.",
    "If we deploy $200M of excess liquidity into the 'Small Scale Manufacturing' segment, will our Tier 1 capital ratios fall below 10.5% during high-stress quarters? Validate this against our Q1 risk datasets.",
    "Check the process status for scenario SBL-2025-00142 and tell me if we are pending human approval from the board or if we can proceed to final execution.",
    "Analyze the leakage in our 'Artisan' segment and propose a strategy to win back market share.",
    "What are the capital implications of investing an additional $50M into our 'Fintech Solutions' product line?",
    "Can you assess the risk of re-allocating 15% of our growth capital to emerging markets, considering our current Tier 1 ratios?",
    "How are our competitors impacting our 'Premium Banking' segment, and what capital adjustments should we consider?",
    "I need a comprehensive strategic response to the Q3 market shifts. Focus on dynamic capital structures.",
    "Can you generate a visual concept for a new marketing campaign to support the 'NextGen Banking' initiative?"
]


@pytest.mark.asyncio
@pytest.mark.parametrize("query", REGRESSION_QUESTIONS)
async def test_regression_questions(query):
    """Regression suite for all C-Suite strategic queries."""
    response = await _run_agent(query)
    assert response, f"Agent returned an empty response for query: {query}"


@pytest.mark.asyncio
async def test_status_check():
    """Agent should handle a status check request."""
    response = await _run_agent("What is the status on SBL-2025-12345")
    assert response, "Agent returned an empty response"

