import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
	selector: 'app-register',
	templateUrl: './register.component.html',
	styleUrl: './register.component.css'
})
export class RegisterComponent {
	user: User | undefined;
	email: string;
	password: string;

	constructor(private router: Router, private authSerrvice: AuthService) {
		this.email = '';
		this.password = '';
	}

	onRegister(): void {
		this.authSerrvice.register(this.email, this.password).subscribe({
			
			next: () => {
				console.log("Register successfully");
				this.router.navigateByUrl('');
			},

			error: (error) => {
				console.log("Registration failed", error);
			}
		})
	}
}
