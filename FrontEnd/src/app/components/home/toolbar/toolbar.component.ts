import { Component, Output, EventEmitter, Input } from '@angular/core';
import { Field } from '../../../models/field.model';

@Component({
	selector: 'app-toolbar',
	templateUrl: './toolbar.component.html',
	styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent {
	@Input() selectedField: Field | null = null;
	@Output() toggleDrawer = new EventEmitter<void>();
	@Output() createField = new EventEmitter<void>();
	@Output() waterPump = new EventEmitter<void>();
	@Output() toggleSensors = new EventEmitter<void>();
	@Output() toggleIrrigation = new EventEmitter<void>();
	@Output() logout = new EventEmitter<void>();
}
