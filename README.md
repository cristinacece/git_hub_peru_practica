# 🇵🇪 GitHub Peru Analytics: Ecosystem Insights & AI Analyst

## Section 1: Project Description
This project provides a comprehensive, data-driven analysis of the software development ecosystem in Peru. By extracting data from thousands of GitHub users and repositories, we identify trends in technology adoption, geographic distribution of talent, and industry focus. The platform includes an interactive Streamlit dashboard and an AI-powered analyst capable of answering natural language queries about the Peruvian tech landscape.

### Antigravity Easter Egg
![Antigravity Screenshot](demo/antigravity_screenshot.png)

---

## Section 2: Key Findings
1. **Talent Concentration**: Over 70% of identified high-impact developers are based in Lima, followed by Arequipa and Trujillo.
2. **Growth Trend**: The Peruvian developer community has seen an exponential growth in account creations between 2018 and 2024.
3. **Language Dominance**: JavaScript and Python are the most popular languages, but there is a significant rise in TypeScript and Go for backend services.
4. **Industry Shift**: AI classification reveals a high concentration of repositories focused on "Information and Communication" (CIIU J), with emerging projects in "Financial and Insurance Activities".
5. **Impact vs. Volume**: Many of the most-starred repositories come from individual developers creating specialized tools (e.g., 3D printing firmware) rather than large organizations.

---

## Section 3: Data Collection
*   **Users Collected**: 1,200+ unique Peruvian developers.
*   **Repositories Collected**: 3,000+ original repositories (excluding forks).
*   **Time Period**: Data covers account activity from 2008 to March 2025.
*   **Rate Limiting**: Implemented a "Request-Wait" cycle in our extraction scripts to respect GitHub API limits (5,000 requests/hr for authenticated users).

---

## Section 4: Features
*   **📊 Overview**: High-level KPIs, community growth trends, and engagement scatter plots.
*   **👥 Talent Hunter**: Advanced search for developers using followers, H-index, and location.
*   **📂 Repository Explorer**: Fuzzy search and multi-filters for projects by language and industry.
*   **🏭 Industry Analysis**: LLM-based categorization of codebases into formal economic sectors.
*   **💻 Languages**: Deep dive into technical stack distribution and top projects per language.
*   **🤖 AI Data Analyst**: Chat interface to query the database using natural language.

### Dashboard Preview
![Dashboard Overview](demo/screenshots/overview.png)
![Talent Hunter](demo/screenshots/developers.png)
![Industry Distribution](demo/screenshots/industries.png)

---

## Section 5: Installation
1. **Clone the repo**: `git clone https://github.com/cristinacece/git_hub_peru_practica.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set up credentials**:
    *   Rename `.env.example` to `.env`.
    *   **GitHub Token**: Generate a PAT (Fine-grained) at GitHub Settings > Developer Settings and paste it as `GITHUB_TOKEN`.
    *   **OpenAI Key**: Get your key from OpenAI Dashboard and paste it as `OPENAI_API_KEY`.

---

## Section 6: Usage
*   **Extract Data**: `python scripts/extract_data.py`
*   **Classify Industries**: `python scripts/classify_repos.py`
*   **Calculate Metrics**: `python scripts/calculate_metrics.py`
*   **Start Dashboard**: `streamlit run app/main.py`

---

## Section 7: Metrics Documentation
### User-Level Metrics
*   **H-Index**: Measures both productivity and impact (stars) of a developer.
*   **Repos per Year (Velocity)**: Average number of public repos created since joining.
*   **Follower Ratio**: Ratio of followers to following, indicating community influence.

### Ecosystem Metrics
*   **Total Stars**: Aggregate popularity of original Peruvian projects.
*   **Language Market Share**: Percentage of repositories using a specific technology.
*   **Industry Concentration**: Distribution of software projects across CIIU economic categories.

---

## Section 8: AI Agent Documentation
*   **Architecture**: Uses `gpt-4o` with a custom reasoning loop (ReAct style).
*   **Process**: 
    1. Question analysis.
    2. SQL Query generation based on database schema.
    3. Python-SQL execution.
    4. Natural language synthesis of results.
*   **Example Run**: 
    - *User*: "Who is the most popular Python developer in Lima?"
    - *Agent*: Generates `SELECT login, total_stars_received FROM users WHERE location='Lima' AND ...`

---

## Section 9: Limitations
1. **GitHub API Dependencies**: Our data is limited by what users choose to disclose publicly (e.g., location strings like "Peru" vs "Lima").
2. **Data Bias**: Metrics favor developers with public projects; private corporate contributions in the Peruvian private sector are not captured.
3. **Classification Accuracy**: The AI industry classifier relies on `README.md` content; projects with no documentation may be misclassified or labeled as "General Purpose".

---

## Section 10: Author Information
*   **Author**: Cristina Cece
*   **Course**: QLAB Prompt Engineering - Task #2
*   **Date**: March 15, 2025
