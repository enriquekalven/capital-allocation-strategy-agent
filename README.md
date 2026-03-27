# Capital Allocation Strategy Agent

A multi-agent system built with the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) that automates capital allocation strategy assessment for the C-Suite. It demonstrates sequential multi-agent orchestration, market intelligence diagnostics, portfolio risk validation, and Firestore-backed repair & resume capabilities.

## A. Overview & Functionalities

### Agent Details

| Property             | Value                                       |
| -------------------- | ------------------------------------------- |
| **Interaction Type** | Workflow                                    |
| **Complexity**       | Advanced                                    |
| **Agent Type**       | Multi-Agent (1 orchestrator + 4 sub-agents) |
| **Vertical**         | Financial Services                          |
| **Framework**        | ADK                                         |
| **Model**            | Gemini 3.1 Pro Preview                      |

### Key Features

| Feature                            | Description                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Multi-Agent Orchestration**      | Orchestrator coordinates 4 specialized sub-agents via `AgentTool` in a sequential workflow              |
| **C-Suite Analytics Context**     | Gemini 3.1 Pro Preview evaluates Month-over-Month (MoM) leakage and Tier 1 capital ratios natively      |
| **Structured Strategy Output**     | Each sub-agent returns validated Pydantic models (e.g., `StrategyBoardBriefing`) via `output_schema`     |
| **Executive Decision Tollgate**    | Orchestrator pauses after capital structuring to present results and wait for explicit board approval   |
| **LLM-as-Judge Audit Trace**       | After-agent callback validates trajectory correctness and data grounding before showing responses       |
| **Scenario Repair & Resume**      | Firestore workflow management tracks each step; workflow can pause on edge cases and resume from checkpoint |
| **Visual Validation (Nano Banana)**| Generates visual high-fidelity concepts using image generation tools for board-level design approvals   |

### Key Architecture Pattern (Sequential)

```mermaid
graph LR
    User([User Prompt]) --> Orchestrator[Orchestrator Agent]
    Orchestrator --> State[Firestore check_process_status]
    State --> Audits{Check Constraints}
    Audits -- Success --> MktIntell[Market Intelligence Agent]
    MktIntell --> Risk[Portfolio Risk Agent]
    Risk --> CapStr[Capital Structure Agent]
    CapStr --> Pause[Wait for Board Approval]
    Pause -- Yes --> GovAud[Governance Auditor Agent]
    GovAud --> UserOutput[Strategic Outcome Delivery]
```

### Example Interaction

**Running a strategic C-Suite query**:

```
User: We are losing 4% MoM in the 'Artisan' segment to Square/Stripe. Analyze our Q1 risk data and external market comps. Identify the 'High-Growth' segment we can win back and propose a proactive capital structure that beats the competition while staying within our Tier 1 capital ratios.

Agent: [Calls check_process_status -> checks constraints]
       [Calls MarketIntelligenceAgent -> analyzes market leakage, synthesize circle/solid mock data]
       [Calls PortfolioRiskAgent -> fetches internal risk metrics, checks Tier 1 > 10.5%]
       [Calls CapitalStructureAgent -> models dynamic rate responses]

       📊 Diagnostic Intelligence:
       - Market Leakage: 4% MoM in Artisan segment to Square/Stripe.
       - Competition Check: Competitors offering 4.5% yield sweep.

       📉 Validated Constraints:
       - Tier 1 Capital: 14.82% (Target > 10.5%). Compliance check PASS.

       📐 Proposed Strategic Capital Proposal:
       - Target Yield Spreads: Pivot simulated rates to 6.5%.
       - Competitor Moat: Push premium banking relationships + sweep yield.
       - Projected IRR: 14.2% (Target: 12.0%).
       - Ratio Impact: -15 bps.

       Shall I finalize the Governance Audit and Briefing Canvas? (yes/no)

User: yes

Agent: [Calls GovernanceAuditorAgent -> finalizes executive memo]

       ✅ Directive STRAT-2026-00142 approved by Governance Committee!
```


**Pause, Repair & Resume example** (using `data/sample_application_incomplete.pdf` which has missing fields):

A. submit the incomplete application

```
User: Process this application for SBL-2025-00391
      [uploads sample_application_incomplete.pdf]

Agent: [check_process_status -> initializes new process]
       [DocumentExtractionAgent -> extracts data, detects missing fields]
       [UnderwritingAgent -> before_tool_callback halts execution]

       I encountered an error while processing your application.
       Cannot proceed to UnderwritingAgent: Pending approval
       - Missing 1 critical field(s): loan_amount_requested

       Please provide a complete document or update the application
       with the required field before we can proceed.
       The workflow has been stopped.

       Reference: SBL-2025-00391
```

B. Repair the data in Firestore:

1. Open the [Firestore Console](https://console.cloud.google.com/firestore) and select the `session-states` database
2. Navigate to **`process_states`** collection → document **`SBL-2025-00391`**
3. Under `steps.DocumentExtractionAgent.data`, fill in the missing field:

- Set `loan_amount_requested` to the correct value (e.g., `150000`)

4. Update `steps.DocumentExtractionAgent.status` from `pending_approval` → `completed`
5. Update the root `overall_status` from `pending_approval` → `active`

C. Resume the workflow

```
User: Resume processing for SBL-2025-00391

Agent: [check_process_status -> detects DocumentExtractionAgent completed]
       [Skips DocumentExtractionAgent, resumes from UnderwritingAgent]
       [UnderwritingAgent -> validates against internal records, checks eligibility]
       [PricingAgent -> calculates rate based on risk tier]
       ...continues normal workflow...
```

## B. Architecture Visuals

![Agent Architecture](agent_pattern.png)

**Complete loan application**

```mermaid
sequenceDiagram
    actor User
    participant Orch as CapitalAllocationStrategy<br/>OrchestratorAgent
    participant FS as Firestore<br/>process_states
    participant MI as MarketIntelligence<br/>Agent
    participant PR as PortfolioRisk<br/>Agent
    participant CS as CapitalStructure<br/>Agent
    participant GA as GovernanceAuditor<br/>Agent
    participant Judge as LLM-as-Judge<br/>Gate

    User->>+Orch: Message (Artisan segment loss query)
    Note over Orch: before_agent_callback<br/>extract_request_id

    Orch->>+FS: check_process_status
    FS-->>-Orch: New strategy scenario initialized

    Note over Orch: before_tool_callback<br/>checks process state<br/>before each agent call

    Orch->>+MI: Analyze market leakage & comps
    MI-->>FS: state_logging (step data)
    MI-->>-Orch: Strategic intelligence data

    Orch->>+PR: Validate internal Q1 risk & Tier 1
    PR->>PR: get_internal_business_data
    PR->>PR: Validate constraints (e.g. > 10.5%)
    PR-->>FS: state_logging (step data)
    PR-->>-Orch: StrategyBoardBriefing (Pydantic)

    Orch->>+CS: Calculate capital structure
    CS->>CS: calculate_loan_pricing
    CS-->>FS: state_logging (step data)
    CS-->>-Orch: Structure results (Pydantic)

    Orch-->>User: Present summary & design visuals
    Note over User,Orch: EXECUTIVE COMMITTEE GATE

    alt User approves
        User->>Orch: "yes"
        Orch->>+GA: Finalize executive canvas
        GA->>GA: finalize_structure_decision
        GA-->>FS: state_logging (step data)
        GA-->>-Orch: Board Memo (Pydantic)
    else User rejects
        User->>Orch: "no"
        Orch-->>User: Scenario execution will not proceed
    end

    Orch->>+Judge: after_agent_callback
    Note over Judge: Validates strategy trajectory,<br/>grounding, completeness
    Judge-->>-Orch: Pass
    Orch-->>-User: Final Board memo
```

**Pause, Repair & Resume:**

```mermaid
sequenceDiagram
    actor User
    actor Operator as Human Operator<br/>(Firestore Console)
    participant Orch as SmallBusinessLoan<br/>OrchestratorAgent
    participant FS as Firestore<br/>process_states
    participant DE as DocumentExtraction<br/>Agent
    participant UW as Underwriting<br/>Agent

    Note over User,UW: PHASE 1 — Pause on missing data

    User->>+Orch: Incomplete PDF + SBL-2025-00391
    Orch->>FS: check_process_status
    FS-->>Orch: New process initialized

    Orch->>+DE: Extract loan application data
    DE-->>FS: state_logging (data with missing fields)<br/>status: pending_approval
    Note over DE,FS: Missing: loan_amount_requested
    DE-->>-Orch: LoanApplicationData (incomplete)

    Orch->>+UW: Validate & check eligibility
    Note over Orch,UW: before_tool_callback<br/>reads Firestore status
    UW->>FS: Check overall_status
    FS-->>UW: pending_approval
    UW-->>-Orch: HALT — Cannot proceed
    Orch-->>-User: Workflow stopped<br/>Missing field: loan_amount_requested

    Note over User,UW: PHASE 2 — Offline repair in Firestore

    Operator->>FS: Fix loan_amount_requested = 150000
    Operator->>FS: Set DocumentExtractionAgent status → completed
    Operator->>FS: Set overall_status → active

    Note over User,UW: PHASE 3 — Resume from checkpoint

    User->>+Orch: Resume processing for SBL-2025-00391
    Orch->>+FS: check_process_status
    FS-->>-Orch: Resume from UnderwritingAgent<br/>Load completed step data into session

    Note over Orch: Skips DocumentExtractionAgent<br/>(already completed)

    Orch->>+UW: Validate & check eligibility
    UW-->>FS: state_logging (step data)
    UW-->>-Orch: UnderwritingReport (Pydantic)
    Note over Orch: Continues normal workflow...
```

**State Management (Firestore):**

```
Process State (per loan_request_id)
  |-- overall_status: active | pending_approval | completed | failed
  |-- steps:
  |     |-- DocumentExtractionAgent: { status, data, completed_at }
  |     |-- UnderwritingAgent:       { status, data, completed_at }
  |     |-- PricingAgent:            { status, data, completed_at }
  |     |-- LoanDecisionAgent:       { status, data, completed_at }
  |-- issues: [ { step, description, resolved } ]
```

## C. Setup & Execution

### Prerequisites

- Python 3.11+
- uv
  - For dependency management and packaging. Please follow the
    instructions on the official
    [uv website](https://docs.astral.sh/uv/) for installation.

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- Google Cloud project with Vertex AI API and Firestore enabled
- `gcloud` CLI authenticated

### Google Cloud Setup

```bash
# Login and set your project
gcloud auth application-default login
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  firestore.googleapis.com

# Create Firestore database for state management
gcloud firestore databases create \
  --database=session-states \
  --location=nam5 \
  --type=firestore-native

```

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd python/agents/capital-allocation-strategy-agent

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your GCP project details
```

### Environment Variables

```bash
# Required
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global

# Firestore
GCP_FIRESTORE_DB=session-states

```

### Sample Documents

Generate the sample loan application PDFs before running the agent:

```bash
uv run python data/generate_sample_applications.py
```

This creates two PDFs in `data/sample_applications/`:

- `sample_application_complete.pdf` -- Happy path (all fields present, strong financials)
- `sample_application_incomplete.pdf` -- Same application with missing fields (triggers repair & resume)

Both represent the same fictional business (Cymbal Coffee Roasters LLC / Jane Doe). The incomplete version is missing the loan amount requested to demonstrate the pause, repair & resume flow.

### Running the Agent

```bash
# Run with ADK web UI
uv run adk web
```

Then open `http://localhost:8000`, select `capital_allocation_strategy_agent`, upload a sample PDF, and send:

```
Process this loan application for SBL-2025-00142
```

## D. Customization & Extension

### Modifying the Flow

- **Prompts:** Each sub-agent has a `prompt.py` in its directory. Modify these to change agent behavior.
- **Orchestrator flow:** Edit `prompt.py` to change the step sequence, add/remove agents, or alter the HITL approval point.
- **Eligibility rules:** Edit `sub_agents/underwriting/eligibility_rules.json` to add or modify business lending criteria.

### Adding Sub-Agents

1. Create a new directory under `sub_agents/` with `agent.py`, `models.py`, `prompt.py`, and optionally `tools.py`
2. Add the agent to the orchestrator's tools list in `agent.py` as an `AgentTool`
3. Update `state_service.py` ALL_STEPS list and `state_callbacks.py` AGENT_OUTPUT_KEY_MAP
4. Update the orchestrator prompt to include the new step

### Connecting Real Data Sources

The mock tools in each sub-agent's `tools.py` are designed to be replaced:

- **`get_internal_business_data`** (underwriting) -- Replace `MOCK_INTERNAL_RECORDS` with calls to your bank's internal API, database, or CRM
- **`calculate_loan_pricing`** (pricing) -- Replace `_determine_risk_tier` with calls to your pricing engine or rate sheet API
- **`finalize_loan_decision`** (loan_decision) -- Replace with calls to your loan origination system

### Changing the Document Type

The `DocumentExtractionAgent` uses Gemini's native multimodal capabilities to read PDFs. To process a different document type:

1. Update `sub_agents/document_extraction/models.py` with new Pydantic fields
2. Update `sub_agents/document_extraction/prompt.py` to describe the new document structure
3. Generate new sample documents in `data/`

### Adding Document AI for Production Extraction

For high-volume production workloads requiring precise, consistent extraction with confidence scores and bounding boxes, you can integrate [Google Document AI](https://cloud.google.com/document-ai) alongside or instead of Gemini's native PDF reading:

1. Create a Document AI custom extractor processor configured for your document type
2. Add a `before_agent_callback` or tool to the `DocumentExtractionAgent` that calls the Document AI API to extract entities from the uploaded PDF
3. Pass the extracted entities to the agent prompt for structured mapping into the Pydantic model
4. Add `google-cloud-documentai` to your dependencies

## E. Tests

For running tests and evaluation, install the extra dependencies:

```bash
uv sync --dev
```

Then run tests from the `capital-allocation-strategy-agent` directory:

```bash
# Unit tests (no GCP required)
uv run pytest tests/unit

# Integration tests (requires GCP credentials and takes 1 to 2 min to run)
uv run pytest tests/integration
```

## F. Evaluation

Ensuring the reliability and accuracy of the C-Suite Strategy Agent is critical before deploying it in a live boardroom environment. We use the [ADK evaluation framework](https://google.github.io/adk-docs/evaluate/) with an LLM-as-Judge approach to validate both the intermediate steps (sub-agent orchestration) and the final outcome (response quality).

### Evaluation Methodology

Our evaluation treats the multi-agent system as a complete pipeline, measuring its performance against a curated dataset of strategy scenarios. We evaluate both the tool call trajectory (did the orchestrator call the right agents in the right order?) and the final response (is the output complete, clear, and semantically correct?).

**The process involves:**

1. **Dataset Ingestion**: Feeding test cases — complete datasets, incomplete datasets, and resume-after-repair scenarios — into the agent as multi-turn conversations.
2. **Execution Tracing**: Logging the orchestrator's routing decisions, sub-agent calls, and tool invocations for each turn.
3. **LLM-as-Judge Assertion**: Using Gemini as a judge model to evaluate tool ordering against rubrics and compare final responses against expected outputs.


### Test Cases

| Test Case | Description | Turns |
| --- | --- | --- |
| `happy_path_with_approval` | Full end-to-end flow: submit query, process through all 4 sub-agents, user approves, strategy decision finalized | 2 |
| `stop_for_reparation_missing_fields` | Incomplete data (missing metrics): agent stops after MarketIntelligence, reports missing data, halts workflow | 1 |
| `resume_after_repair` | Pre-repaired state in Firestore: agent detects completed MarketIntelligence, resumes from PortfolioRiskAgent, processes through Pricing | 1 |

### Evaluation Criteria

| Criterion | Purpose | Threshold | Reference Required |
| --- | --- | --- | --- |
| `rubric_based_tool_use_quality_v1` | Validates tool call ordering using LLM judge against rubrics | 0.8 | No |
| `rubric_based_final_response_quality_v1` | Evaluates response completeness and clarity using LLM judge | 0.8 | No |
| `final_response_match_v2` | Semantic equivalence of response to expected output (LLM-based) | 0.7 | Yes |

### Key Metrics

- **Routing Accuracy (Tool Use Rubrics)**: Did the orchestrator call sub-agents in the correct order? The following ordering rules are enforced:

  | Rubric | Rule |
  | --- | --- |
  | `status_first` | `check_process_status` is called before any agent tools on the initial request |
  | `intelligence_before_risk` | `MarketIntelligenceAgent` is called before `PortfolioRiskAgent` |
  | `risk_before_structure` | `PortfolioRiskAgent` is called before `CapitalStructureAgent` |
  | `structure_before_governance` | `CapitalStructureAgent` is called before `GovernanceAuditorAgent` |
  | `approval_required` | `GovernanceAuditorAgent` is only called after user approval |

- **Response Quality (Final Response Rubrics)**: Is the agent's output complete and actionable?

  | Rubric | Rule |
  | --- | --- |
  | `strategy_summary_completeness` | Response includes diagnostic leakage metrics, risk Tier 1 data, and Strategic capital responses |
  | `clear_next_step` | Response clearly indicates next action: approval prompt, completion confirmation, status report, or missing info request |
  | `error_handling_clarity` | When data is missing or an error occurs, the response clearly identifies what is missing or wrong |


- **Semantic Response Match**: Does the agent's final response convey the same information as the expected reference response? Threshold set to 0.7 to account for natural LLM wording variation.

### Design Decisions

1. **`rubric_based_tool_use_quality_v1` over `tool_trajectory_avg_score`**: When using `AgentTool` wrappers, the orchestrator LLM dynamically generates `request` args containing context from previous steps. Since these args are LLM-generated and unpredictable, we use rubric-based LLM judging to validate tool ordering semantically rather than exact argument matching.

2. **`final_response_match_v2` for semantic matching**: More flexible than exact string matching. The LLM judge evaluates whether the actual response is semantically equivalent to the expected reference, accommodating natural variation in phrasing while catching meaningful omissions.

3. **`rubric_based_final_response_quality_v1` for reference-free evaluation**: Evaluates quality using custom rubrics without requiring a reference response. This catches issues like missing summary fields or unclear next steps even when the overall meaning is correct.

### Building Your Own Eval Set

To implement evaluation for this agent:

1. **Use the sample documents as test inputs.** The synthetic PDFs in `data/sample_applications/` are designed for evaluation:
   - `sample_application_complete.pdf` — all fields present, use for happy-path and approval test cases
   - `sample_application_incomplete.pdf` — missing `loan_amount_requested`, use for repair-flow test cases

2. **Pass documents as `inline_data` in user content.** Gemini reads PDFs natively — base64-encode the file and include it alongside the text prompt in the eval case's `user_content.parts` array.

3. **Use randomly generated SBL IDs** (e.g., `SBL-2025-XXXXX`) for each eval run to avoid Firestore state collisions between runs.

4. **For resume-after-repair test cases**, pre-populate Firestore with a repaired process state (DocumentExtractionAgent marked `completed` with filled-in data, `overall_status` set to `active`) before running the eval. The agent will then skip DocumentExtraction and resume from UnderwritingAgent.

5. **Define expected tool sequences in `intermediate_data.tool_uses`.** For a complete application, the expected sequence is:
   ```
   check_process_status → DocumentExtractionAgent → UnderwritingAgent → PricingAgent
   ```
   For a second turn with user approval:
   ```
   LoanDecisionAgent
   ```

6. **Set the judge model** in your eval config (e.g., `gemini-3.1-pro-preview`) for rubric-based criteria. Both tool use and response quality rubrics use this judge.

See [ADK Evaluation docs](https://google.github.io/adk-docs/evaluate/) and [Evaluation Criteria](https://google.github.io/adk-docs/evaluate/criteria/) for the full evalset schema and available criteria.

## G. Deploy

Use the [Agent Starter Pack](https://goo.gle/agent-starter-pack) to create a production-ready version of this agent with deployment options. Run this command from the root of the `adk-samples` repository:

```bash
uvx agent-starter-pack create my-loan-agent -a local@python/agents/capital-allocation-strategy-agent
```

<details>
<summary>Alternative: Using pip</summary>

```bash
python -m venv .venv && source .venv/bin/activate # On Windows: .venv\Scripts\activate
pip install --upgrade agent-starter-pack
agent-starter-pack create my-loan-agent -a local@python/agents/capital-allocation-strategy-agent
```

</details>

The starter pack will prompt you to select deployment options and provides additional production-ready features including automated CI/CD deployment scripts.

When deploying to Agent Engine, pass the required environment variables using `--set-env-vars` directly via the deploy script (the Makefile does not forward this flag):

```bash
cd my-loan-agent && \
uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > capital_allocation_strategy_agent/app_utils/.requirements.txt && \
uv run -m capital_allocation_strategy_agent.app_utils.deploy \
    --source-packages=./capital_allocation_strategy_agent \
    --entrypoint-module=capital_allocation_strategy_agent.agent_engine_app \
    --entrypoint-object=agent_engine \
    --requirements-file=capital_allocation_strategy_agent/app_utils/.requirements.txt \
    --set-env-vars="GCP_FIRESTORE_DB=session-states,GOOGLE_CLOUD_LOCATION=global"
```

> **Note:** `GOOGLE_CLOUD_LOCATION=global` is required because the Gemini preview model used by this agent is only available in the `global` region, while Agent Engine deploys to a specific region (e.g., `us-central1`). The starter pack preserves this value for model calls.

The service account running the agent must have access to Firestore. For example, if deploying on Agent Engine:

```bash
export PROJECT_ID=your-project-id
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
  --role="roles/datastore.owner" \
  --condition=None
```

## License

Copyright 2026 Google LLC. Licensed under the Apache License, Version 2.0.
