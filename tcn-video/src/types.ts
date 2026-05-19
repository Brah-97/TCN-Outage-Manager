export interface MetricItem {
  label: string;
  value: string;
}

export interface RegionItem {
  name: string;
  outages: number;
  load: number;
}

export interface ClassificationItem {
  label: string;
  value: number;
  color: string;
}

export interface OutageReportProps {
  reportTitle: string;
  reportPeriod: string;
  metrics: MetricItem[];
  regionData: RegionItem[];
  classificationData: ClassificationItem[];
}
