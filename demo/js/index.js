var xmlHttp;
//键盘监听
function onKeyDown(str){
    if(window.event.keyCode == "13" && event.ctrlKey ){
        document.getElementById("search").value += "\n";
    }else if(window.event.keyCode == "13"){
        event.preventDefault();
        sendMessage(str);
    }
}
//发送一个消息
function sendMessage(str) {
    if (str == "") {
        return
    }
    //添加信息

    document.getElementById('talk').innerHTML += `<div class="me" style="clear: both">
                                                <div class="i-talk">
                                                    <div class="me-chat">我</div>
                                                    <div class="content">${str}</div>
                                                    <span class="i-talk-cor"></span>
                                                </div>
                                            </div>`
    //清空输入框
    document.getElementById('search').value = '';


    xmlHttp = GetXmlHttpObject()
    if (xmlHttp == null) {
        alert("no,can not use ajax！");
        return;
    }
    // var url = "http://127.0.0.1:5000/es";
    // url = url + "/keyword=" + str;
    // xmlHttp.onreadystatechange = stateChanged;
    //if(xmlHttp.readyState==4){var mesg = xmlHttp.responseText;}

    //if (mesg=="Sorry could't understand your question."){
    var url = "http://127.0.0.1:5000/chat";
    url = url + "/question=" + str;
    xmlHttp.onreadystatechange = stateChanged;
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
//}
    // else {
    //     var url = "http://127.0.0.1:5000/chat";
    //         url = url + "/question=" + str;
    //     xmlHttp.onreadystatechange = stateChanged;
    //     xmlHttp.open("GET", url, true);
    //     xmlHttp.send();}
    // xmlHttp.open("GET", url, true);
    // xmlHttp.send();
}
//接收到一个消息
function stateChanged(){
    if(xmlHttp.readyState==4){
        var msg=xmlHttp.responseText;
        if (msg[1] != '{') {
                    document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">                                                            
                                                                ${msg}
                                                                </div>
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;
        }
        else {
            var jstr=msg.replace(new RegExp('\\"',"gm"),'"').replace(new RegExp('\n',"gm"),'')
            var obj = JSON.parse(jstr);
            var obj1=JSON.parse(obj)
            document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">
                                                                
                                                               <button class="button" value="show answer" onclick="fn0()" style="display:block;  text-align:left;" id="0">show answer </button>
                                                                <a id="ans0" class="hide">${obj1["0"]["_source"]["answer"]}</a>
                                                                
                                                                 <button class="button" value="show answer" onclick="fn1()" style="display:block;  text-align:left;" id="1">show answer </button>
                                                                <a id="ans1" class="hide">${obj1["1"]["_source"]["answer"]}</a>
                                                                
                                                                <button class="button" value="show answer" onclick="fn2()" style="display:block;  text-align:left;" id="2">show answer </button>
                                                                    <a id="ans2" class="hide">${obj1["2"]["_source"]["answer"]}</a>
                                 
                                                                </div>
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;
        }


    }
    document.getElementById("msg_end").click();
    document.getElementById('search').focus();
}
function fn0() {
    var img = document.getElementById("ans0");
    if (document.getElementById("0").innerHTML == "Hide answer") {
        img.className = "hide";
        document.getElementById("0").innerHTML = "Show answer";}
    else {
        img.className = "show";
        document.getElementById("0").innerHTML = "Hide answer";}
}
function fn1() {
    var img = document.getElementById("ans1");
    if (document.getElementById("1").innerHTML == "Hide answer") {
        img.className = "hide";
        document.getElementById("1").innerHTML = "Show answer";}
    else {
        img.className = "show";
        document.getElementById("1").innerHTML = "Hide answer";}
}
function fn2() {
    var img = document.getElementById("ans2");
    if (document.getElementById("2").innerHTML == "Hide answer") {
        img.className = "hide";
        document.getElementById("2").innerHTML = "Show answer";}
    else {
        img.className = "show";
        document.getElementById("2").innerHTML = "Hide answer";}
}
function GetXmlHttpObject(){
    var xmlHttp=null;
    try{
        xmlHttp=new XMLHttpRequest();
    }catch(e){
        try{
            xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
        }catch(e){
            xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    return xmlHttp;
}

$(".hot-item").live("click",function(){
    var aa=$(this).attr("id");
    var testname=document.getElementById(aa).innerHTML;
    document.getElementById('talk').innerHTML += `<div class="me" style="clear: both">
                                                <div class="i-talk">
                                                    <div class="me-chat">我</div>
                                                    <div class="content">${testname}</div>
                                                    <span class="i-talk-cor"></span>
                                                </div>
                                            </div>`

    xmlHttp = GetXmlHttpObject()
    if (xmlHttp == null) {
        alert("no,can not use ajax！");
        return;
    }
    var url = "http://127.0.0.1:5000/chat";
    url = url + "/question=" + testname;
    xmlHttp.onreadystatechange = stateChanged;
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
    document.getElementById("msg_end").click();
})
