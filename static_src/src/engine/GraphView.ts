import * as d3 from 'd3';

export interface Node {
    id: string;
    title: string;
    type: string;
}

export interface Link {
    source: string;
    target: string;
}

export class GraphView {
    containerSelector: string

    constructor(
        containerSelector: string,
        nodes_: Node[],
        links_: Link[],
        types_?: string[],
        nodeClicked?: (node: any) => void,
        nodeContextMenu?: (node: any, position: DOMRect) => void,
        svgClicked?: () => void,
        svgContextMenu?: () => void,
        ) {
        const drag = (simulation: any) => {
            function dragstarted(d: any) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(d: any) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }

            function dragended(d: any) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }

        const links = links_.map(l => Object.create(l));
        const nodes = nodes_.map(n => Object.create(n));
        const types = types_? types_ : nodes.map(n => n.type);
        const color = d3.scaleOrdinal()
            .domain(types.sort())
            .range(d3.schemeCategory10);
        const radius = 6;

        // Set up SVG for D3
        this.containerSelector = containerSelector;
        const container = d3.select(containerSelector);
        const containerSize =
            (container.node() as HTMLElement).getBoundingClientRect();

        const width = containerSize.width;
        const height = containerSize.height;
        const svg = container
            .append('svg')
            .on('click', () => {
                if (svgClicked) {
                    svgClicked();
                }
                d3.event.preventDefault();
            })
            .on('contextmenu', () => {
                if (svgContextMenu) {
                    svgContextMenu();
                }
                d3.event.preventDefault();
            })
            .attr("viewBox", `${-width/2}, ${-height/2}, ${width}, ${height}`)
            .style("font", "12px sans-serif");

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id((d: any) => d.id))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("x", d3.forceX())
            .force("y", d3.forceY());

        svg.append("defs")
            .append("marker")
            .attr("id", "arrow-link")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -0.5)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("fill", "#999")
            .attr("stroke-opacity", 0.6)
            .attr("d", "M0,-5L10,0L0,5");

        const link = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-width", 1.5)
            .selectAll("path")
            .data(links)
            .join("path")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .attr("marker-end", "url(#arrow-link)");

        const node = svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("fill", (d: any) => color(d.type) as string)
            .attr("opacity", (d: any) => (d.type == 'CALCULATOR' ? 0.6 : 1.0))
            .attr("r", radius)
            .call(drag(simulation));

        node.append("title")
            .text((d: any) => (d.type == 'CALCULATOR' ? d.title : ""));

        node.on("click", function (d) {
            if (nodeClicked) {
                nodeClicked(d);
            }
        });

        node.on("contextmenu", function (d) {
            const position = (this as HTMLElement).getBoundingClientRect();
            if (nodeContextMenu) {
                nodeContextMenu(d, position);
                d3.event.preventDefault();
            }
        });

        const labels = svg.selectAll("text.label")
                .data(nodes)
                .join("text")
                .attr("class", "label")
                .attr("fill", "black")
                .attr("pointer-events", "none")
                .text(function(d) {return d.type == 'CALCULATOR' ? "" : d.title;});

        simulation.on("tick", () => {
            link.attr("d", linkArc);
            node.attr("cx", (d: any) => d.x).attr("cy", (d: any) => d.y);
            labels.attr("transform", function(d) {return "translate(" + (d.x + 4) + "," + (d.y - 4) + ")";});
        });

        function linkArc(d: any) {
            const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
            return `
                    M${d.source.x},${d.source.y}
                    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
                `;
        }

        function linkLine(d: any) {
            return `M${d.source.x},${d.source.y}L${d.target.x},${d.target.y}`;
        }
    }

    public destroy = () => {
        const container = d3.select(this.containerSelector);
        container.selectAll("*").remove();
    }
}
