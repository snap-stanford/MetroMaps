function updateJSON(newData) {

	currentData = newData;
	nodes = [];
	lines = [];
	currentSelectedNode = null;
	
	var nodeObjs = newData.nodes;
	var lineObjs = newData.lines;

	for (var n in nodeObjs) {
		var node = nodeObjs[n];
		nodes.push(node);
	}

	for (var l in lineObjs) {
		var line = lineObjs[l];
		lines.push(line);
	}

	// for now, set selected node to be first node
	for (var k in nodeObjs) {
		break;
	}
	currentSelectedNode = k;
	
	initialize();
	drawMap();
}