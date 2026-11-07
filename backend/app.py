"""VelaiVaasal prototype backend.

Production plan (see registration): FastAPI + LLM API + PostgreSQL (Supabase).
This offline demo uses Flask + SQLite and a rule-based scorer standing in for the LLM,
so it runs anywhere with no network or API keys. The scoring function is isolated in
`score_answer` so an LLM call can replace it without touching the API.
"""
import os
import re
import sqlite3
import time
from flask import Flask, jsonify, request, send_from_directory

from data import ROLES, QUESTIONS, FILLERS, LEVELS

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "..", "frontend", "dist")
DB = os.environ.get("VV_DB", os.path.join(ROOT, "velaivaasal.db"))
LANGS = ("en", "ta", "hi")

app = Flask(__name__, static_folder=None)


# ---------- storage ----------
def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute(
        "CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, student TEXT,"
        " role TEXT, qid TEXT, lang TEXT, overall INTEGER, relevance INTEGER, structure INTEGER,"
        " confidence INTEGER, ts REAL)"
    )
    return con


# ---------- skill path engine ----------
def build_path(role_id, ratings, lang="en"):
    """ratings: {skill_id: 0..3}. Gap = (3 - rating) * weight; biggest gaps come first."""
    role = ROLES[role_id]
    steps, total_gap, max_gap = [], 0, 0
    for s in role["skills"]:
        r = max(0, min(3, int(ratings.get(s["id"], 0))))
        gap = (3 - r) * s["weight"]
        total_gap += gap
        max_gap += 3 * s["weight"]
        steps.append({
            "skill": s["id"], "name": s["name"][lang], "level": r, "level_label": LEVELS[r],
            "gap": gap, "weight": s["weight"],
            "lessons": [{"title": t, "minutes": m} for t, m in s["lessons"]] if gap else [],
            "task": s["task"] if gap else None,
        })
    steps.sort(key=lambda x: (-x["gap"], -x["weight"]))
    steps = [dict(st, order=i + 1) for i, st in enumerate(steps)]
    readiness = round(100 * (1 - total_gap / max_gap)) if max_gap else 0
    minutes = sum(l["minutes"] for st in steps for l in st["lessons"])
    return {"role": role_id, "title": role["title"][lang], "readiness": readiness,
            "total_minutes": minutes, "steps": steps}


# ---------- interview scorer (LLM stand-in) ----------
def score_answer(question, answer, lang="en"):
    text = (answer or "").strip()
    low = text.lower()
    words = re.findall(r"[^\s.,;:!?।()\"']+", low)  # split on spaces/punctuation (\w breaks Tamil/Hindi vowel signs)
    n = len(words)
    if n == 0:
        return {"overall": 0, "relevance": 0, "structure": 0, "confidence": 0,
                "feedback": ["Please say or type an answer first."], "words": 0}

    # relevance: share of expected keywords touched (cap at 4 hits = full marks)
    hits = sorted({k for k in question["kw"] if k.lower() in low})
    relevance = min(100, round(100 * len(hits) / 4))

    # structure: enough sentences, linking words, an example, and a result
    sentences = [s for s in re.split(r"[.!?।\n]+", text) if len(s.split()) >= 3]
    links = sum(1 for w in ("first", "then", "because", "so", "finally", "for example", "result", "also") if w in low)
    structure = min(100, 25 * min(len(sentences), 3) + 10 * min(links, 2) + (5 if n >= 25 else 0))

    # confidence: right length, no filler words, no hedging
    fillers = sum(len(re.findall(r"\b" + re.escape(f) + r"\b", low)) for f in FILLERS)
    length_pts = 60 if 25 <= n <= 120 else 40 if 12 <= n < 25 else 20 if n < 12 else 45
    confidence = max(0, min(100, length_pts + 40 - 10 * fillers))

    overall = round(0.5 * relevance + 0.25 * structure + 0.25 * confidence)

    fb = []
    if relevance >= 75:
        fb.append("Strong answer: you covered the key points (" + ", ".join(hits[:4]) + ").")
    elif relevance >= 25:
        fb.append("You touched some key points. Add more specifics. Hint: " + question["tip"][lang] + "")
    else:
        fb.append("Your answer drifted from the question. Hint: " + question["tip"][lang])
    if len(sentences) < 3:
        fb.append("Try 3 or more sentences: point, example, result.")
    if n < 25:
        fb.append("Your answer is short. Aim for about 30 to 80 words.")
    elif n > 120:
        fb.append("Your answer is long. Trim it to the main points.")
    if fillers:
        fb.append(f"Cut filler words (found {fillers}). A short pause sounds more confident.")
    if overall >= 75 and len(fb) == 1:
        fb.append("Sounds confident. Practise once more, then move to the next question.")
    return {"overall": overall, "relevance": relevance, "structure": structure,
            "confidence": confidence, "feedback": fb, "words": n, "matched": hits}


# ---------- API ----------
@app.get("/api/health")
def health():
    return jsonify(status="ok", roles=len(ROLES))


@app.get("/api/roles")
def roles():
    lang = request.args.get("lang", "en")
    lang = lang if lang in LANGS else "en"
    return jsonify([{"id": k, "title": v["title"][lang],
                     "skills": [{"id": s["id"], "name": s["name"][lang], "weight": s["weight"]} for s in v["skills"]]}
                    for k, v in ROLES.items()])


@app.post("/api/path")
def path():
    body = request.get_json(force=True)
    role_id, lang = body.get("role"), body.get("lang", "en")
    if role_id not in ROLES or lang not in LANGS:
        return jsonify(error="unknown role or language"), 400
    return jsonify(build_path(role_id, body.get("ratings", {}), lang))


@app.get("/api/interview/questions")
def questions():
    role_id, lang = request.args.get("role"), request.args.get("lang", "en")
    if role_id not in ROLES or lang not in LANGS:
        return jsonify(error="unknown role or language"), 400
    qs = QUESTIONS["hr"] + QUESTIONS.get(role_id, [])
    return jsonify([{"id": q["id"], "text": q["q"][lang], "tip": q["tip"][lang],
                     "kind": "HR" if q["id"].startswith("hr") else "Technical"} for q in qs])


@app.post("/api/interview/score")
def score():
    b = request.get_json(force=True)
    pool = QUESTIONS["hr"] + QUESTIONS.get(b.get("role"), [])
    q = next((x for x in pool if x["id"] == b.get("qid")), None)
    lang = b.get("lang", "en")
    if q is None or lang not in LANGS:
        return jsonify(error="unknown question"), 400
    res = score_answer(q, b.get("answer", ""), lang)
    with db() as con:
        con.execute("INSERT INTO attempts (student, role, qid, lang, overall, relevance, structure, confidence, ts)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    (b.get("student", "demo"), b.get("role"), q["id"], lang, res["overall"], res["relevance"],
                     res["structure"], res["confidence"], time.time()))
    return jsonify(res)


@app.get("/api/progress")
def progress():
    student = request.args.get("student", "demo")
    with db() as con:
        rows = con.execute("SELECT qid, overall, ts FROM attempts WHERE student=? ORDER BY id", (student,)).fetchall()
    scores = [r["overall"] for r in rows]
    return jsonify(attempts=len(scores), scores=scores[-10:],
                   average=round(sum(scores) / len(scores)) if scores else 0)


@app.post("/api/progress/reset")
def reset():
    with db() as con:
        con.execute("DELETE FROM attempts WHERE student=?", (request.get_json(force=True).get("student", "demo"),))
    return jsonify(ok=True)


# ---------- serve compiled frontend ----------
@app.get("/", defaults={"p": "index.html"})
@app.get("/<path:p>")
def static_files(p):
    return send_from_directory(DIST, p)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
