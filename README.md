# 🔎 SEO Competitive Opportunity Agent

An AI-powered SEO analysis agent that crawls a website, detects technical SEO issues, prioritizes opportunities, analyzes competitors, and generates actionable recommendations.

Built for the **Agents for Humans Hackathon** using **Strands SDK + Ollama (Llama 3.1)**.

---

## 🚀 What Problem Does It Solve?

SEO professionals often need to manually:

- Crawl websites
- Find technical SEO issues
- Review page-level problems
- Prioritize fixes
- Analyze competitors
- Identify SEO gaps
- Convert findings into actionable recommendations

This process can be time-consuming and repetitive.

The **SEO Competitive Opportunity Agent** combines website crawling, technical SEO auditing, competitive analysis, and AI-assisted opportunity analysis into one workflow.

---

## 💡 Solution

The agent takes a target website and competitor websites as input.

It then:

1. Crawls the websites
2. Extracts important on-page SEO signals
3. Detects technical SEO issues
4. Prioritizes issues
5. Generates SEO recommendations
6. Uses an AI agent to analyze verified crawl evidence
7. Compares the target website with competitors
8. Calculates a Technical Opportunity Score
9. Produces competitive SEO opportunities

---

## ✨ Key Features

### 🔍 Technical SEO Audit

The crawler analyzes pages for signals including:

- HTTP status codes
- Page titles
- Meta descriptions
- H1 headings
- Canonical tags
- Word count
- JavaScript rendering indicators
- Page-level SEO issues

---

### 🎯 Issue Detection & Prioritization

Detected issues are organized by priority:

- 🔴 High
- 🟠 Medium
- 🟢 Low

The dashboard also provides:

- Total pages crawled
- Pages with issues
- Total SEO issues
- Site-wide issue counts
- Affected page URLs

---

### 🤖 AI SEO Opportunity Analysis

The AI layer analyzes verified crawl evidence and generates:

- Executive summary
- Top SEO opportunities
- Evidence supporting each opportunity
- Opportunity scores
- Recommended actions

The AI recommendations are constrained by the website audit data rather than relying only on generic SEO advice.

---

### 📊 Competitor Comparison

The agent can compare a target website against competitor websites using metrics such as:

- Pages crawled
- Average word count
- H1 issue pages
- Total SEO issues

---

### 🎯 Technical Opportunity Score

Each website receives a technical opportunity score based on detected audit findings.

A higher score represents a larger number of detected technical SEO opportunities.

> This score is an internal analysis metric and is not a Google ranking or traffic metric.

---

### 🚀 Competitive Opportunities

The system identifies strategic opportunities such as:

- Technical SEO remediation
- Heading structure improvement
- Competitive SEO gap analysis
- Continuous SEO monitoring

---

## 🧠 Agent Architecture

```text
                 ┌──────────────────────┐
                 │     User Input       │
                 │ Target + Competitors │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Website Crawler     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  SEO Issue Detector  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Technical SEO Audit  │
                 └──────────┬───────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
   ┌───────────────────┐         ┌────────────────────┐
   │ AI Opportunity    │         │ Competitor         │
   │ Analysis          │         │ Comparison         │
   └─────────┬─────────┘         └──────────┬─────────┘
             │                              │
             └──────────────┬───────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ SEO Opportunities &  │
                 │ Recommended Actions  │
                 └──────────────────────┘