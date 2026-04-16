import streamlit as st

st.set_page_config(page_title="AI Incident Triage Accelerator", layout="wide")


def get_sample_incident(scenario: str):
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



def classify_incident(data: dict):
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



def map_ownership(classification: dict):
    if classification["dependency"] == "BGS":
        return "BGS Integration Team"
    return "BDS API Team"



def generate_summary(data: dict, classification: dict):
    if classification["type"] == "dependency_outage":
        return (
            "This incident appears to be caused by downstream BGS latency "
            "based on repeated timeout exceptions and failing BGS trace spans."
        )
    return (
        "This incident appears to be caused by an internal application error "
        "based on service-local exceptions and the absence of a downstream dependency pattern."
    )



def generate_runbook(classification: dict):
    if classification["type"] == "dependency_outage":
        return [
            "Check BGS system status",
            "Verify latency in downstream span",
            "Avoid paging unrelated API teams",
            "Escalate to BGS Integration Team"
        ]

    return [
        "Check application logs for the failing code path",
        "Identify the failing endpoint and exception signature",
        "Review recent deployments or config changes",
        "Escalate to the BDS API Team if the pattern persists"
    ]



def generate_copilot_prompt(data: dict, classification: dict, owner: str, summary: str, steps: list[str]):
    return f"""
You are assisting with Lighthouse incident triage.

Use the structured evidence below to generate:
1. A concise executive incident summary
2. Suggested triage steps
3. A short draft runbook entry

Incident:
{data}

Classification:
{classification}

Owner:
{owner}

Initial Summary:
{summary}

Triage Steps:
{steps}

Rules:
- Be concise and operational
- Do not invent teams or systems
- Keep the language simple
- Focus on speeding up engineering triage
""".strip()


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

st.title("AI Incident Triage Accelerator")
st.caption("AI-enabled productivity workflow for faster incident understanding and triage")

left, right = st.columns([1, 1])

with left:
    st.subheader("Incoming Incident Evidence")
    st.json(incident)

with right:
    st.subheader("System Output")
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

st.subheader("Copilot-Ready Prompt")
st.code(copilot_prompt, language="text")

st.markdown("### Productivity Impact")
st.write("- Reduces time spent manually interpreting incidents")
st.write("- Standardizes classification and ownership mapping")
st.write("- Gives engineers structured input for Copilot-assisted summaries and runbooks")
