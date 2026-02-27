"use client";

import { useState } from "react";
import { Hero } from "@/components/sections/Hero";
import { Footer } from "@/components/sections/Footer";
import { CinematicLoader } from "@/components/layout/CinematicLoader";

export default function Home() {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <main className="relative min-h-screen bg-cyber-black overflow-hidden">
      {isLoading && <CinematicLoader onComplete={() => setIsLoading(false)} />}

      <div className={isLoading ? "opacity-0" : "opacity-100 transition-opacity duration-1000"}>
        <Hero />

        <section className="py-40 flex items-center justify-center relative border-t border-white/5">
          <div className="absolute inset-0 bg-grid-cyber opacity-20" />
          <div className="container px-6 text-center z-10">
            <h2 className="text-5xl md:text-8xl font-black uppercase text-white mb-6 italic tracking-tighter">
              THE <span className="text-neon-blue">PROTOCOL</span> IS LIVE
            </h2>
            <p className="text-white/40 uppercase tracking-[0.4em] max-w-2xl mx-auto text-xs font-mono">
              SYSTEM_AUTH: VALIDATED // SEC_LEVEL: ALPHA // STATUS: READY
            </p>
          </div>
        </section>

        <Footer />
      </div>
    </main>
  );
}

