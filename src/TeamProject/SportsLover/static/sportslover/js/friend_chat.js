var str;
var str2;

function addItem(){
    var itemField = $("#item-field");
    $.post("/add-friend-chat", {chat: itemField.val(), 'roomname':roomname})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

function populateList() {
    $.post("/get-friend-chats/", {'roomname': roomname})
      .done(function(data) {
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


function getUpdates() {
    var list = $("#chat-list")
    var max_time = list.data("max-time")
    $.post("/get-friend-changes/"+ max_time, {'roomname': roomname})
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

var roomname = document.getElementById("roomname").value;

$(document).ready(function () {

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
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

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#item-field").focus();

  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);

});
