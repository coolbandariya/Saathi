"use client";

import { FormEvent, useState } from "react";
import { motion } from "motion/react";
import { ArrowUpRight, AudioLines, Check, Languages, Loader2, MessageCircle, ShieldCheck, Sparkles } from "lucide-react";

type Message = { role: "user" | "assistant"; text: string };

const features = [
  { icon: Languages, title: "Speak naturally", text: "Start in Hindi, with a foundation for regional languages and dialects." },
  { icon: Sparkles, title: "Get guided help", text: "Saathi routes requests to specialist workflows instead of guessing." },
  { icon: ShieldCheck, title: "Continue when ready", text: "With permission, unfinished work can be resumed later." },
];

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function Home() {
  const [input, setInput] = useState("Mujhe scholarship ke baare mein jaanna hai.");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function sendDemo(event?: FormEvent) {
    event?.preventDefault();
    const message = input.trim();
    if (!message || loading) return;
    setMessages((current) => [...current, { role: "user", text: message }]);
    setInput("");
    setLoading(true);
    try {
      const response = await fetch(API_BASE + "/api/v1/conversation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, language: "hi" }),
      });
      if (!response.ok) throw new Error("API unavailable");
      const data = await response.json();
      setMessages((current) => [...current, { role: "assistant", text: data.reply }]);
    } catch {
      setMessages((current) => [...current, { role: "assistant", text: "Demo backend se connection nahi ho paaya. Backend chala kar dobara try karein." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <nav className="nav wrap" aria-label="Main navigation">
        <a className="brand" href="#" aria-label="Saathi home"><span className="brand-mark"><AudioLines size={19} /></span>saathi<span className="brand-dot">.</span></a>
        <div className="nav-right"><span className="status"><i />Prototype in progress</span><a className="nav-link" href="#how">How it works <ArrowUpRight size={15} /></a></div>
      </nav>

      <section className="hero wrap">
        <motion.div className="hero-copy" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.65 }}>
          <div className="eyebrow"><span className="eyebrow-line" />A companion, in your language</div>
          <h1>Help should feel<br /><em>closer.</em></h1>
          <p className="hero-text">A voice-first assistant designed to make everyday information and services easier to access—one conversation at a time.</p>
          <div className="hero-actions"><a className="button button-dark" href="#demo">Explore the demo <ArrowUpRight size={17} /></a><span className="micro-note"><ShieldCheck size={15} /> Your choice. Your consent.</span></div>
          <div className="hero-meta"><span><Check size={14} /> Hindi-first experience</span><span><Check size={14} /> Designed for mobile</span></div>
        </motion.div>

        <motion.div className="voice-card" id="demo" initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.7, delay: 0.12 }}>
          <div className="card-top"><div><span className="tiny-label">SAATHI VOICE</span><div className="card-title">A little help, by voice.</div></div><span className="live-pill"><i /> DEMO</span></div>
          <div className="orb-wrap" aria-hidden="true"><div className="orb-ring ring-one" /><div className="orb-ring ring-two" /><div className="orb"><AudioLines size={34} strokeWidth={1.5} /></div><span className="orb-spark spark-a" /><span className="orb-spark spark-b" /></div>
          <div className="voice-prompt"><span className="prompt-label">TRY SAYING</span><p>“Mujhe scholarship ke baare mein jaanna hai.”</p></div>
          <form onSubmit={sendDemo}>
            <label className="sr-only" htmlFor="demo-message">Say something to Saathi</label>
            <div className="demo-input-row">
              <input id="demo-message" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Type a Hindi request..." maxLength={4000} disabled={loading} />
              <button className="call-button" type="submit" disabled={loading || !input.trim()}>{loading ? <Loader2 size={18} className="spin" /> : <MessageCircle size={18} />}{loading ? "Thinking..." : "Talk to Saathi"}{!loading && <ArrowUpRight size={16} />}</button>
            </div>
          </form>
          {messages.length > 0 && <div className="demo-transcript" aria-live="polite">{messages.map((message, index) => <div className={"bubble " + message.role} key={message.role + "-" + index}><span>{message.role === "user" ? "You" : "Saathi"}</span><p>{message.text}</p></div>)}</div>}
          <p className="demo-caption">Interactive browser demo · Live phone integration remains separate.</p>
        </motion.div>
      </section>

      <section className="trust-strip"><div className="wrap strip-inner"><span>BUILT AROUND PEOPLE</span><span>Voice-first</span><b>·</b><span>Consent-led</span><b>·</b><span>Designed to be accessible</span></div></section>

      <section className="features wrap" id="how">
        <div className="section-heading"><div className="eyebrow"><span className="eyebrow-line" />THE SAATHI APPROACH</div><h2>Technology that listens<br />before it answers.</h2><p>Useful support should be understandable, respectful, and available at the moment it is needed.</p></div>
        <div className="feature-grid">{features.map((feature, index) => { const Icon = feature.icon; return <motion.article className="feature" key={feature.title} initial={{ opacity: 0, y: 15 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * 0.1 }}><div className="feature-icon"><Icon size={20} /></div><span className="feature-number">0{index + 1}</span><h3>{feature.title}</h3><p>{feature.text}</p></motion.article>; })}</div>
      </section>

      <footer className="footer wrap"><a className="brand" href="#"><span className="brand-mark"><AudioLines size={17} /></span>saathi<span className="brand-dot">.</span></a><span>Built with care · Demo 0.3</span><span>© 2026 Saathi</span></footer>
    </main>
  );
}
