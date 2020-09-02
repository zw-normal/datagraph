import { TimeSeriesChart } from "./TimeSeriesChart";
import * as d3 from 'd3';

import { ChartData } from "./ChartDataTypes";

export class TimeSeriesBarChart extends TimeSeriesChart {
    getType(): string {
        return 'bar';
    }

    getDataset(data: ChartData): any {
        const color = d3.scaleOrdinal()
            .domain(data.datasets.map(d => d.label).sort())
            .range(d3.schemeCategory10)

        return data.datasets.map(d => ({
            ...d,
            backgroundColor: color(d.label),
            borderColor: color(d.label)
        }))
    }
}
