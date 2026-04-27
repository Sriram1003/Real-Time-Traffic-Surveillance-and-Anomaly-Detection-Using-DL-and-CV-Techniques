import * as tf from '@tensorflow/tfjs';
import * as coco from '@tensorflow-models/coco-ssd';

let model: coco.ObjectDetection | null = null;

export const loadModel = async () => {
  if (!model) {
    model = await coco.load();
  }
  return model;
};

export interface Prediction {
  class: string;
  score: number;
  bbox: [number, number, number, number];
}

export const detectObjects = async (imageElement: HTMLImageElement | HTMLCanvasElement | HTMLVideoElement): Promise<Prediction[]> => {
  const model = await loadModel();
  const predictions = await model.estimateObjects(imageElement);

  return predictions.map((pred) => ({
    class: pred.class,
    score: pred.score,
    bbox: pred.bbox as [number, number, number, number],
  }));
};

export const filterVehicles = (predictions: Prediction[]): Prediction[] => {
  const vehicleClasses = ['car', 'truck', 'bus', 'motorcycle', 'motorbike'];
  return predictions.filter((pred) =>
    vehicleClasses.some((vc) => pred.class.toLowerCase().includes(vc)) &&
    pred.score > 0.5
  );
};

export const countVehicles = (predictions: Prediction[]) => {
  const counts = {
    cars: 0,
    bikes: 0,
    trucks: 0,
    buses: 0,
  };

  predictions.forEach((pred) => {
    const classLower = pred.class.toLowerCase();
    if (classLower.includes('car')) counts.cars++;
    else if (classLower.includes('motorcycle') || classLower.includes('motorbike')) counts.bikes++;
    else if (classLower.includes('truck')) counts.trucks++;
    else if (classLower.includes('bus')) counts.buses++;
  });

  return counts;
};
