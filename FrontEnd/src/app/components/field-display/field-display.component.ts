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
	irrigationHistory!: IrrigationHistory;
	

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
		
		// Fetch updates on a time period
		this.fieldsSubscription = interval(5000) // 5 seconds
			.pipe(
				switchMap(() => this.fieldsService.get_user_fields(this.user?.id ?? ''))
			)
			.subscribe({
				next: (fields: Field[]) => {
					const updateField = fields.find(f => f.id === this.field.id);

					if (updateField) {
						this.field = updateField;
					}
				},

				error: (error) => {
					console.error("Error fetching fields: ", error);
				}
			})

		// Fetch field location based on coordonates
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
		})

		// Fetch field history
		this.fetchHistory(this.field.id);
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

	toggleEditMode(): void {
		this.editMode = !this.editMode;
		if (this.editMode) {

			// Patch the form with the current field values
			this.fieldForm.patchValue({
				crop_name: this.field.crop_name,
				length: this.field.length,
				width: this.field.width,
				slope: this.field.slope
			});
		}
	}

  	deleteSensor(sensor: Sensor): void {
		console.log("Deleted sensor: ", sensor);
		// Remove the sensor from the field's sensors list
		this.field.sensors = this.field.sensors.filter(s => s !== sensor);	
		
		// Add the deleted sensor to the deletedSensors list
		this.deletedSensors.push(sensor);
	}
	

	addSensor(sensor: Sensor): void {
		// Add the sensor to the field's sensors list if it doesn't already exist
		if (!this.field.sensors.some(s => s.id === sensor.id)) {
			this.field.sensors.push(sensor);
		}

		// Remove the sensor from the available sensors list
		this.availableSensors = this.availableSensors.filter(s => s !== sensor);
	}

	openConfigDialog(): void {
		const dialogRef = this.dialog.open(ConfigDialogComponent, {
			width: '400px',
			data: { fieldId: this.field.id }
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
}
