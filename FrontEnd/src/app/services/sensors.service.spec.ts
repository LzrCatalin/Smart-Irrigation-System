import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SensorsService } from './sensors.service';
import { Sensor } from '../models/sensor.model';
import { Type } from '../models/type.model';
import { Status } from '../models/status.model';

describe('SensorsService', () => {
  let service: SensorsService;
  let httpMock: HttpTestingController;

  const mockSensors: Sensor[] = [
    {
      id: '1',
      name: 'Humidity Sensor',
      type: {
        type: Type.HUMIDITY,
        measured_value: '32%',
        status: Status.AVAILABLE,
        port: 'A0'
      }
    },
    {
      id: '2',
      name: 'Temperature Sensor',
      type: {
        type: Type.TEMPERATURE,
        measured_value: '25°C',
        status: Status.NOT_AVAILABLE,
        port: 'A1'
      }
    }
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SensorsService]
    });

    service = TestBed.inject(SensorsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch sensors by status', () => {
    const status = 'active';

    service.get_sensors_by_status(status).subscribe((sensors: Sensor[]) => {
      expect(sensors.length).toBe(2);
      expect(sensors).toEqual(mockSensors);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/sensors/status/${status}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockSensors);
  });
});
