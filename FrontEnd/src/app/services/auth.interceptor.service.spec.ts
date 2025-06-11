import { TestBed } from '@angular/core/testing';
import { HTTP_INTERCEPTORS, HttpClient} from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthInterceptorService } from './auth.interceptor.service';

describe('AuthInterceptorService', () => {
  let httpMock: HttpTestingController;
  let httpClient: HttpClient;

  const testUrl = '/dummy';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        {
          provide: HTTP_INTERCEPTORS,
          useClass: AuthInterceptorService,
          multi: true
        }
      ]
    });

    httpMock = TestBed.inject(HttpTestingController);
    httpClient = TestBed.inject(HttpClient);
  });

  afterEach(() => {
    httpMock.verify();
    sessionStorage.clear();
  });

  it('should add Authorization header when token is present in sessionStorage', () => {
    const token = 'mocked-access-token';
    sessionStorage.setItem('access_token', token);

    httpClient.get(testUrl).subscribe(response => {
      expect(response).toBeTruthy();
    });

    const req = httpMock.expectOne(testUrl);
    expect(req.request.headers.has('Authorization')).toBeTrue();
    expect(req.request.headers.get('Authorization')).toBe(`Bearer ${token}`);

    req.flush({ success: true });
  });

  it('should NOT add Authorization header when no token is present', () => {
    sessionStorage.removeItem('access_token');

    httpClient.get(testUrl).subscribe(response => {
      expect(response).toBeTruthy();
    });

    const req = httpMock.expectOne(testUrl);
    expect(req.request.headers.has('Authorization')).toBeFalse();

    req.flush({ success: true });
  });
});
