import { Status } from "./status.model";
import { Type } from "./type.model";

export interface SensorType {
	type: Type;
	measuredValue: string;
	status: Status;
	port: String;
}