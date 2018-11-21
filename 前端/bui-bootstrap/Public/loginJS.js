/**
 * Created by tongyurong on 2018/4/10.
 */
//判断本地是否有登录
$(document).ready(function(){
    var customerId=sessionStorage.customerId;
    if (customerId == undefined) {
        alert("请先登录！");
        window.location.href="Public/login.html";
    }

})