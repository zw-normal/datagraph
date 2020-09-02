import { zip } from 'underscore';
import { from } from "rxjs";

import { eventEmitter, EventTypes } from './Events';
import { TimeSeriesLineChart } from '../TimeSeriesLineChart';
import { TimeSeriesBarChart } from '../TimeSeriesBarChart';
import { DataGraphAPI, DataNodeData } from '../DataGraphApi';
import { createDataChart } from '../ChartFactory';
import { ChartType } from '../ChartDataTypes';

(function ($) {
    const dataGraphAPI = new DataGraphAPI();
    let dataChart: TimeSeriesLineChart | TimeSeriesBarChart;
    const $chartDialog: any = $('#data-chart-modal');
    let dataGraphSubscription: any;

    eventEmitter.on(EventTypes.DATA_NODE_SELECTED, (node: any) => {
        if (node && node.chartType) {
            $chartDialog.modal('show');
            $('#spinner-container').show();
            if (dataChart) {
                dataChart.destroy();
            }
            $('#data-chart-canvas').hide();

            dataGraphSubscription = from(dataGraphAPI.getData(node.id))
            .subscribe(
                (data: DataNodeData | null) => {
                        eventEmitter.emit(EventTypes.DATA_NODE_DATA_LOADED, data);
                    },
                error => console.error(error)
                );

            $chartDialog.on('hidden.bs.modal', () => {
                dataGraphSubscription.unsubscribe();
            });
        }
    });

    eventEmitter.on(EventTypes.DATA_NODE_DATA_LOADED, (data: DataNodeData | null) => {
        $('#spinner-container').hide();
        $('#data-chart-canvas').show();

        if (data && data.node.chartType) {
            const chartType = data.node.chartType;
            const labels = data.data.index.map((i: number) => new Date(i));
            const zippedData = zip(...data.data.data);
            const datasets = data.data.columns.map((_: any, i: number) => ({
                label: data.data.columns[i],
                data: zippedData[i]
            }));

            dataChart = createDataChart(
                ChartType[chartType as keyof typeof ChartType],
                'data-chart-canvas',
                {labels, datasets});
        }
    });
})(jQuery);