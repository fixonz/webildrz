"use client";

import React from "react";

export const NodeMap = () => {
    return (
        <div className="relative w-full h-full min-h-[300px] bg-cyber-black/50 rounded-lg overflow-hidden border border-white/5 flex items-center justify-center">
            <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#00f3ff_1px,transparent_1px)] [background-size:20px_20px]" />

            <svg viewBox="0 0 800 400" className="w-full h-full opacity-60">
                {/* Simple stylized world map dots */}
                <g fill="currentColor" className="text-neon-blue/30">
                    {[...Array(50)].map((_, i) => (
                        <circle
                            key={i}
                            cx={Math.random() * 800}
                            cy={Math.random() * 400}
                            r={1 + Math.random() * 2}
                            className="animate-pulse"
                            style={{ animationDelay: `${Math.random() * 2}s` }}
                        />
                    ))}
                </g>

                {/* Active Nodes */}
                <g>
                    {[
                        { x: 200, y: 150, label: "NA_EAST_01" },
                        { x: 450, y: 120, label: "EU_WEST_04" },
                        { x: 600, y: 250, label: "ASIA_SOUTH_02" },
                        { x: 350, y: 300, label: "LATAM_01" },
                    ].map((node, i) => (
                        <g key={i}>
                            <circle cx={node.x} cy={node.y} r="4" className="fill-neon-blue animate-ping opacity-75" />
                            <circle cx={node.x} cy={node.y} r="3" className="fill-neon-blue" />
                            <text
                                x={node.x + 10}
                                y={node.y + 15}
                                className="fill-neon-blue font-mono text-[8px] tracking-widest uppercase"
                            >
                                {node.label}
                            </text>
                            {/* Connection lines to a central hub or between them */}
                            <line
                                x1={400} y1={200} x2={node.x} y2={node.y}
                                stroke="currentColor"
                                className="text-neon-blue/20"
                                strokeWidth="0.5"
                                strokeDasharray="4 4"
                            />
                        </g>
                    ))}
                </g>
            </svg>

            <div className="absolute top-4 left-4 font-mono text-[10px] text-neon-blue/60 uppercase tracking-widest">
                Satellite_Uplink: Active
            </div>
        </div>
    );
};
