import { Sensor } from "./sensor.model";

export interface Field {
	id: string;
	latitude: number;
	longitude: number;
	length: number;
	width: number;
	slope: number;
	soil_type: string;
	crop_name: string;
	user_id: string;
	sensors: Sensor[];
}