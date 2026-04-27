export interface DetectionResult {
  id: string;
  userId: string;
  videoName: string;
  totalVehicles: number;
  detectionMetrics: {
    cars: number;
    bikes: number;
    trucks: number;
    buses: number;
    averageSpeed: number;
    helmetDetections: number;
  };
  createdAt: string;
}

export interface Detection {
  class: string;
  confidence: number;
  bbox: [number, number, number, number];
  speed?: number;
  helmetDetected?: boolean;
}
