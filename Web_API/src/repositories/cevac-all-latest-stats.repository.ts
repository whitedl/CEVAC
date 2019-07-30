import {DefaultCrudRepository} from '@loopback/repository';
import {CevacAllLatestStats, CevacAllLatestStatsRelations} from '../models';
import {MssqlDataSource} from '../datasources';
import {inject} from '@loopback/core';

export class CevacAllLatestStatsRepository extends DefaultCrudRepository<
  CevacAllLatestStats,
  typeof CevacAllLatestStats.prototype.id,
  CevacAllLatestStatsRelations
> {
  constructor(@inject('datasources.mssql') dataSource: MssqlDataSource) {
    super(CevacAllLatestStats, dataSource);
  }
}
