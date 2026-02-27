"use client";

import React, { useEffect, useRef } from "react";
import gsap from "gsap";
import { NodeMap } from "@/components/dashboard/NodeMap";
import {
    BarChart3,
    ShieldAlert,
    Activity,
    Cpu,
    Database,
    Globe,
    Lock
} from "lucide-react";

export default function DashboardPage() {
    const gridRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const ctx = gsap.context(() => {
            gsap.from(".bento-item", {
                scale: 0.9,
                opacity: 0,
                y: 20,
                duration: 0.8,
                stagger: 0.1,
                ease: "power2.out",
            });
        }, gridRef);

        return () => ctx.revert();
    }, []);

    return (
        <div className="min-h-screen bg-cyber-black pt-24 pb-12 px-6">
            <div className="max-w-7xl mx-auto">
                <header className="mb-10 flex justify-between items-end">
                    <div>
                        <h1 className="text-4xl font-black text-white uppercase italic tracking-tighter">
                            Mission <span className="text-neon-orange">Control</span>
                        </h1>
                        <p className="text-white/40 font-mono text-xs uppercase tracking-[0.3em] mt-2">
                            System_Runtime: 1,402 hrs // User: ADMIN_01
                        </p>
                    </div>
                    <div className="hidden md:flex gap-4">
                        <div className="flex flex-col items-end">
                            <span className="text-[10px] text-white/30 uppercase font-mono tracking-widest">Network Load</span>
                            <div className="h-1 w-32 bg-white/5 mt-1 overflow-hidden">
                                <div className="h-full bg-neon-orange w-[65%] animate-pulse" />
                            </div>
                        </div>
                        <div className="flex flex-col items-end">
                            <span className="text-[10px] text-white/30 uppercase font-mono tracking-widest">Core Temp</span>
                            <div className="h-1 w-32 bg-white/5 mt-1 overflow-hidden">
                                <div className="h-full bg-neon-blue w-[42%]" />
                            </div>
                        </div>
                    </div>
                </header>

                <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-4 grid-rows-auto gap-4">
                    {/* Main Map - Large Bento Item */}
                    <div className="bento-item md:col-span-3 md:row-span-2 glass border-white/5 p-6 flex flex-col gap-4">
                        <div className="flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <Globe className="w-4 h-4 text-neon-blue" />
                                <span className="text-xs font-bold text-white uppercase tracking-widest">Global Node Network</span>
                            </div>
                            <span className="text-[10px] font-mono text-neon-blue animate-pulse">LIVE_SYNC</span>
                        </div>
                        <NodeMap />
                    </div>

                    {/* Security Status */}
                    <div className="bento-item glass border-white/5 p-6 flex flex-col gap-4">
                        <div className="flex items-center gap-2">
                            <Lock className="w-4 h-4 text-neon-orange" />
                            <span className="text-xs font-bold text-white uppercase tracking-widest">Security Protocol</span>
                        </div>
                        <div className="flex-1 flex flex-col justify-center items-center gap-4">
                            <div className="relative w-24 h-24 flex items-center justify-center">
                                <svg className="w-full h-full transform -rotate-90">
                                    <circle
                                        cx="48" cy="48" r="40"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                        fill="transparent"
                                        className="text-white/5"
                                    />
                                    <circle
                                        cx="48" cy="48" r="40"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                        fill="transparent"
                                        strokeDasharray="251.2"
                                        strokeDashoffset="62.8"
                                        className="text-neon-orange"
                                    />
                                </svg>
                                <span className="absolute text-xl font-bold text-white">75%</span>
                            </div>
                            <span className="text-[10px] font-mono text-white/40 uppercase">Encrypted_Layer_V3</span>
                        </div>
                    </div>

                    {/* Metrics 1 */}
                    <div className="bento-item glass border-white/5 p-6 flex flex-col gap-4">
                        <div className="flex items-center gap-2">
                            <Cpu className="w-4 h-4 text-neon-blue" />
                            <span className="text-xs font-bold text-white uppercase tracking-widest">CPU Allocation</span>
                        </div>
                        <div className="space-y-4">
                            {[
                                { label: "Kernel", val: "22%" },
                                { label: "Neural", val: "58%" },
                                { label: "Network", val: "14%" },
                            ].map(m => (
                                <div key={m.label} className="space-y-1">
                                    <div className="flex justify-between text-[10px] font-mono text-white/50 uppercase">
                                        <span>{m.label}</span>
                                        <span>{m.val}</span>
                                    </div>
                                    <div className="h-1 w-full bg-white/5">
                                        <div className="h-full bg-neon-blue transition-all" style={{ width: m.val }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Activity Feed */}
                    <div className="bento-item md:col-span-2 glass border-white/5 p-6 flex flex-col gap-4">
                        <div className="flex items-center gap-2">
                            <Activity className="w-4 h-4 text-neon-blue" />
                            <span className="text-xs font-bold text-white uppercase tracking-widest">System Events</span>
                        </div>
                        <div className="space-y-2 font-mono text-[9px] uppercase overflow-hidden">
                            <div className="flex gap-4 text-neon-blue">
                                <span>[12:35:01]</span>
                                <span>INFO</span>
                                <span className="text-white/60">Decentralized link established via Node_42</span>
                            </div>
                            <div className="flex gap-4 text-neon-orange">
                                <span>[12:35:04]</span>
                                <span>WARN</span>
                                <span className="text-white/60">Unknown handshake attempt at EU_WEST_02</span>
                            </div>
                            <div className="flex gap-4 text-neon-blue">
                                <span>[12:35:10]</span>
                                <span>INFO</span>
                                <span className="text-white/60">Protocol 442 re-initialization complete</span>
                            </div>
                        </div>
                    </div>

                    {/* Threat Counter */}
                    <div className="bento-item glass border-white/5 p-6 flex flex-col gap-4 border-l-neon-orange/20">
                        <div className="flex items-center gap-2">
                            <ShieldAlert className="w-4 h-4 text-neon-orange" />
                            <span className="text-xs font-bold text-white uppercase tracking-widest">Active Threats</span>
                        </div>
                        <div className="text-5xl font-black text-white tracking-tighter text-center py-2">
                            0 <span className="text-xs text-neon-orange/40 font-mono tracking-widest">DETECTIONS</span>
                        </div>
                        <div className="mt-auto p-2 bg-neon-orange/5 border border-neon-orange/20 rounded text-center">
                            <span className="text-[8px] font-bold text-neon-orange uppercase tracking-[0.2em]">All Systems Nominal</span>
                        </div>
                    </div>

                    {/* DB Status */}
                    <div className="bento-item glass border-white/5 p-6 flex flex-col gap-4">
                        <div className="flex items-center gap-2">
                            <Database className="w-4 h-4 text-neon-blue" />
                            <span className="text-xs font-bold text-white uppercase tracking-widest">Neural Database</span>
                        </div>
                        <div className="flex-1 flex flex-col justify-end">
                            <div className="flex items-baseline gap-2">
                                <span className="text-3xl font-bold text-white">4.2</span>
                                <span className="text-xs text-white/30 uppercase font-mono">Petabytes Indexed</span>
                            </div>
                            <div className="h-12 flex items-end gap-[2px] mt-4">
                                {[...Array(20)].map((_, i) => (
                                    <div
                                        key={i}
                                        className="flex-1 bg-neon-blue/20 hover:bg-neon-blue transition-colors cursor-help"
                                        style={{ height: `${Math.random() * 100}%` }}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
