"use client";

import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { Preload, OrbitControls, Environment } from "@react-three/drei";
import { EffectComposer, Bloom, Noise, ChromaticAberration, Vignette } from "@react-three/postprocessing";
import { Vector2 } from "three";
import { DataGlobe } from "./DataGlobe";

export default function Scene() {
    return (
        <div className="absolute inset-0 -z-10 bg-cyber-black">
            <Canvas
                shadows
                dpr={typeof window !== 'undefined' ? Math.min(window.devicePixelRatio, 2) : 1}
                camera={{ position: [0, 0, 8], fov: 45 }}
                gl={{
                    antialias: false,
                    alpha: true,
                    powerPreference: "high-performance",
                }}
            >
                <color attach="background" args={["#050505"]} />
                <fog attach="fog" args={["#050505", 5, 20]} />

                <ambientLight intensity={0.1} />
                <pointLight position={[10, 10, 10]} intensity={1.5} color="#00f3ff" />
                <pointLight position={[-10, -10, -10]} intensity={1} color="#ff4d00" />

                <Suspense fallback={null}>
                    <DataGlobe />

                    <EffectComposer multisampling={0}>
                        <Bloom
                            luminanceThreshold={0.2}
                            mipmapBlur
                            intensity={1.5}
                            radius={0.4}
                        />
                        <Noise opacity={0.05} />
                        <ChromaticAberration
                            offset={new Vector2(0.001, 0.001)}
                        />
                        <Vignette eskil={false} offset={0.1} darkness={1.1} />
                    </EffectComposer>
                </Suspense>

                <Preload all />
            </Canvas>
        </div>
    );
}

