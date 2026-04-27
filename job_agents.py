from job_scraper import fetch_jobs
from resume_parser import extract_text_from_resume
import os
import re
from agents import Agent, OpenAIChatCompletionsModel, Runner
from openai import AsyncOpenAI


def _score_badge(score: int) -> str:
    if score >= 85:
        return "🟢 Excellent Match"
    elif score >= 70:
        return "🟡 Good Match"
    elif score >= 50:
        return "🟠 Partial Match"
    else:
        return "🔴 Low Match"


def _parse_skills_from_profile(profile_text: str) -> list[str]:
    lines = profile_text.lower().split("\n")
    skills = []
    in_skills_section = False
    for line in lines:
        if any(kw in line for kw in ["skill", "expertise", "technologies", "tools"]):
            in_skills_section = True
            continue
        if in_skills_section:
            if line.strip().startswith("-") or line.strip().startswith("•"):
                skill_items = re.split(r"[,|]", line.strip().lstrip("-•").strip())
                skills.extend([s.strip() for s in skill_items if len(s.strip()) > 1])
            elif line.strip() == "":
                in_skills_section = False
    if not skills:
        tokens = re.findall(r"\b(?:python|java|javascript|typescript|react|node|sql|aws|gcp|azure|docker|kubernetes|tensorflow|pytorch|scala|go|rust|swift|kotlin|flutter|django|flask|fastapi|spring|rails|vue|angular|graphql|mongodb|postgresql|redis|spark|hadoop|airflow|dbt|tableau|power bi|figma|sketch|photoshop|illustrator|jira|agile|scrum)\b", profile_text.lower())
        skills = list(dict.fromkeys(tokens))
    return skills[:15]


async def run_analysis(resume_path: str):

    client = AsyncOpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1",
        api_key=os.environ["NEBIUS_API_KEY"]
    )

    resume_agent = Agent(
        name="Resume Analyzer",
        instructions="""
        You are an expert resume analyst. Given a resume, extract and return a detailed structured profile in this exact format:

        ## Professional Experience & Career Progression
        List each role with:
        - Job Title | Company | Duration (e.g., "2 yrs 3 months" or "8 months")
        - One sentence on key responsibilities and impact
        Order from most recent to oldest.

        ## Education
        List each qualification:
        - Degree | Field of Study | Institution | Year
        Include certifications if present.

        ## Core Skills & Expertise
        Group skills into categories:
        - Programming Languages: ...
        - Frameworks & Libraries: ...
        - Databases & Cloud: ...
        - Tools & Platforms: ...
        - Soft Skills: ...
        List only skills explicitly mentioned in the resume.

        ## Domain Classification
        State ONE primary domain from this list:
        Software Engineering | Data Science & AI | Design & UX | Product Management |
        DevOps & Cloud | Cybersecurity | Finance & Accounting | Marketing | Sales |
        Healthcare | Legal | Education | Operations | Other
        Then state ONE sub-domain (e.g., "Backend Development", "Computer Vision", "Brand Design").

        ## Career Highlights
        3 bullet points — the most impressive achievements or facts from the resume.

        Be factual. Only use what is in the resume. Do not invent or infer beyond what is stated.
        """,
        model=OpenAIChatCompletionsModel(
            model="meta-llama/Llama-3.3-70B-Instruct",
            openai_client=client
        )
    )

    domain_agent = Agent(
        name="Domain Extractor",
        instructions="""
        You are given a structured resume profile. Extract ONE short job role keyword for a job board search.
        Rules:
        - 1 to 3 words max
        - No seniority words (no "Senior", "Junior", "Lead", "Principal", "Staff")
        - Use common job board search terms
        - Output ONLY the keyword, nothing else

        Examples:
          "Experienced Data Scientist with 5 years..." → data scientist
          "Full Stack Engineer skilled in React and Node..." → full stack developer
          "Machine Learning Engineer at Google..." → machine learning engineer
          "UX Designer with expertise in Figma..." → ux designer
          "Product Manager leading cross-functional teams..." → product manager
          "DevOps Engineer working with Kubernetes..." → devops engineer
        """,
        model=OpenAIChatCompletionsModel(
            model="meta-llama/Llama-3.3-70B-Instruct",
            openai_client=client
        )
    )

    recommendation_agent = Agent(
        name="Job Recommendation Advisor",
        instructions="""
        You are a career advisor. Given a candidate's profile summary and a list of job matches (with relevance scores),
        write a short personalized recommendation section (4–6 sentences) that:
        - Highlights which types of roles are the best fit based on their skills and experience
        - Mentions 1–2 specific technologies or skills they should highlight in applications
        - Gives ONE practical tip for improving their chances (e.g., certifications to pursue, portfolio advice)
        - Mentions what salary range or seniority level they likely qualify for
        Be specific to the actual person's profile, not generic advice.
        """,
        model=OpenAIChatCompletionsModel(
            model="meta-llama/Llama-3.3-70B-Instruct",
            openai_client=client
        )
    )

    resume_text = extract_text_from_resume(resume_path)

    resume_result = await Runner.run(resume_agent, resume_text)
    profile = resume_result.final_output

    domain_result = await Runner.run(domain_agent, profile)
    keyword = domain_result.final_output.strip().lower()

    skills = _parse_skills_from_profile(profile)

    job_data = {}
    error_msg = ""
    try:
        job_data = fetch_jobs(keyword, skills)
    except Exception as e:
        error_msg = str(e)

    live_jobs = job_data.get("live_jobs", [])
    portal_links = job_data.get("portal_links", [])
    fetch_errors = job_data.get("errors", [])

    recommendation_input = f"""
Candidate Profile:
{profile}

Keyword: {keyword}
Skills detected: {', '.join(skills) if skills else 'not parsed'}
Top jobs found: {len(live_jobs)} live listings across multiple platforms
"""
    rec_result = await Runner.run(recommendation_agent, recommendation_input)
    recommendation = rec_result.final_output

    def _job_card(index: int, job: dict, is_portal: bool = False) -> str:
        badge = _score_badge(job['relevance'])
        label = "🔍 Search Portal" if is_portal else "🔴 Live Posting"
        return f"""---
#### {index}. {job['title']}
- {label} &nbsp;|&nbsp; {badge} &nbsp;({job['relevance']}/100)
- **Company / Platform:** {job['company']}
- **Location:** {job['location']}
- **Source:** {job['source']}
- **Apply / Search:** [Open Link →]({job['apply_link']})"""

    all_listings = []
    counter = 1

    if live_jobs:
        for job in live_jobs:
            all_listings.append(_job_card(counter, job, is_portal=False))
            counter += 1
    else:
        all_listings.append(
            f"---\n⚠️ No live job listings met the relevance threshold (≥50).\n\n"
            f"_Details: {'; '.join(fetch_errors) if fetch_errors else 'No results from APIs'}_"
        )

    for job in portal_links:
        all_listings.append(_job_card(counter, job, is_portal=True))
        counter += 1

    all_listings_text = "\n\n".join(all_listings)

    return f"""
## 👤 Candidate Profile

{profile}

---

## 🧠 Personalized Career Recommendation

{recommendation}

---

## 🎯 Best-Fit Job Role
`{keyword}`

---

## 💼 Job Listings & Portal Links
> Live postings are filtered to **relevance ≥ 50** and ranked highest first.
> Portal links open pre-filtered searches on top job platforms.

{all_listings_text}

---

_💡 Tip: Apply through LinkedIn and Indeed for broadest reach, Wellfound for startups, and Dice for tech roles._
"""
