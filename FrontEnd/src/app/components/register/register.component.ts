import { Component } from '@angular/core';
import { User } from '../../models/user.model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user: User | undefined;
  email: string = '';
  password: string = '';
  confirmPassword: string = '';

  constructor(private router: Router, private authSerrvice: AuthService) {}

  onRegister(): void {
    if (this.password !== this.confirmPassword) {
      console.log('Passwords do not match');
      return;
    }

    this.authSerrvice.register(this.email, this.password).subscribe({
      next: () => {
        console.log('Register successfully');
        this.router.navigateByUrl('');
      },
      error: (error) => {
        console.log('Registration failed', error);
      }
    });
  }
}
