import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

interface IntroSceneProps {
  title: string;
  period: string;
}

export const IntroScene: React.FC<IntroSceneProps> = ({ title, period }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo: scale up from 0.6 + fade in
  const logoScale = interpolate(frame, [0, 0.8 * fps], [0.6, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const logoOpacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Title: slide up + fade in, delayed
  const titleY = interpolate(frame, [0.4 * fps, 1.2 * fps], [40, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const titleOpacity = interpolate(frame, [0.4 * fps, 1 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Period: slide up + fade in, more delayed
  const periodY = interpolate(frame, [0.8 * fps, 1.5 * fps], [30, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const periodOpacity = interpolate(frame, [0.8 * fps, 1.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Accent line: width grows
  const lineWidth = interpolate(frame, [1 * fps, 1.8 * fps], [0, 120], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Exit fade (last 0.5s of the 3s scene)
  const exitOpacity = interpolate(
    frame,
    [2.5 * fps, 3 * fps],
    [1, 0],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity: exitOpacity,
      }}
    >
      {/* Radial glow behind logo */}
      <div
        style={{
          position: "absolute",
          width: 400,
          height: 400,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(30,58,122,0.25) 0%, transparent 70%)",
          opacity: logoOpacity,
        }}
      />

      {/* Logo */}
      <Img
        src={staticFile("tcn_logo.png")}
        style={{
          width: 140,
          height: "auto",
          transform: `scale(${logoScale})`,
          opacity: logoOpacity,
          filter: "drop-shadow(0 4px 20px rgba(30,58,122,0.4))",
        }}
      />

      {/* Title */}
      <div
        style={{
          marginTop: 28,
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
          fontFamily:
            "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
          fontSize: 52,
          fontWeight: 700,
          color: "#ffffff",
          letterSpacing: "-0.02em",
          textAlign: "center",
        }}
      >
        {title}
      </div>

      {/* Accent line */}
      <div
        style={{
          width: lineWidth,
          height: 3,
          background: "linear-gradient(90deg, #c81e28, #1e3a7a)",
          borderRadius: 2,
          marginTop: 16,
          opacity: titleOpacity,
        }}
      />

      {/* Period */}
      <div
        style={{
          marginTop: 20,
          transform: `translateY(${periodY}px)`,
          opacity: periodOpacity,
          fontFamily:
            "'SF Mono', 'JetBrains Mono', 'Cascadia Code', monospace",
          fontSize: 20,
          fontWeight: 400,
          color: "rgba(255,255,255,0.55)",
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        {period}
      </div>
    </AbsoluteFill>
  );
};
