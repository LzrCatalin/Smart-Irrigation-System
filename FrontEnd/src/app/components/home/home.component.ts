import { map, mergeMap, from } from 'rxjs';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { News } from '../../models/news.model';
import { Field } from '../../models/field.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { Sensor } from '../../models/sensor.model';
import { Router } from '@angular/router';
import { WeatherDialogComponent } from '../weather-dialog/weather-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { FieldDisplayComponent } from '../field-display/field-display.component';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AddFieldComponent } from '../add-field/add-field.component';
import { ApiService } from '../../services/api.service';

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
	fieldLocations: { [key: string]: string } = {};

	city = '';
	selectedDate = new Date();
	weatherData: any = null;
	showWeatherInput: boolean = false;

	togglePump: boolean = false;

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
	// Pagination for fields
	fieldsPageSize = 2;
	fieldsPageIndex = 0;

	// Pagination for news
	newsPageSize = 1;
	newsPageIndex = 0;

	constructor( private router: Router, 
				private fieldsService: FieldsService,
				private dialog: MatDialog,
				private snackBar: MatSnackBar,
				private apiService: ApiService
				) {}

	ngOnInit(): void {
		console.log("LOADING HOME COMPONENT")
		// Store loggedin user
		this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

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
				this.updatePaginatedFields();
			},
			error: (error) => {
				console.error(error);
				this.errorMessage = 'Could not fetch fields. Please try again later.'
			}
		});
	}

	updatePaginatedFields(): void {
		const start = this.fieldsPageIndex * this.fieldsPageSize;
		const end = start + this.fieldsPageSize;
		this.paginatedFields = this.fields.slice(start, end);
	}

	onFieldsPageChange(event: PageEvent) {
		this.fieldsPageSize = event.pageSize;
		this.fieldsPageIndex = event.pageIndex;
		this.updatePaginatedFields();
	}

	deleteField(field_id: string, field_sensors: Sensor[], event: Event): void {
		event.stopPropagation();
		
		// Enable dialog confirmation for deletion
		const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
			width: '350px',
			data: { message: 'Are you sure you want to delete this field?' }
		});

		// Call function after selecting the option
		dialogRef.afterClosed().subscribe(
			result => {
				if (result) {
					const sensorNames = field_sensors.map(sensor => sensor.name);
					this.fieldsService.delete_field(field_id, sensorNames).subscribe({
						next: () => {
							// Refetch fields after deletion
							if (this.user?.id) {
								this.fetchUserFields(this.user.id);
							}

							// Show success notification
							this.showNotification('Field deleted successfully!');
						},

						error: (error) => {
							console.error(error);
							this.errorMessage = 'Error while deleting field.'

							// Show error notification
							this.showNotification('Failed to delete field.', 'Retry', 5000);
						}
					})
				}
			}
		)
	}

	openFieldDetails(field: Field) {
		// Open FieldDisplay component
		const dialogRef = this.dialog.open(FieldDisplayComponent, {
			width: '400px',
			data: { field }
		});
		
		// Display notification after update field functionalty
		dialogRef.afterClosed().subscribe({
			next: (result) => {
				if (result) {
					if (result.success) {
						this.showNotification('Field updated successfully!');

					} else {
						this.showNotification('Failed to update field.', 'Retry', 5000);
					}
				}
			}
		})
	}


	//////////////////////
	//
	//	Fetch farming news
	//	
	//////////////////////
	fetchFarmingNews(): void {
		this.apiService.getFarmingNews().subscribe({
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
		const start = this.newsPageIndex * this.newsPageSize;
		const end = start + this.newsPageSize;
		this.paginatedNews = this.newsItems.slice(start, end);
	}

	onNewsPageChange(event: PageEvent): void {
		this.newsPageSize = event.pageSize;
		this.newsPageIndex = event.pageIndex;
		this.updatePaginatedNews();
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
		console.log("Selected date: ", this.selectedDate);

	}

	formatDate(date: Date): string {
		// Format date as needed for your API call
		return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
	}

	fetchWeather(): void {
		const formattedDate = this.formatDate(this.selectedDate);
		this.apiService.getWeather(this.city, formattedDate).subscribe({
			next: (response) => {
				this.weatherData = response;
				this.openWeatherDialog();
			},
			error: (error) => {
				console.error('Error fetching weather:', error);
			}
		})
	}

	fetchWeeklyWeather(): void {
		this.apiService.getWeather(this.city).subscribe({
			next: (response) => {
				this.weatherData =  response;
				this.openWeatherDialog();
			},
			error: (error) => {
				console.error('Error fetching weekly weather:', error)
			}
		})
	}
	openWeatherDialog(): void {
		this.dialog.open(WeatherDialogComponent, {
			width: '400px',
			data: { weatherData: this.weatherData }
		});
	}


	
	//////////////////
	//
	//	Notifications
	//
	//////////////////
	showNotification(message: string, action: string = 'Close', duration: number = 3000): void {
		this.snackBar.open(message, action, {
			duration: duration, 
			horizontalPosition: 'right', 
			verticalPosition: 'top',
			panelClass: ['custom-snackbar']
		});
	}


	//////////////////
	//
	//	Side Bar options
	//
	//////////////////
	toggleHome(): void {
		this.router.navigateByUrl('/home')
	}

	toggleCreateField(): void {
		const dialogRef = this.dialog.open(AddFieldComponent, {
			width: '1000px',
			data: {} 
		});
	
		dialogRef.afterClosed().subscribe(result => {
			if (result) {
				console.log('New field added:', result);
				if (this.user?.id) {
					this.fetchUserFields(this.user.id);

					// Display notification
					this.showNotification('Field added successfully!');
				}
			}
		});
	}

	toggleWaterPump(): void {
		this.togglePump = !this.togglePump;
		
		this.fieldsService.toggle_pump(this.togglePump).subscribe({
			next: (res: any) => {
				console.log(res);
			},

			error: (error: any) => {
				console.error('Failed updating pump toggle: ', error);
				this.togglePump = !this.togglePump;
			}
		})
	}

	toggleLogOut(): void {
		sessionStorage.clear();
		localStorage.clear();
		this.router.navigateByUrl('/login')
	}
}
