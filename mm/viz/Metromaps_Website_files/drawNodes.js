/**************************
Map: Draw nodes
**************************/

function drawNodes() {
	for (var n in nodes) {
		
		// If node is shared by just two
		if ((nodes[n].lineIDs).length == 2) {
			var test = nodes[n].lineIDs;
			drawSharedArc(nodes[n]);
		}
		
		// If node is shared, draw arcs
		if ((nodes[n].lineIDs).length > 2) {
			drawSharedArcs(nodes[n]);
		}
		
		drawPlainNode(nodes[n]);
		
		// update currentSelectedNode so it has the whole node data structure
		// and not just the id
		if (nodes[n].id == currentSelectedNode) {
			darkenColor(nodes[n]);
		}
	}
}

function drawPlainNode(nodeData) {
	var node = new Kinetic.Circle({
		radius: nodeData.radius,
		fill: nodeData.color,
		x: nodeData.x,
		y: nodeData.y
	});
	
	var fontsize = (nodeData.displayText == "...") ? 20 : nodeData.importance*5 + 3;

	var label = new Kinetic.Text({
		x: nodeData.x - nodeData.radius*.75,
		y: nodeData.y - nodeData.radius*.75,
		text: nodeData.displayText,
		fontSize: fontsize,
		fontFamily: 'Calibri',
		width: nodeData.radius*1.5,
		height: nodeData.radius*1.5,
		fill: 'white',
		align: 'center'
	});

	nodeData.circleShape = node;
	nodeData.labelShape = label;

	// Add event handlers
	nodeHover(node, nodeData);
	nodeHover(label, nodeData);
	nodeClick(node, nodeData);
	nodeClick(label, nodeData);

	layer.add(node);
	layer.add(label);
}

function drawSharedArc(nodeData) {
	var color = colors[(nodeData.lineIDs)[1]]
	var node = new Kinetic.Circle({
		radius: nodeData.radius + 5,
		stroke: color,
		x: nodeData.x,
		y: nodeData.y,
		strokeWidth: 10
	});

	layer.add(node);
}

function drawSharedArcs(nodeData) {
	var nodeID = nodeData.id;
	var lineIDs = nodeData.lineIDs;
	lineIDs = lineIDs.slice(1,(lineIDs.length));
	
	// accumulate all arcs for this shared node into this data structure
	var myArcs = [];
	
	for (var l in lineIDs) {
		var lineID = lineIDs[l];
		var lineData = getLineById(lineID);
		
		var nodeIndex = parseInt($.inArray(nodeID, lineData.nodeIDs));
		
		var leftPoint = (nodeIndex == 0) ? 
										{x: nodeData.x - 100, y: nodeData.y} :
										{x: getNodeByID((lineData.nodeIDs[nodeIndex - 1])).x, 
										y: getNodeByID((lineData.nodeIDs[nodeIndex - 1])).y};
		var centerPoint = {x: nodeData.x, y: nodeData.y};
		var rightPoint = (nodeIndex == (lineData.nodeIDs.length - 1)) ? 
										{x: nodeData.x + 100, y: nodeData.y} :
										{x: getNodeByID((lineData.nodeIDs[nodeIndex + 1])).x, 
										y: getNodeByID((lineData.nodeIDs[nodeIndex + 1])).y};
		
		var vector1 = {x: leftPoint.x - centerPoint.x, y: leftPoint.y - centerPoint.y};
		var vector2 = {x: rightPoint.x - centerPoint.x, y: rightPoint.y - centerPoint.y};
		var angle1 = Math.atan(vector1.y / vector1.x);
		var angle2 = Math.atan(vector2.y / vector2.x);
		
		// ACCOMMODATING NASTY TRIG GARBAGE
		if (vector1.x < 0) {
			angle1 = angle1 + Math.PI;
		}
		if (vector2.x < 0) {
			angle2 = angle2 + Math.PI;
		}
		
		// Accumulate all of the arcs of this node into array myArcs
		myArcs.push({x: centerPoint.x, 
								 y: centerPoint.y, 
								 radius: nodeData.radius + 2,
								 color: colors[lineID],
								 startAngle: angle1,
								 endAngle: angle2,
								 size: getArcSize(angle1, angle2)});
	}
	
	// Sort the arcs by size
	// Then, greedily draw from largest to smallest
	var mySortedArcs = myArcs.sort(function(a,b){
		return (b.size - a.size);
	});

	for (var a in mySortedArcs){
		var arc = mySortedArcs[a];
		
		//largest angled arc, draw entire circle
		if (a == 0){
			var circle = new Kinetic.Circle({
				x: arc.x,
				y: arc.y,
				radius: arc.radius,
				stroke: arc.color,
				strokeWidth: 10,
			});

			nodeData.circleShape = circle;
			layer.add(circle);
			layer.draw();
		}
		drawArc(arc);
	}
	
}

// Helper function for drawSharedNode
function drawArc(arc) {
	var arcShape = new Kinetic.Shape({
		drawFunc: function(canvas) {
			var context = canvas.getContext();
			var x = arc.x;
			var y = arc.y;
			var radius = arc.radius;
			var startAngle = arc.startAngle;
			var endAngle =  arc.endAngle;
			var counterClockwise = getArcDirection(arc.startAngle, arc.endAngle);
			context.beginPath();
			context.arc(x, y, radius, startAngle, endAngle, counterClockwise);
			context.lineWidth = 10;
			context.strokeStyle = arc.color;
			context.stroke();
		}
	});

	layer.add(arcShape);
	layer.draw();
}

// Helper function for drawSharedNode
function getArcSize(startAngle, endAngle){
	var startAngleMod = startAngle % (2 * Math.PI);
	var endAngleMod = endAngle % (2 * Math.PI);
	var diffAngle = Math.max(startAngleMod, endAngleMod) - 
									Math.min(startAngleMod, endAngleMod);
	if (diffAngle > Math.PI){
		diffAngle = (2 * Math.PI) - diffAngle;
	}
	return diffAngle;
}

// Helper function for drawSharedNode
function getArcDirection(startAngle, endAngle) {
	var startAngleMod = startAngle % (2 * Math.PI);
	var endAngleMod = endAngle % (2 * Math.PI);
	var diffAngle = Math.max(startAngleMod, endAngleMod) - Math.min(startAngleMod, endAngleMod);

	if (startAngleMod > endAngleMod){
		return (diffAngle < Math.PI);
	}
	else if (startAngleMod < endAngleMod){
		return !(diffAngle < Math.PI);
	}
	else{
		//PROBLEM
	}
}