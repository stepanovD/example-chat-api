/**
 * Created by dmitry on 27.02.2017.
 */

api_domain = "http://127.0.0.1:5000";
//api_domain = "http://u22901.netangels.ru";
__r = {};

function load_main_resource() {
    $.getJSON(api_domain + "/api/", function (data) {
        __r = data;
        if (data._links.login != undefined) {
            $("#login-container").show();
            $("#chat-container").hide();
        } else {
            $("#login-container").hide();
            $("#chat-container").show();
        }
    })
        .done(function () {
            console.log("second success");
        })
        .fail(function () {
            console.log("error");
        })
        .always(function () {
            console.log("complete");
        });
}

function login_request() {
    $loginForm = $("#form-login");
    loginVal = $loginForm.find("#login").val();
    passwordVal = $loginForm.find("#inputPassword").val();

    $.ajax(api_domain + __r._links.login, {
            data: JSON.stringify({login: loginVal, password: passwordVal}),
            contentType: 'application/json',
            type : 'POST'
        }
    )
        .
        done(function () {
            console.log("login success");
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

load_main_resource();
