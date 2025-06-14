import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { News } from '../../models/news.model';
import { Field } from '../../models/field.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { ActuatorsService } from '../../services/actuators.service';
import { AlertsService } from '../../services/alerts.service';
import { SystemStateService } from "../../services/system-state.service";
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
import { AlertDialogComponent } from './alert-dialog/alert-dialog.component';
import { MatSidenav } from '@angular/material/sidenav';
import { SystemService } from '../../services/system.service';
import { environment } from '../../../environments/environment';
import { interval, Subscription } from 'rxjs';

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
  hasNewAlerts: boolean = false;
  alertPollingSub!: Subscription;
  alertsNumber: number = 0;

	selectedDate = new Date();
	weatherData: any = null;
	showWeatherInput: boolean = false;
	forecastData: { day: string, icon: string, max: number, min: number, avg: number, description: string, humidity: number, wind: number }[] = [];
  geoCity: string = 'Timisoara';
  city: string = 'Timisoara';

	togglePump: boolean = false;
	toggleSensorsScheduler: boolean = true;
	toggleIrrigationSystem: boolean = true;

	schedulerInterval: number = 15;
	irrigationInterval: number = 20;
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
				private alertsService: AlertsService,
				private systemService: SystemService,
        private systemStateService: SystemStateService
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

		this.systemService.update_scheduler_settings(this.schedulerInterval, this.user.id).subscribe({
			next: () => {
        console.log('Scheduler settings updated');
        this.systemStateService.setSchedulerInterval(this.schedulerInterval * 1000);
      },

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

		this.systemService.update_irrigation_settings(this.irrigationInterval, this.user.id).subscribe({
			next: () => console.log('Irrigation settings updated'),

			error: (error : any) => {
				console.error('Failed to update irrigation settings', error);
				this.showNotification('Failed to update irrigation settings', 'Retry', 5000);
			}
		});
	}

  get isSensorsRunning(): boolean {
    // Return true if system is running (toggleSensorsScheduler is true)
    return !this.toggleSensorsScheduler;
  }

  get isIrrigationRunning(): boolean {
    // Return true if system is running (toggleIrrigationSystem is true)
    return !this.toggleIrrigationSystem;
  }

  ngOnInit(): void {
    this.user = JSON.parse(sessionStorage.getItem('user') ?? '{}').user_data as User;

    if (this.user?.id) {
      this.selectedField = null;
      this.fetchUserFields(this.user.id);
      this.fetchUserAlerts(this.user.id);
      this.startAlertPolling(this.user.id);

      this.initializeSystemStates();
      this.syncInitialStates();
    }

    const storedGeoCity = localStorage.getItem('geoCity');
    if (storedGeoCity) {
      this.geoCity = storedGeoCity;
    }

    this.fetchForecast();
    this.fetchFarmingNews();
    this.tryFetchWeatherByGeolocation();

    const savedSchedulerInterval = localStorage.getItem(`${this.getSchedulerKey()}_interval`);
    this.schedulerInterval = savedSchedulerInterval ? parseInt(savedSchedulerInterval) : 15;

    const savedIrrigationInterval = localStorage.getItem(`${this.getIrrigationKey()}_interval`);
    this.irrigationInterval = savedIrrigationInterval ? parseInt(savedIrrigationInterval) : 20;
  }

  startAlertPolling(user_id: string): void {
    this.alertPollingSub = interval(60000).subscribe(() => {
      this.fetchUserAlerts(user_id);
    });
  }

  initializeSystemStates(): void {
    const schedulerKey = this.getSchedulerKey();
    const irrigationKey = this.getIrrigationKey();

    if (localStorage.getItem(schedulerKey) === null) {
      localStorage.setItem(schedulerKey, JSON.stringify(this.toggleSensorsScheduler));
    }
    if (localStorage.getItem(irrigationKey) === null) {
      localStorage.setItem(irrigationKey, JSON.stringify(this.toggleIrrigationSystem));
    }

    this.toggleSensorsScheduler = JSON.parse(localStorage.getItem(schedulerKey) || 'true');
    this.toggleIrrigationSystem = JSON.parse(localStorage.getItem(irrigationKey) || 'true');
  }

  syncInitialStates(): void {
    if (!this.user?.id) return;

    this.systemService.toggle_sensors_scheduler(this.toggleSensorsScheduler, this.user.id).subscribe({
      next: () => console.log('[INIT] Synced sensor state'),
      error: (error) => console.error('[INIT] Sensor sync failed:', error)
    });

    this.systemService.toggle_irrigation_system(this.toggleIrrigationSystem, this.user.id).subscribe({
      next: () => console.log('[INIT] Synced irrigation state'),
      error: (error) => console.error('[INIT] Irrigation sync failed:', error)
    });
  }

  ngOnDestroy(): void {
    if (this.alertPollingSub) {
      this.alertPollingSub.unsubscribe();
    }
  }

  tryFetchWeatherByGeolocation(): void {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;

          this.apiService.getLocation(lat, lon).subscribe({
            next: (response: any) => {
              const cityName = response.results[0].address_components.find((c: any) =>
                c.types.includes("locality") || c.types.includes("administrative_area_level_1")
              )?.long_name;

              if (cityName) {
                this.geoCity = cityName;
                localStorage.setItem('geoCity', cityName);
                this.city = cityName;
                this.fetchForecast();
                this.showNotification(`Showing weather for your location: ${cityName}`);
              } else {
                this.fallbackToDefaultCity();
              }
            },
            error: () => {
              this.fallbackToDefaultCity();
            }
          });
        },
        (error) => {
          console.warn("User denied location access or error occurred:", error.message);
          this.fallbackToDefaultCity();
        }
      );
    } else {
      this.fallbackToDefaultCity();
    }
  }

  fallbackToDefaultCity(): void {
    this.geoCity = 'Timisoara';
    localStorage.setItem('geoCity', 'Timisoara');
    this.city = this.geoCity;
    this.fetchForecast();
    this.showNotification('Showing weather for default location: Timisoara');
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

					this.systemService.delete_field_from_system(field_id).subscribe({
						next: (res: any) => {
							console.log(res);
						},

						err: (err: any) => {
							console.log(err);
						}
					})

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
			width: '25vw',
			height: '45vw',
			data: { field }
		});

		// Display notification after update field functionality
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


  selectField(field: Field): void {
    if (this.selectedField?.id === field.id) {
        this.selectedField = null;
        this.city = this.geoCity;
        this.fetchForecast();
        this.showNotification(`Field deselected. Showing weather for ${this.geoCity}.`);

    } else {
        this.selectedField = field;
    }
  }

	//////////////////////
	//
	//	Fetch farming news
	//
	//////////////////////
	fetchFarmingNews(): void {
		this.apiService.getFarmingNews().subscribe({
			next: (response: any) => {
        this.newsItems = response.articles
          .filter((article: any) => {
            const content = `${article.title} ${article.description ?? ''}`.toLowerCase();
            return content.includes('agriculture') ||
              content.includes('farmers') || content.includes('crop') ||
              content.includes('john deer');
          })
          .map((article: any) => ({
            title: article.title,
            imageUrl: article.urlToImage ?? 'https://via.placeholder.com/150',
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

  fetchForecast(): void {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${this.city}&units=metric&appid=${environment.weatherApiKey}`;

    this.apiService.getExternal(url).subscribe({
      next: (response: any) => {
        const groupedByDay: { [key: string]: any[] } = {};
        response.list.forEach((item: any) => {
          const date = new Date(item.dt_txt);
          const day = date.toLocaleDateString('en-US', { weekday: 'short' });
          if (!groupedByDay[day]) groupedByDay[day] = [];
          groupedByDay[day].push(item);
        });

        this.forecastData = Object.entries(groupedByDay).slice(0, 7).map(([day, items]: [string, any[]]) => {
          const temps = items.map((entry: any) => entry.main.temp);
          const min = Math.min(...temps);
          const max = Math.max(...temps);
          const avg = temps.reduce((a, b) => a + b, 0) / temps.length;

          const iconCode = items[0].weather[0].icon;
          const icon = `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
          const description = items[0].weather[0].description;

          const humidity = Math.round(
            items.reduce((sum, entry) => sum + entry.main.humidity, 0) / items.length
          );

          const wind = Math.round(
            items.reduce((sum, entry) => sum + entry.wind.speed, 0) / items.length
          );

          return {
            day,
            min: Math.round(min),
            max: Math.round(max),
            avg: Math.round(avg),
            icon,
            description,
            humidity,
            wind
          };
        });
      },
      error: (error) => {
        console.error('Failed to fetch forecast:', error);
      }
    });
  }

	checkWeatherForSelectedField(): void {
		if (!this.selectedField) return;

		this.apiService.getLocation(this.selectedField.latitude, this.selectedField.longitude).subscribe({
			next: (response) => {
				if (response.status === "OK" && response.results.length > 0) {
					const cityName = response.results[0].address_components.find((c: any) =>
						c.types.includes("locality") ?? c.types.includes("administrative_area_level_1")
					)?.long_name;

					if (cityName) {
						this.city = cityName;
						this.fetchForecast();
						this.showNotification(`Weather updated for ${cityName}`);

					} else {
						this.showNotification("Could not determine city from location.");
					}

				} else {
					this.showNotification("Location lookup failed.");
				}
			},

			error: () => {
				this.showNotification("Error getting location from coordinates.");
			}
		});
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
    console.log("Fetch user alerts")
    this.alertsService.get_user_alerts(user_id).subscribe({
      next: (response: any) => {
        const alertsObject = response.alerts ?? {};
        const alertArray = Object.entries(alertsObject).map(([timestampKey, alert]: [string, any]) => ({
          ...alert,
          timestamp: this.parseTimestamp(timestampKey)
        }));

        const lastAlertsLength = this.alertsNumber;
        this.userAlerts = alertArray;
        this.alertsNumber = alertArray.length;

        if (lastAlertsLength < this.alertsNumber) {
          this.hasNewAlerts = true;
        }
      },

      error: (error) => {
        console.error(error);
      }
    });
  }

	parseTimestamp(timestampKey: string): Date | null {
		const [datePart, timePart] = timestampKey.split('T');
		if (!timePart) return null;

		const parts = timePart.split('-');
		if (parts.length < 3) return null;

		const formattedTime = `${parts[0]}:${parts[1]}:${parts[2]}` + (parts[3] ? `.${parts[3]}` : '');
		const isoString = `${datePart}T${formattedTime}`;

		const dateObj = new Date(isoString);
		if (isNaN(dateObj.getTime())) {
			console.warn('Invalid ISO date:', isoString);
			return null;
		}

		return dateObj;
	}

  toggleAlertDrawer() {
    if (this.user?.id && this.userAlerts.length > 0) {

      if (this.hasNewAlerts) {
        this.hasNewAlerts = false;
      }
    }

    this.dialog.open(AlertDialogComponent, {
      width: '600px',
      data: { alerts: this.userAlerts }
    });
  }

	//////////////////
	//
	//	Side Bar options
	//
	//////////////////
	toggleCreateField(): void {
		const dialogRef = this.dialog.open(AddFieldComponent, {
			width: '42vw',
			height: '42vw',
			data: {}
		});

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('New field added:', result);
        if (this.user?.id) {
          this.fetchUserFields(this.user.id);

          this.fetchUserAlerts(this.user.id);

          this.showNotification('Field added successfully!');
        }
      }
    });
	}

	toggleWaterPump(): void {
		if (!this.selectedField || !this.user?.id) {
			this.showNotification('Please select a field first.', 'OK');
			return;
		}

		this.togglePump = !this.togglePump;

		this.actuatorsService.toggle_pump(this.togglePump, this.user.id, this.selectedField.id).subscribe({
			next: (res: any) => console.log(res),
			error: (error: any) => {
				console.error('Failed updating pump toggle: ', error);
				this.togglePump = !this.togglePump;
			}
		});

    if (this.togglePump) {
      this.showNotification(`Water Pump -> Turn ON for ${this.selectedField.crop_name}`);

    } else {
      this.showNotification(`Water Pump -> Turn OFF for ${this.selectedField.crop_name}`);
    }

    // Update for alerts
    this.fetchUserAlerts(this.user.id);
	}

	toggleSensors(): void {
		if (!this.user?.id) return;

		this.toggleSensorsScheduler = !this.toggleSensorsScheduler;

		if (this.toggleSensorsScheduler){
			this.showNotification('Sensors Updates -> Paused');
		} else {
			this.showNotification('Sensors Updates -> Running');
		}

		// Save to localStorage
		localStorage.setItem(this.getSchedulerKey(), JSON.stringify(this.toggleSensorsScheduler));

		// Update backend
		this.systemService.toggle_sensors_scheduler(this.toggleSensorsScheduler, this.user.id).subscribe({
			next: () => console.log('Toggle Scheduler successful'),

			error: (error) => {
				console.error('Toggle Scheduler failed', error);
				this.toggleSensorsScheduler = !this.toggleSensorsScheduler;
				localStorage.setItem(this.getSchedulerKey(), JSON.stringify(this.toggleSensorsScheduler));
			}
		});

    // Update for alerts
    this.fetchUserAlerts(this.user.id);
	}

	toggleIrrigation(): void {
		if (!this.user?.id) return;

		this.toggleIrrigationSystem = !this.toggleIrrigationSystem;

		if (this.toggleIrrigationSystem){
			this.showNotification('Sensors Updates -> Paused');
		} else {
			this.showNotification('Sensors Updates -> Running');
		}

		// Save to localStorage
		localStorage.setItem(this.getIrrigationKey(), JSON.stringify(this.toggleIrrigationSystem));

		// Update backend
		this.systemService.toggle_irrigation_system(this.toggleIrrigationSystem, this.user.id).subscribe({
			next: () => console.log('Toggle Irrigation successful'),

			error: (error) => {
				console.error('Toggle Irrigation failed', error);
				this.toggleIrrigationSystem = !this.toggleIrrigationSystem;
				localStorage.setItem(this.getIrrigationKey(), JSON.stringify(this.toggleIrrigationSystem));
			}
		})

    // Update for alerts
    this.fetchUserAlerts(this.user.id);
	}

	toggleLogOut(): void {
		sessionStorage.clear();
		localStorage.clear();
		this.router.navigateByUrl('/login')
	}
}
