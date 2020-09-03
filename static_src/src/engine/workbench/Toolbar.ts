import { eventEmitter, EventTypes } from './Events';

(function ($) {
    const $dataSourcePicker = $('#data-sources-picker');

    $dataSourcePicker.on('change', () => {
        const ids = $dataSourcePicker.val() as string[];
        eventEmitter.emit(EventTypes.DATA_SOURCES_SELECTED, ids);
    });
    $dataSourcePicker.trigger('change');

    $('#data-sources-reset').on('click', () => {
        $dataSourcePicker.val([]);
        $dataSourcePicker.selectpicker('refresh');
        $dataSourcePicker.trigger('change');
    });
})(jQuery);
