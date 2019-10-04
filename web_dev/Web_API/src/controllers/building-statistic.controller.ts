import {
  Count,
  CountSchema,
  Filter,
  repository,
  Where,
} from '@loopback/repository';
import {
  del,
  get,
  getModelSchemaRef,
  getWhereSchemaFor,
  param,
  patch,
  post,
  requestBody,
} from '@loopback/rest';
import {Building, Statistic} from '../models';
import {BuildingRepository} from '../repositories';

export class BuildingStatisticController {
  constructor(
    @repository(BuildingRepository)
    protected buildingRepository: BuildingRepository,
  ) {}

  @get('/buildings/{id}/statistics', {
    responses: {
      '200': {
        description: "Array of Statistic's belonging to Building",
        content: {
          'application/json': {
            schema: {type: 'array', items: getModelSchemaRef(Statistic)},
          },
        },
      },
    },
  })
  async find(
    @param.path.string('id') id: string,
    @param.query.object('filter') filter?: Filter<Statistic>,
  ): Promise<Statistic[]> {
    return this.buildingRepository.statistics(id).find(filter);
  }

  @post('/buildings/{id}/statistics', {
    responses: {
      '200': {
        description: 'Building model instance',
        content: {'application/json': {schema: getModelSchemaRef(Statistic)}},
      },
    },
  })
  async create(
    @param.path.string('id') id: typeof Building.prototype.buildingsname,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Statistic, {exclude: ['']}),
        },
      },
    })
    statistic: Omit<Statistic, ''>,
  ): Promise<Statistic> {
    return this.buildingRepository.statistics(id).create(statistic);
  }

  @patch('/buildings/{id}/statistics', {
    responses: {
      '200': {
        description: 'Building.Statistic PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async patch(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Statistic, {partial: true}),
        },
      },
    })
    statistic: Partial<Statistic>,
    @param.query.object('where', getWhereSchemaFor(Statistic))
    where?: Where<Statistic>,
  ): Promise<Count> {
    return this.buildingRepository.statistics(id).patch(statistic, where);
  }

  @del('/buildings/{id}/statistics', {
    responses: {
      '200': {
        description: 'Building.Statistic DELETE success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async delete(
    @param.path.string('id') id: string,
    @param.query.object('where', getWhereSchemaFor(Statistic))
    where?: Where<Statistic>,
  ): Promise<Count> {
    return this.buildingRepository.statistics(id).delete(where);
  }
}
