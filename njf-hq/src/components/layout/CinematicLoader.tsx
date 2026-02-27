"use client";

import React, { useEffect, useState, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { shaderMaterial } from "@react-three/drei";
import * as THREE from "three";
import { extend } from "@react-three/fiber";
import gsap from "gsap";

const RingMaterial = shaderMaterial(
    {
        time: 0,
        color: new THREE.Color("#00f3ff"),
    },
    // Vertex Shader
    `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
  `,
    // Fragment Shader
    `
  uniform float time;
  uniform vec3 color;
  varying vec2 vUv;
  void main() {
    vec2 uv = vUv - 0.5;
    float dist = length(uv);
    float ring = smoothstep(0.38, 0.4, dist) - smoothstep(0.42, 0.44, dist);
    
    // Scrambled artifacts
    float angle = atan(uv.y, uv.x);
    float static_noise = fract(sin(dot(vec2(angle, time * 0.001), vec2(12.9898, 78.233))) * 43758.5453);
    if (static_noise > 0.95) ring *= 1.5;
    
    float pulse = sin(time * 3.0) * 0.2 + 0.8;
    float finalAlpha = ring * pulse;
    
    gl_FragColor = vec4(color, finalAlpha);
  }
  `
);

extend({ RingMaterial });

function HolographicRing() {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (meshRef.current) {
            (meshRef.current.material as any).time = state.clock.getElapsedTime();
            meshRef.current.rotation.z += 0.01;
        }
    });

    return (
        <mesh ref={meshRef}>
            <planeGeometry args={[5, 5]} />
            {/* @ts-ignore */}
            <ringMaterial transparent depthWrite={false} blending={THREE.AdditiveBlending} />
        </mesh>
    );
}

const SCRAMBLED_CHARS = "ABCDEFGHIKLMNOPQRSTVXYZ0123456789@#$%&*";

export const CinematicLoader = ({ onComplete }: { onComplete: () => void }) => {
    const [text, setText] = useState("INITIALIZING_KERNEL");
    const [mounted, setMounted] = useState(true);
    const containerRef = useRef<HTMLDivElement>(null);
    const textRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const sequence = [
            "LOADING_ASSETS",
            "DECRYPTING_PROTOCOLS",
            "ESTABLISHING_NEURAL_LINK",
            "SYSTEM_READY"
        ];

        let currentStep = 0;

        const interval = setInterval(() => {
            if (currentStep < sequence.length) {
                const targetText = sequence[currentStep];
                let iteration = 0;

                const scrambleInterval = setInterval(() => {
                    setText(prev =>
                        targetText.split("").map((char, index) => {
                            if (index < iteration) return char;
                            return SCRAMBLED_CHARS[Math.floor(Math.random() * SCRAMBLED_CHARS.length)];
                        }).join("")
                    );

                    iteration += 1 / 3;
                    if (iteration >= targetText.length) {
                        clearInterval(scrambleInterval);
                        currentStep++;
                        if (currentStep === sequence.length) {
                            setTimeout(() => {
                                gsap.to(containerRef.current, {
                                    opacity: 0,
                                    duration: 1,
                                    ease: "power2.inOut",
                                    onComplete: () => {
                                        setMounted(false);
                                        onComplete();
                                    }
                                });
                            }, 1000);
                        }
                    }
                }, 30);
            } else {
                clearInterval(interval);
            }
        }, 2000);

        return () => clearInterval(interval);
    }, [onComplete]);

    if (!mounted) return null;

    return (
        <div
            ref={containerRef}
            className="fixed inset-0 z-[9999] bg-cyber-black flex flex-col items-center justify-center overflow-hidden"
        >
            <div className="absolute inset-0 opacity-20 bg-grid-cyber" />

            <div className="relative w-96 h-96">
                <Canvas camera={{ position: [0, 0, 5] }}>
                    <HolographicRing />
                </Canvas>
            </div>

            <div
                ref={textRef}
                className="mt-8 font-mono text-neon-blue tracking-widest text-lg hologram-text flex items-center gap-4"
            >
                <span className="w-2 h-2 bg-neon-blue animate-pulse" />
                {text}
            </div>

            <div className="absolute bottom-12 left-12 font-mono text-xs text-neon-blue/40 uppercase tracking-[0.3em]">
                MCP-2099 // CORE_OS.V1
            </div>
        </div>
    );
};
