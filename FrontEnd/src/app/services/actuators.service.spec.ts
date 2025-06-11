import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ActuatorsService } from './actuators.service';
import { environment } from '../../environments/environment';

describe('ActuatorsService', () => {
  let service: ActuatorsService;
  let httpMock: HttpTestingController;

  const raspberryURL = `http://${environment.raspberry_id}:5000`;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ActuatorsService]
    });

    service = TestBed.inject(ActuatorsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should toggle pump with correct payload', () => {
    const userId = 'u123';
    const fieldId = 'f456';
    const state = true;

    service.toggle_pump(state, userId, fieldId).subscribe(response => {
      expect(response).toEqual({ success: true });
    });

    const req = httpMock.expectOne(`${raspberryURL}/api/actuators/waterpump/toggle`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({
      state: 1,
      user_id: userId,
      field_id: fieldId
    });

    req.flush({ success: true });
  });

  it('should send state as 0 when pump is turned off', () => {
    service.toggle_pump(false, 'u1', 'f1').subscribe();

    const req = httpMock.expectOne(`${raspberryURL}/api/actuators/waterpump/toggle`);
    expect(req.request.body.state).toBe(0);
    req.flush({});
  });
});
