const WebSocket = require("ws");
const fs = require("fs");

var settings = JSON.parse(fs.readFileSync("settings.json"));
console.log(settings);

var ws = null;

fs.watch("settings.json",(eventType, filename) =>{
  settings = JSON.parse(fs.readFileSync("settings.json"));
  console.log(settings);
  if(ws && ws.isOpen)
    ws.close();
})

reg();

function reg(){
  ws = new WebSocket('wss://jt-cohen-email-dispatcher-82a422eedd2b.herokuapp.com/ws');
  //const ws = new WebSocket('ws://localhost:5001/ws');

  ws.on('error', console.error);

  ws.on('open', function open() {
    ws.isOpen = true;
    for(var email in settings)
      ws.send(JSON.stringify({"registerEmail":email}));
  });

  ws.on('message', function message(msg) {
      msg = JSON.parse(msg)
      if(!msg.pong){
        console.log(msg);
      }
      if(msg.to && msg.to != "LOG"){
        var instrument = settings[msg.to];
      }
  });

  var interId = setInterval(()=>{
    try{
      if(ws.isOpen)
        ws.send(JSON.stringify({ping:1}));
    }catch(e){}
  },1000*30)
  ws.on("close",()=>{
    clearInterval(interId);
    reg();
  })
}