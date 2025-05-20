import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { News } from '../../models/news.model';
import { Field } from '../../models/field.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { ActuatorsService } from '../../services/actuators.service';
import { AlertsService } from '../../services/alerts.service';
import { Sensor } from '../../models/sensor.model';
import { Router } from '@angular/router';
import { WeatherDialogComponent } from '../weather-dialog/weather-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { FieldDisplayComponent } from '../field-display/field-display.component';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AddFieldComponent } from '../add-field/add-field.component';
import { ApiService } from '../../services/api.service';
import { IntervalDialogComponent } from './interval-dialog/interval-dialog.component';
import { UserAlerts } from '../../models/user-alerts.model';
import { AlertDefinition } from '../../models/alerts-definition.model';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.css']
})	
export class HomeComponent implements OnInit{
	@ViewChild('alertDrawer') alertDrawer!: MatSidenav;

	user: User | undefined;
	fields: Field[] = [];
	isFieldExpanded = false;
	selectedField: Field | null = null;
	paginatedFields = this.fields.slice(0, 3);
	fieldLocations: { [key: string]: string } = {};
	userAlerts: any[] = [];
	filteredAlerts: any[] = [];
	availableTypes: string[] = [];
	selectedAlertType: 'INFO' | 'WARNING' = 'INFO';
	alertDrawerOpen = false;

	city = '';
	selectedDate = new Date();
	weatherData: any = null;
	showWeatherInput: boolean = false;

	togglePump: boolean = false;
	toggleSensorsScheduler: boolean = false;
	toggleIrrigationSystem: boolean = false;

	schedulerInterval: number = 15; // Default 15 minutes
	irrigationInterval: number = 20; // Default 20 minutes
	showSchedulerIntervalDialog: boolean = false;
	showIrrigationIntervalDialog: boolean = false;

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
				private apiService: ApiService,
				private actuatorsService: ActuatorsService,
				private alertsService: AlertsService
				) {}
	
	private getSchedulerKey(): string {
		return this.user?.id ? `schedulerState_${this.user.id}` : 'schedulerState_default';
	}

	private getIrrigationKey(): string {
		return this.user?.id ? `irrigationState_${this.user.id}` : 'irrigationState_default';
	}

	//////////////////////
	//
	//	Timers Setup
	//
	//////////////////////
	openSchedulerIntervalDialog(): void {
		const dialogRef = this.dialog.open(IntervalDialogComponent, {
			data: { title: 'Set Sensors Update Interval', initialValue: this.schedulerInterval }
		});
	
		dialogRef.afterClosed().subscribe(result => {
			if (result !== undefined) {
				this.schedulerInterval = result;
				this.saveSchedulerInterval();
			}
		});
	}

	saveSchedulerInterval(): void {
		this.showSchedulerIntervalDialog = false;
		// Save to localStorage
		localStorage.setItem(`${this.getSchedulerKey()}_interval`, this.schedulerInterval.toString());
		// Update backend
		this.updateSchedulerSettings();
	}

	updateSchedulerSettings(): any {
		if (!this.user?.id) return;
		
		this.actuatorsService.update_scheduler_settings(this.schedulerInterval, this.user.id).subscribe({
			next: () => console.log('Scheduler settings updated'),
			
			error: (error : any) => {
				console.error('Failed to update scheduler settings', error);
				this.showNotification('Failed to update scheduler settings', 'Retry', 5000);
			}
		});
	}
	  
	openIrrigationIntervalDialog(): void {
		const dialogRef = this.dialog.open(IntervalDialogComponent, {
			data: { title: 'Set Irrigation Interval', initialValue: this.irrigationInterval }
			});
		
		dialogRef.afterClosed().subscribe(result => {
			if (result !== undefined) {
				this.irrigationInterval = result;
				this.saveIrrigationInterval();
			}
		});
	}
	
	saveIrrigationInterval(): void {
		this.showIrrigationIntervalDialog = false;
		// Save to localStorage
		localStorage.setItem(`${this.getIrrigationKey()}_interval`, this.irrigationInterval.toString());
		// Update backend
		this.updateIrrigationSettings();
	}
	
	updateIrrigationSettings(): any {
		if (!this.user?.id) return;
		
		this.actuatorsService.update_irrigation_settings(this.irrigationInterval, this.user.id).subscribe({
			next: () => console.log('Irrigation settings updated'),
			
			error: (error : any) => {
				console.error('Failed to update irrigation settings', error);
				this.showNotification('Failed to update irrigation settings', 'Retry', 5000);
			}
		});
	}

	ngOnInit(): void {
		// Store loggedin user
		this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

		// Fetch fields for loggedin user
		if (this.user.id !== undefined) {
			this.fetchUserFields(this.user.id);
			this.fetchUserAlerts(this.user.id);

			const savedStateScheduler = localStorage.getItem(this.getSchedulerKey());
    		this.toggleSensorsScheduler = savedStateScheduler ? JSON.parse(savedStateScheduler) : false;
		
			const savedStateIrrigation = localStorage.getItem(this.getIrrigationKey());
			this.toggleIrrigationSystem = savedStateIrrigation ? JSON.parse(savedStateIrrigation) : false;
		}

		// Fetch news
		this.fetchFarmingNews();

		// Load saved intervals
		const savedSchedulerInterval = localStorage.getItem(`${this.getSchedulerKey()}_interval`);
		this.schedulerInterval = savedSchedulerInterval ? parseInt(savedSchedulerInterval) : 15;
		
		const savedIrrigationInterval = localStorage.getItem(`${this.getIrrigationKey()}_interval`);
		this.irrigationInterval = savedIrrigationInterval ? parseInt(savedIrrigationInterval) : 20;
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
	//	Notifications & Alerts
	//
	//////////////////
	showNotification(message: string, action: string = 'X', duration: number = 3000): void {
		this.snackBar.open(message, action, {
			duration: duration, 
			horizontalPosition: 'right', 
			verticalPosition: 'top',
			panelClass: ['custom-snackbar']
		});
	}

	fetchUserAlerts(user_id: string): void {
		this.alertsService.get_user_alerts(user_id).subscribe({
			next: (response: any) => {
				console.log("Raw response: ", response);
			
				const alertsObject = response.alerts || {};
				const alertArray = Object.entries(alertsObject).map(([timestampKey, alert]: [string, any]) => ({
					...alert,
					timestamp: this.parseTimestamp(timestampKey)
				}));
			
				this.userAlerts = alertArray;
				this.filterAlerts();
			
				console.log("Processed alerts: ", this.userAlerts);
				console.log("Length: ", this.userAlerts.length);
			},

			error: (error) => {
				console.error(error);
			}
		});
	}

	filterAlerts(): void {
		console.log('Filtering alerts by type:', this.selectedAlertType);
		
		this.filteredAlerts = this.userAlerts.filter(
			(alert) => alert.type === this.selectedAlertType
		);

		console.log('Filtered alerts:', this.filteredAlerts);
	}

	onAlertTypeChange() {
		console.log('Alert type changed to:', this.selectedAlertType);
		this.filterAlerts();
	}

	toggleAlertDrawer() {
		this.alertDrawerOpen = !this.alertDrawerOpen;
	}
	
	parseTimestamp(timestampKey: string): Date | null {
		// Example input: "2025-05-15T01-14-18-043255"
		// Goal: "2025-05-15T01:14:18.043255"
		
		// Split date and time:
		const [datePart, timePart] = timestampKey.split('T');
		if (!timePart) return null;
	
		// Replace first two dashes with colons, the rest keep as is or replace last dash with dot for fractional seconds
		// timePart example: "01-14-18-043255"
		// Replace to: "01:14:18.043255"
		
		const parts = timePart.split('-');
		if(parts.length < 3) return null;
	
		const formattedTime = `${parts[0]}:${parts[1]}:${parts[2]}` + (parts[3] ? `.${parts[3]}` : '');
		const isoString = `${datePart}T${formattedTime}`;
	
		const dateObj = new Date(isoString);
		return isNaN(dateObj.getTime()) ? null : dateObj;
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
		if (!this.user?.id) return;

		this.togglePump = !this.togglePump;
		
		if (this.togglePump){
			this.showNotification('Water Pump -> Turn ON');
		} else {
			this.showNotification('Water Pump -> Turn OFF');
		}

		this.actuatorsService.toggle_pump(this.togglePump, this.user.id).subscribe({
			next: (res: any) => {
				console.log(res);
			},

			error: (error: any) => {
				console.error('Failed updating pump toggle: ', error);
				this.togglePump = !this.togglePump;
			}
		})
	}

	toggleSensors(): void {
		if (!this.user?.id) return;

		this.toggleSensorsScheduler = !this.toggleSensorsScheduler;

		if (this.toggleSensorsScheduler){
			this.showNotification('Sensors Updates -> Turn OFF');
		} else {
			this.showNotification('Sensors Updates -> Turn ON');
		}
	
		// Save to localStorage
		localStorage.setItem(this.getSchedulerKey(), JSON.stringify(this.toggleSensorsScheduler));

		// Update backend
		this.actuatorsService.toggle_sensors_scheduler(this.toggleSensorsScheduler, this.user.id).subscribe({
			next: () => console.log('Toggle Scheduler successful'),
			
			error: (error) => {
				console.error('Toggle Scheduler failed', error);
				this.toggleSensorsScheduler = !this.toggleSensorsScheduler;
				localStorage.setItem(this.getSchedulerKey(), JSON.stringify(this.toggleSensorsScheduler));
			}
		});
	}

	toggleIrrigation(): void {
		if (!this.user?.id) return;

		this.toggleIrrigationSystem = !this.toggleIrrigationSystem;

		if (this.toggleIrrigationSystem){
			this.showNotification('Sensors Updates -> Turn OFF');
		} else {
			this.showNotification('Sensors Updates -> Turn ON');
		}

		// Save to localStorage
		localStorage.setItem(this.getIrrigationKey(), JSON.stringify(this.toggleIrrigationSystem));

		// Update backend
		this.actuatorsService.toggle_irrigation_system(this.toggleIrrigationSystem, this.user.id).subscribe({
			next: () => console.log('Toggle Irrigation successful'),

			error: (error) => {
				console.error('Toggle Irrigation failed', error);
				this.toggleIrrigationSystem = !this.toggleIrrigationSystem;
				localStorage.setItem(this.getIrrigationKey(), JSON.stringify(this.toggleIrrigationSystem));
			}
		})
	}

	toggleLogOut(): void {
		sessionStorage.clear();
		localStorage.clear();
		this.router.navigateByUrl('/login')
	}
}
