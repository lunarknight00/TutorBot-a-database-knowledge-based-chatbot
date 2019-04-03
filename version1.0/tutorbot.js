var loadingMsgIndex,
    botui = new BotUI('stars-bot'),
    API = 'https://api.github.com/repos/';
	
botui.message.add({
  content: 'Hello!!! I am a tutot robot !'
});

//botui.message.add({
  //human: true,
 // content: 'Hello World from human!'
//});

function sendXHR(repo, cb) {
  var xhr = new XMLHttpRequest();
  var self = this;
  xhr.open('GET', API + repo);
  xhr.onload = function () {
    var res = JSON.parse(xhr.responseText)
    cb(res.stargazers_count);
  }
  xhr.send();
}

function init() {
  botui.message
  .bot({
    delay: 1000,
    content: 'What questions are you going to ask ? '
  })
  .then(function () {
    return botui.action.text({
      delay: 1000,
      action: {
        value: '',
        placeholder: 'Input your question'
      }
    })
  }).then(function (res) {
    loadingMsgIndex = botui.message.bot({
      delay: 200,
      loading: true
    }).then(function (index) {
      loadingMsgIndex = index;
      sendXHR(res.value, ssss)
    });
  });
}

function ssss(stars) {
  botui.message
  .update(loadingMsgIndex, {
    content: 'Sorry,I do not know how to answer this question.'
  })
  .then(init); // ask again for repo. Keep in loop.
}

init();
