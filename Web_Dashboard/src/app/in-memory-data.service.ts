import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';

@Injectable({
  providedIn: 'root'
})
export class InMemoryDataService implements InMemoryDbService {
	createDb() {
		const alerts = [
			{ id: 1, message: 'This is a test alert', building: 'Watt' }
		];
		return {alerts};
	}
}
