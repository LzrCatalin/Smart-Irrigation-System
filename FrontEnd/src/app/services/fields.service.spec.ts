import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FieldsService } from './fields.service';
import { Field } from '../models/field.model';
import { Sensor } from '../models/sensor.model';
import { Type } from '../models/type.model';
import { Status } from '../models/status.model';

describe('FieldsService', () => {
  let service: FieldsService;
  let httpMock: HttpTestingController;

  const mockSensors: Sensor[] = [
    {
      id: 's1',
      name: 'Sensor 1',
      type: {
        type: Type.HUMIDITY,
        measured_value: '30%',
        status: Status.AVAILABLE,
        port: 'A0'
      }
    }
  ];

  const mockField: Field = {
    id: 'f1',
    latitude: 45.0,
    longitude: 24.0,
    length: 100,
    width: 50,
    slope: 5,
    soil_type: 'Loam',
    crop_name: 'Tomatoes',
    user_id: 'u1',
    sensors: mockSensors
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [FieldsService]
    });

    service = TestBed.inject(FieldsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get user fields', () => {
    const userId = 'u1';

    service.get_user_fields(userId).subscribe(fields => {
      expect(fields.length).toBe(1);
      expect(fields[0]).toEqual(mockField);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/fields/all/${userId}`);
    expect(req.request.method).toBe('GET');
    req.flush([mockField]);
  });

  it('should add a field', () => {
    service.add_field(
      mockField.latitude,
      mockField.longitude,
      mockField.length,
      mockField.width,
      mockField.slope,
      mockField.crop_name,
      mockField.soil_type,
      mockField.user_id,
      mockField.sensors
    ).subscribe(field => {
      expect(field).toEqual(mockField);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/fields`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body.crop_name).toBe('Tomatoes');
    req.flush(mockField);
  });

  it('should update a field', () => {
    service.update_field(
      mockField.id,
      mockField.latitude,
      mockField.longitude,
      mockField.length,
      mockField.width,
      mockField.slope,
      mockField.crop_name,
      mockField.soil_type,
      mockField.user_id,
      mockField.sensors,
      [] // no deleted sensors
    ).subscribe(field => {
      expect(field).toEqual(mockField);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/fields/${mockField.id}`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body.field_data.crop_name).toBe('Tomatoes');
    req.flush(mockField);
  });

  it('should delete a field', () => {
    const sensorsToDelete = ['Sensor 1'];

    service.delete_field(mockField.id, sensorsToDelete).subscribe(field => {
      expect(field).toEqual(mockField);
    });

    const req = httpMock.expectOne({
      method: 'DELETE',
      url: `http://localhost:5000/api/fields/${mockField.id}`
    });

    expect(req.request.body).toEqual({ sensors_name: sensorsToDelete });
    req.flush(mockField);
  });
});
