import { Component, Inject } from '@angular/core';
import { User } from '../../models/user.model';
import { Field } from '../../models/field.model';
import { Sensor } from '../../models/sensor.model';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SensorsService } from '../../services/sensors.service';
import { FieldsService } from '../../services/fields.service';
import { ApiService } from '../../services/api.service';
import { interval, Observable, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { ConfigDialogComponent } from './config-dialog/config-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { IrrigationHistory } from '../../models/irrigation-history.mode';
import { HistoryService } from '../../services/history.service';

@Component({
	selector: 'app-field-display',
	templateUrl: './field-display.component.html',
	styleUrl: './field-display.component.css'
})
export class FieldDisplayComponent {
	user: User | undefined;
	field: Field;
	fieldLocation: string = "";
	editMode: boolean = false;
  	fieldForm!: FormGroup;
	availableSensors: Sensor[] = [];
	deletedSensors: Sensor[] = [];
	fieldsSubscription!: Subscription;
	irrigationHistory: IrrigationHistory = {
		fieldId: '',
		history: []
	};
	showAllHistory = false;

	constructor(public dialogRef: MatDialogRef<FieldDisplayComponent>,
		@Inject(MAT_DIALOG_DATA) public data: {field: Field },
		private fb: FormBuilder,
		private sensorsService: SensorsService,
		private fieldsService: FieldsService,
		private historyService: HistoryService,
		private apiService: ApiService,
		private dialog: MatDialog
	) {
		this.field = data.field;
	}

	ngOnInit(): void {
		this.user = JSON.parse(sessionStorage.getItem('user') || '{}').user_data as User;
	
		this.fieldForm = this.fb.group({
			crop_name: [this.field.crop_name, Validators.required],
			length: [this.field.length, [Validators.required, Validators.min(1)]],
			width: [this.field.width, [Validators.required, Validators.min(1)]],
			slope: [this.field.slope, [Validators.required, Validators.min(0)]]
		});
	
		this.fetchAvailableSensors("available");
	
		// PORNEȘTE auto-update DOAR dacă NU e în edit mode
		this.startFieldPolling();
	
		// Fetch location
		this.apiService.getLocation(this.field.latitude, this.field.longitude).subscribe({
			next: (response) => {
				if (response.status === "OK" && response.results.length > 0) {
				this.fieldLocation = response.results[0].formatted_address.slice(8);
				} else {
				this.fieldLocation = "Location not found.";
				}
			},
			error: (error) => {
				console.error("Failed to fetch location for selected field: ", error);
			}
		});
	
		this.fetchHistory(this.field.id);
	}

	ngOnDestroy(): void {
		if (this.fieldsSubscription) {
			this.fieldsSubscription.unsubscribe();
		}
	}

	////////////////////////
	//
	//
	//
	////////////////////////
	fetchAvailableSensors(status: string) {
		this.sensorsService.get_sensors_by_status(status).subscribe({
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
		})
	}

	updateField(): void {
		if (this.fieldForm.valid) {
			this.field.crop_name = this.fieldForm.value.crop_name;
			this.field.length = this.fieldForm.value.length;
			this.field.width = this.fieldForm.value.width;
			this.field.slope = this.fieldForm.value.slope;
			this.toggleEditMode();
		}
	}

	startFieldPolling(): void {
		this.fieldsSubscription = interval(15000)
			.pipe(switchMap(() => this.fieldsService.get_user_fields(this.user?.id ?? '')))
				.subscribe({
					next: (fields: Field[]) => {
						const updateField = fields.find(f => f.id === this.field.id);
				
						if (updateField && !this.editMode) {
							this.field.length = updateField.length;
							this.field.width = updateField.width;
							this.field.slope = updateField.slope;
							this.field.crop_name = updateField.crop_name;
							this.field.latitude = updateField.latitude;
							this.field.longitude = updateField.longitude;
				
							// Update sensors only if no local changes exist
							const localChanges = this.deletedSensors.length > 0 || 
												this.field.sensors.length !== updateField.sensors.length;
				
							if (!localChanges) {
								this.field.sensors = updateField.sensors;
							}
						}
					},

					error: (error) => {
						console.error("Error fetching fields: ", error);
					}
		});
	}

	  
	toggleEditMode(): void {
		this.editMode = !this.editMode;

		if (this.editMode) {
			// Stop auto refresh
			if (this.fieldsSubscription) {
				this.fieldsSubscription.unsubscribe();
			}

			// Patch the form
			this.fieldForm.patchValue({
				crop_name: this.field.crop_name,
				length: this.field.length,
				width: this.field.width,
				slope: this.field.slope
			});

		} else {
			// Resume auto refresh
			this.startFieldPolling();
		}
	}

	deleteSensor(sensor: Sensor): void {
		// Remove sensor from field's active sensors
		this.field.sensors = this.field.sensors.filter(s => s.id !== sensor.id);
	
		// Put it into the availableSensors list if missing
		if (!this.availableSensors.some(s => s.id === sensor.id)) {
			this.availableSensors.push(sensor);
		}
	
		// Add to deleted list for saving
		if (!this.deletedSensors.some(s => s.id === sensor.id)) {
			this.deletedSensors.push(sensor);
		}
	}
	

	addSensor(sensor: Sensor): void {
		// Add the sensor to the field's sensors list if it doesn't already exist
		if (!this.field.sensors.some(s => s.id === sensor.id)) {
			this.field.sensors.push(sensor);
		}

		// Remove the sensor from the available sensors list
		this.availableSensors = this.availableSensors.filter(s => s.id !== sensor.id);

		// If sensor is marked as deleted, do not put it back to deleted sensors list
		this.deletedSensors = this.deletedSensors.filter(s => s.id !== sensor.id);
	}

	openConfigDialog(): void {
		const dialogRef = this.dialog.open(ConfigDialogComponent, {
			width: '23vw',
			height: '26vw',
			data: { 
				fieldId: this.field.id,
				userId: this.user?.id
			}
		});
	
		dialogRef.afterClosed().subscribe(
			result => {
				if (result) {
					console.log("Configuration saved: ", result);
				}
		});
	}

	onSubmit(): void {
		if (this.fieldForm.valid) {
			// Update the field with the new values from the form
			this.field.crop_name = this.fieldForm.value.crop_name;
			this.field.length = this.fieldForm.value.length;
			this.field.width = this.fieldForm.value.width;
			this.field.slope = this.fieldForm.value.slope;
		
			// Call the service to update the field
			this.fieldsService.update_field(
				this.field.id,
				this.field.latitude,
				this.field.longitude,
				this.field.length,
				this.field.width,
				this.field.slope,
				this.field.crop_name,
				this.field.soil_type,
				this.user?.id!,
				this.field.sensors,
				this.deletedSensors
			).subscribe({
				next: (response: Field) => {
					console.log(response);
					this.dialogRef.close(response);
					this.dialogRef.close({ success: true, field: response });
				},

				error: (error) => {
					console.error("Error updating field:", error);
					this.dialogRef.close({ success: false, error: error });
				}
			});
		}
	}

	close(): void {
		this.dialogRef.close();
	}

	fetchHistory(field_id: string): void {
		this.historyService.fetch_field_history(field_id).subscribe({
			next: (response: IrrigationHistory) => {
				console.log(response);
				this.irrigationHistory = {
					...response,
					history: response.history.map(dateStr => 
						dateStr.replace(/(\d{4}-\d{2}-\d{2}T\d{2})-(\d{2})-(\d{2})-(\d+)/, '$1:$2:$3.$4')
					)
				};
			},

			error: (error: IrrigationHistory[]) => {
				console.log(error);
			}
		})
	}


	toggleHistory(): void {
		this.showAllHistory = !this.showAllHistory;
	}
}
