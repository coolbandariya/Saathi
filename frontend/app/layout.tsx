import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import Link from "next/link";
import { ArrowUpRight, AudioLines, LayoutDashboard } from "lucide-react";
import "./globals.css";
const manrope = Manrope({ subsets: ["latin"], display: "swap", variable: "--font-manrope" });
export const metadata: Metadata = {
  title: "Saathi — Speak naturally. Get verified help.",
  description: "A Hindi/Hinglish voice agent that turns natural speech into verified, source-backed assistance.",
  keywords: ["Saathi","voice agent","Hindi AI","Hinglish","agentic AI","verified AI"],
  openGraph: { title: "Saathi — Speak naturally. Get verified help.", description: "A voice-first agent that understands Hindi/Hinglish, selects specialist tools, and refuses to invent facts.", type: "website" },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className={manrope.variable}><body><nav className="site-nav" aria-label="Primary navigation">
  <Link className="site-nav-brand" href="/" aria-label="Saathi home"><span className="site-nav-mark"><AudioLines size={18} /></span>saathi<span className="site-nav-dot">.</span></Link>
  <div className="site-nav-links"><Link href="/">Product</Link><Link href="/dashboard"><LayoutDashboard size={14} /> Demo</Link></div>
  <div className="site-nav-right"><span className="site-nav-status"><i />Available for a live question</span><Link className="site-nav-cta" href="/dashboard">Try Saathi <ArrowUpRight size={14} /></Link></div>
</nav>{children}</body></html>;
}
