import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Sensor } from '../models/sensor.model';

const BASE_URL = 'http://localhost:5000'

@Injectable({
	providedIn: 'root'
})
export class SensorsService {

	constructor(private http: HttpClient) {}

	get_sensors_by_status(status: string): Observable<Sensor[]> {
		return this.http.get<Sensor[]>(`${BASE_URL}/api/sensors/status/${status}`)
	}
}
