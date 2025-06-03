import { Component, OnInit } from '@angular/core';
import { Field } from '../../models/field.model';
import { Sensor } from '../../models/sensor.model';
import { User } from '../../models/user.model';
import { FieldsService } from '../../services/fields.service';
import { Router } from '@angular/router';
import { SensorsService } from '../../services/sensors.service';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSelectChange } from '@angular/material/select';
import { SystemService } from '../../services/system.service';

declare var google: any;

@Component({
selector: 'app-add-field',
templateUrl: './add-field.component.html',
styleUrls: ['./add-field.component.css']
})
export class AddFieldComponent implements OnInit {
	user: User | undefined;
	field!: Field;
	availableSensors: Sensor[] = [];
	selectedSensors: Sensor[] = [];

	map: any;
	marker: any;

	constructor(
		private fieldService: FieldsService,
		private router: Router,
		private sensorService: SensorsService,
		private dialogRef: MatDialogRef<AddFieldComponent>,
		private systemService: SystemService
	) {}

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

		this.fetchAvailableSensors("available");
		this.initMap();
	}

	initMap(): void {
		const center = { lat: 46.0, lng: 25.0 };
		this.map = new google.maps.Map(document.getElementById('map'), {
			center: center,
			zoom: 6
		});

		this.map.addListener('click', (event: any) => {
			this.placeMarker(event.latLng);
		});
	}

	fetchAvailableSensors(status: string) {
		this.sensorService.get_sensors_by_status(status).subscribe({
			next: (response) => {
				this.availableSensors = response.map(sensor => ({
				id: sensor.id,
				name: sensor.name,
				type: {
					type: sensor.type.type,
					measured_value: sensor.type.measured_value,
					status: sensor.type.status,
					port: sensor.type.port
				}
				}));
			},
			error: (error) => {
				console.error(error);
			}
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

	onSensorSelect(event: MatSelectChange): void {
		const newlySelected: Sensor[] = event.value;
		const addedSensors = newlySelected.filter(s => !this.selectedSensors.find(sel => sel.id === s.id));

		addedSensors.forEach(sensor => {
		if (!this.selectedSensors.find(s => s.id === sensor.id)) {
			this.selectedSensors.push(sensor);
			this.availableSensors = this.availableSensors.filter(s => s.id !== sensor.id);
		}
		});
	}

	removeSensor(sensor: Sensor): void {
		this.selectedSensors = this.selectedSensors.filter(s => s.id !== sensor.id);
		if (!this.availableSensors.find(s => s.id === sensor.id)) {
			this.availableSensors.push(sensor);
		}
	}

	onSubmit(): void {
		this.field.sensors = this.selectedSensors;
		this.fieldService.add_field(
		this.field.latitude, this.field.longitude,
		this.field.length, this.field.width, this.field.slope,
		this.field.crop_name, this.field.soil_type,
		this.field.user_id, this.field.sensors
		).subscribe({
			next: (response: Field) => {
				this.dialogRef.close(response);
			},
			error: (error) => {
				console.error("Error" + error);
			}
		});
	}

	onCancel(): void {
		this.dialogRef.close();
	}

	compareSensors(a: Sensor, b: Sensor): boolean {
		return a && b ? a.id === b.id : a === b;
	}
}
