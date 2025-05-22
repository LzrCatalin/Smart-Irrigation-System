import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class ActuatorsService {

	constructor(private http: HttpClient) { }

	toggle_pump(state: boolean, id: string, f_id: string): Observable<any> {
		const stateValue = state ? 1 : 0;
		const user_id = id;
		const field_id = f_id;

		return this.http.post(
			`http://${environment.raspberry_id}:5000/api/actuators/waterpump/toggle`,
			{ 
				state: stateValue,
				user_id: user_id,
				field_id: field_id
			},
		);
	}
}
