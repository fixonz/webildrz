"use client";

import React from "react";
import { Terminal, Github, Twitter, MessageSquare } from "lucide-react";

export function Footer() {
    return (
        <footer className="bg-cyber-black border-t border-white/5 py-20 px-6">
            <div className="max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-20">
                    <div className="md:col-span-2">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-10 h-10 bg-neon-blue/10 rounded flex items-center justify-center border border-neon-blue/40">
                                <Terminal className="w-5 h-5 text-neon-blue" />
                            </div>
                            <span className="text-white font-black tracking-tighter text-2xl uppercase italic">MCP-2099</span>
                        </div>
                        <p className="text-white/40 max-w-sm text-sm leading-relaxed mb-8">
                            The next generation of developer infrastructure. Built for the era of
                            sentient networks, post-quantum security, and decentralized protocols.
                            Engineering, supercharged.
                        </p>
                        <div className="flex gap-4">
                            {[Github, Twitter, MessageSquare].map((Icon, i) => (
                                <a
                                    key={i}
                                    href="#"
                                    className="w-10 h-10 glass border-white/10 rounded flex items-center justify-center text-white/60 hover:text-neon-blue hover:border-neon-blue/40 transition-all duration-300"
                                >
                                    <Icon className="w-4 h-4" />
                                </a>
                            ))}
                        </div>
                    </div>

                    <div>
                        <h4 className="text-white font-bold uppercase tracking-widest text-xs mb-6 font-mono">Platform</h4>
                        <ul className="space-y-4 text-sm text-white/40 uppercase font-mono text-[10px] tracking-widest">
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Interface</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Neural Net</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Runtime</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Security</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="text-white font-bold uppercase tracking-widest text-xs mb-6 font-mono">Resources</h4>
                        <ul className="space-y-4 text-sm text-white/40 uppercase font-mono text-[10px] tracking-widest">
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Documentation</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">API Reference</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Changelog</a></li>
                            <li><a href="#" className="hover:text-neon-blue transition-colors">Support</a></li>
                        </ul>
                    </div>
                </div>

                <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <span className="text-[10px] font-mono text-white/20 uppercase tracking-[0.3em]">
                        © 2099 MCP-2099_DEFENSE_CORP // ALL_RIGHTS_RESERVED
                    </span>
                    <div className="flex gap-8 text-[10px] font-mono text-white/20 uppercase tracking-widest">
                        <a href="#" className="hover:text-white transition-colors">Privacy_Protocol</a>
                        <a href="#" className="hover:text-white transition-colors">Terms_Of_Service</a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
