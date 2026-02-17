export interface WebsocketMessage {
    topic: string;
    payload: SensorData;
    timestamp: number;
}

export interface SensorData {
    sensor: string;
    device: string;
    value: number;
    simulated: boolean;
    timestamp: number;
}