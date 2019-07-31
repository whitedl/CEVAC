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
import {CevacAllLatestStats} from '../models';
import {CevacAllLatestStatsRepository} from '../repositories';

export class StatController {
  constructor(
    @repository(CevacAllLatestStatsRepository)
    public cevacAllLatestStatsRepository : CevacAllLatestStatsRepository,
  ) {}

  @post('/stat', {
    responses: {
      '200': {
        description: 'CevacAllLatestStats model instance',
        content: {'application/json': {schema: getModelSchemaRef(CevacAllLatestStats)}},
      },
    },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacAllLatestStats, {exclude: ['tableid']}),
        },
      },
    })
    cevacAllLatestStats: Omit<CevacAllLatestStats, 'tableid'>,
  ): Promise<CevacAllLatestStats> {
    return await this.cevacAllLatestStatsRepository.create(cevacAllLatestStats);
  }

  @get('/stat/count', {
    responses: {
      '200': {
        description: 'CevacAllLatestStats model count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async count(
    @param.query.object('where', getWhereSchemaFor(CevacAllLatestStats)) where?: Where<CevacAllLatestStats>,
  ): Promise<Count> {
    return await this.cevacAllLatestStatsRepository.count(where);
  }

  @get('/stat', {
    responses: {
      '200': {
        description: 'Array of CevacAllLatestStats model instances',
        content: {
          'application/json': {
            schema: {type: 'array', items: getModelSchemaRef(CevacAllLatestStats)},
          },
        },
      },
    },
  })
  async find(
    @param.query.object('filter', getFilterSchemaFor(CevacAllLatestStats)) filter?: Filter<CevacAllLatestStats>,
  ): Promise<CevacAllLatestStats[]> {
    return await this.cevacAllLatestStatsRepository.find(filter);
  }

  @patch('/stat', {
    responses: {
      '200': {
        description: 'CevacAllLatestStats PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacAllLatestStats, {partial: true}),
        },
      },
    })
    cevacAllLatestStats: CevacAllLatestStats,
    @param.query.object('where', getWhereSchemaFor(CevacAllLatestStats)) where?: Where<CevacAllLatestStats>,
  ): Promise<Count> {
    return await this.cevacAllLatestStatsRepository.updateAll(cevacAllLatestStats, where);
  }

  @get('/stat/{id}', {
    responses: {
      '200': {
        description: 'CevacAllLatestStats model instance',
        content: {'application/json': {schema: getModelSchemaRef(CevacAllLatestStats)}},
      },
    },
  })
  async findById(@param.path.number('id') id: number): Promise<CevacAllLatestStats> {
    return await this.cevacAllLatestStatsRepository.findById(id);
  }

  @patch('/stat/{id}', {
    responses: {
      '204': {
        description: 'CevacAllLatestStats PATCH success',
      },
    },
  })
  async updateById(
    @param.path.number('id') id: number,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacAllLatestStats, {partial: true}),
        },
      },
    })
    cevacAllLatestStats: CevacAllLatestStats,
  ): Promise<void> {
    await this.cevacAllLatestStatsRepository.updateById(id, cevacAllLatestStats);
  }

  @put('/stat/{id}', {
    responses: {
      '204': {
        description: 'CevacAllLatestStats PUT success',
      },
    },
  })
  async replaceById(
    @param.path.number('id') id: number,
    @requestBody() cevacAllLatestStats: CevacAllLatestStats,
  ): Promise<void> {
    await this.cevacAllLatestStatsRepository.replaceById(id, cevacAllLatestStats);
  }

  @del('/stat/{id}', {
    responses: {
      '204': {
        description: 'CevacAllLatestStats DELETE success',
      },
    },
  })
  async deleteById(@param.path.number('id') id: number): Promise<void> {
    await this.cevacAllLatestStatsRepository.deleteById(id);
  }
}
