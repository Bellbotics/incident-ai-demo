# AI Incident Triage Accelerator

Contest-ready Streamlit demo for the Deloitte AI in Action campaign.

## What it shows

A simple, high-signal workflow that improves engineering productivity during incident triage:

- Takes structured incident evidence
- Classifies the issue type
- Maps ownership
- Generates a concise incident summary
- Produces suggested triage steps
- Outputs a Copilot-ready prompt for optional human-in-the-loop AI refinement

This is designed to win by being:
- simple
- credible
- immediately understandable
- clearly tied to delivery productivity

## Demo scenarios

1. **BGS Dependency Timeout**
2. **Internal Application Error**

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Run with Docker

```bash
docker build -t incident-ai-demo .
docker run --rm -p 8501:8501 incident-ai-demo
```

Then open:

```text
http://localhost:8501
```

## Exact 2-minute demo flow

1. Select **BGS Dependency Timeout**
2. Show the incident evidence on the left
3. Show the system output on the right:
   - classification
   - owner
   - confidence
   - summary
   - triage steps
4. Scroll to the Copilot-ready prompt
5. Explain that Copilot can use the structured evidence to produce a polished summary or runbook entry
6. Switch to **Internal Application Error** to show the classification and ownership change

## Exact positioning

Use this framing:

> We are not building an AI product. We are improving incident triage productivity by structuring evidence up front and using AI as an assistive layer where it adds value.

## Exact 2-minute script

> Today when an alert fires, engineers still spend time manually pulling together logs, traces, and ownership information before they can even decide what kind of incident they’re dealing with.
>
> This demo shows a lightweight workflow that structures that evidence up front. On the left is the incoming incident data: alert details, key errors, and trace evidence.
>
> The system then classifies the incident, maps ownership, and generates a concise summary plus suggested triage steps. In this case, it identifies a likely dependency outage involving BGS rather than an internal API regression.
>
> That alone reduces time spent interpreting the incident and helps avoid paging the wrong team. It also gives engineers a consistent starting point instead of relying on tribal knowledge.
>
> From there, we can use Copilot as the assistive layer to turn that structured output into a polished incident summary or draft runbook entry. The result is faster triage, more consistent response, and a repeatable AI-enabled workflow that improves engineering productivity.

## Exact slide content

### Slide 1
**AI Incident Triage Accelerator**  
Improving engineering productivity through structured incident reasoning

### Slide 2
**Challenge**
- Engineers manually piece together alerts, logs, traces, and ownership
- Triage is inconsistent and time-consuming
- Wrong teams can be pulled into dependency incidents

### Slide 3
**Solution**
- Standardize incident evidence
- Classify issue type
- Map correct ownership
- Use Copilot to generate summaries and runbook content from grounded inputs

### Slide 4
**Impact**
- Faster incident understanding
- More consistent triage
- Less reliance on tribal knowledge
- Reusable across teams and organizations

## What not to say

Do not say:
- autonomous AI agent
- production AI platform
- real-time LLM orchestration
- end-to-end automated incident response

Say instead:
- AI-enabled workflow
- structured evidence
- Copilot-assisted summary generation
- productivity improvement
