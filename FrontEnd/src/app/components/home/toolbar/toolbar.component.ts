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

  hoveredButton: string | null = null;

  infoMessages: { [key: string]: string } = {
    toggleDrawer: 'View alerts and notifications',
    createField: 'Create a new field',
    waterPump: 'Manually control the water pump',
    toggleSensors: 'Start or pause sensor readings',
    toggleIrrigation: 'Start or pause automatic irrigation',
    logout: 'Log out of your account'
  };

  emitters: { [key: string]: EventEmitter<void> } = {};

  ngOnInit(): void {
    this.emitters = {
      toggleDrawer: this.toggleDrawer,
      createField: this.createField,
      waterPump: this.waterPump,
      toggleSensors: this.toggleSensors,
      toggleIrrigation: this.toggleIrrigation,
      logout: this.logout
    };
  }

  emit(key: string): void {
    this.emitters[key]?.emit();
  }
}
