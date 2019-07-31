import {Entity, model, property} from '@loopback/repository';

@model({
  settings: {idInjection: false, mssql: {schema: 'dbo', table: 'CEVAC_BUILDING_INFO'}}
})
export class CevacBuildingInfo extends Entity {
  @property({
    type: Number,
    required: false,
    precision: 5,
    scale: 0,
    mssql: {"columnName":"BLDG","dataType":"smallint","dataLength":null,"dataPrecision":5,"dataScale":0,"nullable":"YES"},
  })
  bldg?: Number;

  @property({
    type: String,
    required: true,
    length: 50,
    id: 1,
    mssql: {"columnName":"BuildingSName","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"NO"},
  })
  buildingsname: String;

  @property({
    type: String,
    required: true,
    length: 50,
    mssql: {"columnName":"BuildingDName","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"NO"},
  })
  buildingdname: String;

  @property({
    type: String,
    required: true,
    length: 50,
    mssql: {"columnName":"BuildingKey","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"NO"},
  })
  buildingkey: String;

  @property({
    type: Number,
    required: false,
    precision: 5,
    scale: 0,
    mssql: {"columnName":"YR_BUILT","dataType":"smallint","dataLength":null,"dataPrecision":5,"dataScale":0,"nullable":"YES"},
  })
  yrBuilt?: Number;

  @property({
    type: String,
    required: false,
    length: 50,
    mssql: {"columnName":"BLDG_CLASS","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  bldgClass?: String;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"GSF","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  gsf?: Number;

  @property({
    type: Number,
    required: false,
    precision: 3,
    scale: 0,
    mssql: {"columnName":"FLOORS","dataType":"tinyint","dataLength":null,"dataPrecision":3,"dataScale":0,"nullable":"YES"},
  })
  floors?: Number;

  @property({
    type: Number,
    required: false,
    precision: 5,
    scale: 0,
    mssql: {"columnName":"ROOMS","dataType":"smallint","dataLength":null,"dataPrecision":5,"dataScale":0,"nullable":"YES"},
  })
  rooms?: Number;

  @property({
    type: String,
    required: false,
    length: 50,
    mssql: {"columnName":"BuildingStatus","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  buildingstatus?: String;

  @property({
    type: String,
    required: false,
    length: 50,
    mssql: {"columnName":"BuildingFunction","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  buildingfunction?: String;

  @property({
    type: String,
    required: false,
    length: 100,
    mssql: {"columnName":"ReportLink","dataType":"nvarchar","dataLength":100,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  reportlink?: String;

  // Define well-known properties here

  // Indexer property to allow additional data
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [prop: string]: any;

  constructor(data?: Partial<CevacBuildingInfo>) {
    super(data);
  }
}

export interface CevacBuildingInfoRelations {
  // describe navigational properties here
}

export type CevacBuildingInfoWithRelations = CevacBuildingInfo & CevacBuildingInfoRelations;
