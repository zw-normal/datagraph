declare var jexcel: any;

export class DataNodeEditor {
    $basicSpreadSheet: any;
    $dataSpreadSheet: any;
    $dialog: any;

    constructor() {
        this.$basicSpreadSheet = $('#data-node-editor-spreadsheet-basic') as any;
        this.$dataSpreadSheet = $('#data-node-editor-spreadsheet-data') as any;
        this.$dialog = $('#data-node-editor-modal') as any;

        this.$dialog.on('shown.bs.modal', () => {
            const width = this.$basicSpreadSheet.parent('div').width();

            this.$basicSpreadSheet.jexcel({
                minDimensions: [10, 1],
                defaultColWidth: 100,
                tableOverflow: true,
                tableWidth: `${width}px`,
            });

            this.$dataSpreadSheet.jexcel({
                minDimensions: [10, 15],
                defaultColWidth: 100,
                tableOverflow: true,
                tableWidth: `${width}px`,
            });
        });

        this.$dialog.on('hidden.bs.modal', () => {
            this.$basicSpreadSheet.jexcel('destroy');
            this.$dataSpreadSheet.jexcel('destroy');
        });
    }

    public show = () => {
        this.$dialog.modal('show');
    }
}
