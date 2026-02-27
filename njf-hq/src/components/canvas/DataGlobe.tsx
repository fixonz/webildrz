"use client";

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { shaderMaterial, Points } from "@react-three/drei";
import { extend } from "@react-three/fiber";

const GlobeMaterial = shaderMaterial(
    {
        time: 0,
        color: new THREE.Color("#00f3ff"),
    },
    // Vertex Shader
    `
  uniform float time;
  varying vec2 vUv;
  varying float vElevation;

  // Simple noise function
  float hash(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);
    return fract(p.x * p.y);
  }

  void main() {
    vUv = uv;
    
    vec4 modelPosition = modelMatrix * vec4(position, 1.0);
    
    // Breathing displacement
    float elevation = sin(modelPosition.x * 2.0 + time) * 
                      sin(modelPosition.z * 2.0 + time) * 
                      0.15;
    
    modelPosition.xyz += normal * elevation;
    vElevation = elevation;

    gl_Position = projectionMatrix * viewMatrix * modelPosition;
  }
  `,
    // Fragment Shader
    `
  uniform float time;
  uniform vec3 color;
  varying vec2 vUv;
  varying float vElevation;

  void main() {
    // Scanline interference
    float scanline = sin(vUv.y * 200.0 + time * 10.0) * 0.1;
    
    // Glow based on elevation
    float glow = (vElevation + 0.15) * 2.0;
    
    vec3 finalColor = color * (0.6 + glow + scanline);
    
    // Grid effect
    float grid = sin(vUv.x * 100.0) * sin(vUv.y * 100.0);
    grid = step(0.9, grid);
    
    finalColor += color * grid * 0.5;

    gl_FragColor = vec4(finalColor, 0.4 + grid * 0.3);
  }
  `
);

extend({ GlobeMaterial });

export function DataGlobe() {
    const globeRef = useRef<THREE.Mesh>(null);
    const starsRef = useRef<THREE.Points>(null);

    const starPositions = useMemo(() => {
        const pos = new Float32Array(3000 * 3);
        for (let i = 0; i < 3000; i++) {
            pos[i * 3] = (Math.random() - 0.5) * 50;
            pos[i * 3 + 1] = (Math.random() - 0.5) * 50;
            pos[i * 3 + 2] = (Math.random() - 0.5) * 50;
        }
        return pos;
    }, []);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (globeRef.current) {
            (globeRef.current.material as any).time = time;
            globeRef.current.rotation.y = time * 0.1;
        }
        if (starsRef.current) {
            starsRef.current.rotation.y = time * 0.05 * -1; // Parallax effect
        }
    });

    return (
        <>
            <mesh ref={globeRef}>
                <sphereGeometry args={[2.5, 64, 64]} />
                {/* @ts-ignore */}
                <globeMaterial transparent side={THREE.DoubleSide} />
            </mesh>

            <points ref={starsRef}>
                <bufferGeometry>
                    <bufferAttribute
                        attach="attributes-position"
                        args={[starPositions, 3]}
                    />
                </bufferGeometry>
                <pointsMaterial
                    size={0.02}
                    color="#ffffff"
                    transparent
                    opacity={0.5}
                    sizeAttenuation={true}
                />
            </points>

            {/* Internal Core Glow */}
            <mesh>
                <sphereGeometry args={[2.2, 32, 32]} />
                <meshBasicMaterial color="#00f3ff" transparent opacity={0.05} />
            </mesh>
        </>
    );
}
