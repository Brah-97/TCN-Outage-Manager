import "./index.css";
import { Composition } from "remotion";
import { OutageReport } from "./OutageReport";
import { OutageReportProps } from "./types";

const defaultData: OutageReportProps = {
  reportTitle: "Grid Outage Report",
  reportPeriod: "April 15 — October 4, 2026",
  metrics: [
    { label: "Total Outages", value: "625" },
    { label: "Total Duration", value: "1,982.7 hrs" },
    { label: "Avg Duration", value: "3.17 hrs" },
    { label: "Load Lost", value: "2,418.4 MW" },
    { label: "Substations", value: "86" },
  ],
  regionData: [
    { name: "Lagos", outages: 210, load: 820 },
    { name: "Osogbo", outages: 95, load: 340 },
    { name: "Port-Harcourt", outages: 72, load: 280 },
    { name: "Kaduna", outages: 65, load: 250 },
    { name: "Shiroro", outages: 48, load: 190 },
    { name: "Benin", outages: 42, load: 175 },
    { name: "Abuja", outages: 35, load: 145 },
    { name: "Enugu", outages: 28, load: 110 },
    { name: "Kano", outages: 18, load: 65 },
    { name: "Bauchi", outages: 12, load: 43 },
  ],
  classificationData: [
    { label: "Forced", value: 44.5, color: "#1e3a7a" },
    { label: "Emergency", value: 37, color: "#c81e28" },
    { label: "Planned", value: 18.5, color: "#5080c0" },
  ],
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="OutageReport"
        component={OutageReport}
        durationInFrames={360}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={defaultData}
      />
    </>
  );
};
