import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { SmoothScroll } from "@/components/layout/SmoothScroll";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrains = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "MCP-2099 | Engineering Supercharged",
  description: "Advanced developer platform for the retro-futuristic hacker elite.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className={`${inter.variable} ${jetbrains.variable} font-sans antialiased selection:bg-neon-blue selection:text-black bg-cyber-black text-white`}>
        <SmoothScroll>
          <Navbar />
          <main className="relative min-h-screen">
            {children}
          </main>
        </SmoothScroll>
      </body>
    </html>
  );
}

