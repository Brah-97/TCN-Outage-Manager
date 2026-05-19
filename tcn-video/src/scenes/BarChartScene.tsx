import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { RegionItem } from "../types";

interface BarChartSceneProps {
  regionData: RegionItem[];
}

const BAR_COLORS = ["#1e3a7a", "#c81e28"];

export const BarChartScene: React.FC<BarChartSceneProps> = ({ regionData }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const maxOutages = Math.max(...regionData.map((r) => r.outages));

  // Title
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
  const exitOpacity = interpolate(frame, [2.5 * fps, 3 * fps], [1, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: "0 120px",
        opacity: exitOpacity,
      }}
    >
      {/* Title */}
      <div
        style={{
          position: "absolute",
          top: 80,
          left: 120,
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
        }}
      >
        <div
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            fontSize: 16,
            fontWeight: 500,
            color: "rgba(255,255,255,0.35)",
            textTransform: "uppercase",
            letterSpacing: "0.12em",
            marginBottom: 8,
          }}
        >
          Regional Breakdown
        </div>
        <div
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            fontSize: 36,
            fontWeight: 700,
            color: "#ffffff",
            letterSpacing: "-0.02em",
          }}
        >
          Outages by Region
        </div>
      </div>

      {/* Chart area */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 14,
          width: "100%",
          maxWidth: 1400,
          marginTop: 80,
        }}
      >
        {regionData.map((region, i) => {
          const delay = 6 + i * 3;
          const barProgress = interpolate(
            frame,
            [delay, delay + 0.8 * fps],
            [0, 1],
            {
              extrapolateRight: "clamp",
              extrapolateLeft: "clamp",
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            },
          );
          const rowOpacity = interpolate(
            frame,
            [delay, delay + 0.3 * fps],
            [0, 1],
            { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
          );

          const barWidthPercent =
            (region.outages / maxOutages) * 100 * barProgress;
          const isTop = i < 3;

          return (
            <div
              key={region.name}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 16,
                opacity: rowOpacity,
              }}
            >
              {/* Region name */}
              <div
                style={{
                  width: 160,
                  textAlign: "right",
                  fontFamily:
                    "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
                  fontSize: 16,
                  fontWeight: 500,
                  color: "rgba(255,255,255,0.6)",
                }}
              >
                {region.name}
              </div>

              {/* Bar container */}
              <div
                style={{
                  flex: 1,
                  height: 36,
                  background: "rgba(255,255,255,0.04)",
                  borderRadius: 6,
                  overflow: "hidden",
                  position: "relative",
                }}
              >
                <div
                  style={{
                    width: `${barWidthPercent}%`,
                    height: "100%",
                    background: isTop ? BAR_COLORS[1] : BAR_COLORS[0],
                    borderRadius: 6,
                    opacity: isTop ? 1 : 0.8,
                  }}
                />
              </div>

              {/* Value */}
              <div
                style={{
                  width: 60,
                  fontFamily:
                    "'SF Mono', 'JetBrains Mono', 'Cascadia Code', monospace",
                  fontSize: 16,
                  fontWeight: 600,
                  color: "#ffffff",
                  opacity: barProgress,
                  textAlign: "right",
                }}
              >
                {Math.round(region.outages * barProgress)}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
