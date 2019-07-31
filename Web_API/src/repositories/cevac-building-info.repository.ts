import {DefaultCrudRepository} from '@loopback/repository';
import {CevacBuildingInfo, CevacBuildingInfoRelations} from '../models';
import {MssqlDataSource} from '../datasources';
import {inject} from '@loopback/core';

export class CevacBuildingInfoRepository extends DefaultCrudRepository<
  CevacBuildingInfo,
  typeof CevacBuildingInfo.prototype.buildingsname,
  CevacBuildingInfoRelations
> {
  constructor(
    @inject('datasources.mssql') dataSource: MssqlDataSource,
  ) {
    super(CevacBuildingInfo, dataSource);
  }
}
