import { ChartData, ChartType } from './ChartDataTypes';
import { TimeSeriesLineChart } from "./TimeSeriesLineChart";
import { TimeSeriesBarChart } from "./TimeSeriesBarChart";


export const createDataChart = (
    type: ChartType, canvasId: string, data: ChartData
): TimeSeriesLineChart|TimeSeriesBarChart => {
    if (type == ChartType.TIMESERIESLINE) {
        return new TimeSeriesLineChart(canvasId, data);
    } else if (type == ChartType.TIMESERIESBAR) {
        return new TimeSeriesBarChart(canvasId, data);
    }
}
