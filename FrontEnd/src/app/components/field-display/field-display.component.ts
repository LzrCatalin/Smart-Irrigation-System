import { Component, Inject } from '@angular/core';
import { Field } from '../../models/field.model';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
	selector: 'app-field-display',
	templateUrl: './field-display.component.html',
	styleUrl: './field-display.component.css'
})
export class FieldDisplayComponent {
	field: Field;

	constructor(public dialogRef: MatDialogRef<FieldDisplayComponent>,
		@Inject(MAT_DIALOG_DATA) public data: {field: Field }
	) {
		this.field = data.field;
	}

	close(): void {
		this.dialogRef.close();
	}
}
