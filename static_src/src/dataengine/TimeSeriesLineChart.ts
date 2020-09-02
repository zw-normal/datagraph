import { TimeSeriesChart } from "./TimeSeriesChart";
import * as d3 from 'd3';

import { ChartData } from "./ChartDataTypes";

export class TimeSeriesLineChart extends TimeSeriesChart {
    getType(): string {
        return 'line';
    }

    getDataset(data: ChartData): any {
        const color = d3.scaleOrdinal()
            .domain(data.datasets.map(d => d.label).sort())
            .range(d3.schemeCategory10)

        return data.datasets.map(d => ({
            ...d,
            lineTension: 0.4,
            backgroundColor: `${color(d.label)}20`,
            pointRadius: 1,
            pointBackgroundColor: color(d.label),
            pointHoverRadius: 4,
        }))
    }
}
