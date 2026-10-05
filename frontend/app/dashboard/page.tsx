"use client";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Result = { reply:string; intent:string; demo:boolean; source?:{name:string;url:string;retrieved_at:string;freshness_note?:string|null} };

export default function Dashboard(){
 const [message,setMessage]=useState("गेहूं का मंडी भाव क्या है?");
 const [result,setResult]=useState<Result|null>(null);
 const [loading,setLoading]=useState(false);
 const run=async()=>{setLoading(true);try{const r=await fetch(`${API}/api/v1/agent`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message,language:"hi",household_id:"demo-household"})});setResult(await r.json())}finally{setLoading(false)}};
 return <main style={{minHeight:"100vh",padding:"48px 24px",background:"#f6f2e8",color:"#18161d"}}><div style={{maxWidth:1100,margin:"0 auto"}}>
 <div style={{display:"flex",justifyContent:"space-between",gap:20,alignItems:"center",marginBottom:40}}><div><div style={{letterSpacing:".14em",fontSize:12}}>SAATHI OPERATOR</div><h1 style={{fontSize:"clamp(32px,5vw,64px)",margin:"8px 0"}}>Agent control room.</h1><p style={{maxWidth:650}}>Test the same orchestration contract used by the voice layer. Tool results show their provenance instead of pretending the model is the source.</p></div><a href="/" style={{textDecoration:"none",color:"inherit"}}>← Home</a></div>
 <section style={{display:"grid",gridTemplateColumns:"minmax(0,1.3fr) minmax(280px,.7fr)",gap:20}}>
 <div style={{background:"white",border:"1px solid #ddd6c8",borderRadius:24,padding:24}}><label style={{fontSize:12,letterSpacing:".12em"}}>CALLER REQUEST</label><textarea value={message} onChange={e=>setMessage(e.target.value)} style={{width:"100%",minHeight:130,marginTop:14,padding:18,borderRadius:16,border:"1px solid #d8d0c2",fontSize:18,resize:"vertical"}}/><button onClick={run} disabled={loading} style={{marginTop:14,padding:"13px 18px",borderRadius:999,border:0,background:"#18161d",color:"white",cursor:"pointer"}}>{loading?"Running agent…":"Run Saathi agent"}</button>{result&&<div style={{marginTop:28,padding:20,borderRadius:18,background:"#f6f2e8"}}><div style={{fontSize:12,letterSpacing:".1em"}}>RESPONSE</div><p style={{fontSize:22,lineHeight:1.5}}>{result.reply}</p><div style={{display:"flex",gap:8,flexWrap:"wrap"}}><span style={{padding:"6px 10px",borderRadius:99,background:"white"}}>Intent: {result.intent}</span><span style={{padding:"6px 10px",borderRadius:99,background:"white"}}>{result.demo?"DEMO MODE":"LIVE"}</span></div></div>}</div>
 <aside style={{background:"#18161d",color:"white",borderRadius:24,padding:24}}><div style={{fontSize:12,letterSpacing:".12em",opacity:.7}}>TRACE</div><div style={{marginTop:22,lineHeight:2.1}}>✓ Request received<br/>✓ Intent classified<br/>✓ Specialist selected<br/>✓ Tool boundary enforced<br/>✓ Provenance attached<br/>○ Persistent memory<br/>○ Human escalation</div>{result?.source&&<div style={{marginTop:24,paddingTop:20,borderTop:"1px solid #454149"}}><div style={{fontSize:12,opacity:.7}}>SOURCE</div><strong>{result.source.name}</strong><p style={{fontSize:13,opacity:.75}}>{result.source.freshness_note || "Retrieved from provider."}</p></div>}</aside>
 </section></div></main>
}
