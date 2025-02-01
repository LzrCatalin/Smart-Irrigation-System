import { Component, OnInit } from '@angular/core';
import { Field } from '../../models/field.model';
import { Sensor } from '../../models/sensor.model';
import { SensorType } from '../../models/sensor-type.model';
import { Status } from '../../models/status.model';
import { Type } from '../../models/type.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { Router } from '@angular/router';

declare var google: any;

@Component({
	selector: 'app-add-field',
	templateUrl: './add-field.component.html',
	styleUrls: ['./add-field.component.css']
})
export class AddFieldComponent implements OnInit {
	user: User | undefined;

	field!: Field;

	availableSensors: Sensor[] = [
		{
		id: '1',
		name: 'Humidity Sensor 1',
		type: {
			type: Type.HUMIDITY,
			measuredValue: 'Humidity',
			status: Status.AVAILABLE,
			port: 'A1'
		}
		},
		{
		id: '2',
		name: 'Temperature Sensor 1',
		type: {
			type: Type.TEMPERATURE,
			measuredValue: 'Temperature',
			status: Status.AVAILABLE,
			port: 'A2'
		}
		}
	];

	selectedSensors: Sensor[] = [];

	map: any;
	marker: any;

	constructor(private fieldService: FieldsService, private router: Router) {}

	ngOnInit(): void {
		this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;

		this.field = {
			id: '',
			latitude: 0,
			longitude: 0,
			length: 0,
			width: 0,
			slope: 0,
			soil_type: '',
			crop_name: '',
			user_id: this.user?.id || '',
			sensors: []
		};

		this.initMap();
	}

	initMap(): void {
		const center = { lat:46.0, lng: 25.0 };
		this.map = new google.maps.Map(document.getElementById('map'), {
			center: center,
			zoom: 6
		});

		this.map.addListener('click', (event: any) => {
			this.placeMarker(event.latLng);
		});
	}

	placeMarker(location: any): void {
		if (this.marker) {
			this.marker.setPosition(location);
		
		} else {
			this.marker = new google.maps.Marker({
				position: location, 
				map: this.map
			});
		}

		this.field.latitude = location.lat();
		this.field.longitude = location.lng();
	}

	onSensorSelect(event: Event): void {
		const selectElement = event.target as HTMLSelectElement;
		const sensorId = selectElement.value;
		const selectedSensor = this.availableSensors.find(s => s.id === sensorId);

		if (selectedSensor && !this.selectedSensors.includes(selectedSensor)) {
			this.selectedSensors.push(selectedSensor);
		}
	}

	removeSensor(sensor: Sensor): void {
		this.selectedSensors = this.selectedSensors.filter(s => s.id !== sensor.id);
	}

	onSubmit(): void {
		console.log(this.field.crop_name)
		this.field.sensors =  this.selectedSensors;

		this.fieldService.add_field(this.field.latitude, this.field.longitude,
									this.field.length, this.field.width, this.field.slope,
									this.field.crop_name, this.field.soil_type,
									this.field.user_id, this.field.sensors).subscribe
		({
			next: (response: any) => {
				console.log(response)
				this.router.navigateByUrl('/home')
			},
			error: (error) => {
				console.error("Error" + error)
			}
		})
	}
}
