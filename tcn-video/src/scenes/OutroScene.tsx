import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const scale = interpolate(frame, [0, 0.4 * fps], [0.9, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity,
      }}
    >
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <Img
          src={staticFile("tcn_logo.png")}
          style={{
            width: 80,
            height: "auto",
            filter: "drop-shadow(0 2px 12px rgba(30,58,122,0.3))",
          }}
        />
        <div
          style={{
            marginTop: 16,
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            fontSize: 20,
            fontWeight: 500,
            color: "rgba(255,255,255,0.4)",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
          }}
        >
          Transmission Company of Nigeria
        </div>
      </div>
    </AbsoluteFill>
  );
};
