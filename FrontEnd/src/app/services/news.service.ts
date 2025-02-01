import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class NewsService {

	private apiUrl = `https://newsapi.org/v2/everything?q=farming&apiKey=${environment.newsApiKey}`;

	constructor(private http: HttpClient) { }

	getFarmingNews(): Observable<any> {
		return this.http.get(this.apiUrl)
	}
}
