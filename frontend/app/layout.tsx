import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "WorldCupOps Agent",
  description: "AI Incident Commander for World Cup Operations"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
