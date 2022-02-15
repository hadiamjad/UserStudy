window.tabId=0;
chrome.tabs.query({active:true},
  function(d){
    //current tab_id--d[1].id--d[1].url==top_level_url
    window.tabId = d[0].id;
    chrome.debugger.attach({tabId:tabId}, version,
     function(err){
       if(err)
          console.log(err);
       else
          console.log("debugger attached");
     } );
    chrome.debugger.sendCommand({tabId:tabId}, "Network.enable");
    //blocking specified request
    chrome.webRequest.onBeforeRequest.addListener(
      function(details) { return {cancel: true}; },
      {urls: ["https://assets.sg.content-cdn.io/script/Zone03/js/Lib/MJ_Static-Built.js?v=v2048"]},
      ["blocking"]
    );
    chrome.debugger.onEvent.addListener(onEvent);
  })
function onEvent(debuggeeId, message, params) {
  if (tabId != debuggeeId.tabId)
    return;
  if (message == "Network.requestWillBeSent") {
      fetch("http://localhost:3000/request", {
        method: "POST", 
        body: JSON.stringify({"http_req": params.request.url,
        "request_id":params.requestId,
        "top_level_url": 0,
        "frame_url":params.documentURL,
        "resource_type":params.type,
        "header": params.request.headers,
        "timestamp": params.timestamp,
        "frameId": params.frameId,
        "call_stack":params.initiator}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("Request complete! response");
      }); 
  }
  else if (message == "Network.requestWillBeSentExtraInfo"){
    fetch("http://localhost:3000/requestinfo", {
      method: "POST", 
      body: JSON.stringify({
      "request_id":params.requestId,
      "cookies": params.associatedCookies,
      "headers":params.headers,
      "connectTiming":params.connectTiming,
      "clientSecurityState": params.clientSecurityState}),
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        "Content-Type": "application/json"
      }
    }).then(res => {
      console.log("RequestInfo complete! response");
    }); 

  }
  else if (message == "Network.responseReceived") {
      chrome.debugger.sendCommand({
          tabId: tabId
      }, "Network.getResponseBody", {
          "requestId": params.requestId
      }, function(response) {
              // you get the response body here!
              fetch("http://localhost:3000/response", {
                method: "POST", 
                body: JSON.stringify({
                "request_id":params.requestId,
                "response":params.response,
                "resource_type":params.type}),
                mode: 'cors',
                headers: {
                  'Access-Control-Allow-Origin':'*',
                  "Content-Type": "application/json"
                }
              }).then(res => {
                console.log("Response complete! response");
              });
      });
    

  }
}

var version = "1.0";