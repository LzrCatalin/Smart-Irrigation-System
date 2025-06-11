import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class ApiService {
	private apiWeatherUrl = 'https://api.openweathermap.org/data/2.5';
	private apiNewsUrl = `https://newsapi.org/v2/everything?q=farming&apiKey=${environment.newsApiKey}`;
	private apiGeocodingUrl = `https://maps.googleapis.com/maps/api/geocode/json`

	constructor(private http: HttpClient) { }

	// Request on weather API
	getWeather(city: string, date?: string): Observable<any> {
		const url = date
			? `${this.apiWeatherUrl}/weather?q=${city}&dt=${date}&appid=${environment.weatherApiKey}`
			: `${this.apiWeatherUrl}/forecast?q=${city}&cnt=7&appid=${environment.weatherApiKey}`;

		return this.http.get(url);
	}

	// Request on news API
	getFarmingNews(): Observable<any> {
		return this.http.get(this.apiNewsUrl)
	}

	// Request on location fetch based on latitude and longitude
	getLocation(latitude: number, longitude: number): Observable<any> {
		const url = `${this.apiGeocodingUrl}?latlng=${latitude},${longitude}&key=${environment.googleMapsApiKey}`;
		return this.http.get(url);
	}

	getExternal(url: string): Observable<any> {
		return this.http.get(url);
	}
}
