(function(window, document, undefined) {
var Util = {};

Util.getColorArray = function(nrOfColors) {
	var result = new Array();
	var colorArrayOverview = new Array();

	var colorArray =  ["#FF4900", "#FF9200", "#0B61A4", "#00AF64", "#ffde00"];
	colorArrayOverview.push(colorArray);
	
	var	colorArray2 = ["#00efec", "#FF7400", "#009999", "#00CC00", "#3914AF"];
	colorArrayOverview.push(colorArray2);
 	
 	// // cyan, green, pink, purple
	var colorArray3 = ["#00efec", "#9FEE00", "#CD0074", "#7109AA", "#0A67A3"];
	colorArrayOverview.push(colorArray3);

	var colorArray4 = ["#3fb8e8", "#e86f3f", "#3f63e8", "#e83f63", "#b8e83f"];
	colorArrayOverview.push(colorArray4);
	
	var colorArray5 = ["#D50096", "#22C3C3", "#48E470", "#9c6eff", "#FF9900"];
	colorArrayOverview.push(colorArray5);
	
	var colorArrayIndex = Math.floor(Math.random()*colorArrayOverview.length);
	for (var i = 0; i < nrOfColors; i++) {
		result.push(colorArrayOverview[colorArrayIndex][i]);
	}
	return result;
		
};

Util.getHighlightedColor = function(color) {
	var reduceRGBby = 20;
	var articleColorRGB = hexToRgb(color);
	var articleColor = rgbToHex(Math.max(articleColorRGB.r - reduceRGBby,0),Math.max(articleColorRGB.g - reduceRGBby,0) , Math.max(articleColorRGB.b - reduceRGBby,0));
	return articleColor;
};

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}



window.Util = Util;
})(this, this.document);