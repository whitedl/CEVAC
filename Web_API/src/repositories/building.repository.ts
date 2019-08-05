import {
  DefaultCrudRepository,
  HasManyRepositoryFactory,
  repository,
} from '@loopback/repository';
import {Building, BuildingRelations, Statistic} from '../models';
import {StatisticRepository} from './statistic.repository';
import {MssqlDataSource} from '../datasources';
import {inject, Getter} from '@loopback/core';

export class BuildingRepository extends DefaultCrudRepository<
  Building,
  typeof Building.prototype.buildingsname,
  BuildingRelations
> {
  public readonly statistics: HasManyRepositoryFactory<
    Statistic,
    typeof Building.prototype.buildingsname
  >;

  constructor(
    @inject('datasources.mssql') dataSource: MssqlDataSource,
    @repository.getter('StatisticRepository')
    protected statisticRepositoryGetter: Getter<StatisticRepository>,
  ) {
    super(Building, dataSource);
    this.statistics = this.createHasManyRepositoryFactoryFor(
      'statistics',
      statisticRepositoryGetter,
    );
  }
}
