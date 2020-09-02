export interface DataNode {
    id: string;
    title: string;
    name: string;
    type: string;
    chartType: string;
}

export interface DataEdge {
    source: DataNode;
    dest: DataNode;
}

export interface DataGraph {
    nodes: DataNode[],
    edges: DataEdge[]
}

export interface DataNodeData {
    node: DataNode;
    data: any;
}

export class DataGraphAPI {
    public getData = async (id: string): Promise<DataNodeData | null> => {
        const query = `
                query {
                    dataNode (id: "${id}") { 
                        id, title, name, type, chartType, data
                    }
                }
            `;

        return fetch(
            `${window.location.origin}/graphql`,
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query})
            })
            .then(response => response.json())
            .then(data => {
                const {id, title, name, type, chartType} = data.data.dataNode;
                return {
                    node: {id, title, name, type, chartType},
                    data: JSON.parse(data.data.dataNode.data)
                };
            })
            .catch(error => {
                console.error(error);
                return null;
            });
    }

    public getDataGraph = async (ids: string[]): Promise<DataGraph> => {
        const idsQuery = ids.map(id => `"${id}"`).join(', ');
        const query = `
                query {
                    dataNodes (ids: [${idsQuery}]) { 
                        id, title, name, type, chartType
                    }
                    dataEdges (ids: [${idsQuery}]) {
                        source { id, title, name, type, chartType },
                        dest { id, title, name, type, chartType }
                    }
                }
            `;

        return fetch(
            `${window.location.origin}/graphql`,
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query})
            })
            .then(response => response.json())
            .then(data => {
                const nodes: DataNode[] = data.data.dataNodes;
                const edges: DataEdge[] = data.data.dataEdges;
                if (edges.length > 0) {
                    edges.forEach(e => {
                        if (!this.nodeExist(e.source, nodes)) {
                            nodes.push(e.source)
                        }
                        if (!this.nodeExist(e.dest, nodes)) {
                            nodes.push(e.dest)
                        }
                    });
                }
                return {nodes, edges}
            })
            .catch(error => {
                console.error(error);
                return {nodes: [], edges: []}
            });
    }

    private nodeExist = (node: DataNode, nodes: DataNode[]): boolean => {
        for (let n of nodes) {
            if (n.id === node.id) {
                return true;
            }
        }
        return false;
    }
}

