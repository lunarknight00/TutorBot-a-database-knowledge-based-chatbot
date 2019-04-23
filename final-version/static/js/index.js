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
                                                    <div class="me-chat">me</div>
                                                    <div class="content">${str}</div>
                                                    <span class="i-talk-cor"></span>
                                                </div>
                                            </div>`
    //清空输入框
    document.getElementById('search').value = '';


    xmlHttp = GetXmlHttpObject();
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
    url = url + "/" + str;
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
function getJsonLength(jsonData){

var jsonLength = 0;

for(var item in jsonData){

jsonLength++;

}

return jsonLength;

}
function stateChanged(){
    if(xmlHttp.readyState==4){
        var msg=xmlHttp.responseText;
        if (msg[2] != '{') {
            var str = msg;
            var reg = new RegExp( '"' , "g" )
            var newstr = str.replace( reg , '' );

                    document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">                                                            
                                                                ${newstr}
                                                                </div>
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;
        }
        else {

            var jstr=msg.replace(new RegExp('\\"',"gm"),'"').replace(new RegExp('\n',"gm"),'')
            var obj = JSON.parse(jstr);
            var obj1=JSON.parse(obj);
            var jsonlen = getJsonLength(obj1) ;
            if (jsonlen == 3){
                document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">
                                                                <div text-align:left; style="color:blue">Question:</div>
                                                               <a  text-align:left;" id="q1">${obj1["0"]["_source"]["question"]}</a>
                                                               <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="q1" >${obj1["0"]["_source"]["answer"]}</a> 
                                                                 <p>-------------------------------------------------------------------------------------------</p>
                                                                 <div text-align:left; style="color:blue">Question:</div>
                                                                 <a  text-align:left;" id="q2">${obj1["1"]["_source"]["question"]}</a>
                                                                <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="q2" >${obj1["1"]["_source"]["answer"]}</a> 
                                                                <p>--------------------------------------------------------------------------------------------</p>
                                                                 <div text-align:left; style="color:blue">Question:</div>
                                                                 <a  text-align:left;" id="q3">${obj1["2"]["_source"]["question"]}</a>
                                                                <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="q3" >${obj1["2"]["_source"]["answer"]}</a> 
                                                             </div>   
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;}

            else  if (jsonlen == 1){
                                document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">
                                                                <div text-align:left; style="color:blue">Question:</div>
                                                               <a  text-align:left;" id="0">${obj1["0"]["_source"]["question"]}</a>
                                                               <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="ans0" >${obj1["0"]["_source"]["answer"]}</a> 
                                                             </div>   
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;
            }
            else  if (jsonlen == 2){
                                document.getElementById('talk').innerHTML += `<div class="robot" style="clear: both">
                                                        <div class="chat">
                                                            <div class="robot-icon" style="width:46px;height: 46px;"></div>
                                                            <div class="robot-response">
                                                                <div class="robot-chat">
                                                                <div text-align:left; style="color:blue">Question:</div>
                                                               <a  text-align:left;" id="0">${obj1["0"]["_source"]["question"]}</a>
                                                               <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="ans0" >${obj1["0"]["_source"]["answer"]}</a> 
                                                                 <p>-------------------------------------------------------------------------------------------</p>
                                                                 <div text-align:left; style="color:blue">Question:</div>
                                                                 <a  text-align:left;" id="111">${obj1["1"]["_source"]["question"]}</a>
                                                                <div text-align:left; style="color:red">Answer:</div>
                                                                <a id="ans111" >${obj1["1"]["_source"]["answer"]}</a> 
                                                             </div>   
                                                            </div>
                                                            <span class="robot-talk-cor"></span>
                                                        </div>
                                                    </div>`;
    }}
    document.getElementById("msg_end").click();
    document.getElementById('search').focus();
}}
// function fn0() {
//     var img = document.getElementById("ans0");
//     if (document.getElementById("0").innerHTML == "Hide answer1") {
//         img.className = "hide";
//         document.getElementById("0").innerHTML = "Show answer1";}
//     else {
//         img.className = "show";
//         document.getElementById("0").innerHTML = "Hide answer1";}
// }
// function fn1() {
//     var img = document.getElementById("ans1");
//     if (document.getElementById("1").innerHTML == "Hide answer2") {
//         img.className = "hide";
//         document.getElementById("1").innerHTML = "Show answer2";}
//     else {
//         img.className = "show";
//         document.getElementById("1").innerHTML = "Hide answer2";}
// }
// function fn2() {
//     var img = document.getElementById("ans2");
//     if (document.getElementById("2").innerHTML == "Hide answer3") {
//         img.className = "hide";
//         document.getElementById("2").innerHTML = "Show answer3";}
//     else {
//         img.className = "show";
//         document.getElementById("2").innerHTML = "Hide answer3";}
// }
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
                                                    <div class="me-chat">me</div>
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
    url = url + "/" + testname;
    xmlHttp.onreadystatechange = stateChanged;
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
    document.getElementById("msg_end").click();
})

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent


var grammar = '#JSGF V1.0; '//grammar colors; '//public <color> = ' + colors.join(' | ') + ' ;'

var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
//recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

var diagnostic = document.querySelector('.input-area');
var bg = document.querySelector('html');
var hints = document.querySelector('.hints');



function voice_recongization(){
  console.log('Ready to receive a command.');
  recognition.start();
}


recognition.onresult = function(event) {


  var last = event.results.length - 1;
  var text = event.results[last][0].transcript;

 sendMessage(text)
  console.log('Confidence: ' + event.results[0][0].confidence);
}

recognition.onspeechend = function() {
  recognition.stop();
}

recognition.onnomatch = function(event) {
    que = "I didn't recognise that.";
    sendMessage(que);
}

recognition.onerror = function(event) {
  que = 'Error occurred in recognition: ' + event.error;
  sendMessage(que);
}