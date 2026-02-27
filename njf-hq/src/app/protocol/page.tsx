"use client";

import React from "react";
import { Shield, Lock, Cpu, Globe, Zap, Hash } from "lucide-react";

const PROTOCOLS = [
    {
        title: "Encryption Layer V3",
        icon: Shield,
        desc: "Post-quantum cryptographic standards applied to all neural link transmissions.",
        status: "ENFORCED",
        color: "text-neon-blue",
        bg: "bg-neon-blue/5",
        border: "border-neon-blue/20"
    },
    {
        title: "Sentient Core Auth",
        icon: Lock,
        desc: "Neural-biometric verification for administrative kernel access.",
        status: "ACTIVE",
        color: "text-neon-orange",
        bg: "bg-neon-orange/5",
        border: "border-neon-orange/20"
    },
    {
        title: "Decentralized Mesh",
        icon: Globe,
        desc: "Self-healing network architecture across 40+ global availability zones.",
        status: "SYNCED",
        color: "text-neon-blue",
        bg: "bg-neon-blue/5",
        border: "border-neon-blue/20"
    },
    {
        title: "Smart Contract V4",
        icon: Hash,
        desc: "Autonomous execution of joint-force protocol agreements on-chain.",
        status: "VERIFIED",
        color: "text-white",
        bg: "bg-white/5",
        border: "border-white/20"
    }
];

export default function ProtocolPage() {
    return (
        <div className="min-h-screen bg-cyber-black pt-24 pb-12 px-6">
            <div className="max-w-6xl mx-auto">
                <header className="mb-16 text-center">
                    <h1 className="text-5xl md:text-7xl font-black text-white uppercase italic tracking-tighter">
                        System <span className="text-neon-blue">Protocols</span>
                    </h1>
                    <p className="mt-4 text-white/40 font-mono text-sm uppercase tracking-[0.4em]">
                        Establish_Authority // Secure_Operations // Version_2099.04
                    </p>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {PROTOCOLS.map((protocol, i) => (
                        <div
                            key={i}
                            className={`p-8 glass ${protocol.border} border-l-4 group hover:bg-white/5 transition-all duration-500`}
                        >
                            <div className="flex justify-between items-start mb-6">
                                <div className={`p-3 rounded ${protocol.bg} ${protocol.color}`}>
                                    <protocol.icon className="w-6 h-6" />
                                </div>
                                <span className={`font-mono text-[10px] px-2 py-1 rounded border ${protocol.border} ${protocol.color}`}>
                                    {protocol.status}
                                </span>
                            </div>

                            <h3 className="text-2xl font-bold text-white mb-4 uppercase tracking-tighter italic">
                                {protocol.title}
                            </h3>
                            <p className="text-white/50 text-base leading-relaxed mb-8">
                                {protocol.desc}
                            </p>

                            <div className="flex items-center gap-4 text-[10px] font-mono text-white/20 uppercase tracking-widest">
                                <span>Ref: PROC_00{i + 1}</span>
                                <div className="h-[1px] flex-1 bg-white/5" />
                                <button className="text-neon-blue/60 hover:text-neon-blue transition-colors">
                                    VIEW_DOCS
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-16 p-8 border border-white/5 bg-gradient-to-r from-neon-blue/5 to-transparent rounded-xl flex flex-col md:flex-row items-center gap-8">
                    <div className="flex-1">
                        <h2 className="text-2xl font-bold text-white uppercase italic tracking-tighter mb-2">
                            Neural Integrity Check
                        </h2>
                        <p className="text-white/40 text-sm">
                            All protocols are subjected to real-time verification by the MCP-2099 sentient core.
                        </p>
                    </div>
                    <button className="px-8 py-3 bg-neon-blue text-black font-bold uppercase tracking-widest hover:scale-105 transition-transform flex items-center gap-2">
                        <Zap className="w-4 h-4 fill-current" />
                        Validate Integrity
                    </button>
                </div>
            </div>
        </div>
    );
}
