$( document ).ready(function () {
    $("[name=placeimage]").first().attr("class", "item active");
});

window.onload = function () {
    var check_login = document.getElementById("check_login");
    var login = document.getElementById("login");
    var user = document.getElementById("user");
    var notification = document.getElementById("notification");
    var settings = document.getElementById("settings");
    if (check_login.value!="AnonymousUser") {
        login.style.display = "none";
        user.style.display = "block";
        notification.style.display = "block";
        settings.style.display = "block";
    } else {
        login.style.display = "block";
        user.style.display = "none";
        notification.style.display = "none";
        settings.style.display = "none";
    }
}

function openOriginal() {
    var id = $(".active").attr('id');
    subWin_2=window.open ("/place-photo/"+id, "Place Image", "height=600, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
     if(subWin_2.opener==null){
            subWin_2.opener=self;
        }
}