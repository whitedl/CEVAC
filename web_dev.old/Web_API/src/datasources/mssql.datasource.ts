import {inject} from '@loopback/core';
import {juggler} from '@loopback/repository';
import * as config from './mssql.datasource.json';

export class MssqlDataSource extends juggler.DataSource {
  static dataSourceName = 'mssql';

  constructor(
    @inject('datasources.config.mssql', {optional: true})
    dsConfig: object = config,
  ) {
    super(dsConfig);
  }
}
