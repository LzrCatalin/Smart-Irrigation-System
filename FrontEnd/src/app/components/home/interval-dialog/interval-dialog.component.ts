import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
	selector: 'app-interval-dialog',
	templateUrl: './interval-dialog.component.html',
	styleUrls: ['./interval-dialog.component.css']
})
export class IntervalDialogComponent {
	interval: number;

	constructor(
		public dialogRef: MatDialogRef<IntervalDialogComponent>,
		@Inject(MAT_DIALOG_DATA) public data: {title: string; intervalValue: number}
	)
	{
		this.interval = data.intervalValue;
	}

	onSave(): void {
		this.dialogRef.close(this.interval);
	}

	onCancel(): void {
		this.dialogRef.close();
	}
}
