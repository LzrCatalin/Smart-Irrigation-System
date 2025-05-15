export interface UserAlerts {
	user_id: string;
	alerts: {
		[timestamp: string]: {
			message: string;
			type: string;
		};
	};
}