declare var vegaEmbed: any;

(function ($) {
    vegaEmbed(
      '#vega-chart-container',
      'http://localhost:8000/engine/vega-spec'
    );
})(jQuery);
