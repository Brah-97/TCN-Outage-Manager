import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { MetricItem } from "../types";

interface MetricsSceneProps {
  metrics: MetricItem[];
}

const MetricCard: React.FC<{
  item: MetricItem;
  index: number;
}> = ({ item, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 4; // 4 frames stagger (~130ms at 30fps)

  // Card slides up + fades in
  const y = interpolate(frame, [delay, delay + 0.6 * fps], [50, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const opacity = interpolate(frame, [delay, delay + 0.4 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Counter animation: parse numeric part and animate from 0
  const numMatch = item.value.match(/[\d,.]+/);
  const numericValue = numMatch ? parseFloat(numMatch[0].replace(/,/g, "")) : 0;
  const suffix = item.value.replace(/[\d,.]+/, "").trim();
  const prefix = item.value.indexOf(numMatch?.[0] || "") > 0
    ? item.value.substring(0, item.value.indexOf(numMatch?.[0] || ""))
    : "";

  const counterProgress = interpolate(
    frame,
    [delay + 0.2 * fps, delay + 1.2 * fps],
    [0, 1],
    {
      extrapolateRight: "clamp",
      extrapolateLeft: "clamp",
      easing: Easing.bezier(0.16, 1, 0.3, 1),
    },
  );
  const currentNum = numericValue * counterProgress;

  // Format number with commas + matching decimal places
  const decimalMatch = numMatch?.[0].match(/\.(\d+)/);
  const decimals = decimalMatch ? decimalMatch[1].length : 0;
  const formatted =
    prefix +
    currentNum.toLocaleString("en-US", {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }) +
    (suffix ? " " + suffix : "");

  return (
    <div
      style={{
        transform: `translateY(${y}px)`,
        opacity,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        width: 310,
        height: 170,
        // Double-bezel card
        background: "rgba(255,255,255,0.04)",
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: 16,
        padding: 4,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "rgba(255,255,255,0.03)",
          borderRadius: 13,
          boxShadow: "inset 0 1px 1px rgba(255,255,255,0.06)",
        }}
      >
        {/* Label */}
        <div
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            fontSize: 13,
            fontWeight: 500,
            color: "rgba(255,255,255,0.4)",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 10,
          }}
        >
          {item.label}
        </div>
        {/* Value */}
        <div
          style={{
            fontFamily:
              "'SF Mono', 'JetBrains Mono', 'Cascadia Code', monospace",
            fontSize: 44,
            fontWeight: 600,
            color: "#ffffff",
            letterSpacing: "-0.02em",
          }}
        >
          {formatted}
        </div>
      </div>
    </div>
  );
};

export const MetricsScene: React.FC<MetricsSceneProps> = ({ metrics }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Section title
  const titleOpacity = interpolate(frame, [0, 0.4 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });
  const titleY = interpolate(frame, [0, 0.5 * fps], [20, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Exit
  const exitOpacity = interpolate(
    frame,
    [3 * fps, 3.5 * fps],
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
      {/* Section title */}
      <div
        style={{
          position: "absolute",
          top: 100,
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
          fontFamily:
            "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
          fontSize: 16,
          fontWeight: 500,
          color: "rgba(255,255,255,0.35)",
          textTransform: "uppercase",
          letterSpacing: "0.12em",
        }}
      >
        Key Metrics
      </div>

      {/* Cards row */}
      <div
        style={{
          display: "flex",
          gap: 24,
          flexWrap: "wrap",
          justifyContent: "center",
          maxWidth: 1700,
        }}
      >
        {metrics.map((item, i) => (
          <MetricCard key={item.label} item={item} index={i} />
        ))}
      </div>
    </AbsoluteFill>
  );
};
