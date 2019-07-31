import {Entity, model, property} from '@loopback/repository';

@model({
  settings: {idInjection: false, mssql: {schema: 'dbo', table: 'CEVAC_ALL_LATEST_STATS'}}
})
export class CevacAllLatestStats extends Entity {
  @property({
    type: String,
    required: true,
    length: 50,
    mssql: {"columnName":"BuildingSName","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"NO"},
  })
  buildingsname: String;

  @property({
    type: String,
    required: true,
    length: 50,
    mssql: {"columnName":"Metric","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"NO"},
  })
  metric: String;

  @property({
    type: String,
    required: false,
    length: 50,
    mssql: {"columnName":"DataName","dataType":"nvarchar","dataLength":50,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  dataname?: String;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"AVG","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  avg?: Number;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"SUM","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  sum?: Number;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"MIN","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  min?: Number;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"MIN_NZ","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  minNz?: Number;

  @property({
    type: Number,
    required: false,
    precision: 53,
    mssql: {"columnName":"MAX","dataType":"float","dataLength":null,"dataPrecision":53,"dataScale":null,"nullable":"YES"},
  })
  max?: Number;

  @property({
    type: Date,
    required: false,
    mssql: {"columnName":"last_ETDateTime","dataType":"datetime","dataLength":null,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  lastEtdatetime?: Date;

  @property({
    type: Date,
    required: false,
    mssql: {"columnName":"update_ETDateTime","dataType":"datetime","dataLength":null,"dataPrecision":null,"dataScale":null,"nullable":"YES"},
  })
  updateEtdatetime?: Date;

  @property({
    type: Number,
    required: false,
    precision: 10,
    scale: 0,
    mssql: {"columnName":"TableID","dataType":"int","dataLength":null,"dataPrecision":10,"dataScale":0,"nullable":"YES"},
  })
  tableid?: Number;

  // Define well-known properties here

  // Indexer property to allow additional data
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [prop: string]: any;

  constructor(data?: Partial<CevacAllLatestStats>) {
    super(data);
  }
}

export interface CevacAllLatestStatsRelations {
  // describe navigational properties here
}

export type CevacAllLatestStatsWithRelations = CevacAllLatestStats & CevacAllLatestStatsRelations;
