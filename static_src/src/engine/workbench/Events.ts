import * as events from 'events';

export const eventEmitter = new events.EventEmitter();

export enum EventTypes {
    DATA_SOURCES_SELECTED = 'DataSourcesSelected',
    DATA_SOURCES_LOADED = 'DataSourcesLoaded',
    DATA_NODE_SELECTED = 'DataNodeSelected',
    DATA_NODE_CONTEXT_MENU = 'DataNodeContextMenu',
    DATA_NODE_DATA_LOADED = 'DataNodeDataLoad'
}
