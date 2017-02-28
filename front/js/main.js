/**
 * Created by dmitry on 27.02.2017.
 */

//api_domain = "http://127.0.0.1:5000";
api_domain = "http://u22901.netangels.ru";
__r = {};
auth_token = '';

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
        .always(function () {
            console.log("complete");
        });
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
        .always(function () {
            console.log("login complete");
        });
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
            console.log("registry success");
            load_main_resource();
        })
        .fail(function (data) {
            console.log("registry error");
            console.log(data)
        })
        .always(function () {
            console.log("registry complete");
        });
}

function load_users() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + __r._links.users,
        success: function (data) {
            console.log(data);
        }
    })
        .fail(function () {
            console.log("load_users error");
        })
        .always(function () {
            console.log("complete");
        });
}

function load_shared_messages() {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + __r._links.messages,
        success: function (data) {
            for(var i in data){
                append_message(data[i]);
            }
        }
    })
        .fail(function () {
            console.log("load_messages error");
        })
        .always(function () {
            console.log("load_messages complete");
        });
}

function append_message(message_resource) {
    $('#chat_messages').prepend('<div class="well well-small" id="msg-' + message_resource.id + '">'+
    '<p class="msg-text" id="msg-' + message_resource.id + '-text">' + message_resource.content + '</p>' +
    '<div class="msg-meta">'+
    '<span class="msg-time">' + message_resource.timestamp + '</span>'+
    '<span class="msg-author" id="msg-' + message_resource.id + '-author"></span>'+
    '</div></div>');

    append_author(message_resource.id, message_resource._links.author);
}

function append_author(message_id, author_url) {
    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-Auth-Token", auth_token);
        },
        dataType: "json",
        url: api_domain + author_url,
        success: function (data) {
            $('#msg-' + message_id + '-author').append('<p class="text-info">' + data.email + '</p>')
        }
    });
}

function init_chat(){
    load_shared_messages();
    load_users();

    $("#login-container").hide();
    $("#chat-container").show();
}

load_main_resource();
