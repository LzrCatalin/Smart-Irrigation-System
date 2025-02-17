import { SensorType } from "./sensor-type.model";

export interface Sensor {
	id: string;
	name: string;
	type: SensorType;
}