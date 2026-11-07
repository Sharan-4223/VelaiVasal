import React, { useEffect, useRef, useState } from "react";
import { LANGS, SPEECH, T, SAMPLE_ANSWERS } from "./i18n.js";

const api = async (url, body) => {
  const r = await fetch(url, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : undefined);
  if (!r.ok) throw new Error(url + " " + r.status);
  return r.json();
};

function Ring({ value, label }) {
  const r = 52, c = 2 * Math.PI * r;
  return (
    <div className="ring" role="img" aria-label={`${label} ${value}%`}>
      <svg viewBox="0 0 120 120" width="132" height="132">
        <circle cx="60" cy="60" r={r} className="ring-bg" />
        <circle cx="60" cy="60" r={r} className="ring-fg" strokeDasharray={c} strokeDashoffset={c * (1 - value / 100)} transform="rotate(-90 60 60)" />
      </svg>
      <div className="ring-text"><b>{value}%</b><span>{label}</span></div>
    </div>
  );
}

function Bar({ label, value }) {
  return (
    <div className="bar"><span>{label}</span>
      <div className="track"><i style={{ width: value + "%" }} className={value >= 70 ? "ok" : value >= 40 ? "mid" : "low"} /></div>
      <b>{value}</b></div>
  );
}

function SkillPath({ t, lang, roles, role, setRole, goInterview }) {
  const [ratings, setRatings] = useState({});
  const [path, setPath] = useState(null);
  const current = roles.find((r) => r.id === role);

  useEffect(() => { setPath(null); setRatings({}); }, [role]);
  useEffect(() => { if (path) build(); /* refresh text when language changes */ }, [lang]);

  const build = async () => {
    const rs = {};
    current.skills.forEach((s) => (rs[s.id] = ratings[s.id] ?? 0));
    setPath(await api("/api/path", { role, lang, ratings: rs }));
  };

  return (
    <section>
      <h2>{t.pickRole}</h2>
      <div className="roles" data-testid="roles">
        {roles.map((r) => (
          <button key={r.id} className={"chip" + (r.id === role ? " on" : "")} onClick={() => setRole(r.id)}>{r.title}</button>
        ))}
      </div>

      {current && (
        <div className="card">
          <h2>{t.skillCheck}</h2>
          <p className="muted">{t.skillHelp}</p>
          {current.skills.map((s) => (
            <div className="skill" key={s.id}>
              <div className="skill-name">{s.name}</div>
              <div className="seg" role="radiogroup" aria-label={s.name}>
                {t.levels.map((l, i) => (
                  <button key={i} role="radio" aria-checked={ratings[s.id] === i}
                    className={ratings[s.id] === i ? "on" : ""} onClick={() => setRatings({ ...ratings, [s.id]: i })}
                    data-testid={`rate-${s.id}-${i}`}>{l}</button>
                ))}
              </div>
            </div>
          ))}
          <button className="primary" onClick={build} data-testid="build">{t.build}</button>
        </div>
      )}

      {path && (
        <div className="card" data-testid="path">
          <div className="path-head">
            <Ring value={path.readiness} label={t.readiness} />
            <div>
              <h2>{t.yourPath}</h2>
              <p className="muted">{path.title}</p>
              <p><b>{path.total_minutes}</b> {t.minutes}</p>
              <button className="primary small" onClick={goInterview} data-testid="to-interview">{t.practice} →</button>
            </div>
          </div>
          <ol className="steps">
            {path.steps.map((s) => (
              <li key={s.skill} className={s.gap ? "" : "done"}>
                <div className="step-top"><b>{s.name}</b><span className={"lvl l" + s.level}>{t.levels[s.level]}</span></div>
                {s.gap === 0 ? <p className="muted">{t.strong}</p> : (
                  <>
                    <div className="muted">{t.lessons}</div>
                    <ul>{s.lessons.map((l) => <li key={l.title}>{l.title} <em>{l.minutes} min</em></li>)}</ul>
                    <div className="task"><b>{t.task}:</b> {s.task}</div>
                  </>
                )}
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  );
}

function Interview({ t, lang, role, roles, setRole }) {
  const [qs, setQs] = useState([]);
  const [qi, setQi] = useState(0);
  const [answer, setAnswer] = useState("");
  const [res, setRes] = useState(null);
  const [prog, setProg] = useState({ attempts: 0, scores: [], average: 0 });
  const [listening, setListening] = useState(false);
  const rec = useRef(null);
  const SR = typeof window !== "undefined" && (window.SpeechRecognition || window.webkitSpeechRecognition);

  const loadProg = () => api("/api/progress?student=demo").then(setProg);
  useEffect(() => { api(`/api/interview/questions?role=${role}&lang=${lang}`).then((q) => { setQs(q); }); }, [role, lang]);
  useEffect(() => { setQi(0); setAnswer(""); setRes(null); }, [role]);
  useEffect(() => { loadProg(); }, []);

  const q = qs[qi];
  const submit = async () => {
    setRes(await api("/api/interview/score", { student: "demo", role, qid: q.id, lang, answer }));
    loadProg();
  };
  const toggleMic = () => {
    if (!SR) return alert(t.noMic);
    if (listening) { rec.current && rec.current.stop(); return; }
    const r = new SR(); r.lang = SPEECH[lang]; r.interimResults = false;
    r.onresult = (e) => setAnswer((a) => (a ? a + " " : "") + e.results[0][0].transcript);
    r.onend = () => setListening(false);
    rec.current = r; r.start(); setListening(true);
  };
  const pick = (i) => { setQi(i); setAnswer(""); setRes(null); };

  return (
    <section>
      <div className="roles">
        {roles.map((r) => <button key={r.id} className={"chip" + (r.id === role ? " on" : "")} onClick={() => setRole(r.id)}>{r.title}</button>)}
      </div>
      <h2>{t.pickQ}</h2>
      <div className="qtabs" data-testid="qtabs">
        {qs.map((x, i) => <button key={x.id} className={i === qi ? "on" : ""} onClick={() => pick(i)}>{i + 1}</button>)}
      </div>
      {q && (
        <div className="card">
          <span className="badge">{q.kind === "HR" ? t.kindHR : t.kindTech}</span>
          <h3 className="question" data-testid="question">{q.text}</h3>
          <p className="muted">💡 {t.hint}: {q.tip}</p>
          <textarea rows="5" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder={t.answerHere} data-testid="answer" />
          <div className="row">
            <button className={"mic" + (listening ? " live" : "")} onClick={toggleMic}>🎤 {listening ? t.stop : t.mic}</button>
            <button className="ghost" onClick={() => { setAnswer(SAMPLE_ANSWERS[q.id] || ""); setRes(null); }} data-testid="sample">{t.sample}</button>
            <button className="primary" onClick={submit} disabled={!answer.trim()} data-testid="score">{t.score}</button>
          </div>
        </div>
      )}
      {res && (
        <div className="card" data-testid="result">
          <div className="path-head">
            <Ring value={res.overall} label={t.overall} />
            <div className="bars">
              <Bar label={t.relevance} value={res.relevance} />
              <Bar label={t.structure} value={res.structure} />
              <Bar label={t.confidence} value={res.confidence} />
              <p className="muted">{res.words} {t.words}</p>
            </div>
          </div>
          <h3>{t.feedback}</h3>
          <ul className="fb">{res.feedback.map((f, i) => <li key={i}>{f}</li>)}</ul>
        </div>
      )}
      <div className="card prog" data-testid="progress">
        <h3>{t.progress}</h3>
        <div className="spark">
          {prog.scores.length === 0 ? <span className="muted">–</span> : prog.scores.map((s, i) => (
            <div key={i} className="sbar" style={{ height: Math.max(6, s) + "%" }} title={s}><span>{s}</span></div>
          ))}
        </div>
        <p className="muted">{prog.attempts} {t.attempts} · {t.average} {prog.average}</p>
      </div>
    </section>
  );
}

export default function App() {
  const [lang, setLang] = useState("en");
  const [tab, setTab] = useState("path");
  const [roles, setRoles] = useState([]);
  const [role, setRole] = useState("data-analyst");
  const t = T[lang];

  useEffect(() => { api("/api/roles?lang=" + lang).then(setRoles); document.documentElement.lang = lang; }, [lang]);

  return (
    <div className="app">
      <header>
        <div className="brand"><div className="logo">வ</div><div><h1>VelaiVaasal</h1><p>{t.tagline}</p></div></div>
        <div className="langs" role="group" aria-label="Language">
          {LANGS.map(([k, n]) => <button key={k} className={k === lang ? "on" : ""} onClick={() => setLang(k)} data-testid={"lang-" + k}>{n}</button>)}
        </div>
      </header>
      <nav className="tabs">
        <button className={tab === "path" ? "on" : ""} onClick={() => setTab("path")} data-testid="tab-path">{t.tabPath}</button>
        <button className={tab === "interview" ? "on" : ""} onClick={() => setTab("interview")} data-testid="tab-interview">{t.tabInterview}</button>
        <button disabled title={t.soon}>{t.resume}<small>{t.soon}</small></button>
        <button disabled title={t.soon}>{t.match}<small>{t.soon}</small></button>
      </nav>
      <main>
        {roles.length > 0 && (tab === "path"
          ? <SkillPath t={t} lang={lang} roles={roles} role={role} setRole={setRole} goInterview={() => setTab("interview")} />
          : <Interview t={t} lang={lang} role={role} roles={roles} setRole={setRole} />)}
      </main>
      <footer>{t.offline} · Seva Fest Hackathon 2026</footer>
    </div>
  );
}
