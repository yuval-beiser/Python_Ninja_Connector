const WebSocket = require("ws");
const fs = require("fs");
var NT = require("ninjatrader");

var nt = new NT.default({
    account: "Sim101"
});

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

        /*
        ntMarket(1,instrument,NT.NinjaTraderAction.Buy,(res)=>{
          console.log(res);
        });
        */
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

function ntMarket(qty,instrument,action,cb){
  nt.market({
      action: action,
      quantity: qty,
      tif: NT.NinjaTraderTif.Day,
      instrument: instrument,
      onUpdate: function (status, state) {
          switch (status) {
              case NT.OrderStatus.Rejected:
                  // order rejected
                  cb({
                      stat:"rejected"
                  })
                  break;
              case NT.OrderStatus.Filled:
                  // order filled
                  //console.log(state); // { quantity: 69, price: 49.40 }
                  cb({
                      stat:"filled",
                      state:state
                  })
                  break;
          }
      },
      onRejected: function (state) {
          // order rejected
          cb({
              stat:"rejected",
              state:state
          })
      }
  }); // order accepted after await
}