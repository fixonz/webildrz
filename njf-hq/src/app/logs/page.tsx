"use client";

import React, { useState, useEffect, useRef } from "react";

const INITIAL_LOGS = [
    { time: "12:00:01", level: "SEC", msg: "KERNEL_INIT_SUCCESS: Checksum matches." },
    { time: "12:00:05", level: "INFO", msg: "ESTABLISHING_TLS_HANDSHAKE: Handshake with Node_SYDNEY." },
    { time: "12:00:10", level: "WARN", msg: "LATENCY_THRESHOLD_EXCEEDED: Reroute initiated." },
    { time: "12:00:15", level: "SEC", msg: "SSH_LOGIN_ATTEMPT: Rejected for user GUEST_402." },
];

const LOG_MESSAGES = [
    "DECENTRALIZED_PROTOCOL_SYNC_COMPLETE",
    "NEW_SMART_CONTRACT_DEPLOYED: ID_0x442F",
    "NEURAL_LINK_LATENCY: 12ms",
    "ENCRYPTION_LAYER_ROTATION: Successful",
    "THREAT_DETECTED_AND_QUARANTINED: EU_02",
    "PEER_DISCOVERY_PING: 42 nodes responsive",
    "BLOCKCHAIN_BLOCK_COMMIT: Height 420921",
];

export default function LogsPage() {
    const [logs, setLogs] = useState(INITIAL_LOGS);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const interval = setInterval(() => {
            const newLog = {
                time: new Date().toLocaleTimeString('en-GB', { hour12: false }),
                level: Math.random() > 0.8 ? "WARN" : Math.random() > 0.9 ? "SEC" : "INFO",
                msg: LOG_MESSAGES[Math.floor(Math.random() * LOG_MESSAGES.length)]
            };
            setLogs(prev => [...prev.slice(-49), newLog]);
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="min-h-screen bg-cyber-black pt-24 pb-12 px-6 flex flex-col items-center">
            <div className="max-w-4xl w-full">
                <header className="mb-8 flex justify-between items-center bg-white/5 p-4 border border-white/10 rounded-t-lg">
                    <div className="flex items-center gap-4">
                        <div className="w-3 h-3 bg-neon-blue rounded-full animate-pulse" />
                        <h1 className="text-xl font-bold text-white uppercase tracking-widest font-mono">
                            Terminal: System_Logs
                        </h1>
                    </div>
                    <span className="text-[10px] font-mono text-neon-blue/60 uppercase tracking-[0.4em]">
                        Connection: Secure_Uplink
                    </span>
                </header>

                <div
                    ref={scrollRef}
                    className="bg-black/80 border-x border-b border-white/10 p-6 h-[60vh] overflow-y-auto font-mono text-sm space-y-2 scrollbar-hide scanlines"
                >
                    {logs.map((log, i) => (
                        <div key={i} className="flex gap-4 group">
                            <span className="text-white/20 whitespace-nowrap">[{log.time}]</span>
                            <span className={`font-bold whitespace-nowrap ${log.level === 'SEC' ? 'text-neon-orange' :
                                    log.level === 'WARN' ? 'text-yellow-400' : 'text-neon-blue'
                                }`}>
                                [{log.level}]
                            </span>
                            <span className="text-white/80 group-hover:text-white transition-colors">
                                {log.msg}
                            </span>
                        </div>
                    ))}
                    <div className="flex gap-2 items-center text-neon-blue animate-pulse pt-4">
                        <span className="font-bold">&gt;</span>
                        <div className="w-2 h-4 bg-neon-blue" />
                    </div>
                </div>

                <footer className="mt-4 p-4 glass border-white/5 rounded-lg flex justify-between">
                    <div className="flex gap-8">
                        <div className="flex flex-col">
                            <span className="text-[8px] text-white/40 uppercase tracking-widest">Total Events</span>
                            <span className="text-white font-bold">{logs.length}</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-[8px] text-white/40 uppercase tracking-widest">Buffer Status</span>
                            <span className="text-neon-blue font-bold">OPTIMAL</span>
                        </div>
                    </div>
                    <button
                        onClick={() => setLogs(INITIAL_LOGS)}
                        className="text-[10px] uppercase font-bold text-neon-blue/60 hover:text-neon-blue transition-colors"
                    >
                        Clear_Buffer
                    </button>
                </footer>
            </div>
        </div>
    );
}
