import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { News } from '../../models/news.model';
import { NewsService } from '../../services/news.service';
import { Field } from '../../models/field.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { Sensor } from '../../models/sensor.model';
import { Router } from '@angular/router';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit{
	user: User | undefined;
	fields: Field[] = [];
	isFieldExpanded = false;
	selectedField: Field | null = null;
	paginatedFields = this.fields.slice(0, 3);

	city = '';
	selectedDate = new Date();
	weatherData: any = null;
	showWeatherInput: boolean = false;

	newsItems: News[] = [];
	paginatedNews: News[] = [];
	errorMessage: string = '';
	carouselOptions = {
		loop: true,
		autoplay: true,
		autoplayTimeout: 3000,
		autoplayHoverPause: true,
		responsive: {
		0: { items: 1 },
		600: { items: 2 },
		1000: { items: 3 }
		}
	};

	@ViewChild(MatPaginator) paginator!: MatPaginator;
	pageSize = 1;
	pageIndex = 0;

	constructor(private newsService: NewsService, 
				private router: Router, 
				private fieldsService: FieldsService) {}

	ngOnInit(): void {
		// Store loggedin user
		this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;
		console.log(this.user)

		// Fetch fields for loggedin user
		if (this.user.id !== undefined) {
			this.fetchUserFields(this.user.id);
		}

		// Fetch news
		this.fetchFarmingNews();
	}

	//////////////////////
	//
	//	Fetch user fields
	//
	//////////////////////
	fetchUserFields(user_id: string): void {
		this.fieldsService.get_user_fields(user_id).subscribe({
			next: (response) => {
				console.log(response)
				this.fields = response;
			},
			error: (error) => {
				console.error(error);
				this.errorMessage = 'Could not fetch fields. Please try again later.'
			}
		});
	}

	deleteField(field_id: string, field_sensors: Sensor[]): void {
		console.log(field_id);
		console.log(field_sensors);

		const sensorNames = field_sensors.map(sensor => sensor.name);

		this.fieldsService.delete_field(field_id, sensorNames).subscribe({
			next:(response) => {
				console.log(response);
				this.router.navigateByUrl('/home');
			},

			error: (error) => {
				console.error(error);
				this.errorMessage = 'Error while deleting field.'
			}
		})
	}

	//////////////////////
	//
	//	Fetch farming news
	//	
	//////////////////////
	fetchFarmingNews(): void {
		this.newsService.getFarmingNews().subscribe({
			next: (response: any) => {
				this.newsItems = response.articles.map((article: any) => ({
					title: article.title,
					imageUrl: article.urlToImage || 'https://via.placeholder.com/150',
					newsUrl: article.url
				}));
				this.updatePaginatedNews();
			},
			error: (error) => {
				console.log('Error fetching news:', error);
				this.errorMessage = 'Failed to load news.';
			}
		});
	}

	updatePaginatedNews(): void {
		const start = this.pageIndex * this.pageSize;
		const end = start + this.pageSize;
		this.paginatedNews = this.newsItems.slice(start, end);
	}

	onPageChange(event: PageEvent): void {
		this.pageSize = event.pageSize;
		this.pageIndex = event.pageIndex;
		this.updatePaginatedNews();
		this.paginatedNews = [this.newsItems[event.pageIndex]];
	}


	////////////////	
	//
	//	Fields
	//
	////////////////
	toggleFieldDetails(field: any): void {
		// field.showDetails = !field.showDetails;
		// this.isFieldExpanded = this.fields.some(f => f.showDetails);
	}

	onFieldsPageChange(event: any) {
		const index = event.pageIndex;
		const size = event.pageSize;
		this.paginatedFields = this.fields.slice(index * size, index * size + size);
	}

	openFieldDetails(field: Field) {
		this.selectedField = field;
		const modal = document.querySelector('.modal');
		if (modal instanceof HTMLElement) {
			modal.style.display = 'block';
		}
	}
	
	closeModal() {
		this.selectedField = null;
		const modal = document.querySelector('.modal');
		if (modal instanceof HTMLElement) {
			modal.style.display = 'none';
		}
	}

	///////////////
	//
	//	Weather
	//
	////////////////
	toggleWeatherInput() {
		this.showWeatherInput = !this.showWeatherInput;
	}

	dateChanged(newDate: Date) {
		this.selectedDate = newDate;
	}

	formatDate(date: Date): string {
		// Format date as needed for your API call
		return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
	}

	fetchWeather(): void {}

	//////////////////
	//
	//
	//
	//////////////////
	toggleLogOut(): void {
		sessionStorage.clear();
		localStorage.clear();
		this.router.navigateByUrl('/login')
	}
}
