"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import Scene from "@/components/canvas/Scene";

export function Hero() {
    const containerRef = useRef<HTMLDivElement>(null);
    const titleRef = useRef<HTMLHeadingElement>(null);
    const subtitleRef = useRef<HTMLParagraphElement>(null);

    useEffect(() => {
        const ctx = gsap.context(() => {
            gsap.from(titleRef.current, {
                y: 100,
                opacity: 0,
                duration: 1.5,
                ease: "power4.out",
                delay: 0.5,
            });

            gsap.from(subtitleRef.current, {
                y: 50,
                opacity: 0,
                duration: 1,
                ease: "power3.out",
                delay: 1,
            });
        }, containerRef);

        return () => ctx.revert();
    }, []);

    return (
        <section
            ref={containerRef}
            className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden"
        >
            <Scene />

            <div className="container mx-auto px-6 z-10 text-center pointer-events-none">
                <div className="mb-6 inline-block px-4 py-1.5 glass rounded-full border border-neon-blue/20">
                    <span className="text-neon-blue font-mono text-xs uppercase tracking-[0.3em] flex items-center gap-2">
                        <span className="w-1.5 h-1.5 bg-neon-blue rounded-full animate-pulse" />
                        Strategic Interface Enabled
                    </span>
                </div>

                <h1
                    ref={titleRef}
                    className="text-7xl md:text-9xl font-black tracking-tighter text-white uppercase leading-none"
                >
                    ENGINEERING,<br />
                    <span className="hologram-text italic">SUPERCHARGED</span>
                </h1>

                <p
                    ref={subtitleRef}
                    className="mt-8 max-w-2xl mx-auto text-white/60 text-lg md:text-xl font-light tracking-wide leading-relaxed"
                >
                    Build the future of decentralized infrastructure with our high-fidelity
                    retro-futuristic developer platform. Secure, autonomous, and sentient.
                </p>

                <div className="mt-12 flex flex-col md:flex-row gap-6 justify-center pointer-events-auto">
                    <button className="px-10 py-4 bg-neon-blue text-black font-bold uppercase tracking-widest hover:scale-105 transition-transform duration-300 shadow-[0_0_20px_rgba(0,243,255,0.4)]">
                        Initialize Core
                    </button>
                    <button className="px-10 py-4 glass text-white font-bold uppercase tracking-widest border border-white/10 hover:bg-white/5 transition-all duration-300">
                        View Protocols
                    </button>
                </div>
            </div>

            {/* Decorative HUD Elements */}
            <div className="absolute top-1/2 left-12 -translate-y-1/2 hidden xl:flex flex-col gap-8 opacity-40">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="flex flex-col gap-2">
                        <div className="h-[1px] w-32 bg-gradient-to-r from-neon-blue to-transparent" />
                        <span className="font-mono text-[10px] text-neon-blue uppercase tracking-widest">
                            SRV_NODE_0{i} // ONLINE
                        </span>
                    </div>
                ))}
            </div>

            <div className="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce opacity-40">
                <div className="w-6 h-10 border-2 border-white/20 rounded-full flex justify-center p-1">
                    <div className="w-1 h-2 bg-neon-blue rounded-full" />
                </div>
            </div>
        </section>
    );
}
