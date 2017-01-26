function getRank() {
	var star_1 = document.getElementById("star-5");
	var star_2 = document.getElementById("star-4");
	var star_3 = document.getElementById("star-3");
	var star_4 = document.getElementById("star-2");
	var star_5 = document.getElementById("star-1");
	var rank = document.getElementById("rank")
	if (star_5.checked) {
		rank.value="5";
	}else if (star_4.checked){
		rank.value="4";
	}else if (star_3.checked){
		rank.value="3";
	}else if (star_2.checked){
		rank.value="2";
	}else if (star_2.checked){
		rank.value="1";
	}
}

function addMoreFile() {
	var moreimage = $("#moreimage");
	var num = $(":input[type='file']").length + 1;
	var file = $("<input />").attr("type", "file").attr("name","image"+num);
	moreimage.prepend(file);
}