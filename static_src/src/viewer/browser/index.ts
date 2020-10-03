import embed from 'vega-embed';

import './Browser.scss';

(function ($) {
    const $vegaSpecPicker = $('#vega-spec-picker');
    const $vegaChartContainer = $('#vega-chart-container')

    $vegaSpecPicker.on('change', () => {
        $vegaChartContainer.empty();
        
        const id = $vegaSpecPicker.val() as string[];
        if (id) {
            embed(
                '#vega-chart-container',
                `engine/vega-spec/${id}/`,
                {
                    actions: {
                        export: true,
                        source: true,
                        compiled: false,
                        editor: false
                    }
                }
            ).then(function(result: any) {
                // Access the Vega view instance as result.view
                // https://vega.github.io/vega/docs/api/view/
            }).catch(console.error);
        }
    });
    $vegaSpecPicker.trigger('change');
})(jQuery);
