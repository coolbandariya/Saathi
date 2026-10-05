import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Saathi — Your voice. Your companion.",
  description: "A voice-first assistant for information, services, and follow-ups.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="hi"><body>{children}</body></html>;
}
