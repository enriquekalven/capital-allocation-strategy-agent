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

"""Data models for underwriting — combines validation and eligibility checks."""

from typing import Literal

from pydantic import BaseModel, Field


class FieldComparison(BaseModel):
    """Comparison of a field between the application and internal records."""

    field_name: str = Field(description="Name of the field being compared")
    application_value: str = Field(description="Value from the loan application document")
    internal_value: str = Field(description="Value from Cymbal Bank's internal records")
    match_status: Literal["Match", "No Match", "Partial Match"] = Field(description="Whether the values match")
    notes: str = Field(default="", description="Additional notes about the comparison")


class StrategyBoardBriefing(BaseModel):
    """Structured output model for the C-Suite Strategy Board Briefing."""

    tier_1_capital_status: str = Field(description="Current Tier 1 capital status (e.g., 'MAINTAINED' or 'BREACHED')")
    risk_score: str = Field(description="A numeric or categorical risk score (e.g., 'M1 - Low Risk')")
    compliance_notes: str = Field(description="Any concerns regarding regulatory limits or credit policies")
    summary: str = Field(description="Executive summary of the portfolio risk impact or strategy outline")
