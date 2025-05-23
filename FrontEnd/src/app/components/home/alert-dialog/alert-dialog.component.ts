import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AlertDefinition } from '../../../models/alerts-definition.model';

@Component({
	selector: 'app-alert-dialog',
	templateUrl: './alert-dialog.component.html',
	styleUrls: ['./alert-dialog.component.css']
})

export class AlertDialogComponent {
	selectedAlertType: 'INFO' | 'WARNING' = 'INFO';
	filteredAlerts: any[] = [];
	groupedAlerts: {[data: string]: any[] } = {};
	selectedTimeRange: '24h' | '3d' | '7d' | 'all' = '7d';

	constructor(
		@Inject (MAT_DIALOG_DATA) public data: {
			alerts: any[]
		}
	) {}

	ngOnInit(): void {
		this.selectedAlertType = 'INFO';
		this.filterAlerts();
	}

	// Filter alerts based on selected category
	filterAlerts(): void {
		this.filteredAlerts = this.data.alerts.filter(
			a => a.type === this.selectedAlertType
		);
		
		// Append filtered alerts to another array for more grouping (for each day)
		this.groupedAlerts = this.groupAlertsByDay(this.filteredAlerts);
	}

	// Group filtered alerts based on days (descending)
	private groupAlertsByDay(alerts: any[]): { [day: string]: any[] } {
		const grouped: { [day: string]: any[] } = {};

		let threshold: Date | null = null;
		const now = new Date();

		// Display alerts based user time period pref
		switch (this.selectedTimeRange) {
			case '24h':
				threshold = new Date(now);
				threshold.setHours(now.getHours() - 24);
				break;

			case '3d':
				threshold = new Date(now);
				threshold.setDate(now.getDate() - 3);
				break;

			case '7d':
				threshold = new Date(now);
				threshold.setDate(now.getDate() - 7);
				break;

			case 'all':
			default:
				threshold = null;
		}

		alerts.forEach(alert => {
			if (!alert.timestamp) return;

			const alertDate = new Date(alert.timestamp);
			if (isNaN(alertDate.getTime())) return;

			if (threshold && alertDate < threshold) return;

			const dayStr = alertDate.toLocaleDateString('en-CA'); // YYYY-MM-DD display type
			if (!grouped[dayStr]) grouped[dayStr] = []; // empty list for days w/o alerts
			
			grouped[dayStr].push(alert); // append alert for specific day
		});

		Object.keys(grouped).forEach(day => {
			grouped[day].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
		});

		return grouped;
	}
	
	sortDescending = (a: any, b: any): number => {
		return a.key > b.key ? -1 : 1;
	};

	// Verify if list of alerts is empty or not
	isGroupedAlertsEmpty(): boolean {
		return Object.keys(this.groupedAlerts).length === 0;
	}
}
