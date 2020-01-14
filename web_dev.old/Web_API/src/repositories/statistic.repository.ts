import {DefaultCrudRepository} from '@loopback/repository';
import {Statistic, StatisticRelations} from '../models';
import {MssqlDataSource} from '../datasources';
import {inject} from '@loopback/core';

export class StatisticRepository extends DefaultCrudRepository<
  Statistic,
  typeof Statistic.prototype.tableid,
  StatisticRelations
> {
  constructor(@inject('datasources.mssql') dataSource: MssqlDataSource) {
    super(Statistic, dataSource);
  }
}
