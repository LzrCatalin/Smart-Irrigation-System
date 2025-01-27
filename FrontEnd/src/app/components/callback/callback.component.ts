import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { User } from '../../models/user-model';

@Component({
	selector: 'app-callback',
	templateUrl: './callback.component.html',
	styleUrl: './callback.component.css'
})
export class CallbackComponent {

	constructor(private routeSnapshot: ActivatedRoute, private router: Router) {}

	ngOnInit(): void {
		console.log("CallBack component");

		const access_token = this.routeSnapshot.snapshot.queryParamMap.get('access_token');
		const user_data = this.routeSnapshot.snapshot.queryParamMap.get('user_data');
		const token = this.routeSnapshot.snapshot.queryParamMap.get('token');

		if (access_token && user_data && token) {
			if (typeof sessionStorage !== 'undefined') {
			// sessionStorage.setItem('access_token', access_token);
			const sanitizedUserData = user_data.replace(/'/g, '"');
			const parsedUserData = JSON.parse(sanitizedUserData);

			// Construct the user object
			const user = {
				user_data: parsedUserData as User,
				token: token
			};

			console.log("User object:", user);
			sessionStorage.setItem('user', JSON.stringify(user));
			this.router.navigateByUrl('/home');
			
			} else {
				console.log("Session storage is not supported");
				this.router.navigateByUrl('/login');
			}

		} else {
			console.log("Failed to retrieve access token and user data");
			this.router.navigateByUrl('/login');
		}
	}
}
