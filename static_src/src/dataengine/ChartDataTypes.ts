export interface ChartDataset {
    label: string;
    data: number[];
}

export interface ChartData {
    datasets: ChartDataset[];
    labels: Date[];
}

export enum ChartType {
    TIMESERIESLINE = 'TimeSeriesLine',
    TIMESERIESBAR = 'TimeSeriesSBar'
}
