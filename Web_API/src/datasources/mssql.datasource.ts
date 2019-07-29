import {inject} from '@loopback/core';
import {juggler} from '@loopback/repository';
import * as config from './mssql.datasource.json';

export class MssqlDataSource extends juggler.DataSource {
  static dataSourceName = 'MSSQL';

  constructor(
    @inject('datasources.config.MSSQL', {optional: true})
    dsConfig: object = config,
  ) {
    super(dsConfig);
  }
}
