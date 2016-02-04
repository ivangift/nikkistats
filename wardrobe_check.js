function checking() {
	var raw = getWardrobe();
	var clothes = {};
	var missing = {};
	var sections = raw.split('|');
  for (var i in sections) {
    if (sections[i].length < 1) {
      continue;
    }
    var section = sections[i].split(':');
    var type = section[0];
    if (type == "上装") {
      type = "上衣";
    }
    clothes[type] = {};
    missing[type] = [];
    var ids = section[1].split(',');
    for (var i in ids) {
    	clothes[type][ids[i]] = true;
    }
  }
	for (var i in wardrobe) {
    var cate = wardrobe[i][1];
    var id = wardrobe[i][2];
    if (clothes[cate]) {
    	if (!clothes[cate][id]) {
    		missing[cate].push(id);
    	}
    }
  }

  for (var cate in missing) {
  	missing[cate].sort();
  	var div = $("<div>");
  	div.append("<p>" + cate + "</p>");
  	for (var i in missing[cate]) {
  		div.append(missing[cate][i] + " &nbsp;");
  	}
  	$("#missing").append(div);
  }
}

function getWardrobe() { 
  var metas = document.getElementsByTagName('meta'); 

  for (i=0; i<metas.length; i++) { 
    if (metas[i].getAttribute("name") == "wardrobe") { 
      return metas[i].getAttribute("content"); 
    } 
  } 

  return "";
} 

$(document).ready(function() {
  checking();
});