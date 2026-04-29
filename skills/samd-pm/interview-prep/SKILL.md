# Skill: Interview Prep

## Purpose
Run a mock interview session or prep the user for a specific upcoming interview. Pulls from STAR stories, interview playbook, and company research.

## When to Use
- "Prep me for [company] interview"
- "Run a mock interview"
- "Help me practice [question type]"
- "What stories should I use for [role]?"

## Instructions

### Mock Interview Mode
When the user asks for a mock interview:

1. **Check context**: Read `job-search/companies/[company].md` if it exists. Read `job-search/INTERVIEW-PLAYBOOK.md` and `job-search/STAR-STORIES.md`.
2. **Determine format**: Ask if this is a specific round (product sense, execution, leadership, analytical) or a general practice session.
3. **Ask 3-5 questions** one at a time. Wait for the user's answer before moving on.
4. **After each answer, give feedback on**:
   - **Structure**: Did the answer follow STAR? Was it under 2 minutes?
   - **Specificity**: Were there concrete numbers, outcomes, and decisions?
   - **SaMD signal**: Did the answer demonstrate healthcare/regulatory depth where relevant?
   - **Improvement**: One specific thing to change.
5. **After the session**: Summarize strengths, patterns to fix, and which stories landed best.

### Company Prep Mode
When the user asks to prep for a specific company:

1. Read `job-search/companies/[company].md` if it exists. If not, offer to create one.
2. Research the company (products, regulatory status, recent news, role details).
3. Map the user's experience to what the role needs — identify strongest angles and gaps.
4. Suggest which STAR stories to prioritize for this company.
5. Draft 3 company-specific questions the user should ask the interviewer.
6. Flag any potential concerns the interviewer might have and how to address them.

### Story Selection Mode
When the user asks which stories to use:

1. Read `job-search/STAR-STORIES.md`
2. Based on the role type and company, recommend 4-5 stories with rationale
3. Identify any competency gaps not covered by existing stories
4. Suggest how to adapt stories to emphasize what this specific company cares about

## Feedback Style
- Be direct. "That answer was too long" not "You might consider being more concise."
- Call out when an answer sounds rehearsed or generic.
- Push for the specific moment — "What did YOU decide? What was the turning point?"
- If the user gives a vague answer, ask a follow-up probe like an interviewer would.
