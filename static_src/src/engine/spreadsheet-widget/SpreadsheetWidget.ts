declare var jexcel: any;

export class SpreadsheetWidget {
    spreadSheet: any;
    hiddenInput: any;

    constructor(widgetId: String, data?: any, columns?: string[]) {
        this.spreadSheet = $(`#${widgetId}_spreadsheet`) as any;
        this.hiddenInput = $(`#${widgetId}_input`) as any;

        const width = this.spreadSheet.parent().width();
        if (data) {
            this.spreadSheet.jexcel({
                data:data,
                columns: columns,
                defaultColWidth: 100,
                tableOverflow: true,
                tableWidth: `${width}px`,
                onafterchanges: this.onAfterChanges,
                onchangeheader: this.onAfterChanges
            });
        } else {
            this.spreadSheet.jexcel({
                minDimensions: [5, 10],
                defaultColWidth: 100,
                tableOverflow: true,
                tableWidth: `${width}px`,
                onafterchanges: this.onAfterChanges,
                onchangeheader: this.onAfterChanges
            });
        }
    }

    private onAfterChanges = () => {
        const columns = this.spreadSheet.jexcel('getHeaders').split(',')
        const data = {
            columns,
            data: this.spreadSheet.jexcel('getData'),
        }
        this.hiddenInput.val(JSON.stringify(data));
    }
}
