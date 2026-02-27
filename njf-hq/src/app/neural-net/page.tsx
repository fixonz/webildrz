"use client";

import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { OrbitControls, Preload } from "@react-three/drei";
import { NeuralBrain } from "@/components/canvas/NeuralBrain";
import { EffectComposer, Bloom, Noise } from "@react-three/postprocessing";

export default function NeuralNetPage() {
    return (
        <div className="relative w-full h-screen bg-cyber-black overflow-hidden pt-24">
            <div className="absolute inset-0 z-0 opacity-20 bg-grid-cyber" />

            <div className="container mx-auto px-6 relative z-10 flex flex-col md:flex-row items-center h-full">
                <div className="w-full md:w-1/2 flex flex-col gap-6 text-left order-2 md:order-1">
                    <div className="inline-block px-3 py-1 bg-neon-blue/10 border border-neon-blue/40 rounded text-neon-blue font-mono text-xs uppercase tracking-[0.3em]">
                        Status: Core_Sentient_Online
                    </div>
                    <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-white uppercase italic">
                        NEURAL <span className="text-neon-blue">SYNAPSE</span>
                    </h1>
                    <p className="max-w-md text-white/50 text-lg font-light leading-relaxed">
                        The sentient core of MCP-2099. Interact with the neural cluster to
                        visualize data flows and cross-chain synaptic firings in real-time.
                    </p>

                    <div className="grid grid-cols-2 gap-4 mt-8">
                        <div className="p-4 glass border-white/5 flex flex-col gap-1">
                            <span className="text-[10px] text-neon-blue uppercase font-mono tracking-widest">Active Neurons</span>
                            <span className="text-2xl font-bold text-white tracking-tighter">1,204,921</span>
                        </div>
                        <div className="p-4 glass border-white/5 flex flex-col gap-1">
                            <span className="text-[10px] text-neon-orange uppercase font-mono tracking-widest">Throughput</span>
                            <span className="text-2xl font-bold text-white tracking-tighter">42.8 GB/s</span>
                        </div>
                    </div>
                </div>

                <div className="w-full md:w-1/2 h-[50vh] md:h-full order-1 md:order-2">
                    <Canvas camera={{ position: [0, 0, 8], fov: 45 }}>
                        <ambientLight intensity={0.5} />
                        <pointLight position={[10, 10, 10]} intensity={1} color="#00f3ff" />

                        <Suspense fallback={null}>
                            <NeuralBrain />

                            <EffectComposer multisampling={0}>
                                <Bloom luminanceThreshold={0.5} intensity={2} radius={0.4} />
                                <Noise opacity={0.05} />
                            </EffectComposer>
                        </Suspense>

                        <OrbitControls enableZoom={false} enablePan={false} />
                        <Preload all />
                    </Canvas>
                </div>
            </div>

            {/* Decorative Overlays */}
            <div className="absolute top-1/4 right-12 w-32 h-64 border-r border-t border-white/10 hidden xl:block" />
            <div className="absolute bottom-1/4 left-12 w-32 h-64 border-l border-b border-white/10 hidden xl:block" />
        </div>
    );
}
