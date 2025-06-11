import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { environment } from '../../environments/environment';
import { ApiService } from './api.service';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService]
    });

    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch forecast weather when no date is provided', () => {
    const city = 'London';

    service.getWeather(city).subscribe(response => {
      expect(response).toBeTruthy();
    });

    const expectedUrl = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&cnt=7&appid=${environment.weatherApiKey}`;
    const req = httpMock.expectOne(expectedUrl);
    expect(req.request.method).toBe('GET');

    req.flush({ mock: 'forecast' });
  });

  it('should fetch weather for a specific date', () => {
    const city = 'Paris';
    const date = '1651015200';

    service.getWeather(city, date).subscribe(response => {
      expect(response).toBeTruthy();
    });

    const expectedUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&dt=${date}&appid=${environment.weatherApiKey}`;
    const req = httpMock.expectOne(expectedUrl);
    expect(req.request.method).toBe('GET');

    req.flush({ mock: 'specific-date' });
  });

  it('should fetch farming news', () => {
    service.getFarmingNews().subscribe(data => {
      expect(data).toBeTruthy();
    });

    const req = httpMock.expectOne(`https://newsapi.org/v2/everything?q=farming&apiKey=${environment.newsApiKey}`);
    expect(req.request.method).toBe('GET');

    req.flush({ articles: [] });
  });

  it('should fetch location from lat/lng', () => {
    const lat = 45.0;
    const lng = 25.0;

    const expectedUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${environment.googleMapsApiKey}`;

    service.getLocation(lat, lng).subscribe(data => {
      expect(data).toBeTruthy();
    });

    const req = httpMock.expectOne(expectedUrl);
    expect(req.request.method).toBe('GET');

    req.flush({ results: [] });
  });

  it('should fetch from external URL', () => {
    const customUrl = 'https://example.com/api/test';

    service.getExternal(customUrl).subscribe(data => {
      expect(data).toEqual({ ok: true });
    });

    const req = httpMock.expectOne(customUrl);
    expect(req.request.method).toBe('GET');

    req.flush({ ok: true });
  });
});
