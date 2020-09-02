import { Chart } from 'chart.js';
import 'hammerjs';
import 'chartjs-plugin-zoom';
import moment from 'moment';

import { ChartData } from "./ChartDataTypes";

export abstract class TimeSeriesChart {
    chart: any

    constructor(canvasId: string, data: ChartData) {
        const ctx = (document.getElementById(canvasId) as HTMLCanvasElement).getContext('2d');
        this.chart = new Chart(ctx, {
            type: this.getType(),
            data: {
                labels: data.labels,
                datasets: this.getDataset(data)
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 8,
                            maxRotation: 0
                        },
                        time: {
                            unit: 'month',
                        }
                    }]
                },
                tooltips: {
                    mode: 'index',
                    callbacks: {
                        title: function (tooltipItems) {
                            return moment(
                                Date.parse(tooltipItems[0].xLabel as string)).format('LL');
                        }
                    }
                },
                plugins: {
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x',
                            speed: 20,
                            threshold: 10,
                        },
                        zoom: {
                            enabled: true,
                            mode: 'x',
                            speed: 0.1,
                            sensitivity: 3,
                        }
                    },
                }
            },
        });
    }

    public update = (data: ChartData) => {
        this.chart.data = {
            labels: data.labels,
            datasets: this.getDataset(data)
        };
        this.chart.update();
    }

    public destroy = () => {
        this.chart.destroy()
    }

    abstract getType(): string;
    abstract getDataset(data: ChartData): any;
}