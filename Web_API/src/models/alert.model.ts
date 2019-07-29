import {Entity, model, property} from '@loopback/repository';

@model({
  settings: {
    mssql: {
      table: "CEVAC_ALL_ALERTS_EVENTS_HIST"
    },
  },
})
export class Alert extends Entity {  
  @property({
    type: 'number',
    id: true,
    required: true,
  })
  EventID: number;

  @property({
    type: 'string',
    required: true,
  })
  AlertType: string;

  @property({
    type: 'string',
  })
  AlertMessage?: string;

  @property({
    type: 'string',
  })
  Metric?: string;

  @property({
    type: 'string',
    required: true,
  })
  BuildingSName: string;

  @property({
    type: 'string',
  })
  BuildingDName?: string;

  @property({
    type: 'boolean',
    required: true,
    default: 0,
  })
  Acknowledged: boolean;

  @property({
    type: 'boolean',
    required: true,
    default: 0,
  })
  Resolved: boolean;

  @property({
    type: 'date',
    required: true,
  })
  ETDateTime: string;

  @property({
    type: 'date',
    required: true,
  })
  DetectionTimeET: string;


  constructor(data?: Partial<Alert>) {
    super(data);
  }
}

export interface AlertRelations {
  // describe navigational properties here
}

export type AlertWithRelations = Alert & AlertRelations;
