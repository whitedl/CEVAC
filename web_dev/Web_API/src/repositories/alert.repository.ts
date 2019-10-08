import {DefaultCrudRepository} from '@loopback/repository';
import {Alert, AlertRelations} from '../models';
import {MssqlDataSource} from '../datasources';
import {inject} from '@loopback/core';

export class AlertRepository extends DefaultCrudRepository<
  Alert,
  typeof Alert.prototype.EventID,
  AlertRelations
> {
  constructor(@inject('datasources.mssql') dataSource: MssqlDataSource) {
    super(Alert, dataSource);
  }
}
