var NT = require("ninjatrader");

var nt = new NT.default({
    account: "Sim101"
});

function ntMarket(qty,instrument,action,cb){
    nt.market({
        action: NT.NinjaTraderAction.Buy,
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
    }).then(()=>{
        process.exit()
    });  // order accepted after await
}


ntMarket(4,"NQ 09-23",NT.NinjaTraderAction.Buy,(res)=>{
    console.log(res);
});


 console.log("Buy")