const express = require('express')
const app = express();
const bodyParser = require('body-parser');
const port = 3000;
const cors = require('cors');
// const {MongoClient} = require('mongodb');
// const uri="mongodb://studentarezionish:yhHzR8BgMm4eZRy6@mongo:27017/NetworkCallStack";
// const client = new MongoClient(uri);
const jsonfile = require('jsonfile');
let website = ['null'];

app.use(cors({credentials: true, origin: true}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// (async function () {
//   await client.connect();
//   console.log("connected to Database");
// })();

async function insertRequest(newHttpReq){ 
  //const result = await client.db("NetworkCallStack").collection("request").insertOne(newHttpReq);
  //console.log(`New request created with the following id: ${result.insertedId}`);
  const file = 'request.json';
  jsonfile.writeFile(file, newHttpReq, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertRequestInfo(newHttpReq){ 
  //const result = await client.db("NetworkCallStack").collection("request").insertOne(newHttpReq);
  //console.log(`New request created with the following id: ${result.insertedId}`);
  const file = 'requestInfo.json';
  jsonfile.writeFile(file, newHttpReq, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertResponse(newHttpResp){ 
  //const result = await client.db("NetworkCallStack").collection("response").insertOne(newHttpResp);
  //console.log(`New response created with the following id: ${result.insertedId}`);
  const file = 'responses.json';
  jsonfile.writeFile(file, newHttpResp, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}

async function insertInfo(newInfo){ 
  //const result = await client.db("NetworkCallStack").collection("request").insertOne(newHttpReq);
  //console.log(`New request created with the following id: ${result.insertedId}`);
  const file = 'cookie_storage.json';
  jsonfile.writeFile(file, newInfo, { flag: 'a' }, function (err) {
    if (err) console.error(err);
  })
}


app.post('/request', (req, res) => {
  //console.log(req.body);
  if (req.body.http_req != "http://localhost:3000/cookiestorage"){
    req.body.top_level_url = website[0];
    insertRequest(req.body);
  }
  res.send("request-success");
})

app.post('/requestinfo', (req, res) => {
  insertRequestInfo(req.body);
  res.send("request-success");
})

app.post('/response', (req, res) => {
  //console.log("response");
  insertResponse(req.body);
  res.send("response-success");
})

app.post('/cookiestorage', (req, res) => {
  //console.log("response");
  insertInfo(req.body);
  res.send("response-success");
})

app.post('/complete', (req, res) => {
  //console.log("response");
  website[0] = req.body.website;
  res.send("response-success");
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
})