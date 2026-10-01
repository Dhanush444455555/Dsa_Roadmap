# DSA Roadmap AI

**DSA Roadmap AI** is an intelligent full-stack web application that allows users to upload any DSA/LeetCode sheet (PDF, DOCX, TXT, CSV) or select a built-in curated problem set to generate a personalized, prerequisite-ordered preparation roadmap.

---

## 🌟 Key Features

1. **Multi-Format Document Ingestion**
   - Ingests **PDF, DOCX, TXT, CSV/TSV** sheets or direct pasted text.
   - Normalizes problem numbers, titles, difficulties, and topics.
   - Built-in dataset fallback (150+ curated Top SDE questions) for instant roadmaps without uploading.

2. **Deterministic Prerequisite Graph & Interleaved Scheduling**
   - Orders topics along a verified prerequisite DAG:
     $$\text{Arrays} \to \text{Hashing} \to \text{Two Pointers} \to \text{Sliding Window} \to \text{Binary Search} \to \text{Stack} \to \text{Linked List} \to \text{Trees} \to \text{Graphs} \to \text{DP}$$
   - Concept interleaving prevents topic fatigue (avoids 20 consecutive Array questions).
   - Difficulty curve adapts to user level:
     - **Beginner**: 65% Easy • 35% Medium
     - **Average**: 25% Easy • 60% Medium • 15% Hard
     - **Advanced**: 10% Easy • 55% Medium • 35% Hard

3. **Algorithm Concept Similarity Mapping**
   - Maps problems to classic algorithmic patterns without scraping copyrighted statements:
     - `1710 Maximum Units on a Truck` $\to$ *Fractional Knapsack (Greedy by Value/Weight)*
     - `1834 Single-Threaded CPU` $\to$ *Shortest Job First (Min-Heap Simulation)*
     - `55 Jump Game` $\to$ *Greedy Reachability*
     - `141 Linked List Cycle` $\to$ *Floyd's Tortoise and Hare Cycle Detection*
     - `704 Binary Search` $\to$ *Divide and Conquer Search*
     - `875 Koko Eating Bananas` $\to$ *Binary Search on Answer Space*

4. **Spaced Repetition Scheduler**
   - Automatically queues solved problems for review on **Day 2**, **Day 7**, and **Day 21** intervals.

5. **Weak Topic Detection & Adaptive Recommendations**
   - Tracks mastery per DSA concept and recommends reinforcement problems for topics with $<50\%$ completion.

---

## 📂 Project Structure

```
dsa-roadmap-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py                # REST endpoints
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── session.py               # SQLite engine / Postgres ready
│   │   │   └── models.py                # Problem, Roadmap, Item, Revision models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── dsa_schemas.py           # Pydantic schemas & validation
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_parser.py       # PDF/DOCX/TXT/CSV extractor
│   │   │   ├── problem_extractor.py     # Regex & entity extraction
│   │   │   ├── problem_classifier.py    # Topic & difficulty classification
│   │   │   ├── similarity_engine.py     # TF-IDF & conceptual similarity
│   │   │   ├── roadmap_generator.py     # DAG scheduling & interleaving
│   │   │   ├── recommendation_engine.py # Weak topic detection
│   │   │   ├── revision_engine.py       # Spaced repetition logic
│   │   │   └── llm_service.py           # Optional LLM enrichment
│   │   ├── data/
│   │   │   └── problems.json            # 150+ Curated SDE Problem Database
│   │   ├── __init__.py
│   │   └── main.py                      # FastAPI application
│   ├── uploads/                         # Sample upload files
│   ├── requirements.txt
│   ├── generate_seed_dataset.py
│   ├── test_flow.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx               # Navigation bar & streak pill
│   │   │   ├── ProblemCard.jsx          # LeetCode link, concept, status
│   │   │   ├── ProgressBar.jsx          # Progress bar
│   │   │   ├── StatsCard.jsx            # KPI metric cards
│   │   │   └── WeakTopicAlert.jsx       # AI weak topic recommendations
│   │   ├── pages/
│   │   │   ├── Landing.jsx              # Landing page & 5-step blueprint
│   │   │   ├── UploadPage.jsx           # File dropzone & text paste
│   │   │   ├── PreviewProblems.jsx      # Imported problem inspection
│   │   │   ├── ConfigureRoadmap.jsx     # Level, duration, count selectors
│   │   │   ├── RoadmapView.jsx          # Monthly & weekly visual plan
│   │   │   ├── TodayProblems.jsx        # Daily focused tasks
│   │   │   ├── ProgressDashboard.jsx    # Analytics & topic mastery
│   │   │   ├── RevisionPage.jsx         # Spaced repetition list (Day 2/7/21)
│   │   │   └── SettingsPage.jsx         # API keys & dataset export
│   │   ├── services/
│   │   │   └── api.js                   # Axios client
│   │   ├── store/
│   │   │   └── useDSAStore.js           # Zustand global state
│   │   ├── App.jsx                      # Routes
│   │   ├── main.jsx                     # Vite React entrypoint
│   │   └── index.css                    # Tailwind CSS
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### 2. Backend Setup & Run

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Start the FastAPI backend server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   *The backend will run at `http://localhost:8000` (API Docs at `http://localhost:8000/docs`).*

---

### 3. Frontend Setup & Run

1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The web application will open at `http://localhost:5173`.*

---

## 🧪 Testing the Complete Flow (Prompt Test Case)

You can test the exact benchmark problem set directly in the UI or via CLI:

### Sample Problem Input:
```text
55 — Jump Game
121 — Best Time to Buy and Sell Stock
141 — Linked List Cycle
206 — Reverse Linked List
704 — Binary Search
875 — Koko Eating Bananas
1046 — Last Stone Weight
1710 — Maximum Units on a Truck
1834 — Single-Threaded CPU
```

### Steps in Web Interface:
1. Open `http://localhost:5173` and click **"Upload DSA Sheet"**.
2. Upload `backend/uploads/sample_dsa_sheet.txt` or paste the text above in the **Direct Text Paste** tab.
3. Click **"Parse and Extract Problems"** $\to$ Review the extracted problems in `/preview`.
4. Click **"Configure Roadmap"**:
   - **Level**: `Average`
   - **Duration**: `3 Months`
   - **Target**: `20 Problems`
5. Click **"Generate Personalized Roadmap"**:
   - Notice the prerequisite ordering: Linked List $\to$ Binary Search $\to$ Heap $\to$ Greedy $\to$ DP.
   - Each problem displays its LeetCode link, difficulty badge, and similar concept (e.g. `1710` $\to$ *Fractional Knapsack*, `1834` $\to$ *Shortest Job First*).
6. Mark any problem **"Completed"**:
   - Observe the progress bar increment in real time.
   - Navigate to `/revision` to see your Day 2, Day 7, and Day 21 spaced repetition schedule.
   - Check `/progress` for topic mastery metrics and weak topic suggestions.

### Run Automated Backend Test:
```bash
cd backend
python test_flow.py
```

---

## 🔒 Security & Best Practices
- **No hardcoded API keys**: LLM keys are read exclusively from environment variables or local browser settings.
- **Copyright compliant**: Only displays LeetCode numbers, titles, topics, difficulties, and algorithmic metadata without scraping full proprietary statements.
- **Resilient Fallback**: Operates deterministically even without an LLM API key.
