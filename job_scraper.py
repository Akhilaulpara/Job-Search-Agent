import requests
import urllib.parse
from typing import Optional


def _encode(keyword: str) -> str:
    return urllib.parse.quote(keyword)


def _simplify_keyword(keyword: str) -> str:
    kw = keyword.lower().strip()
    simplifications = {
        "machine learning engineer": "machine learning",
        "data scientist": "data science",
        "software engineer": "software engineer",
        "backend engineer": "backend developer",
        "frontend engineer": "frontend developer",
        "full stack engineer": "full stack developer",
        "fullstack engineer": "full stack developer",
        "devops engineer": "devops",
        "cloud engineer": "cloud",
        "product manager": "product manager",
        "data analyst": "data analyst",
        "ai engineer": "artificial intelligence",
        "nlp engineer": "natural language processing",
        "mlops engineer": "mlops",
        "security engineer": "cybersecurity",
        "mobile developer": "mobile developer",
        "android developer": "android",
        "ios developer": "ios",
        "ux designer": "ux design",
        "ui designer": "ui design",
        "graphic designer": "graphic design",
    }
    for long, short in simplifications.items():
        if long in kw:
            return short
    return kw


def _compute_relevance_score(job_title: str, job_description: str, skills: list[str], target_role: str) -> int:
    title_lower = job_title.lower()
    desc_lower = job_description.lower() if job_description else ""
    role_lower = target_role.lower()

    score = 0

    role_words = [w for w in role_lower.split() if len(w) > 2]
    title_matches = sum(1 for w in role_words if w in title_lower)
    if role_words:
        score += int((title_matches / len(role_words)) * 50)

    if skills:
        matched_skills = sum(
            1 for skill in skills
            if skill.lower() in title_lower or skill.lower() in desc_lower
        )
        score += int((matched_skills / len(skills)) * 50)

    return min(score, 100)


def fetch_jobs_from_remotive(keyword: str, skills: list[str]) -> list[dict]:
    url = f"https://remotive.com/api/remote-jobs?search={_encode(keyword)}&limit=10"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("jobs", [])[:5]:
        apply_url = job.get("url", "")
        if not apply_url:
            continue
        title = job.get("title", "N/A")
        desc = job.get("description", "")
        jobs.append({
            "title": title,
            "company": job.get("company_name", "N/A"),
            "location": job.get("candidate_required_location", "Remote"),
            "apply_link": apply_url,
            "source": "Remotive",
            "relevance": _compute_relevance_score(title, desc, skills, keyword),
        })
    return jobs


def fetch_jobs_from_jobicy(keyword: str, skills: list[str]) -> list[dict]:
    url = f"https://jobicy.com/api/v2/remote-jobs?tag={_encode(keyword)}&count=5"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("jobs", [])[:5]:
        apply_url = job.get("url", "")
        if not apply_url:
            continue
        title = job.get("jobTitle", "N/A")
        desc = job.get("jobExcerpt", "")
        jobs.append({
            "title": title,
            "company": job.get("companyName", "N/A"),
            "location": job.get("jobGeo", "Remote"),
            "apply_link": apply_url,
            "source": "Jobicy",
            "relevance": _compute_relevance_score(title, desc, skills, keyword),
        })
    return jobs


def fetch_jobs_from_arbeitnow(keyword: str, skills: list[str]) -> list[dict]:
    url = f"https://www.arbeitnow.com/api/job-board-api?search={_encode(keyword)}"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("data", [])[:5]:
        apply_url = job.get("url", "")
        if not apply_url:
            continue
        title = job.get("title", "N/A")
        desc = job.get("description", "")
        jobs.append({
            "title": title,
            "company": job.get("company_name", "N/A"),
            "location": job.get("location", "Remote"),
            "apply_link": apply_url,
            "source": "Arbeitnow",
            "relevance": _compute_relevance_score(title, desc, skills, keyword),
        })
    return jobs


def fetch_jobs_from_themuse(keyword: str, skills: list[str]) -> list[dict]:
    url = f"https://www.themuse.com/api/public/jobs?category={_encode(keyword)}&page=1&level=Entry+Level&level=Mid+Level&level=Senior+Level"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("results", [])[:4]:
        apply_url = job.get("refs", {}).get("landing_page", "")
        if not apply_url:
            continue
        title = job.get("name", "N/A")
        desc = " ".join([c.get("body", "") for c in job.get("contents", [])])
        company = job.get("company", {}).get("name", "N/A")
        locations = job.get("locations", [])
        location = locations[0].get("name", "Remote") if locations else "Remote"
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "apply_link": apply_url,
            "source": "The Muse",
            "relevance": _compute_relevance_score(title, desc, skills, keyword),
        })
    return jobs


def fetch_jobs_from_himalayas(keyword: str, skills: list[str]) -> list[dict]:
    url = f"https://himalayas.app/jobs/api?q={_encode(keyword)}&limit=5"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("jobs", [])[:5]:
        apply_url = job.get("applicationLink", "") or job.get("url", "")
        if not apply_url:
            continue
        title = job.get("title", "N/A")
        desc = job.get("description", "")
        jobs.append({
            "title": title,
            "company": job.get("companyName", "N/A"),
            "location": job.get("location", "Remote"),
            "apply_link": apply_url,
            "source": "Himalayas",
            "relevance": _compute_relevance_score(title, desc, skills, keyword),
        })
    return jobs


def get_curated_portal_links(keyword: str, skills: list[str]) -> list[dict]:
    encoded = _encode(keyword)
    encoded_plus = keyword.replace(" ", "+")

    portals = [
        {
            "title": f"{keyword.title()} Jobs on LinkedIn",
            "company": "LinkedIn",
            "location": "Worldwide",
            "apply_link": f"https://www.linkedin.com/jobs/search/?keywords={encoded}&f_TPR=r604800",
            "source": "LinkedIn",
            "relevance": 85,
        },
        {
            "title": f"{keyword.title()} Jobs on Indeed",
            "company": "Indeed",
            "location": "Worldwide",
            "apply_link": f"https://www.indeed.com/jobs?q={encoded_plus}&sort=date",
            "source": "Indeed",
            "relevance": 82,
        },
        {
            "title": f"{keyword.title()} Jobs on Glassdoor",
            "company": "Glassdoor",
            "location": "Worldwide",
            "apply_link": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_plus}&fromAge=7",
            "source": "Glassdoor",
            "relevance": 80,
        },
        {
            "title": f"{keyword.title()} Jobs on Wellfound (AngelList)",
            "company": "Wellfound",
            "location": "Startups & Remote",
            "apply_link": f"https://wellfound.com/role/r/{keyword.lower().replace(' ', '-')}",
            "source": "Wellfound",
            "relevance": 78,
        },
        {
            "title": f"{keyword.title()} Jobs on Dice",
            "company": "Dice",
            "location": "Worldwide",
            "apply_link": f"https://www.dice.com/jobs?q={encoded_plus}&datePosted=ONE_WEEK",
            "source": "Dice",
            "relevance": 75,
        },
        {
            "title": f"{keyword.title()} Jobs on SimplyHired",
            "company": "SimplyHired",
            "location": "Worldwide",
            "apply_link": f"https://www.simplyhired.com/search?q={encoded_plus}",
            "source": "SimplyHired",
            "relevance": 72,
        },
        {
            "title": f"{keyword.title()} Jobs on ZipRecruiter",
            "company": "ZipRecruiter",
            "location": "Worldwide",
            "apply_link": f"https://www.ziprecruiter.com/candidate/search?search={encoded_plus}",
            "source": "ZipRecruiter",
            "relevance": 70,
        },
    ]
    return portals


def fetch_jobs(keyword: str, skills: Optional[list[str]] = None) -> list[dict]:
    if skills is None:
        skills = []

    keyword = keyword.strip()
    simple = _simplify_keyword(keyword)
    all_jobs: list[dict] = []
    errors: list[str] = []

    fetchers = [
        ("Remotive", fetch_jobs_from_remotive),
        ("Jobicy", fetch_jobs_from_jobicy),
        ("Arbeitnow", fetch_jobs_from_arbeitnow),
        ("The Muse", fetch_jobs_from_themuse),
        ("Himalayas", fetch_jobs_from_himalayas),
    ]

    for name, fetcher in fetchers:
        for kw in [keyword, simple]:
            try:
                results = fetcher(kw, skills)
                if results:
                    all_jobs.extend(results)
                    break
            except Exception as e:
                errors.append(f"{name} ({kw}): {e}")

    seen_links = set()
    unique_jobs = []
    for job in all_jobs:
        link = job.get("apply_link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_jobs.append(job)

    unique_jobs = [j for j in unique_jobs if j.get("relevance", 0) >= 50]
    unique_jobs.sort(key=lambda j: j.get("relevance", 0), reverse=True)

    portal_links = get_curated_portal_links(keyword, skills)

    return {
        "live_jobs": unique_jobs[:8],
        "portal_links": portal_links,
        "errors": errors,
    }
