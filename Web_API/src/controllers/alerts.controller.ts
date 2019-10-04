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
import {Alert} from '../models';
import {AlertRepository} from '../repositories';

export class AlertsController {
  constructor(
    @repository(AlertRepository)
    public alertRepository: AlertRepository,
  ) {}

  @post('/alerts', {
    responses: {
      '200': {
        description: 'Alert model instance',
        content: {'application/json': {schema: {'x-ts-type': Alert}}},
      },
    },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Alert, {exclude: ['EventID']}),
        },
      },
    })
    alert: Omit<Alert, 'id'>,
  ): Promise<Alert> {
    return await this.alertRepository.create(alert);
  }

  @get('/alerts/count', {
    responses: {
      '200': {
        description: 'Alert model count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async count(
    @param.query.object('where', getWhereSchemaFor(Alert)) where?: Where<Alert>,
  ): Promise<Count> {
    return await this.alertRepository.count(where);
  }

  @get('/alerts', {
    responses: {
      '200': {
        description: 'Array of Alert model instances',
        content: {
          'application/json': {
            schema: {type: 'array', items: {'x-ts-type': Alert}},
          },
        },
      },
    },
  })
  async find(
    @param.query.object('filter', getFilterSchemaFor(Alert))
    filter?: Filter<Alert>,
  ): Promise<Alert[]> {
    return await this.alertRepository.find(filter);
  }

  @patch('/alerts', {
    responses: {
      '200': {
        description: 'Alert PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Alert, {partial: true}),
        },
      },
    })
    alert: Alert,
    @param.query.object('where', getWhereSchemaFor(Alert)) where?: Where<Alert>,
  ): Promise<Count> {
    return await this.alertRepository.updateAll(alert, where);
  }

  @get('/alerts/{id}', {
    responses: {
      '200': {
        description: 'Alert model instance',
        content: {'application/json': {schema: {'x-ts-type': Alert}}},
      },
    },
  })
  async findById(@param.path.number('id') id: number): Promise<Alert> {
    return await this.alertRepository.findById(id);
  }

  @patch('/alerts/{id}', {
    responses: {
      '204': {
        description: 'Alert PATCH success',
      },
    },
  })
  async updateById(
    @param.path.number('id') id: number,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Alert, {partial: true}),
        },
      },
    })
    alert: Alert,
  ): Promise<void> {
    await this.alertRepository.updateById(id, alert);
  }

  @put('/alerts/{id}', {
    responses: {
      '204': {
        description: 'Alert PUT success',
      },
    },
  })
  async replaceById(
    @param.path.number('id') id: number,
    @requestBody() alert: Alert,
  ): Promise<void> {
    await this.alertRepository.replaceById(id, alert);
  }

  @del('/alerts/{id}', {
    responses: {
      '204': {
        description: 'Alert DELETE success',
      },
    },
  })
  async deleteById(@param.path.number('id') id: number): Promise<void> {
    await this.alertRepository.deleteById(id);
  }
}
