import matplotlib.pyplot as plt
import os
import networkx as nx
import numpy as np
import pandas as pd
import json
from graphviz import Digraph

# from stellargraph.data import BiasedRandomWalk
# from stellargraph import StellarGraph
# from stellargraph import datasets
# from IPython.display import display, HTML
print('-----------------Import----------------')

# node labels
label = [0]

def addNode(nodes, name, type, TC, FC, classlabel):
  if name not in nodes.keys():
    nodes[name] = [label[0], type, 0, 0, classlabel]
    label[0] += 1
  if classlabel == 0:
    nodes[name][2] += TC
    nodes[name][3] += FC
  return nodes[name][0]

def addEdge(edges, src, tar, type):
  if str(src)+'@'+str(tar) not in edges.keys():
    edges[str(src)+'@'+str(tar)] = [src, tar, type]


# storage_dic = {'_gid' = [002, 5288992, 1], '_svd' = [5]}
# script_dic = {'https://ad/test.js': [set->[_gid,..], get->[_svd, ..]]}
def addStorage(script_dic, storage_dic, dataset):  
  """
  {"top_level_url":"https://cmovies.online/","function":"cookie_setter","cookie:":"__PPU_BACKCLCK_3714332=true; expires=Wed, 16 Feb 2022 19:06:24 GMT; path=/; domain=cmovies.online","stack":"Error\n    at HTMLDocument.set (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:39:17)\n    at e.<computed>.<computed> [as saveSessionCustomKey] (https://lurgaimt.net/tag.min.js:1:43145)\n    at https://lurgaimt.net/tag.min.js:1:47814\n    at _ (https://lurgaimt.net/tag.min.js:1:8934)\n    at https://lurgaimt.net/tag.min.js:1:47689\n    at ln (https://lurgaimt.net/tag.min.js:1:48253)\n    at HTMLScriptElement.g (https://cmovies.online/:1630:60191)"}
  """
  """
  {"top_level_url":"https://eus.rubiconproject.com/usync.html?p=btwnex&endpoint=eu","function":"cookie_getter","cookie:":"khaos=KZPV8CZP-15-K5E0; audit=1|GRYZojcvauLxCRmi07Abd33bvG56iVGUHpZdkt6wQBl5wrSQggMQUFeGcsFVzcEJPOh1wtc3tgnqFTrNE4+z9kqVaHlG5SlgpmvllXEtYN4=","stack":"Error\n    at HTMLDocument.get (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:19:17)\n    at readCookie (https://eus.rubiconproject.com/usync.js:4:1684)\n    at runSyncs (https://eus.rubiconproject.com/usync.js:4:10507)\n    at Image.d.onload (https://eus.rubiconproject.com/usync.js:4:9415)"}
  """
  """
  {"top_level_url":"https://cmovies.online/","function":"indexdb_getter","storage:":{"_iiq_sync":"1645034787118","000000160024004d004e003t004a004c0040003t002m002m002o002k002m0024":"002a006u004d006m006n0064006n006o006m004d0051004s004n004d00690068006n0066006b006800670058006n004d0051004r004n004d006l0068006m006j006i006h006m0068004d0051006h006o006f006f004n004d006j006l0068006p006c006i006o006m005q006n0064006n0068004d0051006u004d006m006n0064006n006o006m004d0051004r004n004d00690068006n0066006b006800670058006n004d0051003f004r004n004d006l0068006m006j006i006h006m0068004d0051006h006o006f006f004n004d006j006l0068006p006c006i006o006m005q006n0064006n0068004d0051006h006o006f006f006w006w","000000160024002m002m002o002k002m0024":"0016009b006u008w008z008l008o008p008o007p0094006u007i0079007e007c007d0078007b007c007f007g007e007g007a007b0074006u0095008y008w008z008l008o008p008o007p0094006u007i007500790074005w006u008t008x00900092008p00930093008t008z008y0093006u007i008f008h009d","_iiq_fdata":"{\"pcid\":\"8d8307a6-33ff-4c30-b2c1-3bf70366cf33\",\"pcidDate\":1645034787112}","mgMuidn":"m1gqWoDFcW6a","bf001a61-ea58-4c69-33b4-1b01154b26f5":"6758687d7c1f9247508625","_iiq_fdata_1548712036":"{\"callCount\":1,\"failCount\":0,\"noDataCounter\":1,\"cttl\":43200000}","_mgIntentiq":"{\"time\":1645034787118,\"data\":\"e30=\"}","_mgPvid":"17f03b6cd7394629387"},"stack":"Error\n    at get (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:61:17)\n    at https://dozubatan.com/400/4414273:1:48414\n    at https://dozubatan.com/400/4414273:1:48824"}
  """
  if dataset["function"] == 'cookie_setter':
      if dataset["cookie:"] != "":
        
        if dataset["cookie:"].split("=")[0] not in storage_dic.keys():
          storage_dic[dataset["cookie:"].split("=")[0]] = []
        if dataset["cookie:"].split(";")[0].split('=')[1] not in storage_dic[dataset["cookie:"].split("=")[0]]:
          storage_dic[dataset["cookie:"].split("=")[0]].append(dataset["cookie:"].split(";")[0].split('=')[1])
        
        script_url = getStorageScriptFromStack(dataset["stack"])
        if script_url not in script_dic.keys():
           script_dic[script_url] = [[],[]]
        if dataset["cookie:"].split("=")[0] not in script_dic[script_url][0]:
          script_dic[script_url][0].append(dataset["cookie:"].split("=")[0])
 
  elif dataset["function"] == 'cookie_getter':
      if dataset["cookie:"] != "":
        
        script_url = getStorageScriptFromStack(dataset["stack"])
        lst = dataset["cookie:"].split(';')
        for item in lst:
          if item.split('=')[0] not in storage_dic.keys():
            storage_dic[item.split('=')[0]] = []
          if item.split('=')[1] not in storage_dic[item.split('=')[0]]:
            storage_dic[item.split('=')[0]].append(item.split('=')[1])
        
          if script_url not in script_dic.keys():
            script_dic[script_url] = [[],[]]
          if item.split('=')[0] not in script_dic[script_url][1]:
            script_dic[script_url][1].append(item.split('=')[0])

  else:
      if dataset["storage:"] != "":
        
        script_url = getStorageScriptFromStack(dataset["stack"])
        for key in dataset["storage:"]:
          if key not in storage_dic.keys():
            storage_dic[key] = []
          if dataset["storage:"][key] not in storage_dic[key]:
            storage_dic[key].append(dataset["storage:"][key]) 
          
          if script_url not in script_dic.keys():
            script_dic[script_url] = [[],[]]
          if key not in script_dic[script_url][1]:
            script_dic[script_url][1].append(key)

# script sample -> at l (https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
# return https://c.amazon-adsystem.com/aax2/apstag.js
def getStorageScriptFromStack(script):
    script = script.split('\n')[2]
    try:
        script = script.split('(')[1] # https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
    except:
        pass
    return "https:"+ script.split(':')[1]

# getting initiator of the request. Sample object attached below:
"""
"stack": {
    "callFrames": [],
    "parent": {
        "callFrames": [{
            "columnNumber": 8972,
            "functionName": "IntentIqObject.appendImage",
            "lineNumber": 0,
            "scriptId": "135",
            "url": "https://cdn.adskeeper.com/js/IIQUniversalID.js"
        }, {
            "columnNumber": 9797,
            "functionName": "IntentIqObject.pixelSync",
            "lineNumber": 0,
            "scriptId": "135",
            "url": "https://cdn.adskeeper.com/js/IIQUniversalID.js"
        }, {
            "columnNumber": 13627,
            "functionName": "IntentIqObject",
            "lineNumber": 0,
            "scriptId": "135",
            "url": "https://cdn.adskeeper.com/js/IIQUniversalID.js"
        }, {
            "columnNumber": 66101,
            "functionName": "_getDataFromApi",
            "lineNumber": 0,
            "scriptId": "71",
            "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
        }, {
            "columnNumber": 65592,
            "functionName": "t.onload",
            "lineNumber": 0,
            "scriptId": "71",
            "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
        }],
        "description": "Image",
        "parent": {
            "callFrames": [{
                "columnNumber": 65556,
                "functionName": "_init",
                "lineNumber": 0,
                "scriptId": "71",
                "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
            }, {
                "columnNumber": 1510,
                "functionName": "_addHookPromiseBody",
                "lineNumber": 0,
                "scriptId": "71",
                "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
            }, {
                "columnNumber": 1194,
                "functionName": "",
                "lineNumber": 0,
                "scriptId": "71",
                "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
            }],
            "description": "load",
            "parent": {
                "callFrames": [{
                    "columnNumber": 1173,
                    "functionName": "",
                    "lineNumber": 0,
                    "scriptId": "71",
                    "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                }, {
                    "columnNumber": 1078,
                    "functionName": "",
                    "lineNumber": 0,
                    "scriptId": "71",
                    "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                }, {
                    "columnNumber": 70097,
                    "functionName": "processHooks",
                    "lineNumber": 0,
                    "scriptId": "71",
                    "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                }],
                "description": "setTimeout",
                "parent": {
                    "callFrames": [{
                        "columnNumber": 67564,
                        "functionName": "render",
                        "lineNumber": 0,
                        "scriptId": "71",
                        "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                    }],
                    "description": "await",
                    "parent": {
                        "callFrames": [{
                            "columnNumber": 101965,
                            "functionName": "_loadAds",
                            "lineNumber": 0,
                            "scriptId": "71",
                            "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                        }, {
                            "columnNumber": 100746,
                            "functionName": "a.id.app.context.<computed>",
                            "lineNumber": 0,
                            "scriptId": "71",
                            "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                        }, {
                            "columnNumber": 103032,
                            "functionName": "",
                            "lineNumber": 0,
                            "scriptId": "71",
                            "url": "https://jsc.adskeeper.com/b/i/bidgear.cmovies.online.1248860.es6.js"
                        }, {
                            "columnNumber": 0,
                            "functionName": "",
                            "lineNumber": 4,
                            "scriptId": "127",
                            "url": "https://servicer.adskeeper.com/1248860/1?pv=5&cbuster=1645034786243595018584&uniqId=011ad&niet=4g&nisd=false&jsv=es6&w=300&h=250&cols=1&ref=&cxurl=https%3A%2F%2Fcmovies.online%2F&lu=https%3A%2F%2Fcmovies.online%2F&sessionId=620d3d22-08133&pageView=1&pvid=17f03b6cd7698cc3ec3&implVersion=11&dpr=2"
                        }],
                        "description": "await"
                    }
                }
            }
        }
    }
}, "type": "script"
}
}
"""
def getInitiator(stack):
    if len(stack['callFrames']) != 0:
      return stack['callFrames'][0]['url']
    else:
      return getInitiator(stack["parent"])

# getting the redirection link. Sample object attached below:
"""
{
    "request_id": "23715.82",
    "response": {
        "connectionId": 1526,
        "connectionReused": false,
        "encodedDataLength": 303,
        "fromDiskCache": false,
        "fromPrefetchCache": false,
        "fromServiceWorker": false,
        "headers": {
            "access-control-allow-credentials": "true",
            "access-control-allow-methods": "GET",
            "access-control-allow-origin": "null",
            "cache-control": "no-cache, no-store, must-revalidate",
            "content-encoding": "gzip",
            "content-type": "application/json; charset=utf-8",
            "date": "Wed, 16 Feb 2022 17:10:36 GMT",
            "expires": "0",
            "pragma": "no-cache",
            "server-processing-duration-in-ticks": "6863",
            "strict-transport-security": "max-age=31536000; preload;",
            "vary": "Accept-Encoding"
        },
        "mimeType": "application/json",
        "protocol": "h2",
        "remoteIPAddress": "74.119.119.139",
        "remotePort": 443,
        "responseTime": 1645031437432.098,
        "securityState": "unknown",
        "status": 200,
        "statusText": "",
        "timing": {
            "connectEnd": 57.628,
            "connectStart": 3.953,
            "dnsEnd": 3.953,
            "dnsStart": 3.939,
            "proxyEnd": -1,
            "proxyStart": -1,
            "pushEnd": 0,
            "pushStart": 0,
            "receiveHeadersEnd": 106.129,
            "requestTime": 174911.812454,
            "sendEnd": 75.873,
            "sendStart": 70.75,
            "sslEnd": 57.604,
            "sslStart": 32.748,
            "workerFetchStart": -1,
            "workerReady": -1,
            "workerRespondWithSettled": -1,
            "workerStart": -1
        },
        "url": "https://mug.criteo.com/sid?cpp=dWo4V3xmeDFpWnBMSUZJRGhnQmlSRDdhZlVjcTY0SDQvZzlieWhBaDJYdjJVTWhYSXdxSUhYY0VSeCtwZTZYTldCOGNNYW5tSXhCZWlYWUlJMzZraFNNTFpnZVF5Nk9EZlhnK1BRcGp1bnY1NU9YbXdqR3VmWFN5YXJPa3p2TlB0cnZnN3I0S0NsMitYaHo1MWEwLzZ3TVM2OFBiNC9RWFNaNkNpaXd3Zy91VmRCODAwRHZIZDYza0t3dForYnRzVk5JT2paK2tpYWpmYm1OOXd3V0VMb1c2U2YwcE0wUVBpZVJNOGtYWkNXaVAxVTBJPXw&cppv=2"
    },
    "resource_type": "XHR"
}

"""
def getRedirection(request_id, request_url):
  with open(r'server/responses.json') as file:
      for line in file:
        dataset = json.loads(line)
        if dataset['request_id'] == request_id:
          if dataset["response"]["url"] != request_url:
            return dataset["response"]["url"] 
          else:
            return None

# Function checks if storage key-value is shared in url or not
def IsInfoShared(storage_dic, url):
  for key in storage_dic:
    for item in storage_dic[key]:
      if item in url:
        return key
  
  return None

def createWebGraph(url):
    
    # name: [id, type, TC, FC, label]
    nodes = {}
    # src@tar = [src_id, tar_id, type]
    edges = {}
    # script_dic = {'https://ad/test.js': [set->[_gid,..], get->[_svd, ..]]}
    script_dic = {} 
    # storage_dic = {'_gid' = [002, 5288992, 1], '_svd' = [5]}
    storage_dic = {}

    # initial HTML iframe
    src = addNode(nodes, "Network@https://"+url+"/", "Network", 0 , 0, -1)
    tar = addNode(nodes, "HTML@https://"+url+"/", "HTML@iframe", 0 , 0, -2)
    addEdge(edges, src, tar, 'Network->HTML/Script')
    src = addNode(nodes, "Script@https://"+url+"/", "Script", 0 , 0, 0)
    addEdge(edges, tar, src, 'Initiated')

    # creating storage nodes and edges
    with open(r'server/cookie_storage.json') as file:
      for line in file:
        dataset = json.loads(line)
        if url in dataset["top_level_url"]:
          addStorage(script_dic, storage_dic, dataset) 
    for key in storage_dic:
      addNode(nodes, "Storage@"+key, "Storage", 0 , 0, -3)
    
    # reading big request data line by line
    with open(r'labellings.json') as file:
      for line in file:
        data = json.loads(line)
        for dataset in data:
          ######### Single request level graph plotting #########
          # check to ensure graph is for one page
          if dataset['top_level_url'] == url:
            # create network node
            src = addNode(nodes, "Network@"+dataset["http_req"], "Network", 0 , 0, -1)
            
            # check if request is redirected
            rdurl = getRedirection(dataset["request_id"], dataset["http_req"])
            if rdurl is not None:
              tar = addNode(nodes, "Network@"+rdurl, "Network", 0 , 0, -1)
              addEdge(edges, src, tar, 'Redirection')
            
            # check if resource type is not script then create simple HTML node
            if dataset["resource_type"] != "Script":
              tar = addNode(nodes, "HTML@"+dataset["http_req"], "HTML@"+dataset["resource_type"], 0, 0, -2)
            # create script node
            else:
              tar = addNode(nodes, "Script@"+dataset["http_req"], dataset["resource_type"], 0, 0, 0)
            # create edge between the Request -> HTML/Script
            addEdge(edges, src, tar, 'Network->HTML/Script')
            
            # if its initiated by call stack javascript
            # else its generated from main iframe
            if dataset['call_stack']['type'] == 'script':
              if dataset['easylistflag'] == 1 or dataset['easyprivacylistflag'] == 1 or dataset['ancestorflag'] == 1:
                tar = addNode(nodes, "Script@"+getInitiator(dataset['call_stack']['stack']), "Script", 1, 0, 0)
              else:
                tar = addNode(nodes, "Script@"+getInitiator(dataset['call_stack']['stack']), "Script", 0, 1, 0)
              addEdge(edges, tar, src, 'Initiated')
            else:
              addEdge(edges, nodes["HTML@https://www."+url+"/"][0], src, 'Initiated')
            
            # Links between storage nodes and script [setter, getter]
            if dataset["http_req"] in script_dic.keys():
              # script -> setter 
              if len(script_dic[dataset["http_req"]][0]) != 0:
                 for item in script_dic[dataset["http_req"]][0]:
                   addEdge(edges, nodes['Script@'+dataset["http_req"]][0], nodes['Storage@'+item][0], 'Storage Setter')
              # getter -> script
              if len(script_dic[dataset["http_req"]][1]) != 0:
                 for item in script_dic[dataset["http_req"]][1]:
                   addEdge(edges, nodes['Storage@'+item][0], nodes['Script@'+dataset["http_req"]][0], 'Storage Getter')

            # if url has storage info 
            val = IsInfoShared(storage_dic, dataset["http_req"])
            if val is not None:
              addEdge(edges, nodes['Storage@'+val][0], src, 'Info Shared')
    
    print(nodes)
    print(edges)

    plot = Digraph(comment='The Round Table')

    for key in nodes:
      
      if nodes[key][1] == 'Script':
        if nodes[key][2] == 0:
          plot.node(str(nodes[key][0]), str(nodes[key][0]), color='green', style='filled')
        elif nodes[key][3] == 0 and nodes[key][2] != 0:
          plot.node(str(nodes[key][0]), str(nodes[key][0]), color='red', style='filled')
        else:
          plot.node(str(nodes[key][0]), str(nodes[key][0]), color='yellow', style='filled')
      elif nodes[key][4] == -3:
        plot.node(str(nodes[key][0]), str(nodes[key][0]), color='blue', style='filled')
      elif nodes[key][4] == -2:
        plot.node(str(nodes[key][0]),str(nodes[key][0]), color='orange', style='filled')
      else:
        plot.node(str(nodes[key][0]), str(nodes[key][0]), color='purple', style='filled')
    
    for key in edges:
      if edges[key][2] == 'Network->HTML/Script':
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='normal')
      elif edges[key][2] == 'Info Shared':
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='diamond')
      elif edges[key][2] == 'Initiated':
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='tee')
      elif edges[key][2] == 'Redirection':
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='halfopen')
      elif edges[key][2] == 'Storage Getter':
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='crow')
      else:
        plot.edge(str(edges[key][0]), str(edges[key][1]), arrowhead='crow')
    
    plot.render('test-output/arabic.json.gv', view=True)


def main2():
  createWebGraph('arabic.chat')
  # string = {'stack': {'callFrames': [], 'parent': {'callFrames': [{'columnNumber': 181, 'functionName': 'fireTag$$module$dist$src$container$fireTags', 'lineNumber': 96, 'scriptId': '129', 'url': 'https://ap.lijit.com/sync'}, {'columnNumber': 241, 'functionName': 'fireTags$$module$dist$src$container$fireTags', 'lineNumber': 99, 'scriptId': '129', 'url': 'https://ap.lijit.com/sync'}, {'columnNumber': 210, 'functionName': 'dataCallback$$module$dist$src$container$getDataFromServer', 'lineNumber': 102, 'scriptId': '129', 'url': 'https://ap.lijit.com/sync'}, {'columnNumber': 9, 'functionName': '', 'lineNumber': 0, 'scriptId': '154', 'url': 'https://ap.lijit.com/containertag?containerId=18&zoneId=598981&v=2'}], 'description': 'Image'}}, 'type': 'script'}

  #print(getInitiator(string['stack']))
  # script_dic = {}
  # storage_dic = {}
  # dataset1 = {"top_level_url":"https://cmovies.online/","function":"cookie_setter","cookie:":"__PPU_BACKCLCK_3714332=true; expires=Wed, 16 Feb 2022 19:06:24 GMT; path=/; domain=cmovies.online","stack":"Error\n    at HTMLDocument.set (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:39:17)\n    at e.<computed>.<computed> [as saveSessionCustomKey] (https://lurgaimt.net/tag.min.js:1:43145)\n    at https://lurgaimt.net/tag.min.js:1:47814\n    at _ (https://lurgaimt.net/tag.min.js:1:8934)\n    at https://lurgaimt.net/tag.min.js:1:47689\n    at ln (https://lurgaimt.net/tag.min.js:1:48253)\n    at HTMLScriptElement.g (https://cmovies.online/:1630:60191)"}
  # dataset2 = {"top_level_url":"https://eus.rubiconproject.com/usync.html?p=btwnex&endpoint=eu","function":"cookie_getter","cookie:":"khaos=KZPV8CZP-15-K5E0; audit=1|GRYZojcvauLxCRmi07Abd33bvG56iVGUHpZdkt6wQBl5wrSQggMQUFeGcsFVzcEJPOh1wtc3tgnqFTrNE4+z9kqVaHlG5SlgpmvllXEtYN4=","stack":"Error\n    at HTMLDocument.get (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:19:17)\n    at readCookie (https://eus.rubiconproject.com/usync.js:4:1684)\n    at runSyncs (https://eus.rubiconproject.com/usync.js:4:10507)\n    at Image.d.onload (https://eus.rubiconproject.com/usync.js:4:9415)"}
  # dataset3 = {"top_level_url":"https://cmovies.online/","function":"indexdb_getter","storage:":{"_iiq_sync":"1645034787118","000000160024004d004e003t004a004c0040003t002m002m002o002k002m0024":"002a006u004d006m006n0064006n006o006m004d0051004s004n004d00690068006n0066006b006800670058006n004d0051004r004n004d006l0068006m006j006i006h006m0068004d0051006h006o006f006f004n004d006j006l0068006p006c006i006o006m005q006n0064006n0068004d0051006u004d006m006n0064006n006o006m004d0051004r004n004d00690068006n0066006b006800670058006n004d0051003f004r004n004d006l0068006m006j006i006h006m0068004d0051006h006o006f006f004n004d006j006l0068006p006c006i006o006m005q006n0064006n0068004d0051006h006o006f006f006w006w","000000160024002m002m002o002k002m0024":"0016009b006u008w008z008l008o008p008o007p0094006u007i0079007e007c007d0078007b007c007f007g007e007g007a007b0074006u0095008y008w008z008l008o008p008o007p0094006u007i007500790074005w006u008t008x00900092008p00930093008t008z008y0093006u007i008f008h009d","_iiq_fdata":"{\"pcid\":\"8d8307a6-33ff-4c30-b2c1-3bf70366cf33\",\"pcidDate\":1645034787112}","mgMuidn":"m1gqWoDFcW6a","bf001a61-ea58-4c69-33b4-1b01154b26f5":"6758687d7c1f9247508625","_iiq_fdata_1548712036":"{\"callCount\":1,\"failCount\":0,\"noDataCounter\":1,\"cttl\":43200000}","_mgIntentiq":"{\"time\":1645034787118,\"data\":\"e30=\"}","_mgPvid":"17f03b6cd7394629387"},"stack":"Error\n    at get (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:61:17)\n    at https://dozubatan.com/400/4414273:1:48414\n    at https://dozubatan.com/400/4414273:1:48824"}
  # addStorage(script_dic, storage_dic, dataset1)
  # addStorage(script_dic, storage_dic, dataset2)
  # addStorage(script_dic, storage_dic, dataset3)
  # print(script_dic)
  # print(storage_dic)

main2()