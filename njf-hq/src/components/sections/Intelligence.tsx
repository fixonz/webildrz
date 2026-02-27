"use client";

import { motion } from "framer-motion";
import { Cpu, Globe, Zap, Terminal, ShieldAlert, Radio } from "lucide-react";

const items = [
    {
        title: "Tactical Awareness",
        desc: "Real-time orbital tracking and neural-linked surveillance feeds.",
        icon: Globe,
        color: "neon-cyan",
        className: "md:col-span-2 md:row-span-2",
    },
    {
        title: "Neural Core",
        desc: "Sentient AI for rapid threat detection.",
        icon: Cpu,
        color: "neon-magenta",
        className: "md:col-span-1 md:row-span-1",
    },
    {
        title: "Rapid Deploy",
        desc: "Sub-light response protocols.",
        icon: Zap,
        color: "neon-violet",
        className: "md:col-span-1 md:row-span-1",
    },
    {
        title: "Encryption",
        desc: "Post-quantum secure communication layers.",
        icon: Terminal,
        color: "neon-cyan",
        className: "md:col-span-1 md:row-span-2",
    },
    {
        title: "Cyber Shield",
        desc: "Advanced firewall against cognitive influence.",
        icon: ShieldAlert,
        color: "neon-magenta",
        className: "md:col-span-1 md:row-span-1",
    },
    {
        title: "Frequency",
        desc: "Secure broadcast across all dimensions.",
        icon: Radio,
        color: "neon-violet",
        className: "md:col-span-1 md:row-span-1",
    },
];

export function Intelligence() {
    return (
        <section id="intel" className="py-24 relative overflow-hidden bg-grid">
            <div className="container mx-auto px-6">
                <div className="mb-16">
                    <h2 className="text-4xl md:text-6xl font-black uppercase text-white tracking-tighter">
                        Intelligence <span className="text-neon-magenta">Hub</span>
                    </h2>
                    <div className="h-1 w-24 bg-neon-magenta mt-4" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 auto-rows-[200px]">
                    {items.map((item, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.1 }}
                            className={`glass p-8 group relative overflow-hidden rounded-2xl flex flex-col justify-between ${item.className}`}
                        >
                            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                            <div className="relative z-10">
                                <item.icon className={`w-10 h-10 mb-6 text-${item.color}`} />
                                <h3 className="text-2xl font-bold text-white mb-2 uppercase tracking-tighter">{item.title}</h3>
                                <p className="text-muted-foreground text-sm uppercase tracking-widest">{item.desc}</p>
                            </div>

                            <div className={`h-1 w-0 group-hover:w-full transition-all duration-500 bg-${item.color}`} />
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
