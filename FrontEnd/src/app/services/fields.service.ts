import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Field } from '../models/field.model';
import { Sensor } from '../models/sensor.model';

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
}
