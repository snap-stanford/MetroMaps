function drawLines() {
	for (var l in lines) {
		var currentNodeSet = lines[l].nodeIDs;
		
		for (var n = 0; n < currentNodeSet.length - 1; n++) {
			var startNode = getNodeByID(currentNodeSet[n]);
			var endNode = getNodeByID(currentNodeSet[n+1]);
			var lineWidth = 30;
			
			var dups = getDups(startNode.lineIDs, endNode.lineIDs);
			
			if (dups.length > 1) {
				drawRainbowSeg(startNode, endNode, dups, lineWidth);
			}
			else {
				var segment = new Kinetic.Line({
					points: [startNode.x, startNode.y, endNode.x, endNode.y],
					stroke: colors[lines[l].id],
					strokeWidth: lineWidth
				});
				layer.add(segment);
			}
		}
	}
}

function drawRainbowSeg(leftNode, rightNode, dups, lineWidth) {
	// Get info on this segment
	// Also, calculate width of each seg in rainbow -- depends on how many need to share
	var leftNodePoint = {x: leftNode.x, y: leftNode.y};
	var rightNodePoint = {x: rightNode.x, y: rightNode.y};
	var width = lineWidth / (dups.length); 
	
	var perpSlope = (-1) * ((leftNode.x - rightNode.x)/
													(leftNode.y - rightNode.y));
	var basePointLeft = offsetPoint (leftNodePoint, 15, perpSlope, true);
	var basePointRight = offsetPoint (rightNodePoint, 15, perpSlope, true);
	
	var currentPointLeft = offsetPoint (basePointLeft, width/2, perpSlope, false);
	var currentPointRight = offsetPoint (basePointRight, width/2, perpSlope, false);
	
	for (var s in dups) {
		var color = colors[parseInt(dups[s])];
		
		var lineSegment = new Kinetic.Line({
			points: [currentPointLeft, currentPointRight],
			stroke: color,
			strokeWidth: width,
			lineCap: 'round',
			lineJoin: 'round'
		});		
		layer.add(lineSegment);
		layer.draw();
		
		currentPointLeft = offsetPoint (currentPointLeft, width, perpSlope, false);
		currentPointRight = offsetPoint (currentPointRight, width, perpSlope, false);
	}
}

// Helper function for drawRainbowLineSegment 
// determine which lines are shared by two neighboring nodes
function getDups (array1, array2) {
	var dups = [];
	for (var a in array1) {
		for (var b in array2) {
			if (array1[a] == array2[b]) {
				dups.push(array1[a]);
			}
		}
	}
	return dups;
}

// Helper function for drawRainbowLineSegment
// Find offset and iteratively draw different lines up
function offsetPoint (originalPoint, distance, slope, down) {
	if (slope == undefined){
		console.log("slope is undefined");
	}
	else if (slope == Infinity) {
		var offset = distance;
		if (down) {
			offset = offset * -1;
		}
		return {x: originalPoint.x, y: originalPoint.y + offset};
	}
	else {
		var xOffset = Math.sqrt((distance * distance)/(slope * slope + 1));
		var yOffset = slope * xOffset;
		if (down){
			xOffset = xOffset * -1;
			yOffset = yOffset * -1;
		}
		return {x: originalPoint.x + xOffset, y: originalPoint.y + yOffset};
	}
}



function drawLineLabels() {
	for (var l in lines) {
		var currentNodeSet = lines[l].nodeIDs;
		drawLineLabel(lines[l], 
									getNodeByID(currentNodeSet[0]), 
									getNodeByID(currentNodeSet[1]));
	}
}

function drawLineLabel(line, firstNode, secondNode) {	
	var labelWidth = (secondNode.x - firstNode.x - firstNode.radius - secondNode.radius);
	labelWidth = Math.min(labelWidth, 200);
	
	var lineLabel = new Kinetic.Text({
		x: firstNode.x + firstNode.radius,
		y: firstNode.y + 16,
		width: labelWidth,
		text: line.line_label,
		fontSize: 15,
		fontFamily: 'Calibri',
		align: 'center',
		fill: colors[line.id]
	});
	
	var tab = new Kinetic.Rect({
		x: firstNode.x + firstNode.radius,
		y: firstNode.y + 16,
		fill: '#f9f9f9',
		width: labelWidth,
		height: lineLabel.getHeight() + 5,
		shadowColor: 'black',
		shadowBlur: 10,
		shadowOffset: [5, 5],
		shadowOpacity: 0.2,
		cornerRadius: 5
	});
	
 	var slope = (secondNode.y - firstNode.y)/(secondNode.x - firstNode.x)
 	var angle = Math.atan(slope)
	
 	tab.rotate(angle);
 	lineLabel.rotate(angle);
 	
 	tab.on('mouseenter', function() {
		tab.moveToTop();
		lineLabel.moveToTop();
		layer.draw();
	});
	lineLabel.on('mouseenter', function() {
		tab.moveToTop();
		lineLabel.moveToTop();
		layer.draw();
	});
	
	layer.add(tab);
	layer.add(lineLabel);
	layer.add(lineLabel);
}