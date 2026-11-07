# VelaiVaasal - Prototype Demo (Seva Fest Hackathon 2026, Placement & Education)

Working prototype of the **Skill Path Builder** and **Mock Interview Coach**, in English, Tamil and Hindi, running offline on sample data.

## Run
```bash
./run.sh            # compiles the React source, runs backend tests, starts the server
# open http://localhost:8000
```
Manual steps:
```bash
cd frontend && npm install && npm run build      # JSX -> dist/app.js (esbuild)
cd ../backend && pip install flask && python3 app.py
python3 tests/test_backend.py                    # 7 API tests
python3 tests/e2e_screenshots.py                 # browser test + screenshots (needs playwright)
```

## What is in the demo
- **Skill Path**: pick a target role, do a 4-level skill check, get a personal roadmap ordered by (gap x employer weight), job-readiness score, lessons and mini-tasks.
- **Mock Interview**: HR + role questions, type or speak (browser Web Speech API: en-IN / ta-IN / hi-IN), instant feedback on relevance, structure and confidence; progress saved in SQLite.
- Mobile-first, light page, language switch for all UI text and questions.
- Resume Studio and Opportunity Match are shown as "Coming next" (as stated in the registration's prototype scope).

## Prototype vs plan
| Registration plan | This demo |
|---|---|
| React PWA | React 19 bundled with esbuild (manifest included; no service worker yet) |
| FastAPI | Flask (FastAPI could not be installed offline); the endpoints map 1:1 |
| LLM API + Tamil/Hindi STT | Rule-based scorer `score_answer()` + browser speech recognition. Swap the function for an LLM call. |
| PostgreSQL (Supabase) | SQLite |

The scorer is a transparent heuristic (keyword coverage, sentence structure, length/filler words). It is a stand-in, not an AI evaluation. Sample data and the demo were not tested with real students.
