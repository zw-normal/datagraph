import { SpreadsheetWidget } from './SpreadsheetWidget';

(function ($) {
    $("div[id$='_spreadsheet']").each(function() {
        const spreadSheetId = $(this).attr('id');

        const widgetId = spreadSheetId.substr(
            0, spreadSheetId.length - 12);
        const inputId = `${widgetId}_input`
        const dataValue = ($(`#${inputId}`) as any).val();
        if (dataValue) {
            const data = JSON.parse(dataValue);
            new SpreadsheetWidget(
                widgetId,
                data.data,
                data.columns.map((c: string) => ({title: c})));
        } else {
            new SpreadsheetWidget(widgetId);
        }
    });
})(jQuery);
