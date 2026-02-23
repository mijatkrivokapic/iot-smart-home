export interface WebsocketMessage {
  topic: string;
  payload: SensorData;
  timestamp: number;
}

export interface SensorData {
  sensor: string;
  device: string;
  value: number | string | { temperature: number; humidity: number };
  simulated: boolean;
  timestamp: number;
}
