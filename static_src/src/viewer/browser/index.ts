import './Browser.scss';

declare var vegaEmbed: any;

(function ($) {
    const $vegaSpecPicker = $('#vega-spec-picker');

    $vegaSpecPicker.on('change', () => {
        const id = $vegaSpecPicker.val() as string[];
        if (id) {
            vegaEmbed(
                '#vega-chart-container',
                `engine/vega-spec/${id}/`,
                {
                    actions: false
                }
            ).then(function(result: any) {
                // Access the Vega view instance as result.view
                // https://vega.github.io/vega/docs/api/view/
            }).catch(console.error);
        }
    });
    $vegaSpecPicker.trigger('change');
})(jQuery);
