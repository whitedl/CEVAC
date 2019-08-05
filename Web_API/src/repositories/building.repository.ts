import {DefaultCrudRepository} from '@loopback/repository';
import {Building, BuildingRelations} from '../models';
import {MssqlDataSource} from '../datasources';
import {inject} from '@loopback/core';

export class BuildingRepository extends DefaultCrudRepository<
  Building,
  typeof Building.prototype.buildingsname,
  BuildingRelations
> {
  constructor(@inject('datasources.mssql') dataSource: MssqlDataSource) {
    super(Building, dataSource);
  }
}
