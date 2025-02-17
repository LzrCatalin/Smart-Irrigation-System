import { Status } from "./status.model";
import { Type } from "./type.model";

export interface SensorType {
	type: Type;
	measured_value: string;
	status: Status;
	port: String;
}