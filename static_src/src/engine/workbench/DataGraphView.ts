import { eventEmitter, EventTypes } from './Events';
import { GraphView } from '../GraphView';
import { DataGraph, DataGraphAPI } from '../DataGraphApi';

(function ($) {
    const dataGraphAPI = new DataGraphAPI();
    const $nodeContextMenu = $('#data-graph-context-menu');
    const uuidRegex = /[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/g
    let graphView: GraphView;

    eventEmitter.on(EventTypes.DATA_SOURCES_SELECTED, (nodeIds: string[]) => {
        $nodeContextMenu.removeClass('show').hide();
        if (graphView) {
            graphView.destroy();
        }

        dataGraphAPI.getDataGraph(nodeIds)
            .then((graph: DataGraph) => {
                eventEmitter.emit(EventTypes.DATA_SOURCES_LOADED, graph);
            })
            .catch(console.error);
    });

    eventEmitter.on(EventTypes.DATA_SOURCES_LOADED, (graph: DataGraph) => {
        if (graph && graph.nodes && graph.edges) {
            const nodes = graph.nodes.map(n => ({id: n.id, title: n.title, type: n.type}));
            const edges = graph.edges.map(e => ({source: e.source.id, target: e.dest.id}));

            graphView = new GraphView(
                '#graph-container', nodes, edges,
                ['READER', 'TRANSFORM', 'WRITER'],
                (node: any) => {
                    eventEmitter.emit(EventTypes.DATA_NODE_SELECTED, node);
                },
                (node: any, position: DOMRect) => {
                    eventEmitter.emit(EventTypes.DATA_NODE_CONTEXT_MENU, node, position)
                },
                () => {
                    $nodeContextMenu.removeClass('show').hide();
                });
        }
    });

    $nodeContextMenu.on('click', "a", function() {
        $nodeContextMenu.removeClass('show').hide();
    });
    eventEmitter.on(EventTypes.DATA_NODE_CONTEXT_MENU,
        (node: any, position: DOMRect) => {
        if ($nodeContextMenu.length) {
            $nodeContextMenu.find('a').each(function () {
                const href = $(this).attr('href').replace(uuidRegex, node.id);
                $(this).attr('href', href);
            });

            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            $nodeContextMenu.css({
                display: 'block',
                left: `${position.left + scrollLeft}px`,
                top: `${position.top + scrollTop + 16}px`
            }).addClass('show');
        }
    });
})(jQuery);
