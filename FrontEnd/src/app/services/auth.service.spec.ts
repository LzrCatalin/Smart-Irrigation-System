import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import { User } from '../models/user.model';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  const mockUser: User = new User('1', 'test@example.com');

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should login and return a user', () => {
    const email = 'test@example.com';
    const password = 'securepass';

    service.login(email, password).subscribe(user => {
      expect(user.email).toBe(email);
      expect(user.id).toBe('1');
    });

    const req = httpMock.expectOne(`http://localhost:5000/login`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ email, password });

    req.flush({ id: '1', email: 'test@example.com' });
  });

  it('should register and return a user', () => {
    const email = 'new@example.com';
    const password = 'newpass';

    service.register(email, password).subscribe(user => {
      expect(user.email).toBe(email);
      expect(user.id).toBe('1');
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/users`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ email, password });

    req.flush({ id: '1', email: 'new@example.com' });
  });
});
