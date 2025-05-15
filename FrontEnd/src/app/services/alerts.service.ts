import { Injectable } from '@angular/core';
import { UserAlerts } from '../models/user-alerts.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AlertDefinition } from '../models/alerts-definition.model';

const BASE_URL = 'http://localhost:5000'

@Injectable({
	providedIn: 'root'
})
export class AlertsService {

	constructor(private http: HttpClient) { }
	
	get_user_alerts(user_id: string): Observable<any> {
		return this.http.get<any>(`${BASE_URL}/api/alerts/${user_id}`)
	}
}
