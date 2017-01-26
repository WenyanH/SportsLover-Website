$('.datetimepicker').datetimepicker();

function selectBall() {
	var item = document.getElementById("Ball");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectSky() {
	var item = document.getElementById("Sky");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectMountain() {
	var item = document.getElementById("Mountain");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectWater() {
	var item = document.getElementById("Water");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectMotor() {
	var item = document.getElementById("Motor");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectIce() {
	var item = document.getElementById("Ice");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function selectWild() {
	var item = document.getElementById("Wild");
	var sportsclass = document.getElementById("id_sportsclass");
	sportsclass.value = item.id;
}

function cancelGroup() {
	window.close();
}