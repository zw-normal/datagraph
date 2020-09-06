import './Browser.scss';

declare var vegaEmbed: any;

(function ($) {
    vegaEmbed(
        '#vega-chart-container',
        'http://localhost:8000/engine/vega-spec/a45663e9-6317-4a7c-b0f2-4501485a4cde/',
        {
            actions: false
        }
    ).then(function(result: any) {
        // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
    }).catch(console.error);
})(jQuery);
