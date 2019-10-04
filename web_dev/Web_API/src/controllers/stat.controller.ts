import {
  Count,
  CountSchema,
  Filter,
  repository,
  Where,
} from '@loopback/repository';
import {
  post,
  param,
  get,
  getFilterSchemaFor,
  getModelSchemaRef,
  getWhereSchemaFor,
  patch,
  put,
  del,
  requestBody,
} from '@loopback/rest';
import {Statistic} from '../models';
import {StatisticRepository} from '../repositories';

export class StatController {
  constructor(
    @repository(StatisticRepository)
    public statisticRepository: StatisticRepository,
  ) {}

  @post('/stat', {
    responses: {
      '200': {
        description: 'Statistic model instance',
        content: {'application/json': {schema: getModelSchemaRef(Statistic)}},
      },
    },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Statistic, {exclude: ['tableid']}),
        },
      },
    })
    statistic: Omit<Statistic, 'tableid'>,
  ): Promise<Statistic> {
    return await this.statisticRepository.create(statistic);
  }

  @get('/stat/count', {
    responses: {
      '200': {
        description: 'Statistic model count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async count(
    @param.query.object('where', getWhereSchemaFor(Statistic))
    where?: Where<Statistic>,
  ): Promise<Count> {
    return await this.statisticRepository.count(where);
  }

  @get('/stat', {
    responses: {
      '200': {
        description: 'Array of Statistic model instances',
        content: {
          'application/json': {
            schema: {type: 'array', items: getModelSchemaRef(Statistic)},
          },
        },
      },
    },
  })
  async find(
    @param.query.object('filter', getFilterSchemaFor(Statistic))
    filter?: Filter<Statistic>,
  ): Promise<Statistic[]> {
    return await this.statisticRepository.find(filter);
  }

  @patch('/stat', {
    responses: {
      '200': {
        description: 'Statistic PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Statistic, {partial: true}),
        },
      },
    })
    statistic: Statistic,
    @param.query.object('where', getWhereSchemaFor(Statistic))
    where?: Where<Statistic>,
  ): Promise<Count> {
    return await this.statisticRepository.updateAll(statistic, where);
  }

  @get('/stat/{id}', {
    responses: {
      '200': {
        description: 'Statistic model instance',
        content: {'application/json': {schema: getModelSchemaRef(Statistic)}},
      },
    },
  })
  async findById(@param.path.number('id') id: number): Promise<Statistic> {
    return await this.statisticRepository.findById(id);
  }

  @patch('/stat/{id}', {
    responses: {
      '204': {
        description: 'Statistic PATCH success',
      },
    },
  })
  async updateById(
    @param.path.number('id') id: number,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Statistic, {partial: true}),
        },
      },
    })
    statistic: Statistic,
  ): Promise<void> {
    await this.statisticRepository.updateById(id, statistic);
  }

  @put('/stat/{id}', {
    responses: {
      '204': {
        description: 'Statistic PUT success',
      },
    },
  })
  async replaceById(
    @param.path.number('id') id: number,
    @requestBody() statistic: Statistic,
  ): Promise<void> {
    await this.statisticRepository.replaceById(id, statistic);
  }

  @del('/stat/{id}', {
    responses: {
      '204': {
        description: 'Statistic DELETE success',
      },
    },
  })
  async deleteById(@param.path.number('id') id: number): Promise<void> {
    await this.statisticRepository.deleteById(id);
  }
}
