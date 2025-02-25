import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog'

@Component({
	selector: 'app-weather-dialog',
	templateUrl: './weather-dialog.component.html',
	styleUrl: './weather-dialog.component.css'
})
export class WeatherDialogComponent {

	// Variable that helps us to see which case of weather to display
	isWeekly: boolean = false;
	weatherList: any[] = [];
	cityName: string = '';

	constructor(@Inject(MAT_DIALOG_DATA) public data: any) {
		// Check if the data is for a week (has a 'list' array)
		if (data.weatherData && data.weatherData.list) {
			this.isWeekly = true;
			this.weatherList = data.weatherData.list; 
			this.cityName = data.weatherData.city.name;
		}
	}

	// Method to convert kelvin to celsius
	getCelsius(kelvin: number): number{ 
		return Math.round(kelvin - 273.15);
	}

	// Method to convert timestamp to a readable date
	getDate(timestamp: number): string {
		// Convert miliseconds
		const date = new Date(timestamp * 1000);
		return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
	}
	
	// Method to get weather icon based on weather condition
	getWeatherIcon(weatherMain: string): string {
		switch (weatherMain.toLowerCase()) {
			case 'clear':
				return 'wb_sunny';

			case 'clouds':
				return 'wb_cloudy';

			case 'rain':
				return 'umbrella';

			case 'snow':
				return 'ac_unit';

			case 'thunderstorm':
				return 'flash_on';

			case 'drizzle':
				return 'grain';

			case 'mist':
			case 'smoke':
			case 'haze':
			case 'fog':
				return 'cloud';

			default:
				return 'wb_sunny';
		}
	}
}
