// http://masonry.desandro.com/masonry.pkgd.js added as external resource
// http://masonry.desandro.com/components/classie/classie.js added as external resource


//global variables
var node;
var articles;
var container = document.querySelector('.masonry');

//  given data for article tiles
// var colorArray = getColorArray(5);
var nodeId = 0;
var widthReference = 200;
var heightReference = 200;
var importanceUnit = 50;
var heightImportance = false;


// Masonry library
var msnry = new Masonry( container, {
	columnWidth: 1
});


// articlesObject should be fetched from server in the future and not from example javascript israel-data.js file
function getArticlesObj(node, articles) {
	var articlesObject = new Array();

	for (key in articles) {
		var article = articles[key];
		if (node.id == articles[key].nodeID) {
			articlesObject.push(articles[key]);
		}
    }
	return articlesObject;
}

// is called when clicked on node
function populateArticles(node) {
	var node = node;
	var articlesObj = getArticlesObj(node, currentData.articles);
	articles = getArticlesObj(node, currentData.articles);


	// console.log("old articles: ");
	// console.log(articles);


	// console.log("new articles: ");
	// console.log(finalJson);
	// console.log(finalJson.articles);

	// articles = finalJson.articles;

	// remove current articles 
	while (container.hasChildNodes()) {
		//console.log("in remov");
		msnry.remove(container.lastChild);
		container.removeChild(container.lastChild);
	}

	
	// random # articles are shown -
	// startingIndex = Math.floor(Math.random()*articles.length);
	var startingIndex = 0;
	if (startingIndex == articles.length-1){
		startingIndex = articles.length-2;
	}

	drawArticles(startingIndex, articles.length-1, articles, msnry, node);		

	
	//Binds event listener to window resize, so layout is triggered when the browser window is resized.
	msnry.bindResize()

}

// getWidth of respective article  based on importance
function getWidth(article, widthReference, importanceUnit){
	var result = widthReference+(article.importance*importanceUnit);
	var id = "article" + article.id;
	return result;
}


// gets Height of respective article
function getHeigth(article, heightReference, heightImportance, importanceUnit){
	var result = heightReference+(article.importance*importanceUnit);
	if (heightImportance) {
		return result;
	}
	else 
		return heightReference;
}

function generateRandomImportance(){
	return Math.floor(1+Math.random()*5);

}

// draw dynamically all the articles
function drawArticles(startingArtInd, endArtInd, articles, msnry, node) {
	// hide info element
	$('.box #info').hide();

	// var articleColor = colorArray[0];
	var articleColor =  Util.getHighlightedColor(node.color);
	// var articleColor = node.color;

	var currentWidthInLine = 0;
	var maxWidth = container.clientWidth - 15;
	
	var inRow = 1;
	var maxNrOfRows = 2;

	// draw each article box
	for (var i = startingArtInd; i < endArtInd; i++)  {

		articles[i].importance = generateRandomImportance();


		/// create div with article+i ID
		var article = document.createElement('div');

		//only show a certain Nr of rows (and onlys shows complete rows)
		if (inRow<=maxNrOfRows) {
		container.appendChild( article );
		}
		else {
			//leave for loop
			break;
		}
		article.id ='article'+i;	
		article.className = "item";
		

		var articleWidth = getWidth(articles[i], widthReference, importanceUnit)
		currentWidthInLine += articleWidth;

		// get the right width of each element: the last item in the row gets expanded to the maxSize of the container
		// if not last item
		if (i < endArtInd - 1 ){
			var nextArticleWidth = getWidth(articles[i+1], widthReference, importanceUnit)
			// if last item in row
			if (nextArticleWidth + currentWidthInLine > maxWidth) {
				article.style.width = articleWidth + (maxWidth - currentWidthInLine) +"px";
				inRow++;
				// console.log("in last item , next ArticleWIdth;" + nextArticleWidth );
				// console.log("in last item ;" + article.style.width );
				// console.log('currentWidthInLine:' + currentWidthInLine);
				// console.log('maxWidth:' + maxWidth);
				currentWidthInLine = 0;
			}
			else {
				// console.log('else');
				article.style.width = articleWidth +"px";
			}
		}
		else {
			// console.log('in last element else');
			article.style.width = articleWidth +"px";
		}		

			
		// console.log("after the loop :" + article.style.width);
		// console.log("-----next Tile");
		article.style.height = getHeigth(articles[i], heightReference, heightImportance, importanceUnit)  +"px";
		// article.style.width = "250px";
		// article.style.height = "250px";

		
		/// add text to articleDiv
		var articleText = document.createElement('div');
		articleText.className = "item-content";
		var importanceClass = "importance"+articles[i].importance;
		articleText.innerHTML = '<div class="title ' + importanceClass + '" >'+  articles[i].title +  '<div class="publisher timestamp">' + articles[i].publisher + ', ' + articles[i].timestamp + '</div></div>' ; 
		// $(articleText).append("<div class='previewText'>" + articles[i].previewText.substring(0,100) + "... </br></div>");
		// $(articleText).append("<div class='timestamp'>"	 + articles[i].timestamp + "</div>");
		// $(articleText).append("<div class='publisher'> By: " + articles[i].publisher + "</div>");
		articleText.style.width = article.style.width;
		articleText.style.height = article.style.height;
		articleText.style.background = articleColor;
		article.appendChild(articleText);

		// add backGround picture to articleDiv
		var articleBackground = document.createElement('div');
		articleBackground.className = "article-background-pic";
		// CSS of this div
		//articleBackground.style.backgroundImage = 'url(' + articles[i].image + ')';
		articleBackground.style.top =  articleText.style.top;
		articleBackground.style.left = articleText.offsetLeft + "px";
		articleBackground.style.top = articleText.offsetTop + "px";
		articleBackground.style.width = article.style.width;
		articleBackground.style.height = article.style.height;
		article.appendChild(articleBackground);

		// gives the article as js Object and the articleDiv element
		TileLightbox.createLightbox(articles[i], articleBackground);


		msnry.appended( article );
		//makes visual,appearing effects
		msnry.layout();

	}
}


