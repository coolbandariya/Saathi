"use client";\nimport "./home.css";

import { motion } from "motion/react";
import { ArrowRight, ArrowUpRight, AudioLines, Check, CheckCircle2, Database, Languages, Mic2, PhoneCall, ShieldCheck, Sparkles, Wheat, Zap } from "lucide-react";

const scenarios = [
  [Wheat,"Mandi bhav","“गेहूं ka mandi bhav aur kal baarish?”","Extract place + commodity, query specialist sources, then answer with provenance."],
  [ShieldCheck,"Government schemes","“Kisan yojana ke baare mein batao”","Guide the user without pretending an eligibility decision has been verified."],
  [PhoneCall,"Human fallback","“Mujhe kisi insaan se baat karni hai”","Escalate immediately instead of forcing automation past the user’s request."],
] as const;

const proof = [
  [Languages, "Hindi / Hinglish", "Natural code-mixed speech in a voice-first flow."],
  [Database, "Verified tools", "Government market data and weather stay outside the model."],
  [ShieldCheck, "No invented facts", "Missing context triggers clarification instead of a guess."],
] as const;

const steps = [["01","Listen","Sarvam speech"],["02","Understand","Intent + entities"],["03","Verify","Specialist tools"],["04","Respond","Grounded Hindi"]] as const;

export default function Home() {
  return <main>
    <nav className="nav wrap" aria-label="Primary navigation">
      <a className="brand" href="/" aria-label="Saathi home"><span className="brand-mark"><AudioLines size={19}/></span>saathi<span className="brand-dot">.</span></a>
      <div className="nav-right"><span className="status"><i/>Competition build · 2026</span><a className="nav-link" href="/dashboard">Open live demo <ArrowUpRight size={15}/></a></div>
    </nav>

    <section className="hero wrap">
      <motion.div className="hero-copy" initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{duration:.65}}>
        <div className="eyebrow"><span className="eyebrow-line"/>VOICE-FIRST · HINDI / HINGLISH</div>
        <h1>Speak naturally.<br/><em>Get verified help.</em></h1>
        <p className="hero-text">Saathi turns everyday Hindi speech into a verified action path — understanding the request, choosing the right specialist tool, and refusing to invent what it cannot verify.</p>
        <div className="hero-actions"><a className="button button-dark" href="/dashboard">Try the golden demo <ArrowRight size={17}/></a><a className="text-link" href="#proof">See why it is different <ArrowUpRight size={15}/></a></div>
        <div className="hero-meta"><span><Check size={14}/> Source-backed answers</span><span><Check size={14}/> Human fallback</span><span><Check size={14}/> Consent-led</span></div>
      </motion.div>

      <motion.div className="hero-stage" initial={{opacity:0,scale:.97}} animate={{opacity:1,scale:1}} transition={{duration:.7,delay:.12}}>
        <div className="stage-top"><div><span className="tiny-label">SAATHI · GOLDEN PATH</span><div className="card-title">One request. A visible chain.</div></div><span className="live-pill"><i/> DEMO READY</span></div>
        <div className="voice-scene"><div className="voice-orb"><AudioLines size={31}/></div><div className="voice-copy"><span>CALLER SAYS</span><strong>“Kal Sonipat mein गेहूं ka mandi bhav kya hai? Baarish ka chance bhi batao.”</strong></div></div>
        <div className="mini-trace">{steps.map(([num,title,sub],i)=><div className="mini-step" key={num}><span>{num}</span><strong>{title}</strong><small>{sub}</small>{i<3&&<ArrowRight size={13}/>}</div>)}</div>
        <div className="verified-banner"><CheckCircle2 size={17}/><div><strong>Answer only after verification</strong><span>AGMARKNET · Open-Meteo · retrieval time + provenance</span></div><Zap size={15}/></div>
      </motion.div>
    </section>

    <section className="proof-strip" id="proof"><div className="wrap proof-grid">{proof.map(([Icon,label,text])=><article className="proof-card" key={label}><div className="proof-icon"><Icon size={18}/></div><div><strong>{label}</strong><p>{text}</p></div></article>)}</div></section>

    <section className="difference wrap">
      <div className="section-heading"><div className="eyebrow"><span className="eyebrow-line"/>THE DIFFERENCE</div><h2>Most assistants answer.<br/><em>Saathi verifies.</em></h2><p>The model can decide what to ask and which declared tool to use. It does not get to decide what is true.</p></div>
      <div className="scenario-grid">
        {scenarios.map(([Icon,label,prompt,text],i)=><motion.article className="scenario-card" key={label as string} initial={{opacity:0,y:15}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*.08}}><span className="scenario-number">0{i+1}</span><div className="scenario-icon"><Icon size={19}/></div><span className="scenario-label">{label}</span><h3>{prompt}</h3><p>{text}</p></motion.article>)}
      </div>
    </section>

    <section className="architecture"><div className="wrap architecture-inner">
      <div className="architecture-copy"><div className="eyebrow"><span className="eyebrow-line"/>BUILT TO BE INSPECTED</div><h2>Agentic where it matters.<br/><em>Deterministic where it counts.</em></h2><p>Speech becomes structured intent. Intent selects a declared capability. The capability returns evidence. Saathi speaks only from that evidence.</p><a className="button button-light" href="/dashboard">Open the operator view <ArrowUpRight size={16}/></a></div>
      <div className="architecture-flow">{([[Mic2,"Speech","Sarvam STT"],[Sparkles,"Intent","Hindi + entities"],[Database,"Tools","OGD + weather"],[ShieldCheck,"Evidence","Provenance"],[AudioLines,"Voice","Sarvam TTS"]] as const).map(([Icon,title,sub],i)=><div className="arch-node" key={title as string}><div className="arch-icon"><Icon size={18}/></div><strong>{title}</strong><small>{sub}</small>{i<4&&<ArrowRight className="arch-arrow" size={15}/>}</div>)}</div>
    </div></section>

    <section className="final-cta wrap"><div><span className="eyebrow"><span className="eyebrow-line"/>READY FOR A REAL QUESTION?</span><h2>Bring Saathi a messy sentence.<br/><em>We’ll show the chain.</em></h2></div><a className="button button-dark" href="/dashboard">Enter the demo <ArrowUpRight size={17}/></a></section>
    <footer className="footer wrap"><a className="brand" href="/" aria-label="Saathi home"><span className="brand-mark"><AudioLines size={17}/></span>saathi<span className="brand-dot">.</span></a><span>Voice-first · source-backed · consent-led</span><span>© 2026 Saathi</span></footer>
  </main>;
}
