var hide;
var group_name;
var group_subject;
var friend_name;
var roomname="";
var compare;
var arg = "";

function tips_pop() {　
    view(group_name);
    friend(friend_name);
    var MsgPop = document.getElementById("winpop");
    var popH = parseInt(MsgPop.style.height);
    if (popH <= 40) {
        MsgPop.style.display = "block";
        hide = setInterval("changeH('up')", 2);
    }
    else {
        hide = setInterval("changeH('down')", 2);
    }
}
function changeH(str) {

    var MsgPop = document.getElementById("winpop");
    var popH = parseInt(MsgPop.style.height);
    if (str == "up") {
        if (popH <= 210) {
            MsgPop.style.height = (popH + 8).toString() + "px";
        }
        else {
            clearInterval(hide);
        }
    }
    if (str == "down") {
        if (popH >= 40) {
            MsgPop.style.height = (popH - 8).toString() + "px";
        }
        else {
            clearInterval(hide);
        }
    }
}
window.onload = function () {
    document.getElementById('winpop').style.height = '0px';
    getJoinedGroup();
    getFriends();
    setTimeout("tips_pop()", 1000);
}

function view(s) {
    var str = '';
    for (var i = 0; i < s.length; i++) {
        str += "<li style=\"list-style-type:none;\"><a style=\"margin-left:-20px\"href='javascript:createChat("+s[i]+")'>" + group_subject[i] + "</a><a style=\"float:right; margin-right:3px;margin-left:10px\" href=\"/quit-group/"+s[i]+"\">Quit</a></li>";
    }
    document.getElementById("myorder").innerHTML = "<h5 style=\"margin-left:5px\">Groups</h5><ul>" + str + "</ul>";
}

function friend(s) {
    var str = '';
    for (var i = 0; i < s.length; i++) {
        arg=s[i];
        str += "<li><a href=\"javascript:friendChat("+arg+")\" id=\""+s[i]+"\">" + s[i] + "</a></li>";
    }
    document.getElementById("myfriend").innerHTML = "<hr><h5 style=\"margin-left:5px\">Friends</h5><ul>" + str + "</ul>";
}

function getJoinedGroup() {
    $.get("/get-joined-group/")
        .done(function (data) {
            group_name = data['group'];
            group_subject = data['group_subject'];
            console.log(data['group']);
            console.log(data['group_subject']);
        });
}

function getFriends() {
    $.get("/get-friends/")
        .done(function (data) {
            friend_name = data['friend'];
            compare = data['user'];
        });
}

function createChat(id) {
    window.open ("/post-chat/"+id, "Chat Room", "height=700, width=1200, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}

function friendChat(arg) {
    var arg = $(arg).html()
    if (arg<compare){
        roomname = arg + "_" +compare;
    }else{
        roomname = compare+"_"+arg;
    }
    window.open ("/friend-chat/"+roomname, "Chat Room", "height=600, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}