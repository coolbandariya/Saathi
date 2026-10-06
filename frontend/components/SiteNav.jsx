"use client";

import Link from "next/link";
import { AudioLines, ArrowUpRight, Mic2 } from "lucide-react";
import "./SiteNav.css";

export default function SiteNav({ variant = "light", status = "Competition build · 2026" }) {
  const dashboard = variant === "dashboard";
  return (
    <nav className={`site-nav ${variant}`} aria-label="Primary navigation">
      <Link className="site-brand" href="/" aria-label="Saathi home">
        <span className="site-brand-mark">{dashboard ? <Mic2 size={17} /> : <AudioLines size={19} />}</span>
        saathi<span className="site-brand-dot">.</span>
      </Link>
      <div className="site-nav-right">
        <span className="site-status"><i /> {status}</span>
        {dashboard ? (
          <Link className="site-nav-link" href="/">Product <ArrowUpRight size={14} /></Link>
        ) : (
          <Link className="site-nav-link" href="/dashboard">Open live demo <ArrowUpRight size={15} /></Link>
        )}
      </div>
    </nav>
  );
}
