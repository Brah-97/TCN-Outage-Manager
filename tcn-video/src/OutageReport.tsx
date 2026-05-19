import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { OutageReportProps } from "./types";
import { IntroScene } from "./scenes/IntroScene";
import { MetricsScene } from "./scenes/MetricsScene";
import { BarChartScene } from "./scenes/BarChartScene";
import { ClassificationScene } from "./scenes/ClassificationScene";
import { OutroScene } from "./scenes/OutroScene";

export const OutageReport: React.FC<OutageReportProps> = (props) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(145deg, #0a1628 0%, #0f2040 40%, #0a1628 100%)",
      }}
    >
      {/* Subtle grid overlay */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      {/* Scene 1: Intro — Logo + Title (0s–3s) */}
      <Sequence durationInFrames={3 * fps}>
        <IntroScene
          title={props.reportTitle}
          period={props.reportPeriod}
        />
      </Sequence>

      {/* Scene 2: Metrics Cards (3s–6.5s) */}
      <Sequence from={3 * fps} durationInFrames={3.5 * fps}>
        <MetricsScene metrics={props.metrics} />
      </Sequence>

      {/* Scene 3: Bar Chart — Outages by Region (6.5s–9.5s) */}
      <Sequence from={6.5 * fps} durationInFrames={3 * fps}>
        <BarChartScene regionData={props.regionData} />
      </Sequence>

      {/* Scene 4: Classification Donut (9.5s–11.5s) */}
      <Sequence from={9.5 * fps} durationInFrames={2 * fps}>
        <ClassificationScene classificationData={props.classificationData} />
      </Sequence>

      {/* Scene 5: Outro (11.5s–12s) */}
      <Sequence from={11.5 * fps} durationInFrames={0.5 * fps}>
        <OutroScene />
      </Sequence>
    </AbsoluteFill>
  );
};
