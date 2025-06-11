import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HistoryService } from './history.service';
import { IrrigationHistory } from '../models/irrigation-history.mode';

describe('HistoryService', () => {
  let service: HistoryService;
  let httpMock: HttpTestingController;

  const mockHistory: IrrigationHistory = {
    fieldId: 'abc123',
    history: [
      '2024-06-01T12:00:00Z - Irrigation started',
      '2024-06-01T12:10:00Z - Irrigation stopped',
    ]
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [HistoryService]
    });

    service = TestBed.inject(HistoryService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch irrigation history for a field', () => {
    const fieldId = 'abc123';

    service.fetch_field_history(fieldId).subscribe((data: IrrigationHistory) => {
      expect(data.fieldId).toBe('abc123');
      expect(data.history.length).toBe(2);
      expect(data).toEqual(mockHistory);
    });

    const req = httpMock.expectOne(`http://localhost:5000/api/history/${fieldId}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockHistory);
  });
});
