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
import {CevacBuildingInfo} from '../models';
import {CevacBuildingInfoRepository} from '../repositories';

export class BuildingController {
  constructor(
    @repository(CevacBuildingInfoRepository)
    public cevacBuildingInfoRepository : CevacBuildingInfoRepository,
  ) {}

  @post('/buildings', {
    responses: {
      '200': {
        description: 'CevacBuildingInfo model instance',
        content: {'application/json': {schema: getModelSchemaRef(CevacBuildingInfo)}},
      },
    },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacBuildingInfo, {exclude: ['buildingsname']}),
        },
      },
    })
    cevacBuildingInfo: Omit<CevacBuildingInfo, 'buildingsname'>,
  ): Promise<CevacBuildingInfo> {
    return await this.cevacBuildingInfoRepository.create(cevacBuildingInfo);
  }

  @get('/buildings/count', {
    responses: {
      '200': {
        description: 'CevacBuildingInfo model count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async count(
    @param.query.object('where', getWhereSchemaFor(CevacBuildingInfo)) where?: Where<CevacBuildingInfo>,
  ): Promise<Count> {
    return await this.cevacBuildingInfoRepository.count(where);
  }

  @get('/buildings', {
    responses: {
      '200': {
        description: 'Array of CevacBuildingInfo model instances',
        content: {
          'application/json': {
            schema: {type: 'array', items: getModelSchemaRef(CevacBuildingInfo)},
          },
        },
      },
    },
  })
  async find(
    @param.query.object('filter', getFilterSchemaFor(CevacBuildingInfo)) filter?: Filter<CevacBuildingInfo>,
  ): Promise<CevacBuildingInfo[]> {
    return await this.cevacBuildingInfoRepository.find(filter);
  }

  @patch('/buildings', {
    responses: {
      '200': {
        description: 'CevacBuildingInfo PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacBuildingInfo, {partial: true}),
        },
      },
    })
    cevacBuildingInfo: CevacBuildingInfo,
    @param.query.object('where', getWhereSchemaFor(CevacBuildingInfo)) where?: Where<CevacBuildingInfo>,
  ): Promise<Count> {
    return await this.cevacBuildingInfoRepository.updateAll(cevacBuildingInfo, where);
  }

  @get('/buildings/{id}', {
    responses: {
      '200': {
        description: 'CevacBuildingInfo model instance',
        content: {'application/json': {schema: getModelSchemaRef(CevacBuildingInfo)}},
      },
    },
  })
  async findById(@param.path.string('id') id: string): Promise<CevacBuildingInfo> {
    return await this.cevacBuildingInfoRepository.findById(id);
  }

  @patch('/buildings/{id}', {
    responses: {
      '204': {
        description: 'CevacBuildingInfo PATCH success',
      },
    },
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(CevacBuildingInfo, {partial: true}),
        },
      },
    })
    cevacBuildingInfo: CevacBuildingInfo,
  ): Promise<void> {
    await this.cevacBuildingInfoRepository.updateById(id, cevacBuildingInfo);
  }

  @put('/buildings/{id}', {
    responses: {
      '204': {
        description: 'CevacBuildingInfo PUT success',
      },
    },
  })
  async replaceById(
    @param.path.string('id') id: string,
    @requestBody() cevacBuildingInfo: CevacBuildingInfo,
  ): Promise<void> {
    await this.cevacBuildingInfoRepository.replaceById(id, cevacBuildingInfo);
  }

  @del('/buildings/{id}', {
    responses: {
      '204': {
        description: 'CevacBuildingInfo DELETE success',
      },
    },
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.cevacBuildingInfoRepository.deleteById(id);
  }
}
