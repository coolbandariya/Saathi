import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";
const manrope = Manrope({ subsets: ["latin"], display: "swap", variable: "--font-manrope" });
export const metadata: Metadata = {
  title: "Saathi — Speak naturally. Get verified help.",
  description: "A Hindi/Hinglish voice agent that turns natural speech into verified, source-backed assistance.",
  keywords: ["Saathi","voice agent","Hindi AI","Hinglish","agentic AI","verified AI"],
  openGraph: { title: "Saathi — Speak naturally. Get verified help.", description: "A voice-first agent that understands Hindi/Hinglish, selects specialist tools, and refuses to invent facts.", type: "website" },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className={manrope.variable}><body>{children}</body></html>;
}
