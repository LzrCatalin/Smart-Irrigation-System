import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ActuatorsService } from '../../../services/actuators.service';

@Component({
	selector: 'app-config-dialog',
	templateUrl: './config-dialog.component.html',
	styleUrl: './config-dialog.component.css'
})
export class ConfigDialogComponent {
	configForm !: FormGroup;
	fieldId: string;

	constructor(
		private fb: FormBuilder,
		public dialogRef: MatDialogRef<ConfigDialogComponent>,
		private actuatorService: ActuatorsService,
		@Inject(MAT_DIALOG_DATA) public data: {fieldId: string}
	)
	{
		this.fieldId = data.fieldId;
	}

	ngOnInit(): void {
		this.configForm = this.fb.group({
			target_humidity: ['', Validators.required],
			min_humidity: ['', Validators.required],
			max_watering_time: ['', Validators. required],
		});
	}

	onSubmit(): void {
		if (this.configForm.valid)
		{
			const result = {
				fieldId: this.fieldId,
				...this.configForm.value
			};
			
			this.actuatorService.update_field_config(result).subscribe({
				next: (response: any) => {
					console.log(response);
				},
				
				error: (error: any) => {
					console.error(error)
				}
			})
			
			this.dialogRef.close(result);
		}
	}

	onCancel(): void {
		this.dialogRef.close();
	}
}
