from strands import Agent
from strands.models.ollama import OllamaModel

from tools.website_audit import (
    audit_website,
    get_agent_audit_summary,
)

from tools.competitor_comparison import compare_websites


# ============================================================
# OLLAMA MODEL
# ============================================================

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.2,
    max_tokens=800,
)


# ============================================================
# SEO AGENT
# ============================================================
# This agent has access to the SEO tools.
# It is useful for testing the agent/tool architecture.

seo_agent = Agent(
    model=ollama_model,
    tools=[
        get_agent_audit_summary,
        compare_websites,
    ],
)


# ============================================================
# LIGHTWEIGHT AI SEO ANALYSIS AGENT
# ============================================================
# IMPORTANT:
# This agent does NOT have tools.
#
# The Streamlit application already performs:
#   1. Website crawling
#   2. SEO auditing
#   3. Competitor comparison
#
# Therefore this agent only analyzes the verified evidence.
# This prevents unnecessary tool calls and avoids the
# Streamlit AI-analysis hanging problem.

ai_seo_agent = Agent(
    model=ollama_model,
    tools=[],
)