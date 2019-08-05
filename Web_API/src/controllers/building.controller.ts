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
import {Building} from '../models';
import {BuildingRepository} from '../repositories';

export class BuildingController {
  constructor(
    @repository(BuildingRepository)
    public cevacBuildingInfoRepository: BuildingRepository,
  ) {}

  @post('/buildings', {
    responses: {
      '200': {
        description: 'Building model instance',
        content: {'application/json': {schema: getModelSchemaRef(Building)}},
      },
    },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Building, {exclude: ['buildingsname']}),
        },
      },
    })
    building: Omit<Building, 'buildingsname'>,
  ): Promise<Building> {
    return await this.cevacBuildingInfoRepository.create(building);
  }

  @get('/buildings/count', {
    responses: {
      '200': {
        description: 'Building model count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async count(
    @param.query.object('where', getWhereSchemaFor(Building))
    where?: Where<Building>,
  ): Promise<Count> {
    return await this.cevacBuildingInfoRepository.count(where);
  }

  @get('/buildings', {
    responses: {
      '200': {
        description: 'Array of Building model instances',
        content: {
          'application/json': {
            schema: {
              type: 'array',
              items: getModelSchemaRef(Building, {includeRelations: true}),
            },
          },
        },
      },
    },
  })
  async find(
    @param.query.object('filter', getFilterSchemaFor(Building))
    filter?: Filter<Building>,
  ): Promise<Building[]> {
    return await this.cevacBuildingInfoRepository.find(filter);
  }

  @patch('/buildings', {
    responses: {
      '200': {
        description: 'Building PATCH success count',
        content: {'application/json': {schema: CountSchema}},
      },
    },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Building, {partial: true}),
        },
      },
    })
    building: Building,
    @param.query.object('where', getWhereSchemaFor(Building))
    where?: Where<Building>,
  ): Promise<Count> {
    return await this.cevacBuildingInfoRepository.updateAll(building, where);
  }

  @get('/buildings/{id}', {
    responses: {
      '200': {
        description: 'Building model instance',
        content: {
          'application/json': {
            schema: getModelSchemaRef(Building, {includeRelations: true}),
          },
        },
      },
    },
  })
  async findById(@param.path.string('id') id: string): Promise<Building> {
    return await this.cevacBuildingInfoRepository.findById(id);
  }

  @patch('/buildings/{id}', {
    responses: {
      '204': {
        description: 'Building PATCH success',
      },
    },
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Building, {partial: true}),
        },
      },
    })
    building: Building,
  ): Promise<void> {
    await this.cevacBuildingInfoRepository.updateById(id, building);
  }

  @put('/buildings/{id}', {
    responses: {
      '204': {
        description: 'Building PUT success',
      },
    },
  })
  async replaceById(
    @param.path.string('id') id: string,
    @requestBody() building: Building,
  ): Promise<void> {
    await this.cevacBuildingInfoRepository.replaceById(id, building);
  }

  @del('/buildings/{id}', {
    responses: {
      '204': {
        description: 'Building DELETE success',
      },
    },
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.cevacBuildingInfoRepository.deleteById(id);
  }
}
