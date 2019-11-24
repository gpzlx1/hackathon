import PIL 
import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

def json2net(data):
    node_info = {}
    for x in data['operators'].keys():
        node_info[(x,data['operators'][x]['properties']['title'])] = data['operators'][x]['properties']['information']
    
    link_info = {}
    for x in data['links'].keys():
        unitdata = {}
        unitdata['fromOperator'] = data['links'][x]['fromOperator']
        unitdata['toOperator'] = data['links'][x]['toOperator']
        link_info[x] = unitdata

    from_seq = [0 for i in range(len(node_info))]
    to_seq = [0 for i in range(len(node_info))]
    for x in link_info.keys():
        from_seq[link_info[x]['fromOperator']] +=1
        to_seq[link_info[x]['toOperator']] +=1

    opStart = to_seq.index(0)
    opEnd = from_seq.index(0)

    seq = []
    op = opStart
    while op != str(opEnd):
        flag = False
        seq.append(op)
        for x in link_info.keys():
            if link_info[x]['fromOperator'] == op:
                flag = True
                op = link_info[x]['toOperator']
                break
        if flag == False:
            break
    
    result = []
    for x in seq:
        d = {}
        for k in node_info.keys():
            if int(k[0]) == x:
                if  k[1][0:10] == 'Start Node':
                    d['name'] = 'start'
                elif k[1][0:8] == 'End Node':
                    d['name'] = 'end'
                elif k[1][0:15] == 'Fully-connected':
                    d['name'] = 'dense'
                elif k[1][0:7] == 'Pooling':
                    d['name'] = 'pool'
                elif k[1][0:10] == 'Activation':
                    d['name'] = 'act'
                elif k[1][0:7] == 'Dropout':
                    d['name'] = 'dropout'
                elif k[1][0:11] == 'Convolution':
                    d['name'] = 'conv'
                for m in node_info[k].keys():
                    d[m] = node_info[k][m]
                break
        result.append(d)
    return result, seq


def get_outputshape(nnParamter):
    output = [28, 28, 1]
    err = {}
    err["status"] = False
    err["index"] = -1
    if(nnParamter[-1]["name"] != "end"):
        err["msg"] = "You should design a complete nerual network"
        return False, err
    for i in range(0, len(nnParamter)):
        value = nnParamter[i]

        if i == 0:
            if value["name"] != "dense" and value["name"] != "conv":
                err["index"] = 1
                err["msg"] = "the first layer should be conv or dense"
                return False, err

        if value["name"] == "act" or value["name"] == "dropout":
            continue
        elif value["name"] == "conv" or value["name"] == "pool":
            if output[0] < value["sizeX"]:
                err["index"] = i + 1
                err["msg"] = "the sizeX and strideX is not valied"
                return False, err
            if output[1] < value["sizeY"]:
                err["index"] = i + 1
                err["msg"] = "the sizeY and strideY is not valied"
                return False, err
            x1 = int((output[0] - 1 + 1) / value["strideX"] + 0.5)
            x2 = int((output[0] + 1 - value["sizeX"]) / value["strideX"] + 0.5)
            x = min(x1, x2)
            y1 = int((output[0] - 1 + 1) / value["strideX"] + 0.5)
            y2 = int((output[0] + 1 - value["sizeX"]) / value["strideX"] + 0.5)
            y = min(y1, y2)
            if value["name"] == "conv":
                output = [x,y,value["channel"]]
            else:
                output[0] = x
                output[1] = y
        elif value["name"] == "dense":
            output[2] = value["num"]
        elif value["name"] == "end":
            if output[0] == 1 and output[1] == 1:
                err["status"] = True
                err["if_add"] = False
                return True, err
            else:
                err["status"] = True
                err["if_add"] = True
                return True, err
        else:
            err["msg"] = "you should never see this line in console"
            return False, err
    err["msg"] = "you should never see this line in console"
    return False, err



#有许多限制
#dropout 后面没有激活
#池化层后面不能接激活
#激活后面不能接激活
#第一层固定为卷积
#最后一层固定为全连接
# 卷积 conv
# 池化 pool
# 全连接 dense
# dropout
# 激活 act
def get_next(nnParameter, index):
    length = len(nnParameter)
    if(index + 1 < length):
        if(nnParameter[index+1]["name"] == "act"):
            return True, nnParameter[index+1]["ActivationFunc"].lower()
        else:
            return False, False
    else:
        return False, False

class CNN(object):
    def __init__(self, nnParameter, if_add):
        model = models.Sequential()
        #先不搞错误处理
        length = len(nnParameter)
        i = 0
        while i < length:
            layer = nnParameter[i]
            if i == 0 and layer["name"] == "conv" : #第一层特殊
                status, act_name = get_next(nnParameter, i)
                if status:
                    model.add(layers.Conv2D(layer["channel"], \
                    (layer["sizeX"], layer["sizeY"]), strides=(layer["strideX"],layer["strideY"]), activation=act_name, input_shape=(28, 28, 1)))
                    i = i + 1
                else:
                    model.add(layers.Conv2D(layer["channel"], \
                    (layer["sizeX"], layer["sizeY"]), strides=(layer["strideX"],layer["strideY"]), input_shape=(28, 28, 1)))

            elif i == 0 and layer["name"] == "dense": #第一层特殊
                status, act_name = get_next(nnParameter, i)
                if status:
                    model.add(layers.Dense(layer["num"], activation=act_name, input_shape=(28,28,1)))
                    i = i + 1
                else:
                    model.add(layers.Dense(layer["num"], input_shape=(28,28,1)))
            
            elif i != length - 1:#不是最后一层

                if layer["name"] == "conv":
                    status, act_name = get_next(nnParameter, i)
                    if status:
                        model.add(layers.Conv2D(layer["channel"], \
                        (layer["sizeX"], layer["sizeY"]), strides=(layer["strideX"],layer["strideY"]), activation=act_name))
                        i = i + 1
                    else:
                        model.add(layers.Conv2D(layer["channel"], \
                        (layer["sizeX"], layer["sizeY"]), strides=(layer["strideX"],layer["strideY"])))

                elif layer["name"] == "dropout":
                    model.add(layers.Dropout(layer["rate"]))

                elif layer["name"] == "act":
                    i = i + 1
                    continue
 
                elif layer["name"] == "dense":
                    status, act_name = get_next(nnParameter, i)
                    if status:
                        model.add(layers.Dense(layer["num"], activation=act_name))
                        i = i + 1
                    else:
                        model.add(layers.Dense(layer["num"]))
                elif layer["name"] == "pool":
                    model.add(layers.MaxPooling2D((layer["sizeX"], layer["sizeY"]), strides=(layer["strideX"],layer["strideY"])))
            
            else: #最后一层
                if(if_add):
                    model.add(layers.Flatten())
                model.add(layers.Dense(layer["OutputDim"], activation='softmax'))  

            i = i + 1    

        model.summary()

        self.model = model

def switchToNum(nnParameter):
    for term in nnParameter:
        if term["name"] == "conv":
            term["sizeX"] =int(term["sizeX"])
            term["sizeY"] = int(term["sizeY"])
            term["strideX"] = int(term["strideX"])
            term["strideY"] = int(term["strideY"])
            term["channel"] = int(term["channel"])

        if term["name"] == "pool":
            term["sizeX"] =int(term["sizeX"])
            term["sizeY"] = int(term["sizeY"])
            term["strideX"] = int(term["strideX"])
            term["strideY"] = int(term["strideY"])
        
        if term["name"] == "dense":
            term["num"] = int(term["num"])
        
        if term["name"] == "dropout":
            term["rate"] = float(term["rate"])
    return nnParameter


 
def cnn(data):
    if data['operators'] == {} or data['links'] == {}:
        err = {}
        err["status"] = False
        err["msg"] = "the canvas should not be null and you should design a complete workflow"
        err["index"] = -1
        return False, err
    nn, seq = json2net(data)
    nn = nn[1:]
    nn = switchToNum(nn)
    status, err = get_outputshape(nn)
    if(status):
        cnn = CNN(nn, err["if_add"])
        return True, cnn
    else:
        err["index"] = seq[err["index"]]
        return False, err

