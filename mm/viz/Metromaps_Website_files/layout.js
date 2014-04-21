function setLayout() {
	setXPos();
	setYPos();
}

function setXPos() {
	var resize = 60 * nodes.length;
	if (resize > getPanelWidth()) {
		setPanelWidth(resize);
	}
	var spacing = getPanelWidth()/(nodes.length+2);
	var currentPos = getPanelWidth()/(nodes.length+2);
	
	//nodes are sorted by date at this point (done in setNodeProperties)
	for (var i = 0; i < nodes.length; i++) {
		nodes[i].x = currentPos;
		currentPos += spacing;
	}
}

function setYPos() {

	var lineIds = lines.map(function(lineObj){ return lineObj.id;});
	if (lineIds.length > 1) {
		var possibleOrderings = permute(lineIds, [], []);
		var optimalOrdering = findOptimalOrder(possibleOrderings);
	}
	else {
		var optimalOrdering = lineIds;
	}
	var spacing = getPanelHeight()/(lines.length + 1);
	var currentPos = getPanelHeight()/(lines.length + 1);
	var lineYs = {};
	
	for (var i = 0; i < optimalOrdering.length; i++) {
		var lineNumber = optimalOrdering[i];
		lineYs[lineNumber] = currentPos;
		currentPos += spacing;
	}
	
	// Assign Y values to each node, average of the lines it is on
	for (var n in nodes) {
		var myYSum = 0;
		var myLines = nodes[n].lineIDs;
		for (var l in myLines) {
			var currLine = myLines[l];
			myYSum += lineYs[currLine];
		}// Give each ordering a score based on how many nodes they share

		var myYAverage = myYSum / myLines.length;
		nodes[n].y = myYAverage;
	}
}

// Recursively find all orderings of the lines
function permute(input, permArr, usedChars) {
	var i, ch;
	for (i = 0; i < input.length; i++) {
			ch = input.splice(i, 1)[0];
			usedChars.push(ch);
			if (input.length == 0) {
					permArr.push(usedChars.slice());
			}
			permute(input, permArr, usedChars);
			input.splice(i, 0, ch);
			usedChars.pop();
	}
	return permArr;
};

function findOptimalOrder(possibleOrderings) {
	var highestScore = 0;
	if (possibleOrderings.length > 0) {
		var highestOrder = possibleOrderings[0];
	}
	for (var order in possibleOrderings) {
		var orderIntersections = getOrderIntersections(possibleOrderings[order]);
		if (orderIntersections > highestScore) {
			highestScore = orderIntersections;
			highestOrder = possibleOrderings[order];
		}
	}
	return highestOrder;
}

function getOrderIntersections(order) {
	var intersections = 0;
	for (var i = 1; i < order.length; i++) {
		var line = getLineById(parseInt(order[i]));
		var prevLine = getLineById(parseInt(order[i - 1]));
		
		var nodeIDs = line.nodeIDs;
		var prevLineNodeIDs = prevLine.nodeIDs;
		
		for (var r = 0; r < nodeIDs.length; r++) {
			for(var s = 0; s < prevLineNodeIDs.length; s++) {
				if (parseInt(nodeIDs[r]) == parseInt(prevLineNodeIDs[s])) {
					intersections++;
				}
			}
		}
	}
	return intersections;
}