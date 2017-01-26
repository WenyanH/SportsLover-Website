var str;
var str2;

function addItem(){
    var itemField = $("#item-field");
    $.post("/add-chat", {chat: itemField.val(), 'group_id':group_id})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

function populateList() {
    $.post("/get-chats/", {'group_id': group_id})
      .done(function(data) {
          var flag=false;
          members = data.members.split(",");
          var member = $("#member");
          friends = data.friends.split(",");
          for (var i=0; i<members.length; i++){
            for(var j=0; j<friends.length;j++){
                if(members[i]==friends[j]){
                    flag=true;
                }
            }
            if(flag == true){
                var member_html = $("<div></div>").attr("class","panel-body").html(
                "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                +members[i]
                +"</h4></div><div style=\"float:right\">"
                +"<input class=\"btn-sm btn-warning\" type=\"submit\" text=\"Add item\" value=\"Friends\" disabled>"
                +"<input class=\"btn-sm btn-warning\" type=\"submit\" onclick='pay()' text=\"Add item\" value=\"Pay\" style=\"margin-left:10px;float:right\">"
                +"</div></div></div></div>"
                )
                member.append(member_html);
            }
            if(flag == false){
                if(members[i]==data.user){
                    var member_html = $("<div></div>").attr("class","panel-body").html(
                    "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                    +members[i]
                    +"</h4></div><div style=\"float:right\">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" text=\"Add item\" value=\"Myself\" disabled>"
                    +"</div></div></div></div>"
                    )
                }
                if(members[i]!=data.user){
                    str = members[i];
                    str2=data.user;
                    var member_html = $("<div></div>").attr("class","panel-body").html(
                    "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                    +members[i]
                    +"</h4></div><div style=\"float:right\">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" name=\"request\" onclick=\"friendRequest(\'"+members[i]+"\')\" text=\"Add item\" value=\"UnFriends\" id="+members[i]+">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" onclick='pay()' text=\"Add item\" value=\"Pay\" style=\"margin-left:10px;float:right\">"
                    +"</div></div></div></div>"
                    )
                }
                member.append(member_html);
            }
            flag=false;
          }
          var list = $("#chat-list");
          list.data('max-time', data['max-time']);
          list.html('')
          for (var i = 0; i < data.chats.length; i++) {
              chat = data.chats[i];
              var new_chat = $(chat.html);
              new_chat.data("chat-id", chat.id);
              if(chat.sender==data.user){
                new_chat.attr("style","color:purple")
              }
              list.append(new_chat);
          }
      });
}

function updateMember(){
    $.post("/get-chats/", {'group_id': group_id})
      .done(function(data) {
          members = data.members.split(",");
          var member = $("#member");
          $('#member').children().first().siblings().remove();
          var flag=false;
          friends = data.friends.split(",");
          for (var i=0; i<members.length; i++){
            for(var j=0; j<friends.length;j++){
                if(members[i]==friends[j]){
                    flag=true;
                }
            }
            if(flag == true){
                var member_html = $("<div></div>").attr("class","panel-body").html(
                "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                +members[i]
                +"</h4></div><div style=\"float:right\">"
                +"<input class=\"btn-sm btn-warning\" type=\"submit\" text=\"Add item\" value=\"Friends\" disabled>"
                +"<input class=\"btn-sm btn-warning\" type=\"submit\" onclick='pay()' text=\"Add item\" value=\"Pay\" style=\"margin-left:10px;float:right\">"
                +"</div></div></div></div>"
                )
                member.append(member_html);
            }
            if(flag == false){
                if(members[i]==data.user){
                    var member_html = $("<div></div>").attr("class","panel-body").html(
                    "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                    +members[i]
                    +"</h4></div><div style=\"float:right\">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" text=\"Add item\" value=\"Myself\" disabled>"
                    +"</div></div></div></div>"
                    )
                }
                if(members[i]!=data.user){
                    str = members[i];
                    str2=data.user;
                    var member_html = $("<div></div>").attr("class","panel-body").html(
                    "<div class=\"media\"><div class=\"media-body\"><div style=\"float:left\"><h4>"
                    +members[i]
                    +"</h4></div><div style=\"float:right\">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" onclick=\"friendRequest(\'"+members[i]+"\')\" name=\"request\" text=\"Add item\" value=\"UnFriends\" id="+members[i]+">"
                    +"<input class=\"btn-sm btn-warning\" type=\"submit\" onclick='pay()' text=\"Add item\" value=\"Pay\" style=\"margin-left:10px;float:right\" >"
                    +"</div></div></div></div>"
                    )
                }
                member.append(member_html);
            }
            flag=false;
          }
      });
}

function getUpdates() {
    var list = $("#chat-list")
    var max_time = list.data("max-time")
    $.post("/get-changes/"+ max_time, {'group_id': group_id})
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.chats.length; i++) {
              var chat = data.chats[i];
              if (chat.deleted) {
                  $("#chat_" + chat.id).remove();
              } else {
                  var new_chat = $(chat.html);
                  new_chat.data("chat-id", chat.id);
                  if(chat.sender==data.user){
                    new_chat.attr("style","color:purple")
                  }
                  list.append(new_chat);
              }
          }
      });
}

function friendRequest(reciever){
  sender = str2;
  var notification = sender+" want to be friend with you.";
  $.post("/friend_request/", {'notification': notification, 'reciever':reciever, 'sender':sender})
  .done(function(data){
      if(data.send == "never"){
        $('body').html("<p>You have sent the friend request to the user</p><p>Turn off the page and wait for approval.</p>");
      }
      if(data.send == "already"){
         $('body').html("<p>You have already send friend request with this user.</p>");
      }
  });
}

function pay(){
  window.open('/charge/');
}

var group_id = document.getElementById("group_id").value;

$(document).ready(function () {

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

  // Add event-handlers
  $("#add-btn").click(addItem);
  $("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );
  //$("#todo-list").click(deleteItem);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#item-field").focus();

  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);
  window.setInterval(updateMember, 5000);
  $("[name=request]").click(friendRequest);

});
