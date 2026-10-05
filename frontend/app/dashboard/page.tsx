"use client";

import Link from "next/link";

import { useEffect, useMemo, useRef, useState } from "react";
import { motion } from "motion/react";
import {
  ArrowLeft, ArrowRight, ArrowUpRight, Bot, CheckCircle2, ChevronDown,
  CloudRain, FileText, Languages, MapPin, Mic2, PhoneCall, Play,
  ShieldCheck, Sparkles, UserRound, Volume2, Wheat, X, Zap, type LucideIcon
} from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEMO_LOCATION = { latitude: 28.9931, longitude: 77.0151, label: "Sonipat district · demo context" };

type Source = { name: string; url: string; retrieved_at: string; freshness_note?: string | null };
type Result = {
  reply: string;
  intent: string;
  demo: boolean;
  correlation_id?: string;
  source?: Source;
  escalated?: boolean;
  escalation_reason?: string | null;
  confidence?: number | null;
};

const scenarios = [
  { id: "mandi", label: "Mandi bhav", text: "सोनीपत मंडी में गेहूं का आज क्या भाव है?", icon: Wheat },
  { id: "weather", label: "Weather", text: "कल बारिश होगी?", icon: CloudRain },
  { id: "scheme", label: "Yojana", text: "मेरे लिए किसान की सरकारी योजना बताओ", icon: ShieldCheck },
  { id: "human", label: "Human help", text: "मुझे किसी इंसान से बात करनी है", icon: UserRound },
] as const;

const flowSteps: [string, string, string, LucideIcon][] = [
  ["01", "Listen", "Voice / missed call", Mic2],
  ["02", "Understand", "Language + intent", Languages],
  ["03", "Act", "Specialist + tools", Bot],
  ["04", "Protect", "Consent boundary", ShieldCheck],
  ["05", "Escalate", "Human when needed", UserRound],
];

const judgeSteps = [
  ["call", "Call event simulated", "Voice channel", PhoneCall],
  ["lang", "Hindi understood", "Language + intent", Languages],
  ["agent", "Farming route selected", "Specialist routing", Bot],
  ["tool", "Mandi source checked", "Verified tool", Wheat],
  ["memory", "Consent boundary shown", "No silent memory", ShieldCheck],
  ["fallback", "Human fallback ready", "Escalation", UserRound],
] as const;

export default function Dashboard() {
  const [message, setMessage] = useState<string>(scenarios[0].text);
  const [scenario, setScenario] = useState("mandi");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [voiceState, setVoiceState] = useState<"idle" | "listening" | "thinking" | "speaking">("idle");
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [memoryConsent, setMemoryConsent] = useState(false);
  const [reminderConsent, setReminderConsent] = useState(false);
  const [showJudge, setShowJudge] = useState(true);
  const [judgeIndex, setJudgeIndex] = useState(-1);
  const [expanded, setExpanded] = useState<string | null>("memory");
  const [apiOnline, setApiOnline] = useState(false);
  const [apiReady, setApiReady] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API}/health/ready`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error("health check failed");
        const body = await response.json();
        setApiOnline(true);
        setApiReady(body.status === "ready");
      })
      .catch(() => {
        setApiOnline(false);
        setApiReady(false);
      });
    return () => controller.abort();
  }, []);

  const trace = useMemo(() => [
    ["01", "Call / request received", true],
    ["02", "Language + intent detected", true],
    ["03", "Specialist agent selected", !!result],
    ["04", "Verified tool boundary", !!result],
    ["05", "Source + timestamp attached", !!result?.source],
    ["06", "Household memory", memoryConsent && !!result],
    ["07", "Human fallback", result?.intent === "human"],
  ] as const, [result, memoryConsent]);

  const selectScenario = (id: string) => {
    const item = scenarios.find((entry) => entry.id === id) ?? scenarios[0];
    setScenario(id);
    setMessage(item.text);
    setResult(null);
    setJudgeIndex(-1);
    setVoiceState("idle");
  };

  const toggleVoice = async () => {
    setVoiceError(null);
    if (recorderRef.current) {
      recorderRef.current.stop();
      setVoiceState("thinking");
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setVoiceError("Browser microphone recording is not available here.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorderRef.current = recorder;
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };
      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        recorderRef.current = null;
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || "audio/webm" });
        if (!blob.size) {
          setVoiceState("idle");
          setVoiceError("No voice was captured.");
          return;
        }

        setLoading(true);
        setVoiceState("thinking");
        try {
          const form = new FormData();
          form.append("audio", blob, "caller.webm");
          form.append("language", "hi");
          form.append("household_id", "demo-household");
          form.append("latitude", String(DEMO_LOCATION.latitude));
          form.append("longitude", String(DEMO_LOCATION.longitude));
          form.append("location_label", DEMO_LOCATION.label);
          const response = await fetch(`${API}/api/v1/voice/turn`, { method: "POST", body: form });
          const body = await response.json();
          if (!response.ok) throw new Error(body.detail || `Voice request failed: ${response.status}`);
          setMessage(body.transcript || message);
          setResult(body);
          setVoiceState(body.audio_base64 ? "speaking" : "idle");

          if (body.audio_base64) {
            const bytes = Uint8Array.from(atob(body.audio_base64), (char) => char.charCodeAt(0));
            const audio = new Audio(URL.createObjectURL(new Blob([bytes], { type: body.audio_mime_type || "audio/wav" })));
            audio.onended = () => { URL.revokeObjectURL(audio.src); setVoiceState("idle"); };
            await audio.play();
          }
        } catch (error) {
          setVoiceState("idle");
          setVoiceError(error instanceof Error ? error.message : "Voice provider is not configured.");
        } finally {
          setLoading(false);
        }
      };
      recorder.start();
      setVoiceState("listening");
    } catch {
      setVoiceError("Microphone permission was denied or unavailable.");
      setVoiceState("idle");
    }
  };

  const run = async () => {
    setLoading(true);
    setVoiceState("thinking");
    try {
      const response = await fetch(`${API}/api/v1/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, language: "hi", household_id: "demo-household", location: DEMO_LOCATION }),
      });
      if (!response.ok) throw new Error(`Agent request failed: ${response.status}`);
      setResult(await response.json());
      setVoiceState("idle");
    } catch {
      setResult({
        reply: "Backend se connection nahi ho paaya. Saathi live result invent nahi karega — provider status check karein.",
        intent: "general",
        demo: true,
      });
      setVoiceState("idle");
    } finally {
      setLoading(false);
    }
  };

  const startJudge = () => {
    setShowJudge(true);
    setResult(null);
    setJudgeIndex(0);
    setVoiceState("listening");
  };

  const nextJudgeStep = () => {
    if (judgeIndex < judgeSteps.length - 1) {
      setJudgeIndex((value) => value + 1);
      if (judgeIndex + 1 === 2) setVoiceState("thinking");
      if (judgeIndex + 1 === 3) setVoiceState("speaking");
    } else {
      setVoiceState("idle");
      setJudgeIndex(-1);
    }
  };

  return (
    <main className="command-shell">
      <nav className="command-nav">
        <Link href="/" className="command-brand">
          <span><Mic2 size={17} /></span>saathi<span className="brand-dot">.</span>
        </Link>
        <div className="command-nav-meta">
          <span className="connection"><i /> {apiOnline ? (apiReady ? "API ready" : "API online · providers gated") : "API offline"}</span>
          <span className="nav-divider" />
          <span className="operator"><UserRound size={14} /> Operator</span>
        </div>
      </nav>

      <div className="command-wrap">
        <header className="command-header">
          <div>
            <div className="eyebrow"><span className="eyebrow-line" /> SAATHI COMMAND CENTER</div>
            <h1>From voice to <em>action.</em></h1>
            <p>Inspect the complete demo journey: language, specialist routing, verified tools, evidence, consent boundaries and human fallback.</p>
          </div>
          <div className="header-badges">
            <span><Zap size={13} /> {apiOnline ? (apiReady ? "API ready" : "API online") : "API offline"}</span>
            <span><ShieldCheck size={13} /> Consent-led</span>
            <span><Languages size={13} /> Hindi-first</span>
            {!showJudge && <button type="button" className="judge-toggle" onClick={() => setShowJudge(true)}>Show judge mode</button>}
          </div>
        </header>

        {showJudge && (
          <section className="judge-panel" aria-labelledby="judge-mode-title">
            <div className="judge-copy">
              <div className="panel-kicker">JUDGE MODE · GOLDEN DEMO</div>
              <div className="judge-title-row"><h2 id="judge-mode-title">One call. One visible chain.</h2><button type="button" className="judge-close" onClick={() => setShowJudge(false)} aria-label="Close judge mode"><X size={16} /></button></div>
              <p>Run the recommended 60-second story: request → Hindi → farming intent → verified tools → evidence → human fallback.</p>
              <button type="button" className="judge-start" onClick={startJudge}>
                <Play size={15} fill="currentColor" /> Start golden demo
              </button>
            </div>
            <div className="judge-timeline">
              {judgeSteps.map(([id, title, sub, Icon], index) => {
                const active = judgeIndex === index;
                const done = judgeIndex > index;
                return (
                  <button type="button" className={`judge-step ${active ? "active" : ""} ${done ? "done" : ""}`} key={id} onClick={() => setJudgeIndex(index)} aria-current={active ? "step" : undefined}>
                    <span>{done ? <CheckCircle2 size={14} /> : <Icon size={14} />}</span>
                    <strong>{title}</strong>
                    <small>{sub}</small>
                  </button>
                );
              })}
            </div>
            {judgeIndex >= 0 && (
              <div className="judge-live">
                <span className="voice-pulse"><Mic2 size={17} /></span>
                <div><strong>{judgeSteps[judgeIndex][1]}</strong><small>{judgeSteps[judgeIndex][2]}</small></div>
                <button type="button" onClick={nextJudgeStep}>{judgeIndex === judgeSteps.length - 1 ? "Finish" : "Next"} <ArrowRight size={14} /></button>
              </div>
            )}
          </section>
        )}

        <section className="status-grid">
          <article className="metric-card accent">
            <div className="metric-icon"><PhoneCall size={18} /></div>
            <div><small>VOICE CHANNEL</small><strong>Missed call → Saathi</strong><p>Provider-gated · Exotel adapter ready</p></div>
          </article>
          <article className="metric-card">
            <div className="metric-icon"><Bot size={18} /></div>
            <div><small>ORCHESTRATOR</small><strong>Specialist routing</strong><p>Deterministic intent + tool boundary</p></div>
          </article>
          <article className="metric-card">
            <div className="metric-icon"><Sparkles size={18} /></div>
            <div><small>VOICE STATE</small><strong>{voiceState === "idle" ? "Ready" : voiceState === "listening" ? "Listening" : voiceState === "thinking" ? "Thinking" : "Speaking"}</strong><p>Live adapter state · demo-safe</p></div>
          </article>
        </section>

        <section className="workspace">
          <div className="caller-panel">
            <div className="panel-head">
              <div><span className="panel-kicker">CALLER SIMULATOR</span><h2>What would you ask Saathi?</h2></div>
              <span className="demo-tag"><i /> DEMO · SAFE MODE</span>
            </div>

            <div className="caller-context">
              <div className={`caller-avatar ${voiceState !== "idle" ? "pulse" : ""}`}><Mic2 size={23} /></div>
              <div><strong>Unknown caller</strong><span>Hindi · Sonipat district</span></div>
              <span className={`call-state ${voiceState !== "idle" ? "busy" : ""}`}>{voiceState.toUpperCase()}</span>
            </div>

            <div className="scenario-tabs" role="tablist" aria-label="Demo scenarios">
              {scenarios.map(({ id, label, icon: Icon }) => (
                <button type="button" key={id} role="tab" aria-selected={scenario === id} className={scenario === id ? "selected" : ""} onClick={() => selectScenario(id)}>
                  <Icon size={14} />{label}
                </button>
              ))}
            </div>

            <textarea value={message} onChange={(event) => setMessage(event.target.value)} aria-label="Caller request" />

            <div className="voice-controls">
              <button type="button" className={`voice-button ${voiceState === "listening" ? "active" : ""}`} onClick={toggleVoice} aria-label="Toggle microphone" disabled={loading || voiceState === "speaking"}>
                <Mic2 size={18} /> {voiceState === "listening" ? "Stop recording" : "Start voice"}
              </button>
              <span><Volume2 size={13} /> Real mic → STT → agent → TTS when the voice provider is configured</span>
            </div>

            {voiceError && <div className="voice-error" role="alert" aria-live="assertive">{voiceError}</div>}

            <button type="button" className="run-button" onClick={run} disabled={loading || !message.trim()}>
              <Bot size={18} />{loading ? "Saathi is thinking…" : "Run this conversation"}<ArrowUpRight size={17} />
            </button>

            {result && (
              <motion.div className="answer-card" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <div className="answer-label"><span><Bot size={15} /> SAATHI RESPONSE</span><b>{result.intent}</b></div>
                <p>{result.reply}</p>
                {result.source ? (
                  <div className="source-row"><CheckCircle2 size={15} /><div><strong>{result.source.name}</strong><span>{result.source.freshness_note || "Provider result retrieved with timestamp."}</span><small>Retrieved · {new Date(result.source.retrieved_at).toLocaleString()}</small>{result.source.url && <a href={result.source.url} target="_blank" rel="noreferrer">View source ↗</a>}</div></div>
                ) : (
                  <div className="source-row warning"><ShieldCheck size={15} /><div><strong>No live source attached</strong><span>Saathi will not present an unverified answer as live fact.</span></div></div>
                )}
                {result.correlation_id && <div className="correlation-line">Correlation ID · <code>{result.correlation_id}</code></div>}
              </motion.div>
            )}
          </div>

          <aside className="trace-panel">
            <div className="panel-head dark-head">
              <div><span className="panel-kicker">AGENT TRACE</span><h2>Every step is inspectable.</h2></div>
              <Sparkles size={19} />
            </div>
            <div className="trace-list">
              {trace.map(([num, label, active]) => (
                <div className={`trace-item ${active ? "active" : ""}`} key={num}>
                  <span className="trace-num">{num}</span><span className="trace-line" /><span className="trace-label">{label}</span>
                  {active ? <CheckCircle2 size={15} /> : <span className="pending-dot" />}
                </div>
              ))}
            </div>
            <div className="privacy-box"><ShieldCheck size={17} /><div><strong>No invented facts.</strong><p>Tool-backed answers carry provenance. Demo data stays visibly marked.</p></div></div>
          </aside>
        </section>

        <section className="context-grid">
          <article className="context-card">
            <div className="context-title"><div><span className="panel-kicker">FIELD CONTEXT</span><h3>Where should Saathi look?</h3></div><MapPin size={18} /></div>
            <div className="location-row"><div className="map-placeholder"><MapPin size={23} /><span>FIELD CONTEXT</span></div><div><strong>Sonipat district</strong><p>Explicit demo context is passed to the API. No browser GPS is claimed.</p><span className="source-status"><i /> Location source · contextual</span></div></div>
          </article>

          <article className="context-card">
            <div className="context-title"><div><span className="panel-kicker">SOURCE HEALTH</span><h3>What can we trust?</h3></div><CheckCircle2 size={18} /></div>
            <div className="health-list">
              <div><span><Wheat size={14} /> Mandi tool</span><b className="demo-badge">DEMO / API-ready</b></div>
              <div><span><CloudRain size={14} /> Weather tool</span><b className="live-badge">Open-Meteo adapter</b></div>
              <div><span><ShieldCheck size={14} /> Scheme rules</span><b className="live-badge">Deterministic</b></div>
            </div>
          </article>
        </section>

        <section className="consent-card" aria-labelledby="consent-title">
          <div className="context-title"><div><span className="panel-kicker">HOUSEHOLD MEMORY</span><h3 id="consent-title">Remember only with permission.</h3></div><ShieldCheck size={18} /></div>
          <p className="consent-intro">Saathi separates useful continuity from silent surveillance. Each future memory/reminder capability has its own consent boundary.</p>
          <div className="consent-options">
            <button type="button" className={`consent-option ${memoryConsent ? "on" : ""}`} aria-pressed={memoryConsent} onClick={() => setMemoryConsent((value) => !value)}>
              <span className="toggle">{memoryConsent ? <CheckCircle2 size={14} /> : <X size={14} />}</span>
              <div><strong>Household memory</strong><small>{memoryConsent ? "Consented for this demo household" : "Not enabled"}</small></div>
              <ChevronDown size={14} />
            </button>
            <button type="button" className={`consent-option ${reminderConsent ? "on" : ""}`} aria-pressed={reminderConsent} onClick={() => setReminderConsent((value) => !value)}>
              <span className="toggle">{reminderConsent ? <CheckCircle2 size={14} /> : <X size={14} />}</span>
              <div><strong>Outbound reminders</strong><small>{reminderConsent ? "Consent recorded in demo state" : "Not enabled"}</small></div>
              <ChevronDown size={14} />
            </button>
          </div>
          <div className="consent-note"><ShieldCheck size={14} /> In production, consent, opt-out, quiet hours and deletion must be persisted server-side.</div>
        </section>

        <section className="fallback-card" aria-labelledby="fallback-title">
          <div className="fallback-icon"><UserRound size={22} /></div>
          <div className="fallback-copy"><span className="panel-kicker">HUMAN FALLBACK</span><h3 id="fallback-title">When confidence drops, hand the call to a person.</h3><p>Saathi can package the conversation context for a volunteer instead of forcing the model to answer beyond its safety or confidence boundary.</p></div>
          <div className="fallback-status"><span><i /> Ready</span><small>Policy threshold · 0.65</small></div>
        </section>

        <section className="flow-strip">
          {flowSteps.map(([num, title, sub, Icon], i) => (
            <div className="flow-step" key={num}><span>{num}</span><Icon size={17} /><div><strong>{title}</strong><small>{sub}</small></div>{i < 4 && <ArrowUpRight size={14} />}</div>
          ))}
        </section>

        <footer className="command-footer" aria-label="Saathi footer">
          <span>SAATHI · VOICE-FIRST ACCESS</span><span>Prototype control room · 2026</span>
          <Link href="/"><ArrowLeft size={14} /> Back to product</Link>
        </footer>
      </div>
    </main>
  );
}
