"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Terminal, Sun, Moon, Zap } from "lucide-react";

const navItems = [
    { name: "Interface", href: "/" },
    { name: "Neural Net", href: "/neural-net" },
    { name: "Protocol", href: "/protocol" },
    { name: "Logs", href: "/logs" },
    { name: "Dashboard", href: "/dashboard" },
];

export function Navbar() {
    const [isDark, setIsDark] = useState(true);
    const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

    const toggleTheme = () => {
        setIsDark(!isDark);
        document.documentElement.classList.toggle("dark");
        // In a real app, this would also update 3D scenes via a global state
    };

    return (
        <nav className="fixed top-6 left-0 right-0 z-[100] flex justify-center px-4">
            <div className="glass flex items-center gap-8 px-6 py-2 rounded-xl border border-white/5 max-w-4xl w-full justify-between">
                <Link href="/" className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-neon-blue/10 rounded flex items-center justify-center border border-neon-blue/40 shadow-[0_0_15px_rgba(0,243,255,0.2)]">
                        <Terminal className="w-5 h-5 text-neon-blue" />
                    </div>
                    <div className="hidden sm:block">
                        <span className="text-white font-black tracking-tighter text-lg block leading-none">MCP-2099</span>
                        <span className="text-neon-blue font-mono text-[8px] uppercase tracking-[0.4em]">Developer OS</span>
                    </div>
                </Link>

                <ul className="hidden md:flex items-center gap-1">
                    {navItems.map((item, idx) => (
                        <li key={item.name}>
                            <Link
                                href={item.href}
                                className="relative px-4 py-2 group overflow-hidden block"
                                onMouseEnter={() => setHoveredIndex(idx)}
                                onMouseLeave={() => setHoveredIndex(null)}
                            >
                                <span className="relative z-10 text-[10px] uppercase font-mono tracking-widest text-white/50 group-hover:text-neon-blue transition-colors duration-300">
                                    {hoveredIndex === idx && <span className="mr-1 text-neon-blue animate-pulse">&gt;</span>}
                                    {item.name}
                                </span>
                                <span className="absolute bottom-0 left-0 w-full h-[1px] bg-neon-blue transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left" />
                            </Link>
                        </li>
                    ))}
                </ul>

                <div className="flex items-center gap-4">
                    <button
                        onClick={toggleTheme}
                        className="p-2 hover:bg-white/5 rounded-lg transition-colors text-white/60 hover:text-white"
                    >
                        {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                    </button>

                    <Link
                        href="/dashboard"
                        className="hidden sm:flex items-center gap-2 px-6 py-2 bg-neon-blue/10 border border-neon-blue/40 text-neon-blue rounded text-[10px] font-bold uppercase tracking-widest hover:bg-neon-blue hover:text-black transition-all duration-300 shadow-[0_0_10px_rgba(0,243,255,0.1)]"
                    >
                        <Zap className="w-3 h-3 fill-current" />
                        Initialize
                    </Link>
                </div>
            </div>
        </nav>
    );
}
