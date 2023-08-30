const express = require('express')
const fs = require('fs');
const path = require('path')
var parseMessage = require('gmail-api-parse-message');

const USER_ID = "jt.ninjamarkettrader@gmail.com";



const {
  google
} = require('googleapis');

const PORT = process.env.PORT || 5001

var app = express();
var expressWs = require('express-ws')(app);

const _LOG = console.log;
console.log = (msg)=>{
  onEmail({to:"LOG",LOG:msg});
};

authAndWatch();
runAtSpecificTimeOfDay(1,0,authAndWatch);

function runAtSpecificTimeOfDay(hour, minutes, func)
{
  const twentyFourHours = 86400000;
  const now = new Date();
  let eta_ms = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, minutes, 0, 0).getTime() - now;
  if (eta_ms < 0)
  {
    eta_ms += twentyFourHours;
  }
  setTimeout(function() {
    //run once
    func();
    // run every 24 hours from now on
    setInterval(func, twentyFourHours);
  }, eta_ms);
}

function getCreds(cb){
  fs.readFile('gmail/quickstart/credentials.json', (err, content) => {
    cb(JSON.parse(content));
  });
}

var auth_token;
function authAndWatch(){
    getCreds((creds)=>{
      authorize(creds, (auth) => {
        auth_token = auth;
        watchMyLabel(auth)
      });
    })
}

function authorize(credentials, cb) {
    const {
        client_secret,
        client_id,
        redirect_uris
    } = credentials.installed;

    const oAuth2Client = new google.auth.OAuth2(
        client_id, client_secret, redirect_uris[0]);

    fs.readFile("gmail/quickstart/token.json", (err, token) => {
        oAuth2Client.setCredentials(JSON.parse(token));
        cb(oAuth2Client);
    });
}

async function watchMyLabel(auth) {
  const gmail = google.gmail({
      version: 'v1',
      auth
  });
  const res = await gmail.users.watch({
      userId: USER_ID,
      requestBody: {
          labelIds: ['UNREAD'],
          labelFilterAction: "include",
          topicName: 'projects/jt-cohen/topics/JT-Cohen'
      }
  });
}

app.post('/gmail',express.json(),(req, res) => {
  
    res.sendStatus(200);

    //getCreds((creds)=>{
      //authorize(creds, (auth) => {
        const gmail = google.gmail({
          version: 'v1',
          auth: auth_token
        });

        gmail.users.messages.list({
          auth:auth_token,
          userId: USER_ID},(err,resp)=>{
            if(!err){
              if(resp.data.messages){
                for(var i=0;i<resp.data.messages.length;i++){
                  ((id)=>{
                    gmail.users.messages.get({auth: auth_token, userId: USER_ID, id:id }, (err, email) => {
                      if(!err){
                        const re = /[^@<\s]+@[^@\s>]+/
                        var em = parseMessage(email.data)
                        
                        var m = { id:id,
                                  date:em.headers.date, 
                                  from:em.headers.from.match(re)[0],
                                  to:em.headers.to.match(re)[0],
                                  subject:em.headers.subject, 
                                  text:em.textPlain.trim()};

                        console.log(m);
                        if(m.to == USER_ID)
                          return;

                        gmail.users.messages.delete({auth: auth_token, userId: USER_ID, id:id }, (err, res) => {});
                        
                        const diffMS = (new Date()).getTime()-(new Date(m.date)).getTime();
                        if(diffMS<=3000)
                          onEmail(em)
                        else
                          console.log("Too late: " + diffMS);
                      }
                    });
                  })(resp.data.messages[i].id);
                
                }
              }
            }
            else{
              console.log("LIST ERROR")
              console.log(err);
            }
          });
       
      //});
    //})
  }
);

app.use(express.static(path.join(__dirname, 'public')))
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs')
  .get('/', (req, res) => res.render('pages/index'))
  .listen(PORT, () => console.log(`Listening on ${ PORT }`))

  var wsArray = [];
  app.ws('/ws', function(ws, req) {
    ws._JTC_email = [];
    ws.on('message', function(msg) {
      try{
        msg = JSON.parse(msg);
        if(msg.registerEmail){
          ws._JTC_email.push(msg.registerEmail);
          ws.send(JSON.stringify({"registered":msg.registerEmail}));
        }
        if(msg.ping)
          ws.send(JSON.stringify({pong:1}));
      }catch(e){
        console.log(e);
      }
    });
  });

  function onEmail(email){
    var clients = expressWs.getWss().clients;
    for (const c of clients)
      if(c._JTC_email.indexOf(email.to)!=-1)
        c.send(JSON.stringify(email));
  }