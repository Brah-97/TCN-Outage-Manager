import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { ClassificationItem } from "../types";

interface ClassificationSceneProps {
  classificationData: ClassificationItem[];
}

export const ClassificationScene: React.FC<ClassificationSceneProps> = ({
  classificationData,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

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

  // Donut animation progress
  const donutProgress = interpolate(frame, [0.2 * fps, 1.4 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Exit
  const exitOpacity = interpolate(frame, [1.5 * fps, 2 * fps], [1, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // SVG donut chart
  const size = 340;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 130;
  const strokeWidth = 50;
  const circumference = 2 * Math.PI * radius;

  let cumulativeAngle = 0;
  const total = classificationData.reduce((s, d) => s + d.value, 0);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity: exitOpacity,
      }}
    >
      {/* Title */}
      <div
        style={{
          position: "absolute",
          top: 80,
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
            textAlign: "center",
          }}
        >
          Classification
        </div>
        <div
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            fontSize: 36,
            fontWeight: 700,
            color: "#ffffff",
            letterSpacing: "-0.02em",
            textAlign: "center",
          }}
        >
          Outage Types
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 80, marginTop: 40 }}>
        {/* Donut */}
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
          {classificationData.map((item) => {
            const fraction = item.value / total;
            const dashLength = circumference * fraction * donutProgress;
            const dashGap = circumference - dashLength;
            const rotation = cumulativeAngle * donutProgress;
            cumulativeAngle += fraction * 360;

            return (
              <circle
                key={item.label}
                cx={cx}
                cy={cy}
                r={radius}
                fill="none"
                stroke={item.color}
                strokeWidth={strokeWidth}
                strokeDasharray={`${dashLength} ${dashGap}`}
                strokeLinecap="butt"
                transform={`rotate(${rotation - 90} ${cx} ${cy})`}
              />
            );
          })}
          {/* Center text */}
          <text
            x={cx}
            y={cy - 8}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#ffffff"
            fontFamily="'SF Mono', 'JetBrains Mono', monospace"
            fontSize="42"
            fontWeight="700"
          >
            {Math.round(total * donutProgress)}%
          </text>
          <text
            x={cx}
            y={cy + 24}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="rgba(255,255,255,0.4)"
            fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            fontSize="13"
            letterSpacing="0.08em"
          >
            TOTAL
          </text>
        </svg>

        {/* Legend */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {classificationData.map((item, i) => {
            const legendDelay = 0.4 * fps + i * 6;
            const legendOpacity = interpolate(
              frame,
              [legendDelay, legendDelay + 0.3 * fps],
              [0, 1],
              { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
            );
            const legendX = interpolate(
              frame,
              [legendDelay, legendDelay + 0.5 * fps],
              [20, 0],
              {
                extrapolateRight: "clamp",
                extrapolateLeft: "clamp",
                easing: Easing.bezier(0.16, 1, 0.3, 1),
              },
            );

            return (
              <div
                key={item.label}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                  opacity: legendOpacity,
                  transform: `translateX(${legendX}px)`,
                }}
              >
                <div
                  style={{
                    width: 16,
                    height: 16,
                    borderRadius: 4,
                    background: item.color,
                  }}
                />
                <div>
                  <div
                    style={{
                      fontFamily:
                        "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                      fontSize: 18,
                      fontWeight: 600,
                      color: "#ffffff",
                    }}
                  >
                    {item.label}
                  </div>
                  <div
                    style={{
                      fontFamily:
                        "'SF Mono', 'JetBrains Mono', monospace",
                      fontSize: 28,
                      fontWeight: 700,
                      color: item.color,
                      marginTop: 2,
                    }}
                  >
                    {(item.value * donutProgress).toFixed(1)}%
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
