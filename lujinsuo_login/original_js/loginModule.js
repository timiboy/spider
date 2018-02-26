var Login_NS = {
    isCheckAjaxVCodeOk: !1,
    isSubmitted: !1,
    $errorTips: $(".errorTips"),
    checkCaptchaErrorMsg: "",
    loginTimeout: function () {
        var a = $("#status").val();
        "timeOut" == a && Login_NS.showErrors("登录超时，请您重新登录。")
    }, checkCaptcha: function (a, e) {
        var s = a || e.value;
        if (!s || s == $(e).data("placeholder")) return Login_NS.checkCaptchaErrorMsg = "请填写验证码。", $.validator.messages.checkCaptcha = Login_NS.checkCaptchaErrorMsg, !1;
        if (!Login_NS.isCheckAjaxVCodeOk) {
            var o = {};
            o.inputValue = s, o.source = "login", $.ajax({
                type: "GET",
                async: !1,
                cache: !1,
                dataType: "json",
                url: "captcha/pre-check",
                data: o,
                success: function (a) {
                    switch (Login_NS.isCheckAjaxVCodeOk = !1, a.result) {
                    case "SUCCESS":
                        return Login_NS.isCheckAjaxVCodeOk = !0, !0;
                    case "EXPIRED":
                    case "INPUT_WRONG_CODE":
                    case "INPUT_WRONG_CODE_AJAX":
                    case "IMAGE_ID_NOT_EXIST":
                    case "REAPPLY":
                    case "INVALIDED_CHECK":
                    case "IPADDRESS_WRONG":
                    case "UNDEFINED":
                    default:
                        Login_NS.isCheckAjaxVCodeOk = !1, Login_NS.checkCaptchaErrorMsg = "验证码错误。"
                    }
                }, error: function () {
                    Login_NS.checkCaptchaErrorMsg = "验证码错误。", Login_NS.isCheckAjaxVCodeOk = !1
                }
            }).error(errorHandler()), Login_NS.isCheckAjaxVCodeOk || Login_NS.changeCaptcha(!0), $.validator.messages.checkCaptcha = Login_NS.checkCaptchaErrorMsg
        }
        return Login_NS.isCheckAjaxVCodeOk
    }, changeCaptcha: function (a, e) {
        return $("#validateImg").attr("src", "captcha/captcha.jpg?source=login&_=" + (new Date).getTime()), Login_NS.isCheckAjaxVCodeOk = !1, e || $("#validNum").val(""), a && $("#validNum").focus(), !1
    }, showErrors: function (a, e) {
        $("#" + e).parent().addClass("error");
        var s = Login_NS.$errorTips.hide().empty().html('<i class="icon minusCircleIcon"></i>').append('<p class="errorContent">' + a + "</p>").show();
        s.slideDown("fast"), "validNum" == e && $("#validNum").siblings(".icon").removeClass("correctCircleIcon").addClass("failureCircleIcon")
    }, removeErrors: function (a) {
        $(".errorTips").slideUp("fast"), $("#" + a).parent().removeClass("error"), "validNum" == a && $("#validNum").siblings(".icon").removeClass("failureCircleIcon").addClass("correctCircleIcon")
    }, changeTab: function (a) {
        "mobile" == a ? ($("#userNameLogin").attr("data-placeholder", "手机号"), $(".place-holder").html("手机号"), $('.login-tab[data-role="userName"]').removeClass("active"), $("#loginFlagValue").val("2"), $("#forgetUserName").length > 0 && $("#forgetUserName").css("display", "none"), $('.login-tab[data-role="' + a + '"]').addClass("active")) : "userName" == a && ($("#userNameLogin").attr("data-placeholder", "用户名"), $(".place-holder").html("用户名"), $("#forgetUserName").length > 0 && $("#forgetUserName").css("display", ""), $('.login-tab[data-role="mobile"]').removeClass("active"), $('.login-tab[data-role="' + a + '"]').addClass("active"), $("#loginFlagValue").val(""))
    }, rsaChg: function () {
        if ($("#pwd").val()) {
            var a = new RSAKey;
            a.setPublic($("#publicKey").val(), $("#rsaExponent").val());
            var e = a.encrypt($("#pwd").val());
            $("#password").val(e), $("#pwd").val("************")
        }
    }, winResize: function () {
        var a = $(window).height(),
            e = ($(document).height(), $("#lufax-header").height() + 3),
            s = $(".lufax-footer").height() + 71,
            o = e + s + 650;
        o > a ? $(".login-wrap").height(650) : $(".login-wrap").height(a - e - s)
    }, clearText: function () {
        $("#pwd").val(""), $("#validNum").siblings(".icon").removeClass("correctCircleIcon").removeClass("failureCircleIcon")
    }, isMobile: function () {
        var a = /iphone|ipod|blackberry|android|iemobile/i;
        return a.test(navigator.userAgent.toLowerCase())
    }, showSafeImgBox: function (a) {
        var e = [];
        e.push('<div class="safeimage-wrap">'), e.push('<a class="closebtn cancleBtn J_closesafeImage" href="javascript:;"></a>'), e.push('<div class="safeimage-top">'), e.push('<span class="safeimage-title">' + a.userName + "，您好，请设置安全头像</span>"), e.push("</div>"), e.push('<div class="safeimage-con">'), e.push('<div class="safeimage-step safeimage-stepbox1">'), e.push('<div class="safe-type">方式一：上传图片作为安全头像</div>'), e.push('<a href="/user/safeimage" class="btns btn_info btn-large" style="position: absolute; right:20px; top:15px;">自定义头像</a>'), e.push("</div>"), e.push('<div class="safeimage-step safeimage-stepbox2">'), e.push('<div class="safe-type">方式二：使用随机分配的图片作为安全头像</div>'), e.push('<a style="width:70px;position: absolute; right:20px; top:60px;" class="btns btn_cancel btn-large J_saveDefault">确定</a>'), e.push('<img src="' + a.avatarUrl + '">'), e.push("</div>"), e.push("</div>"), e.push("</div>"), lufax.popup.blankPopup({
            content: e.join("")
        }), $(".J_saveDefault").unbind().bind("click", function () {
            $.ajax({
                url: "service/avatar/modify-user-avatar-info",
                dataType: "json",
                data: {
                    source: "user-web",
                    imgId: "0"
                },
                type: "POST",
                success: function (a) {
                    location.href = UrlPrefix.myHostUrl + "/account"
                }
            })
        })
    }, isMobileNo: function (a) {
        return /^((1)[\d]{10})$/.test(a)
    }, showCaptcha: function () {
        $(".J_validNumBox").hasClass("hidden") && ($(".J_validNumBox").removeClass("hidden"), $(".J_validNum").removeClass("hidden"), $(".J_validNum").val($(".J_validNum").attr("data-placeholder")))
    }, syncCookieToDomain: function (a) {
        if (a && "function" == typeof a) try {
            SSO.syncCookieToDomain(a)
        } catch (e) {
            a()
        } else try {
            SSO.syncCookieToDomain(function () {})
        } catch (e) {}
    }, checkUserStatus: function (a) {
        var e = this;
        if ("0" == a.avatarStatus && !e.isMobile() && "1" == a.cardBindStatus && "1" == a.securityQuestionStatus && "1" == a.tradingPasswordStatus && "1" == a.nameAuthentication) return e.showSafeImgBox(a), void $(".J_closesafeImage").unbind().bind("click", function () {
            if (!loginUserStatusChecker || !loginUserStatusChecker.statusCheck(a, a.redirectPath)) try {
                SSO.syncCookieToDomain(function () {
                    window.location = a.redirectPath
                })
            } catch (e) {
                window.location = a.redirectPath
            }
        });
        try {
            SSO.syncCookieToDomain(function () {
                window.location = a.redirectPath
            })
        } catch (s) {
            window.location = a.redirectPath
        }
    }, createDeviceFingerPrint: function () {
        var a = "",
            e = "",
            s = "",
            o = $("#deviceKey"),
            i = $("#deviceInfo");
        if (lufax.util.fingerPrint && (a = lufax.util.fingerPrint.getAesEncriptedFingerPrintInfo())) {
            e = a.key, s = a.info;
            var n = new RSAKey;
            n.setPublic($("#publicKey").val(), $("#rsaExponent").val());
            var t = n.encrypt(e);
            o && o.val(t), i && i.val(s)
        }
    }, showIdTips: function (a, e) {
        lufax.popup.newIconPopup({
            popupTitleName: "重要提示",
            iconClass: "",
            message: '<p class="message-title" style="text-align: center" ><i class="ld-icon ld-icon-exclamation" style=" margin: 0 5px 0 0;color: #FF921B "></i>您的身份证件将于' + e.idValidEndDate + '到期，逾期未更换将影响您的正常工作，请更换证件。</p><div class="union-success" ></div>',
            contentWidth: "530px",
            bodyPadding: "20px 20px 40px 40px ",
            closeDisplay: "true",
            button: "<a class='btns btn_info cancleBtn' href='javascript:void(0);' data-sk='OK_JointLogin'>立即更換</a>",
            onCancel: function () {
                try {
                    SSO.syncCookieToDomain(function () {
                        window.location = url("replace-passport")
                    })
                } catch (a) {
                    window.location = url("replace-passport")
                }
            }, onClose: function () {
                Login_NS.checkUserStatus(data)
            }
        })
    }, checkShouldFace: function (a, e) {
        $.ajax({
            url: url("get-user-status"),
            type: "GET",
            data: {
                securityAuthLoginStatus: "1"
            },
            dataType: "json",
            async: !1,
            success: function (s) {
                if (s.data.securityAuthLoginStatus && "1" == s.data.securityAuthLoginStatus) try {
                    SSO.syncCookieToDomain(function () {
                        window.location.href = url("ym-face?redirectPath=" + a.redirectPath)
                    })
                } catch (o) {
                    window.location.href = url("ym-face?redirectPath=" + a.redirectPath)
                } else e()
            }, error: function (a) {
                e()
            }
        })
    }, checkUserInfoAfterLoginSuccess: function (a) {
        $.ajax({
            url: url("gerUserInfo"),
            type: "GET",
            dataType: "json",
            async: !1,
            success: function (e) {
                e ? 1 == e.idValidPopup ? 0 == e.idValidStatus || 1 == e.idValidStatus ? "01" == e.nationality || "02" == e.nationality ? Login_NS.showIdTips(1, e) : "03" == e.nationality && Login_NS.showIdTips(0, e) : Login_NS.checkUserStatus(a) : a.isForceSetTradingPwd && "1" == a.isForceSetTradingPwd ? lufax.popup.newIconPopup({
                    popupTitleName: "重要提示",
                    iconClass: "",
                    message: '<p class="message-title" style="text-align: center" ><i class="ld-icon ld-icon-exclamation" style=" margin: 0 5px 0 0;color: #FF921B "></i>您未设置交易密码,为保障您的资金安全,建议您立即设置</p><div class="union-success" ></div>',
                    contentWidth: "530px",
                    bodyPadding: "20px 20px 40px 40px ",
                    closeDisplay: "false",
                    button: "<a class='btns btn_info cancleBtn' href='javascript:void(0);' data-sk='OK_JointLogin'>立即前往</a>",
                    onCancel: function () {
                        try {
                            SSO.syncCookieToDomain(function () {
                                window.location = url("set-trade-password")
                            })
                        } catch (a) {
                            window.location = url("set-trade-password")
                        }
                    }
                }) : Login_NS.checkUserStatus(a) : Login_NS.checkUserStatus(a)
            }, error: function (e) {
                Login_NS.checkUserStatus(a)
            }
        })
    }, dealLoginRequest: function (a) {
        $("#loginFlagnew").html("登&emsp;录"), $("#loginBtn").removeClass("disabled");
        var e = JSON.parse(a),
            s = e.maskMobileNo;
        if ("00" != e.resultId) return e && "MOBILE_NO_DUPLICATE" === e.resultMsg ? LufaxPopup.popup({
            popupTitleName: "提示",
            iconClass: "exclamationCircleIcon",
            message: "<span class='orange_word'>手机号码" + s + "与多个账户相关联，仅可使用用户名登录</span>",
            button: "<a class='btns btn_info close ml20' href='javascript:;' target='_self' id='userNameLoginOnlyButton'>使用用户名登录</a>",
            onClose: function () {
                Login_NS.changeTab("userName"), $("#loginSwitchValue").val("用户名"), $("#loginFlagValue").val(""), $("#loginSwitchValue").trigger("change"), $("#userNameLogin").val("").focus().blur()
            }
        }) : e && "MOBILENO_LOGIN_SWITCH_OFF" === e.resultMsg && LufaxPopup.popup({
            popupTitleName: "提示",
            iconClass: "exclamationCircleIcon",
            message: "<span class='orange_word'>手机号登陆开关已关闭，仅可使用用户名登录</span>",
            button: "<a class='btns btn_info close ml20' href='javascript:;' target='_self' id='userNameLoginOnlyButton'>使用用户名登录</a>",
            onClose: function () {
                Login_NS.changeTab("userName"), $("#loginSwitchValue").val("用户名"), $("#loginFlagValue").val(""), $("#loginSwitchValue").trigger("change"), $("#userNameLogin").val("").focus().blur()
            }
        }), e.redirectPath ? ("LOGIN_RESOURCE_IS_OVER_AMOUNT" == e.resultMsg && IframeCrossDomain_NS.isFromIframe ? window.location = e.redirectPath + "&fromDomain=" + encodeURIComponent(IframeCrossDomain_NS.fromDomain) : window.location = e.redirectPath, !1) : ("MISS_VCODE" == e.resultMsg || "MISS_VCODE" == e.resultId ? Login_NS.showCaptcha() : Login_NS.showErrors(e.failedMessage), Login_NS.clearText(), Login_NS.changeCaptcha(!1), !1);
        if (Login_NS.syncCookieToDomain(), IframeCrossDomain_NS.isFromIframe) IframeCrossDomain_NS.crossDomainStatusCallback();
        else {
            if (loginUserStatusChecker && loginUserStatusChecker.statusCheck(e, e.redirectPath)) return;
            Login_NS.checkShouldFace(e, function () {
                "0" == e.passwordPower ? lufax.popup.newIconPopup({
                    popupTitleName: "重要提示",
                    iconClass: "",
                    message: '<p class="message-title" style="text-align: center" ><i class="ld-icon ld-icon-exclamation" style=" margin: 0 5px 0 0;color: #FF921B "></i>由于您的登录密码安全级别较低，为保障您的账户安全，请修改登录密码</p><div class="union-success" ></div>',
                    contentWidth: "530px",
                    bodyPadding: "20px 20px 40px 40px ",
                    closeDisplay: "false",
                    button: "<a class='btns btn_info cancleBtn' href='javascript:void(0);' data-sk='OK_JointLogin'>立即修改</a>",
                    onCancel: function () {
                        try {
                            SSO.syncCookieToDomain(function () {
                                window.location = url("modify-password")
                            })
                        } catch (a) {
                            window.location = url("modify-password")
                        }
                    }
                }) : Login_NS.checkUserInfoAfterLoginSuccess(e)
            })
        }
    }, login: function () {
        $("#loginBtn").click(function () {
            var a = $("#loginFlagValue").val();
            if ("2" == a ? $("#loginForm").validate().settings.messages.userName.required = "请填写手机号码" : $("#loginForm").validate().settings.messages.userName.required = "请填写用户名", Login_NS.createDeviceFingerPrint(), !Login_NS.isSubmitted && (Login_NS.isSubmitted = !0, setTimeout("Login_NS.isSubmitted = false", 2e3), $("#loginForm").valid())) {
                if (Login_NS.rsaChg(), $("#loginBtn").hasClass("disabled")) return;
                $("#loginBtn").addClass("disabled"), $("#loginFlagnew").html("登录中"), $(".J_validNum").val() == $(".J_validNum").data("placeholder") && $(".J_validNum").val(""), $.post(window.location.href, $("#loginForm").serialize(), Login_NS.dealLoginRequest).error(errorHandler())
            }
        })
    }, blurUserName: function () {
        $("#userNameLogin").bind("blur", function () {
            Login_NS.doCheckUser()
        })
    }, getLoginSwitchValue: function (a) {
        $.ajax({
            url: "service/parameter/get-parameter",
            dataType: "json",
            data: {
                name: a
            },
            type: "GET",
            success: function (a) {
                a && a.data && "1" === a.data.value
            }, error: function () {}
        })
    }, doCheckUser: function () {
        $("#lboCheck").hasClass("hidden") || $("#lboCheck").addClass("hidden"), $("#isLboCrsOpen").hasClass("hidden") || $("#isLboCrsOpen").addClass("hidden"), $("#isOpenLboAccStatus1").hasClass("hidden") || $("#isOpenLboAccStatus1").addClass("hidden");
        var a = $.trim($("#userNameLogin").val());
        "" != a && $(".J_validNumBox").hasClass("hidden") && $.ajax({
            url: "service/login/captcha-authorize",
            dataType: "json",
            data: {
                source: "PC",
                username: a
            },
            type: "POST",
            success: function (e) {
                console.log("service/login/captcha-authorize" + JSON.stringify(e)), e && "true" == e.captcha ? (Login_NS.showCaptcha(), $("#lboCheck").hasClass("hidden") || $("#lboCheck").addClass("hidden"), $(".ljb-tip").hasClass("hidden") || $(".ljb-tip").addClass("hidden"), $("#openlbo").val("0")) : "lu.com" == location.hostname.split(".").slice(location.hostname.split(".").length - 2).join(".") && $.ajax({
                    url: url("getUserLboInfo"),
                    dataType: "json",
                    data: {
                        loginId: a,
                        loginFlag: $("#loginflagvalue").val()
                    },
                    type: "GET",
                    success: function (a) {
                        if (console.log("getUserLboInfo data:" + JSON.stringify(a)), (!a.resultId || "-1" != a.resultId) && a.resultId && "1" == a.resultId) {
                            console.log("getUserLboInfo data:" + JSON.stringify(a)), $("#openlbo").val("1"), $("body").addClass("openlbo"), $(".login-inner").css("padding-top", "0"), $(".loginBlock").css("padding-top", "0");
                            var e = $("#loginBtn"),
                                s = $("#agreeLbo");
                            e.data("t-category", "Master_account_notice_checkbox"), e.data("t-title", "Master_account_notice_checkbox"), e.data("t-checkbox_if_check", "1"), s.on("click", function () {
                                "checked" == s.attr("checked") ? e.data("t-checkbox_if_check", "1") : e.data("t-checkbox_if_check", "0")
                            }), $("#hIsOpenLboAccStatus").val(a.isOpenLboAccStatus), a.isOpenLboAccStatus && "1" == a.isOpenLboAccStatus ? ($("#lboCheck").removeClass("hidden"), $("#isOpenLboAccStatus1").removeClass("hidden"), "0" == a.crsInfoStatus ? ($("#crsInfoStatus0").removeClass("hidden"), $("#crsInfoStatus1").hasClass("hidden") || $("#crsInfoStatus1").addClass("hidden"), $("#crsInfoStatus2").hasClass("hidden") || $("#crsInfoStatus2").addClass("hidden"), $("#crsInfoStatus3").hasClass("hidden") || $("#crsInfoStatus3").addClass("hidden"), $("#isLboCrsOpen").hasClass("hidden") || $("#isLboCrsOpen").addClass("hidden")) : "1" == a.crsInfoStatus ? ($("#crsInfoStatus1").removeClass("hidden"), $("#crsInfoStatus0").hasClass("hidden") || $("#crsInfoStatus0").addClass("hidden"), $("#crsInfoStatus2").hasClass("hidden") || $("#crsInfoStatus2").addClass("hidden"), $("#crsInfoStatus3").hasClass("hidden") || $("#crsInfoStatus3").addClass("hidden"), $("#isLboCrsOpen").hasClass("hidden") || $("#isLboCrsOpen").addClass("hidden")) : "2" == a.crsInfoStatus ? ($("#crsInfoStatus2").removeClass("hidden"), $("#crsInfoStatus1").hasClass("hidden") || $("#crsInfoStatus1").addClass("hidden"), $("#crsInfoStatus0").hasClass("hidden") || $("#crsInfoStatus0").addClass("hidden"), $("#crsInfoStatus3").hasClass("hidden") || $("#crsInfoStatus3").addClass("hidden"), $("#isLboCrsOpen").removeClass("hidden")) : "3" == a.crsInfoStatus && ($("#crsInfoStatus3").removeClass("hidden"), $("#crsInfoStatus1").hasClass("hidden") || $("#crsInfoStatus1").addClass("hidden"), $("#crsInfoStatus2").hasClass("hidden") || $("#crsInfoStatus2").addClass("hidden"), $("#crsInfoStatus0").hasClass("hidden") || $("#crsInfoStatus0").addClass("hidden"), $("#isLboCrsOpen").removeClass("hidden"))) : ($("#isOpenLboAccStatus1").hasClass("hidden") || $("#isOpenLboAccStatus1").addClass("hidden"), $("#lboCheck").hasClass("hidden") || $("#lboCheck").addClass("hidden")), $("#lboCheck").hasClass("hidden") || $("#hIsSignLboUserCrsChecked").val("1")
                        }
                    }, error: function () {}
                })
            }
        })
    }, changeTab: function (a) {
        "mobile" == a ? ($("#userNameLogin").attr("data-placeholder", "手机号"), $(".place-holder").html("手机号"), $('.login-tab[data-role="userName"]').removeClass("active"), $("#loginFlagValue").val("2"), $("#forgetUserName").length > 0 && $("#forgetUserName").css("display", "none"), $('.login-tab[data-role="' + a + '"]').addClass("active"), $("#iconView").removeClass("user").addClass("mobile")) : "userName" == a && ($("#userNameLogin").attr("data-placeholder", "用户名"), $(".place-holder").html("用户名"), $("#forgetUserName").length > 0 && $("#forgetUserName").css("display", ""), $('.login-tab[data-role="mobile"]').removeClass("active"), $('.login-tab[data-role="' + a + '"]').addClass("active"), $("#loginFlagValue").val(""), $("#iconView").removeClass("mobile").addClass("user"))
    }
};