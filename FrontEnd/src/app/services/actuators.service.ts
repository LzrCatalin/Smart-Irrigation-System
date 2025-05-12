import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class ActuatorsService {

	constructor(private http: HttpClient) { }

	toggle_pump(state: boolean): Observable<any> {
		const stateValue = state ? 1 : 0;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/waterpump/toggle`,
			{ state: stateValue },
		);
	}

	toggle_sensors_scheduler(state: boolean): Observable<any> {
		const stateValue = state ? 1 : 0;
		console.log(stateValue)

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/scheduler/toggle`,
			{ state: stateValue },
		);
	}

	toggle_irrigation_system(state: boolean): Observable<any> {
		const stateValue = state ? 1 : 0;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/irrigation/toggle`,
			{ state: stateValue },
		);
	}

	update_scheduler_settings(interval: number): any {
		const intervalValue = interval;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/scheduler/updated_timer`,
			{ interval: intervalValue },
		);
	}

	update_irrigation_settings(interval: number): any {
		const intervalValue = interval;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/irrigation/updated_timer`,
			{ interval: intervalValue },
		);
	}

	update_field_config(data: any): any {
		return this.http.put(
			`http://${environment.raspberry_id}:5000/api/actuators/field_config`,
			data
		);
	}
}
