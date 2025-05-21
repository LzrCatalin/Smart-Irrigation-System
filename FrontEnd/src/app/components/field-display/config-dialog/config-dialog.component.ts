import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { SystemService } from '../../../services/system.service';

@Component({
	selector: 'app-config-dialog',
	templateUrl: './config-dialog.component.html',
	styleUrl: './config-dialog.component.css'
})
export class ConfigDialogComponent {
	configForm !: FormGroup;
	fieldId: string;
	userId: string;

	constructor(
		private fb: FormBuilder,
		public dialogRef: MatDialogRef<ConfigDialogComponent>,
		private systemService: SystemService,
		@Inject(MAT_DIALOG_DATA) public data: {fieldId: string, userId: string}
	)
	{
		this.fieldId = data.fieldId;
		this.userId = data.userId;
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
				userId: this.userId,
				...this.configForm.value
			};
			
			this.systemService.update_field_config(result).subscribe({
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
