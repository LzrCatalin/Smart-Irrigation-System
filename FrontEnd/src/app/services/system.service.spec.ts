import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SystemService } from './system.service';
import { environment } from '../../environments/environment';

describe('SystemService', () => {
  let service: SystemService;
  let httpMock: HttpTestingController;

  const raspberry_id = environment.raspberry_id;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SystemService]
    });

    service = TestBed.inject(SystemService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should toggle sensors scheduler', () => {
    service.toggle_sensors_scheduler(true, 'user123').subscribe(response => {
      expect(response).toEqual({ toggled: true });
    });

    const req = httpMock.expectOne(`http://${raspberry_id}:5000/api/system/scheduler/toggle`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ state: 1, user_id: 'user123' });
    req.flush({ toggled: true });
  });

  it('should toggle irrigation system', () => {
    service.toggle_irrigation_system(false, 'user123').subscribe(response => {
      expect(response).toEqual({ toggled: true });
    });

    const req = httpMock.expectOne(`http://${raspberry_id}:5000/api/system/irrigation/toggle`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ state: 0, user_id: 'user123' });
    req.flush({ toggled: true });
  });
});
