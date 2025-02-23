import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class WeatherService {
	private apiUrl = 'https://api.openweathermap.org/data/2.5';

	constructor(private http: HttpClient) { }

	getWeather(city: string, date?: string): Observable<any> {
		const url = date
			? `${this.apiUrl}/weather?q=${city}&dt=${date}&appid=${environment.weatherApiKey}`
			: `${this.apiUrl}/forecast?q=${city}&cnt=7&appid=${environment.weatherApiKey}`;
		
		return this.http.get(url);
	}
}
