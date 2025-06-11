import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AlertsService } from './alerts.service';
import { AlertDefinition } from '../models/alerts-definition.model';

describe('AlertsService', () => {
  let service: AlertsService;
  let httpMock: HttpTestingController;

  const mockAlerts: AlertDefinition[] = [
    {
      user_id: 'u123',
      message: 'Humidity too low in field 1',
      alert_type: 'HUMIDITY',
      timestamp: '2024-06-01T12:00:00Z'
    },
    {
      user_id: 'u123',
      message: 'Temperature exceeds safe limit',
      alert_type: 'TEMPERATURE',
      timestamp: '2024-06-01T13:00:00Z'
    }
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AlertsService]
    });

    service = TestBed.inject(AlertsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch user alerts', () => {
    const userId = 'u123';

    service.get_user_alerts(userId).subscribe(alerts => {
      expect(alerts.length).toBe(2);
      expect(alerts).toEqual(mockAlerts);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/alerts/${userId}`);
    expect(req.request.method).toBe('GET');

    req.flush(mockAlerts);
  });
});
