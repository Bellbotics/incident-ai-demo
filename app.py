import time
import streamlit as st

st.set_page_config(page_title="AI Incident Triage Accelerator", layout="wide")

def get_sample_incident(scenario):
    if scenario == "Internal Application Error":
        return {
            "alert": "High 500 error rate",
            "service": "benefits-documents",
            "env": "prod",
            "errors": [
                "NullPointerException"
            ],
            "messages": [
                "NullPointerException in document upload handler",
                "Unhandled exception in request processing"
            ],
            "trace": {
                "failing_span": "documents.upload",
                "latency_ms": 450
            }
        }

    return {
        "alert": "High 500 error rate",
        "service": "benefits-documents",
        "env": "prod",
        "errors": [
            "BGSServiceException",
            "SocketTimeoutException"
        ],
        "messages": [
            "Read timed out calling BGS",
            "Retry exhausted after 3 attempts"
        ],
        "trace": {
            "failing_span": "bgs.claims.lookup",
            "latency_ms": 8200
        }
    }

def classify_incident(data):
    errors = " ".join(data["errors"]).lower()
    messages = " ".join(data["messages"]).lower()

    if "nullpointerexception" in errors:
        return {
            "type": "internal_error",
            "dependency": None,
            "confidence": 0.88
        }

    if "bgs" in errors or "bgs" in messages:
        if "timeout" in messages:
            return {
                "type": "dependency_outage",
                "dependency": "BGS",
                "confidence": 0.90
            }

    return {
        "type": "internal_error",
        "dependency": None,
        "confidence": 0.60
    }

def map_ownership(classification):
    if classification["dependency"] == "BGS":
        return "BGS Integration Team"
    return "BDS API Team"

def generate_summary(data, classification):
    if classification["type"] == "dependency_outage":
        return (
            "This incident appears to be caused by downstream BGS latency "
            "based on repeated timeout exceptions and failing BGS trace spans."
        )
    return (
        "This incident appears to be isolated to the service based on the current "
        "error signature and lack of downstream dependency evidence."
    )

def generate_runbook(classification):
    if classification["type"] == "dependency_outage":
        return [
            "Check BGS system status",
            "Verify latency in downstream span",
            "Avoid paging unrelated API teams",
            "Escalate to BGS integration team"
        ]

    return [
        "Check application logs",
        "Identify failing endpoint",
        "Review recent deployments",
        "Escalate to BDS API team if issue persists"
    ]

def generate_copilot_prompt(data, classification, owner, summary, steps):
    return f"""
You are assisting with Lighthouse incident triage.

We have already structured the incident evidence below.

Incident:
- Alert: {data["alert"]}
- Service: {data["service"]}
- Environment: {data["env"]}
- Errors: {", ".join(data["errors"])}
- Messages: {"; ".join(data["messages"])}
- Trace: failing span {data["trace"]["failing_span"]}, latency {data["trace"]["latency_ms"]}ms

Classification:
- Type: {classification["type"]}
- Dependency: {classification["dependency"] or "None"}
- Confidence: {int(classification["confidence"] * 100)}%

Owner:
- {owner}

Please produce:
1. A concise incident summary for engineers
2. Suggested triage steps
3. A short runbook entry
4. A 2-sentence executive summary

Rules:
- Be concise
- Do not invent teams or systems
- Keep it practical and operational
- Focus on speeding up engineering work
""".strip()

def generate_ai_output(scenario, owner):
    if scenario == "Internal Application Error":
        return {
            "enhanced_summary": (
                "The current incident appears to be an internal application failure rather than "
                "a downstream dependency issue. The NullPointerException pattern suggests the "
                "problem is isolated to the benefits-documents service and should be handled by the BDS API team."
            ),
            "runbook_draft": [
                "Review the failing application code path for the document upload handler",
                "Check for recent deploys or configuration changes",
                "Validate whether the error is isolated to one endpoint or broader service logic",
                "Escalate to the BDS API team and consider rollback if correlated with a recent release"
            ],
            "executive_update": (
                "The incident currently appears to be an internal service issue rather than a shared dependency failure. "
                "The owning API team has a clear triage path and the blast radius appears limited."
            )
        }

    return {
        "enhanced_summary": (
            "The incident is most consistent with a shared downstream BGS latency issue rather than "
            "an isolated API regression. Repeated timeout signatures and the failing BGS trace span "
            "suggest the API is experiencing dependency-driven errors."
        ),
        "runbook_draft": [
            "Confirm BGS latency or timeout indicators across affected services",
            "Validate the downstream span and error concentration before escalating",
            "Avoid paging unrelated API teams when the dependency pattern is clear",
            "Escalate to the BGS integration team and post a concise shared incident update"
        ],
        "executive_update": (
            "The incident appears to be driven by a downstream BGS issue and not an isolated application defect. "
            "The workflow quickly identifies the correct owner and reduces unnecessary triage across other teams."
        )
    }

st.title("AI Incident Triage Accelerator")
st.caption("AI-enabled productivity workflow for faster incident understanding and triage")

scenario = st.selectbox(
    "Demo Scenario",
    ["BGS Dependency Timeout", "Internal Application Error"]
)

incident = get_sample_incident(scenario)
classification = classify_incident(incident)
owner = map_ownership(classification)
summary = generate_summary(incident, classification)
runbook = generate_runbook(classification)
copilot_prompt = generate_copilot_prompt(
    incident, classification, owner, summary, runbook
)

left, right = st.columns([1, 1])

with left:
    st.subheader("Incoming Incident Evidence")
    st.json(incident)

with right:
    st.subheader("Structured System Output")
    c1, c2, c3 = st.columns(3)
    c1.metric("Classification", classification["type"].replace("_", " ").title())
    c2.metric("Owner", owner)
    c3.metric("Confidence", f"{int(classification['confidence'] * 100)}%")

    st.markdown("### Incident Summary")
    st.info(summary)

    st.markdown("### Suggested Triage Steps")
    for step in runbook:
        st.write(f"- {step}")

st.divider()

st.subheader("AI Assist Layer")
st.write(
    "The system does the deterministic work first — classification and ownership mapping. "
    "AI then builds on top of that structured context to generate a refined summary and draft runbook."
)

if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.ai_output = None

if st.button("Generate AI Output"):
    with st.spinner("Generating AI-assisted summary and runbook..."):
        time.sleep(1.0)
        st.session_state.ai_output = generate_ai_output(scenario, owner)
        st.session_state.generated = True

if st.session_state.generated and st.session_state.ai_output:
    ai_output = st.session_state.ai_output
    st.success("AI-assisted output generated")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Enhanced Summary")
        st.success(ai_output["enhanced_summary"])

        st.markdown("### Executive Update")
        st.info(ai_output["executive_update"])

    with col2:
        st.markdown("### Draft Runbook")
        for step in ai_output["runbook_draft"]:
            st.write(f"- {step}")

st.divider()

st.subheader("Copilot-Ready Prompt")
st.code(copilot_prompt, language="text")

st.markdown("### How to Explain the Architecture")
st.write("- Left side: incoming alert, logs, and trace evidence")
st.write("- Right side: deterministic classification, ownership mapping, and initial triage guidance")
st.write("- AI layer: generates the narrative and runbook content from the structured context")
st.write("- Positioning: structured incident evidence + Copilot-assisted triage")

st.markdown("### Productivity Impact")
st.write("- Reduces time spent manually interpreting incidents")
st.write("- Standardizes classification and ownership mapping")
st.write("- Gives engineers structured input for Copilot-assisted summaries and runbooks")
