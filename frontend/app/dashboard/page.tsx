"use client";

import { useMemo, useState } from "react";
import { motion } from "motion/react";
import { ArrowLeft, ArrowUpRight, Bot, CheckCircle2, Clock3, CloudRain, Languages, Mic2, PhoneCall, ShieldCheck, Sparkles, UserRound, Wifi, Wheat } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Result = { reply:string; intent:string; demo:boolean; correlation_id?:string; source?:{name:string;url:string;retrieved_at:string;freshness_note?:string|null} };
const quickCalls = [
  ["Mandi bhav","गेहूं का मंडी भाव क्या है?",Wheat],
  ["Weather","कल बारिश होगी?",CloudRain],
  ["Yojana","मेरे लिए किसान की सरकारी योजना बताओ",ShieldCheck],
  ["Human help","मुझे किसी इंसान से बात करनी है",UserRound],
] as const;

export default function Dashboard(){
 const [message,setMessage]=useState(quickCalls[0][1]);
 const [result,setResult]=useState<Result|null>(null);
 const [loading,setLoading]=useState(false);
 const run=async()=>{
   setLoading(true);
   try{
     const r=await fetch(`${API}/api/v1/agent`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message,language:"hi",household_id:"demo-household"})});
     setResult(await r.json());
   }catch{setResult({reply:"Backend se connection nahi ho paaya. Demo ko galat live result nahi dikhana chahiye.",intent:"general",demo:true});}
   finally{setLoading(false);}
 };
 const trace=useMemo(()=>[
   ["01","Call / request received",true],["02","Language + intent detected",true],["03","Specialist agent selected",!!result],["04","Verified tool boundary",!!result],["05","Source + timestamp attached",!!result?.source],["06","Household memory",false],["07","Human fallback",result?.intent==="human"]
 ],[result]);
 return <main className="command-shell">
  <nav className="command-nav"><a href="/" className="command-brand"><span><Mic2 size={17}/></span>saathi<span className="brand-dot">.</span></a><div className="command-nav-meta"><span className="connection"><i/> Demo systems ready</span><span className="nav-divider"/><span className="operator"><UserRound size={14}/> Operator</span></div></nav>
  <div className="command-wrap">
   <header className="command-header"><div><div className="eyebrow"><span className="eyebrow-line"/> SAATHI COMMAND CENTER</div><h1>From voice to <em>action.</em></h1><p>See how one caller request moves through language, specialist agents, verified tools and human fallback.</p></div><div className="header-badges"><span><Wifi size={13}/> API ready</span><span><ShieldCheck size={13}/> Consent-led</span><span><Languages size={13}/> Hindi-first</span></div></header>
   <section className="status-grid">
    <article className="metric-card accent"><div className="metric-icon"><PhoneCall size={18}/></div><div><small>VOICE CHANNEL</small><strong>Missed call → Saathi</strong><p>Provider-gated · Exotel adapter ready</p></div></article>
    <article className="metric-card"><div className="metric-icon"><Bot size={18}/></div><div><small>ORCHESTRATOR</small><strong>6 specialist paths</strong><p>Deterministic routing + provider boundary</p></div></article>
    <article className="metric-card"><div className="metric-icon"><Clock3 size={18}/></div><div><small>TRACE ID</small><strong>{result?.correlation_id || "Waiting for call"}</strong><p>Propagated across the API request</p></div></article>
   </section>
   <section className="workspace">
    <div className="caller-panel">
     <div className="panel-head"><div><span className="panel-kicker">CALLER SIMULATOR</span><h2>What would you ask Saathi?</h2></div><span className="demo-tag"><i/> DEMO</span></div>
     <div className="caller-context"><div className="caller-avatar"><Mic2 size={23}/></div><div><strong>Unknown caller</strong><span>Hindi · Sonipat, Haryana</span></div><span className="call-state">READY</span></div>
     <textarea value={message} onChange={e=>setMessage(e.target.value)} aria-label="Caller request"/>
     <div className="quick-row">{quickCalls.map(([label,text,Icon])=><button key={label} onClick={()=>setMessage(text)}><Icon size={15}/>{label}</button>)}</div>
     <button className="run-button" onClick={run} disabled={loading}><Mic2 size={18}/>{loading?"Saathi is thinking…":"Run this conversation"}<ArrowUpRight size={17}/></button>
     {result&&<motion.div className="answer-card" initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}><div className="answer-label"><span><Bot size={15}/> SAATHI RESPONSE</span><b>{result.intent}</b></div><p>{result.reply}</p>{result.source&&<div className="source-row"><CheckCircle2 size={15}/><div><strong>{result.source.name}</strong><span>{result.source.freshness_note||"Provider result retrieved with timestamp."}</span></div></div>}</motion.div>}
    </div>
    <aside className="trace-panel"><div className="panel-head dark-head"><div><span className="panel-kicker">AGENT TRACE</span><h2>Every step is inspectable.</h2></div><Sparkles size={19}/></div><div className="trace-list">{trace.map(([num,label,active])=><div className={`trace-item ${active?"active":""}`} key={num}><span className="trace-num">{num}</span><span className="trace-line"/><span className="trace-label">{label}</span>{active?<CheckCircle2 size={15}/>:<span className="pending-dot"/>}</div>)}</div><div className="privacy-box"><ShieldCheck size={17}/><div><strong>No invented facts.</strong><p>Tool-backed answers carry provenance. Demo data stays visibly marked.</p></div></div></aside>
   </section>
   <section className="flow-strip">{[["01","Listen","Voice / missed call",Mic2],["02","Understand","Language + intent",Languages],["03","Act","Specialist + tools",Bot],["04","Remember","Consent-based memory",ShieldCheck],["05","Escalate","Human when needed",UserRound]].map(([num,title,sub,Icon],i)=><div className="flow-step" key={num}><span>{num}</span><Icon size={17}/><div><strong>{title}</strong><small>{sub}</small></div>{i<4&&<ArrowUpRight size={14}/>}</div>)}</section>
   <footer className="command-footer"><span>SAATHI · VOICE-FIRST ACCESS</span><span>Prototype control room · 2026</span><a href="/"><ArrowLeft size={14}/> Back to product</a></footer>
  </div>
 </main>
}