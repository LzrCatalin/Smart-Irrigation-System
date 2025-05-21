import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';


@Injectable({
	providedIn: 'root'
})
export class SystemService {

	constructor(private http: HttpClient) { }

	// add_field_into_system(field_id: string): any {
	// 	return this.http.post(
	// 		`http://${environment.raspberry_id}:5000/api/system/field_config/${field_id}`
	// 	);
	// }

	delete_field_from_system(field_id: string): any {
		return this.http.delete<any>(
			`http://${environment.raspberry_id}:5000/api/system/${field_id}`
		);
	}

	update_field_config(data: any): any {
		return this.http.put(
			`http://${environment.raspberry_id}:5000/api/system/field_config`,
			data
		);
	}

	toggle_sensors_scheduler(state: boolean, id: string): Observable<any> {
		const stateValue = state ? 1 : 0;
		const user_id = id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/system/scheduler/toggle`,
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
			`http://${environment.raspberry_id}:5000/api/system/irrigation/toggle`,
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
			`http://${environment.raspberry_id}:5000/api/system/scheduler/updated_timer`,
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
			`http://${environment.raspberry_id}:5000/api/system/irrigation/updated_timer`,
			{ 
				interval: intervalValue,
				user_id: user_id 
			},
		);
	}
}
