/**************************
Map: Helpers
**************************/

var _panelWidth = 2000;

function setLineProperties() {
	for (var l in lines) {
		var nodeIDs = lines[l].nodeIDs;
		var nodeData = [];
		for (var n in nodeIDs) {
			var node = getNodeByID(nodeIDs[n]);
			nodeData.push(node);
		}
		nodeData = sortByDate(nodeData);
		var sortedNodeIDs = [];
		for (var n in nodeData) {
			sortedNodeIDs.push(nodeData[n].id);
		}
		lines[l].nodeIDs = sortedNodeIDs;
	}
}

function setNodeProperties() {
	nodes = sortByDate(nodes);
	
	var dateSortedNodes = sortByDate(nodes);
	
	for (var n in nodes) {
		nodes[n].importance = Math.floor(Math.random()*3 + 1);
		nodes[n].radius = nodes[n].importance * 23;
		nodes[n].color = colors[nodes[n].lineIDs[0]];
		
		if (nodes[n].importance == 1) {
			nodes[n].displayText = "...";
		}
		else {
			nodes[n].displayText = nodes[n].label;
		}
	}
}

function sortByDate(nodes) {
	var sortedNodes = nodes.sort(function(a,b){
		return (Date.parse(a.time) - Date.parse(b.time));
	});
	return sortedNodes;
}

function getPanelWidth() {
	return _panelWidth;
}

function setPanelWidth(newWidth) {
	_panelWidth = newWidth;
}

function getPanelHeight() {
	return 400;
}

function getNodeByID(id) {
	for (var n in nodes) {
		if (nodes[n].id == id) {
			return nodes[n];
		}
	}
	return null;
}

function getLineById(lineId) {
	for (var l in lines) {
		if (lines[l].id == lineId) {
			return lines[l];
		}
	}
}

function initializeColors() {
	var numLines = lines.length;
	var colorArray = Util.getColorArray(numLines);
  colors = {};
	
	var i = 0;
	for (var l in lines) {
		var lineID = lines[l].id;
		colors[lineID] = colorArray[i];
		i++;
	}
}