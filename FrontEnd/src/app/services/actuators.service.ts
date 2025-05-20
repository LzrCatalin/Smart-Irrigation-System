import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class ActuatorsService {

	constructor(private http: HttpClient) { }

	toggle_pump(state: boolean, id: string): Observable<any> {
		const stateValue = state ? 1 : 0;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/waterpump/toggle`,
			{ 
				state: stateValue,
				user_id: user_id
			},
		);
	}

	toggle_sensors_scheduler(state: boolean, id: string): Observable<any> {
		const stateValue = state ? 1 : 0;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/scheduler/toggle`,
			{ 
				state: stateValue,
				user_id: user_id
			},
		);
	}

	toggle_irrigation_system(state: boolean, id: string): Observable<any> {
		const stateValue = state ? 1 : 0;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/irrigation/toggle`,
			{ 
				state: stateValue,
				user_id: user_id
			},
		);
	}

	update_scheduler_settings(interval: number, id: string): any {
		const intervalValue = interval;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/scheduler/updated_timer`,
			{ 
				interval: intervalValue,
				user_id: user_id 
			},
		);
	}

	update_irrigation_settings(interval: number, id: string): any {
		const intervalValue = interval;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/irrigation/updated_timer`,
			{ 
				interval: intervalValue,
				user_id: user_id 
			},
		);
	}

	update_field_config(data: any): any {
		return this.http.put(
			`http://${environment.raspberry_id}:5000/api/actuators/field_config`,
			data
		);
	}
}
