# 📄 Job Search Agent

An AI-powered job matching application that analyzes your resume and recommends the most relevant job opportunities from multiple job portals — complete with relevance scoring, personalized career advice, and a sleek dark-mode UI.

Built with **Streamlit**, **Nebius AI** (Llama 3.3 70B), and a multi-source job aggregation engine.

---

## ✨ Features

- 📑 **Smart Resume Parsing** — Extracts text from PDF and DOCX resumes
- 🧠 **AI-Powered Analysis** — Uses Llama 3.3 70B via Nebius to extract:
  - Professional Experience & Career Progression (with durations like "2 yrs 3 months")
  - Education & Certifications
  - Core Skills & Expertise (grouped by category)
  - Domain Classification (Software Engineering, Design, Product Management, etc.)
  - Career Highlights
- 🎯 **Domain Detection** — Auto-detects the best-fit job role keyword
- 💼 **Multi-Portal Job Aggregation** — Fetches live jobs from **5 free APIs** + adds **7 curated search portals**:
  - **Live API sources:** Remotive, Jobicy, Arbeitnow, The Muse, Himalayas
  - **Search portals:** LinkedIn, Indeed, Glassdoor, Wellfound (AngelList), Dice, SimplyHired, ZipRecruiter
- 📊 **Relevance Scoring** — Each job is scored 0–100 based on title and skill match. Only jobs scoring **≥ 50** are displayed.
- 🌟 **Personalized Recommendations** — AI career advisor tailors suggestions to your specific profile
- 🌙 **Professional Dark Mode UI** — Polished, user-friendly interface with custom styling

---

## 📂 Project Structure

```
resume-job-matcher/
├── .streamlit/
│   └── config.toml          # Streamlit dark theme config
├── assets/
│   └── Nebius.png           # Optional logo (can be removed)
├── app.py                   # Streamlit main app
├── job_agents.py            # AI agents for resume analysis & recommendations
├── job_scraper.py           # Multi-portal job fetching engine
├── resume_parser.py         # PDF/DOCX text extraction
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed)
└── README.md
```

---

## 🛠️ Tech Stack

| Component         | Technology                          |
| ----------------- | ----------------------------------- |
| Frontend          | Streamlit                           |
| LLM Backend       | Nebius AI (Llama 3.3 70B Instruct)  |
| Agent Framework   | OpenAI Agents SDK                   |
| Resume Parsing    | pdfplumber, python-docx             |
| Job APIs          | Remotive, Jobicy, Arbeitnow, The Muse, Himalayas |
| HTTP Client       | requests                            |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- A free **Nebius API key** — sign up at [https://studio.nebius.com](https://studio.nebius.com)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/resume-job-matcher.git
cd resume-job-matcher
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, create one with:

```txt
streamlit
nest-asyncio
python-dotenv
pdfplumber
python-docx
openai
openai-agents
requests
```

### 4. Configure environment variables (optional)

Create a `.env` file in the project root:

```env
NEBIUS_API_KEY=your_nebius_api_key_here
```

> You can also enter the API key directly in the app's sidebar at runtime.

### 5. Set up dark mode (recommended)

Create a `.streamlit/config.toml` file:

```toml
[theme]
base = "dark"
primaryColor = "#3b82f6"
backgroundColor = "#0f1117"
secondaryBackgroundColor = "#161b27"
textColor = "#e2e8f0"
font = "sans serif"
```

### 6. Run the app

```bash
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

---

## 🧭 How to Use

1. **Upload** your resume (PDF or DOCX) in the sidebar
2. **Enter** your Nebius API key
3. Click **🔍 Analyze Resume**
4. Wait a few seconds while the AI analyzes your profile and fetches matching jobs
5. Browse:
   - Your detailed candidate profile
   - Personalized career recommendations
   - Live job postings ranked by relevance score
   - Direct deep-link searches to top job portals

---

## 🎯 Relevance Scoring System

Each job is scored **0–100** based on:

- **50 points** — How well the job title matches your target role
- **50 points** — How many of your detected skills appear in the job title or description

Jobs are categorized as:

| Score   | Badge                |
| ------- | -------------------- |
| 85–100  | 🟢 Excellent Match   |
| 70–84   | 🟡 Good Match        |
| 50–69   | 🟠 Partial Match     |
| < 50    | ❌ Filtered out       |

---

## 🔌 Job Portal Coverage

| Portal         | Type            | Description                                   |
| -------------- | --------------- | --------------------------------------------- |
| Remotive       | Live API        | Remote jobs across all categories             |
| Jobicy         | Live API        | Curated remote-friendly listings              |
| Arbeitnow      | Live API        | European-focused job board                    |
| The Muse       | Live API        | Mid-to-senior career roles                    |
| Himalayas      | Live API        | Remote-first companies                        |
| LinkedIn       | Deep-link       | World's largest professional network          |
| Indeed         | Deep-link       | Largest general job aggregator                |
| Glassdoor      | Deep-link       | Jobs + company reviews                        |
| Wellfound      | Deep-link       | Startup-focused (formerly AngelList)          |
| Dice           | Deep-link       | Tech-specialized                              |
| SimplyHired    | Deep-link       | Broad job aggregator                          |
| ZipRecruiter   | Deep-link       | Fast-apply listings                           |

---

## 📸 Screenshots

> _Add your own screenshots here once deployed._

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙏 Acknowledgements

- [Nebius AI Studio](https://studio.nebius.com) — for free LLM API access
- [Meta Llama 3.3](https://llama.meta.com) — for the underlying model
- [Streamlit](https://streamlit.io) — for the beautiful Python UI framework
- [Remotive](https://remotive.com), [Jobicy](https://jobicy.com), [Arbeitnow](https://arbeitnow.com), [The Muse](https://www.themuse.com), [Himalayas](https://himalayas.app) — for free public job APIs


