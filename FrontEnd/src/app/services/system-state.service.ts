import { Injectable } from '@angular/core';
import { BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SystemStateService {

  private schedulerIntervalSubject = new BehaviorSubject<number>(30000); // default interval
  schedulerInterval$ = this.schedulerIntervalSubject.asObservable();

  constructor() { }

  setSchedulerInterval(value: number): void
  {
    console.log("Scheduler interval change: " + value);
    this.schedulerIntervalSubject.next(value);
  }
}
