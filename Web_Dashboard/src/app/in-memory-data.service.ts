import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';

@Injectable({
  providedIn: 'root'
})
export class InMemoryDataService implements InMemoryDbService {
	createDb() {
		const alerts = [
			{ id: 1, message: 'This is a test alert', building: 'Watt' },
      { id: 2, message: 'This is a test alert', building: 'Watt' },
      { id: 3, message: 'This is a test alert', building: 'Watt' },
      { id: 4, message: 'This is a test alert', building: 'Watt' },
      { id: 5, message: 'This is a test alert', building: 'Watt' }
		];
		return {alerts};
	}
}
