"use client";

import { useRef, useMemo, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { shaderMaterial } from "@react-three/drei";
import { extend } from "@react-three/fiber";

const BrainMaterial = shaderMaterial(
    {
        time: 0,
        color: new THREE.Color("#00f3ff"),
    },
    // Vertex Shader
    `
  uniform float time;
  varying vec2 vUv;
  varying float vNoise;

  // Simple 3D Noise function (Simplex-ish)
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

  float snoise(vec3 v) {
    const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
    const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);

    vec3 i  = floor(v + dot(v, C.yyy) );
    vec3 x0 =   v - i + dot(i, C.xxx) ;

    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min( g.xyz, l.zxy );
    vec3 i2 = max( g.xyz, l.zxy );

    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;

    i = mod289(i);
    vec4 p = permute( permute( permute(
               i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
             + i.y + vec4(0.0, i1.y, i2.y, 1.0 ))
             + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));

    float n_ = 0.142857142857;
    vec3  ns = n_ * D.wyz - D.xzx;

    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);

    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_ );

    vec4 x = x_ *ns.x + ns.yyyy;
    vec4 y = y_ *ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);

    vec4 b0 = vec4( x.xy, y.xy );
    vec4 b1 = vec4( x.zw, y.zw );

    vec4 s0 = floor(b0)*2.0 + 1.0;
    vec4 s1 = floor(b1)*2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));

    vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
    vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;

    vec3 p0 = vec3(a0.xy,h.x);
    vec3 p1 = vec3(a0.zw,h.y);
    vec3 p2 = vec3(a1.xy,h.z);
    vec3 p3 = vec3(a1.zw,h.w);

    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
    p0 *= norm.x;
    p1 *= norm.y;
    p2 *= norm.z;
    p3 *= norm.w;

    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1),
                                  dot(p2,x2), dot(p3,x3) ) );
  }

  void main() {
    vUv = uv;
    float noise = snoise(position * 2.0 + time * 0.5);
    vNoise = noise;
    
    vec3 pos = position + normal * noise * 0.3;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
  `,
    // Fragment Shader
    `
  uniform float time;
  uniform vec3 color;
  varying vec2 vUv;
  varying float vNoise;

  void main() {
    // Branching vein effect
    float vein = sin(vUv.x * 20.0 + vNoise * 10.0 + time) * 
                 sin(vUv.y * 20.0 + vNoise * 10.0 + time);
    vein = smoothstep(0.45, 0.5, vein);
    
    vec3 finalColor = mix(vec3(0.01), color, vein + (vNoise + 1.0) * 0.5);
    gl_FragColor = vec4(finalColor, 0.8);
  }
  `
);

extend({ BrainMaterial });

const PARTICLE_COUNT = 400;

export function NeuralBrain() {
    const meshRef = useRef<THREE.Mesh>(null);
    const particlesRef = useRef<THREE.Points>(null);
    const [hovered, setHovered] = useState(false);

    // Initialize particles
    const particles = useMemo(() => {
        const temp = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(Math.random() * 2 - 1);
            const radius = 2.5 + Math.random() * 0.5;

            temp.push({
                position: new THREE.Vector3(
                    radius * Math.sin(phi) * Math.cos(theta),
                    radius * Math.sin(phi) * Math.sin(theta),
                    radius * Math.cos(phi)
                ),
                velocity: new THREE.Vector3(
                    (Math.random() - 0.5) * 0.01,
                    (Math.random() - 0.5) * 0.01,
                    (Math.random() - 0.5) * 0.01
                ),
                intensity: 0
            });
        }
        return temp;
    }, []);

    const particlePositions = useMemo(() => new Float32Array(PARTICLE_COUNT * 3), []);
    const particleColors = useMemo(() => new Float32Array(PARTICLE_COUNT * 3), []);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (meshRef.current) {
            (meshRef.current.material as any).time = time;
            meshRef.current.rotation.y = time * 0.2;
        }

        if (particlesRef.current) {
            particles.forEach((p, i) => {
                // Orbit logic
                p.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), 0.005);
                p.position.applyAxisAngle(new THREE.Vector3(1, 0, 0), 0.002);

                // Repulsion logic
                particles.forEach((p2, j) => {
                    if (i === j) return;
                    const dist = p.position.distanceTo(p2.position);
                    if (dist < 0.2) {
                        const force = p.position.clone().sub(p2.position).normalize().multiplyScalar(0.001);
                        p.velocity.add(force);
                    }
                });

                // Dampen velocity
                p.velocity.multiplyScalar(0.95);
                p.position.add(p.velocity);

                // Constraint to shell
                const d = p.position.length();
                if (d < 2.5) p.position.multiplyScalar(2.5 / d);
                if (d > 3.5) p.position.multiplyScalar(3.5 / d);

                // Colors/Intensity
                if (hovered) {
                    p.intensity = THREE.MathUtils.lerp(p.intensity, 1, 0.1);
                } else {
                    p.intensity = THREE.MathUtils.lerp(p.intensity, 0, 0.05);
                }

                const baseColor = new THREE.Color("#00f3ff");
                const burstColor = new THREE.Color("#ff4d00");
                const finalColor = baseColor.clone().lerp(burstColor, p.intensity);

                particlePositions[i * 3] = p.position.x;
                particlePositions[i * 3 + 1] = p.position.y;
                particlePositions[i * 3 + 2] = p.position.z;

                particleColors[i * 3] = finalColor.r;
                particleColors[i * 3 + 1] = finalColor.g;
                particleColors[i * 3 + 2] = finalColor.b;
            });

            particlesRef.current.geometry.attributes.position.needsUpdate = true;
            particlesRef.current.geometry.attributes.color.needsUpdate = true;
        }
    });

    return (
        <group
            onPointerOver={() => setHovered(true)}
            onPointerOut={() => setHovered(false)}
        >
            <mesh ref={meshRef}>
                <sphereGeometry args={[2, 128, 128]} />
                {/* @ts-ignore */}
                <brainMaterial transparent />
            </mesh>

            <points ref={particlesRef}>
                <bufferGeometry>
                    <bufferAttribute
                        attach="attributes-position"
                        args={[particlePositions, 3]}
                        usage={THREE.DynamicDrawUsage}
                    />
                    <bufferAttribute
                        attach="attributes-color"
                        args={[particleColors, 3]}
                        usage={THREE.DynamicDrawUsage}
                    />
                </bufferGeometry>
                <pointsMaterial
                    size={0.08}
                    vertexColors
                    transparent
                    opacity={0.8}
                    blending={THREE.AdditiveBlending}
                />
            </points>

            <mesh scale={[1.1, 1.1, 1.1]}>
                <sphereGeometry args={[2, 64, 64]} />
                <meshBasicMaterial color="#00f3ff" wireframe transparent opacity={0.1} />
            </mesh>
        </group>
    );
}
