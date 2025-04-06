import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Field } from '../models/field.model';
import { Sensor } from '../models/sensor.model';
import { environment } from '../../environments/environment';

const BASE_URL = 'http://localhost:5000'

@Injectable({
	providedIn: 'root'
})
export class FieldsService {

	constructor(private http: HttpClient) { }

	get_user_fields(user_id: string): Observable<Field[]> {
		return this.http.get<Field[]>(`${BASE_URL}/api/fields/all/${user_id}`)
	}

	add_field(latitude: number, longitude: number, length: number, width: number, slope: number, crop_name: string, soil_type: string, user: string, sensors: Sensor[]): Observable<Field> {
		return this.http.post<Field>(`${BASE_URL}/api/fields`, {latitude, longitude, length, width, slope, crop_name, soil_type, user, sensors})
	}

	update_field(id: string, latitude: number, longitude: number, length: number, width: number, slope: number, crop_name: string, soil_type: string, user: string, sensors: Sensor[], deleted_sensors: Sensor[]) {
		const field_body = {
			field_data: {latitude, longitude, length, width, slope, crop_name, soil_type, user, sensors},
			deleted_data: {deleted_sensors}
		}

		return this.http.put<Field>(`${BASE_URL}/api/fields/${id}`, field_body)
	}
	
	delete_field(id: string, sensors_name: string[]): Observable<Field> {
		const options = {
			body: { sensors_name } 
		};
		return this.http.delete<Field>(`${BASE_URL}/api/fields/${id}`, options)
	}

	toggle_pump(state: boolean): Observable<any> {
		const stateValue = state ? 1 : 0;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/waterpump/toggle`,
			{ state: stateValue },
		);
	}
}