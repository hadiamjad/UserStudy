def dependency_graph(key, json_filepath, unique_nodes, unique_edges, test, train):
  # syntax: {"script_url": ["unique_identifier", "label", "tracking_count", "non-tracking_count", test, train]}
  # count +1 for tracking & -1 for non-tracking
  with open(json_filepath) as file:
    for line in file:
      data = json.loads(line)
      for dataset in data:
        # handling non-script type
        if dataset['call_stack']['type'] != 'script': pass
        else:
          # recursively add uniques nodes in the graph
          # if its tracking http call then update the tracking count of all scripts in that stack
          if dataset['easylistflag'] == 1 or dataset['easyprivacylistflag'] == 1 or dataset['ancestorflag'] == 1:
            rec_stack_nodes_adder(dataset['call_stack']['stack'], unique_nodes, label, 1, key, test, train)
            # recursively add tracking edges in the graph
            rec_plot_edges(dataset['call_stack']['stack'], unique_nodes, unique_edges, 1, None, key)
          # if its non-tracking http call then update the non-tracking count of all scripts in that stack
          else:
            rec_stack_nodes_adder(dataset['call_stack']['stack'], unique_nodes, label, 0, key, test, train)
            # recursively add non tracking edges in the graph
            rec_plot_edges(dataset['call_stack']['stack'], unique_nodes, unique_edges, 0, None, key)
  
    return unique_nodes, unique_edges

# Description: it creates edges in the plot recursively
# input: stack = stack object as shown in the image above
# input: unique_nodes = unique nodes in the given website trace
# input: unique_edges = unique edges in the given website trace
# input: trackingflag = tracking request or non-tracking request
# input: prev = It is set when we are jumping from base to parent and initially not set
# return: nothing
def rec_plot_edges(stack, unique_nodes, unique_edges, trackingflag, prev, key):
  for i in range(len(stack['callFrames'])-1):
    if prev is not None:
         if key == 'script':
            prevKey1 = unique_nodes[stack['callFrames'][i]['url']][0]
            prevKey2 = prev
         else:
           prevKey1 = unique_nodes[stack['callFrames'][i]['url']+"@"+stack['callFrames'][i]['functionName']][0] 
           prevKey2 = prev
         
         # if edge is not already created only then create that edge (prev-condition)
         if prevKey1 +"@"+ prevKey2 not in unique_edges.keys():
                unique_edges[prevKey1 +"@"+ prevKey2] = [prevKey1, prevKey2, 0, 0]
         if trackingflag == 1:
                unique_edges[prevKey1 +"@"+ prevKey2][2] += 1
         else:
                unique_edges[prevKey1 +"@"+ prevKey2][3] += 1
    
    if key == 'script':
            basicKey1 = unique_nodes[stack['callFrames'][i+1]['url']][0] 
            basicKey2 = unique_nodes[stack['callFrames'][i]['url']][0]
    else:
            basicKey1 = unique_nodes[stack['callFrames'][i+1]['url']+"@"+stack['callFrames'][i+1]['functionName']][0] 
            basicKey2 = unique_nodes[stack['callFrames'][i]['url']+"@"+stack['callFrames'][i]['functionName']][0]
    
    # if edge is not already created then create and assign tracking and non-tracking count
    if basicKey1 +"@"+ basicKey2 not in unique_edges.keys():
                  unique_edges[basicKey1 +"@"+ basicKey2] = [basicKey1, basicKey2, 0, 0]
             
    # if edge is already created then update tracking and non-tracking count
    if trackingflag == 1:
            unique_edges[basicKey1 +"@"+ basicKey2][2] += 1
    else:
            unique_edges[basicKey1 +"@"+ basicKey2][3] += 1

  # if parent object doen't exist return (base-case)
  if 'parent' not in stack.keys(): return
  # in case where base is empty but parent exists
  elif len(stack['callFrames']) == 0: rec_plot_edges(stack['parent'], unique_nodes, unique_edges, trackingflag, None, key)
  # else send recursive call for parent and set the prev
  else: 
    if key == 'script':
      rec_plot_edges(stack['parent'],
                          unique_nodes, unique_edges, trackingflag, unique_nodes[stack['callFrames'][len(stack['callFrames'])-1]['url']][0], key)
    else:
      rec_plot_edges(stack['parent'],
                          unique_nodes, unique_edges, trackingflag, unique_nodes[stack['callFrames'][len(stack['callFrames'])-1]['url']+"@"+stack['callFrames'][len(stack['callFrames'])-1]['functionName']][0], key)


# Description: it appends the unique node url+functionname+linenumber+columnnumber recursively
# input: stack = stack object as shown in the image above
# input: unique_nodes = unique nodes in the given stack
# input: label = its the label for the uique node
# input: plot = dot plot object
# return: nothing
def rec_stack_nodes_adder(stack, unique_nodes, label, trackingflag, key, test, train):
  # append unique script_url's
  for item in stack['callFrames']:
    if key == 'script':
       basicKey = item['url']
    else:
       basicKey = item['url']+"@"+item['functionName']
    if basicKey not in unique_nodes.keys():
      unique_nodes[basicKey] = [str(label[0]), 0, 0, test, train]
      # plot.node( str(label[0]), item['url'])
      label[0] += 1
    # if its tracking call then +1 the tracking count for that node
    if trackingflag == 1:
      unique_nodes[basicKey][1] += 1
    # else if its non-tracking call then +1 the non-tracking count for that node
    else:
      unique_nodes[basicKey][2] += 1
    
    # setting test and train
    if unique_nodes[basicKey][3] != 1:
      unique_nodes[basicKey][3] = test
    if unique_nodes[basicKey][4] != 1:
      unique_nodes[basicKey][4] = train
  
  # if parent object doen't exist return (base-case)
  if 'parent' not in stack.keys(): return
  # else send a recursive call for this
  else: rec_stack_nodes_adder(stack['parent'], unique_nodes, label, trackingflag, key,  test, train)


# print("\n---------TRAIN.JSON--------------")
# unique_nodes,unique_edges = dependency_graph("script", "/content/TwoLabelledRequestForTesting.json", unique_nodes, unique_edges, 1, 0)
# print("\n---------TEST.JSON--------------")

# script sample -> at l (https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
def getScriptFromStack(script):
    try:
        script = script.split('(')[1] # https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
    except:
        pass
    return "https:"+ script.split(':')[1]

## cookie_storage nodes and edges should be added
## edges:
## cookie-script get ->/set <-
## 
def Cookie_Storage(json_filepath, unique_nodes, unique_edges):
    with open(json_filepath) as file:
        for line in file:
            dataset = json.loads(line)
            # creating cookie edges and nodes
            if "cookie:" in dataset.keys()  and dataset["cookie:"] != "":
                try:
                    if dataset["cookie:"].split("=")[0] not in unique_nodes.keys():
                        unique_nodes[dataset["cookie:"].split("=")[0]] = [str(label[0]), -1, -1, 0, 0]
                        label[0] +=1
                    # this case should never occur becasue script should be present before
                    # if getScriptFromStack(dataset["stack"].split("\n")[2]) not in unique_nodes.keys():
                    #    unique_nodes[getScriptFromStack(dataset["stack"].split("\n")[2])] = [str(label[0]), 0, 0 , 0, 0]    
                    #    label[0] +=1
                    # cookie node label
                    key1 = unique_nodes[dataset["cookie:"].split("=")[0]][0]
                    # script node label
                    key2 = unique_nodes[getScriptFromStack(dataset["stack"].split("\n")[2])][0]
                    # cookie-script get ->/set <-
                    if dataset["function"] == "cookie_getter":
                        if key1 + "@" + key2 not in unique_edges.keys():
                            unique_edges[key1 +"@"+ key2] = [key1, key2]
                    else:
                        if key2 + "@" + key1 not in unique_edges.keys():
                            unique_edges[key2 +"@"+ key1] = [key2, key1]
                except:
                    pass
            # creating storage cookies and edges
            elif "storage:" in dataset.keys() and dataset["storage:"] != "":
                try:
                    # script node label
                    key2 = unique_nodes[getScriptFromStack(dataset["stack"].split("\n")[2])][0]
                    for key in dataset["storage:"]:
                        if key not in unique_nodes.keys():
                            unique_nodes[key] = [str(label[0]), -2, -2, 0, 0]
                            label[0] +=1 
                            # storage node label
                            key1 = unique_nodes[key][0]
                            if key1 + "@" + key2 not in unique_edges.keys():
                                unique_edges[key1 +"@"+ key2] = [key1, key2]
                except:
                    pass

######################


def getDF_srctar(dic, df):
  i = 0
  for key in dic:
    df.loc[i] = [dic[key][0], dic[key][1]]
    i +=1
  return df

# test_tuple = []
# train_tuple = []
# label = [0(mixed), 1(tracking), 2(non-tracking), -2(cookie), -1(storage)]
def getDF_Nodes(dic, df):
  i = 0
  for key in dic:
    str = key.split('@', 1)
    if dic[key][1] == -1:
        label = -1
    elif dic[key][1] == -2:
        label = -2 
    elif dic[key][1] == 0:
      label = 2
    elif dic[key][2] == 0:
      label = 1
    else:
      label = 0
    df.loc[i] = [dic[key][0], label, str[0], dic[key][3], dic[key][4]]
    # if dic[key][3] == 1:
    #   test_tuple.append((dic[key][0], label))
    # if dic[key][4] == 1:
    #   train_tuple.append((dic[key][0], label))
    i +=1
  return df



def main():
    # unique node and edges
    # unique_nodes => script:[id, tracking, non-tracking, test, train] for cookie -1, -1 for storage -2, -2
    # unique_edges => script_id@script_id: [script_id, script_id] or cookies_id, storage_id
    unique_nodes = {}
    unique_edges = {}

    unique_nodes, unique_edges = dependency_graph("script", "labellings.json", unique_nodes, unique_edges, 0, 0)

    Cookie_Storage("server/cookie_storage.json", unique_nodes, unique_edges)
    # print (unique_nodes)
    
    df = pd.DataFrame(columns=['source', 'target'])
    df2 = pd.DataFrame(columns=['node', 'label', 'script_url', 'test', 'train'])
    
    df = getDF_srctar(unique_edges, df)
    df2 = getDF_Nodes(unique_nodes, df2)
    print("\n---------DF,DF2--------------")

    plot = Digraph(comment='The Round Table')

    nodes = []
    # label = [0(mixed)->yellow, 1(tracking)->red, 2(non-tracking)->green, -2(storage)->blue, -1(cookie)->orange]
    for i in df2.index:
        if df2['label'][i] == -2:
            plot.node(df2['node'][i], df2['node'][i], color='blue', style='filled')
        elif df2['label'][i] == -1:
            plot.node(df2['node'][i], df2['node'][i], color='orange', style='filled')
        elif df2['label'][i] == 2:
            plot.node(df2['node'][i], df2['node'][i], color='green', style='filled')
        elif df2['label'][i] == 1:
            plot.node(df2['node'][i], df2['node'][i], color='red', style='filled')
        elif df2['label'][i] == 0:
            plot.node(df2['node'][i], df2['node'][i], color='yellow', style='filled')

            
    print("\n---------NODES--------------")

    edges = []
    for i in df.index:
    # if (int(df['source'][i]), int(df['target'][i])) not in edges and (int(df['target'][i]), int(df['source'][i])) not in edges:
        edges.append((int(df['source'][i]), int(df['target'][i])))
        plot.edge(df['source'][i], df['target'][i])
    print("\n---------EDGES--------------")

    # rendering the plot
    plot.render('test-output/test.json.gv', view=True)
