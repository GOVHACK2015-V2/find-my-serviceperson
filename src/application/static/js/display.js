var options = {};
var nodes = new vis.DataSet(options);
var edges = new vis.DataSet(options);
var nodeCountIndex=1


function plantRoot(data, container){
    
    climbTree(data, null)
    
    var data = {
        nodes: nodes,
        edges: edges
    };
    
    var network = new vis.Network(container, data, options)
    
}

function climbTree(root, parentID){
        var thisNodesID = nodeCountIndex++
        //console.log(root.name)
        
        nodes.add([{id: thisNodesID, label: root.name}]);
        if (!(parentID === null)){
            edges.add([{from: parentID, to: thisNodesID}]);
        }
        
        for (key in root.children) {
                climbTree(root.children[key], thisNodesID)
        }
}
 

/*
function baseNode() {  
    nodes.add([{id: 0, label: "root"}]);
}


function AddNode(baseNodeID, text) {  
    nodes.add([{id: nodeCount, label: text}]);
    edges.add([{from: baseNodeID, to: nodeCount}]);

  return nodeCount++
}


function draw(container){
        var data = {
        nodes: nodes,
        edges: edges
    };
    var network = new vis.Network(container, data, options)
} */   