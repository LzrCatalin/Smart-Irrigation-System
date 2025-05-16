import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IrrigationHistory } from '../models/irrigation-history.mode';

const BASE_URL = 'http://localhost:5000'

@Injectable({
	providedIn: 'root'
})
export class HistoryService {

	constructor(private http: HttpClient) { }

	fetch_field_history(field_id: string): Observable<IrrigationHistory> {
		return this.http.get<IrrigationHistory>(`${BASE_URL}/api/history/${field_id}`)
	}
}
