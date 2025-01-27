import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';


@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.css']
})

export class LoginComponent {
	email: string;
	password: string;
	user: User | undefined;

	constructor(private authService: AuthService,
				private router: Router) {
		this.email = '';
		this.password = '';
	}

	onLogin(): void {
		console.log("Trying to login with: ", this.email, this.password)
		this.authService.login(this.email, this.password).subscribe({

			next: (data: User) => {
				this.user = data;
				sessionStorage.setItem('user', JSON.stringify(this.user));
				// Redirect home
				this.router.navigateByUrl('/home');
			},

			error: () => {
				console.log("Failed to log in.");
			}
		});
	}


	loginWithGoogle(): void {
		console.log("Google Auth selected...");
		window.location.href = 'http://192.168.1.12:5000/login';
	}
}
