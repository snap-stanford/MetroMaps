/**************************
Map: Kick off the map
**************************/

drawMap();

function drawMap() {
	drawTime();
	drawLines();
	drawNodes();
	drawLineLabels();
	stage.add(layer);
}

function drawTime() {
	var dateSortedNodes = sortByDate(nodes);
	var onethird_index = Math.floor(dateSortedNodes.length / 3);
	var twothird_index = Math.floor(dateSortedNodes.length * 2 / 3);
	var onethird_date = dateSortedNodes[onethird_index].time;
	var twothird_date = dateSortedNodes[twothird_index].time;
	var onethird_xpos = dateSortedNodes[onethird_index].x;
	var twothird_xpos = dateSortedNodes[twothird_index].x;
	
	var onethird_line = new Kinetic.Line({
		points: [onethird_xpos, 0, onethird_xpos, 400],
		stroke: 'black',
		strokeWidth: 1,
	});
	var twothird_line = new Kinetic.Line({
		points: [twothird_xpos, 0, twothird_xpos, 400],
		stroke: 'black',
		strokeWidth: 1,
	});
	var onethird_label = new Kinetic.Text({
		x: onethird_xpos+5,
		y: 380,
		text: onethird_date,
		fontSize: 12,
		fontFamily: 'Calibri',
		fill: 'black'
	});
	var twothird_label = new Kinetic.Text({
		x: twothird_xpos+5,
		y: 380,
		text: twothird_date,
		fontSize: 12,
		fontFamily: 'Calibri',
		fill: 'black'
	});
	
	layer.add(onethird_line);
	layer.add(twothird_line);
	layer.add(onethird_label);
	layer.add(twothird_label);
}