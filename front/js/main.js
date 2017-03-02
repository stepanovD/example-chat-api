/**
 * Created by dmitry on 27.02.2017.
 */

//api_domain = "http://127.0.0.1:5000";
api_domain = "http://u22901.netangels.ru";
__r = {};
auth_token = '';
__e = {users: [], currentChat: undefined};

function load_main_resource() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + "/api/",
        success: function (data) {
            __r = data;
            if (data._links.login != undefined) {
                $("#login-container").show();
                $("#chat-container").hide();
            } else {
                init_chat();
            }
        }
    })
        .done(function () {
            console.log("second success");
        })
        .fail(function () {
            console.log("error");
            $("#login-container").show();
            $("#chat-container").hide();
        })
}

function login_request() {
    $loginForm = $("#form-login");
    emailVal = $loginForm.find("#email").val();
    passwordVal = $loginForm.find("#inputPassword").val();

    $.ajax(api_domain + '/api/login/', {
            data: JSON.stringify({email: emailVal, password: passwordVal}),
            contentType: 'application/json',
            type: 'POST'
        }
    )
        .
        done(function (data) {
            console.log("login success");
            auth_token = data.token;
            load_main_resource();
        })
        .fail(function (data) {
            console.log("login error");
            console.log(data)
        })
}

function registry_request() {
    $loginForm = $("#form-login");
    emailVal = $loginForm.find("#email").val();
    passwordVal = $loginForm.find("#inputPassword").val();

    $.ajax(api_domain + '/api/registry/', {
            data: JSON.stringify({email: emailVal, password: passwordVal}),
            contentType: 'application/json',
            type: 'POST'
        }
    )
        .
        done(function (data) {
            alert("registry success");
        })
        .fail(function (data) {
            console.log("registry error");
            console.log(data)
        })
}

function send_message() {
    $msgForm = $("#form-message");
    msgVal = $msgForm.find("#inputMessage").val();

    resource = __e.currentChat == undefined ? {content: msgVal} :
    {content: msgVal, chat_id: __e.currentChat.id};

    $.ajax(api_domain + __r._links.messages, {
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth-Token", auth_token);
            },
            data: JSON.stringify(resource),
            contentType: 'application/json',
            type: 'POST'
        }
    )
        .
        done(function (data) {
            refresh_chat();
        })
        .fail(function (data) {
            alert("failed");
            console.log(data)
        })
}

function load_users() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + __r._links.users,
        success: function (data) {
            for (var i in data) {
                __e.users[data[i]._links.self] = data[i];
            }
            //console.log(data);
        }
    })
        .fail(function () {
            console.log("load_users error");
        })
}

function load_messages() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + (__e.currentChat == undefined ? __r._links.messages : __e.currentChat._links.messages),
        success: function (data) {
            for (var i in data) {
                append_message(data[i]);
            }
        }
    })
        .fail(function () {
            console.log("load_messages error");
        })
}

function append_message(message_resource) {
    authorClass = message_resource._links.author == __r._links.self ? "self-msg col-lg-offset-4" : "";
    //authorClassColor = message_resource._links.author == __r._links.self ? "bg-success" : "bg-primary";
    $('#chat_messages').prepend('<div class="row"><div class="well well-small col-lg-5 msg ' + authorClass + '" id="msg-' + message_resource.id + '">' +
    '<p class="msg-text" id="msg-' + message_resource.id + '-text">' + message_resource.content + '</p>' +
    '<div class="msg-meta">' +
    '<span class="msg-time">' + message_resource.timestamp + '</span>' +
    '<span class="msg-author" id="msg-' + message_resource.id + '-author"></span>' +
    '</div></div></div>');

    append_author(message_resource.id, message_resource._links.author);
}

function append_author(message_id, author_url) {
    $('#msg-' + message_id + '-author').append('<p class="text-info">' + __e.users[author_url].email + '</p>');
    //$.ajax({
    //    beforeSend: function (request) {
    //        request.setRequestHeader("X-Auth-Token", auth_token);
    //    },
    //    dataType: "json",
    //    url: api_domain + author_url,
    //    success: function (data) {
    //        $('#msg-' + message_id + '-author').append('<p class="text-info">' + data.email + '</p>')
    //    }
    //});
}

function load_chats() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + __r._links.chats,
        success: function (data) {
            for (var i in data) {
                append_chat(data[i]);
            }
        }
    })
        .fail(function () {
            console.log("load_messages error");
        })
}

function load_chat(chat_url) {
    if (chat_url == undefined) {
        __e.currentChat = undefined;
        refresh_chat();
    } else {
        $.ajax({
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth-Token", auth_token);
            },
            dataType: "json",
            url: api_domain + chat_url,
            success: function (data) {
                __e.currentChat = data;
                refresh_chat();
            }
        })
            .fail(function () {
                console.log("load_messages error");
            })
    }
}

function append_chat(chat_resource) {
    $chatsPanel = $('#dynamic-chats');
    var link = $('<a class="chat-selector" href="#"><div class="row">' + chat_resource.title + '</div></a>');
    link.click(function () {
        load_chat(chat_resource._links.self);
    });
    $chatsPanel.append(link);
}

function init_chat() {
    load_users();
    load_chats();
    load_messages();

    $("#login-container").hide();
    $("#chat-container").show();
}

function refresh_chat() {
    $('#chat_messages').empty();
    $('#inputMessage').val('');
    load_messages();
}

load_main_resource();
