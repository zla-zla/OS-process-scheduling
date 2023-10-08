from flask import Flask, request
from OS.System import System
from OS.PCB import PCB
from OS.Config import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
sys = System()

# 返回PCB列表，刷新操作
@app.route('/os/get_PCB_list', methods=['GET'])
def getPCBList():
    print('所有进程：' + str(sys.pcbQueue.toJson()))
    return sys.pcbQueue.toJson(), 200

# 表单发送进程基本数据，创建进程
@app.route('/os/create_PCB', methods=['POST'])
def createPCB():
    # 获取表单信息并转化
    form = request.get_json(silent=True)
    print('创建进程表单：' + str(form))
    pid = sys.pcbQueue.getNextPID()  # 自动生成PID
    time = int(form['form']['time'])    # 获取进程所需时间
    ram = int(form['form']['ram'])      # 获取进程所需内存
    priority = int(form['form']['priority'])    # 获取进程优先级
    prop_str = form['form']['property']         # 获取进程类别是同步还是独立的
    precursor_list = form['form']['precursor']  # 获取进程前驱
    # 同步进程
    if prop_str == '0':
        prop = Property.INDEPENDENT
    # 独立进程（异步进程）
    elif prop_str == '1':
        prop = Property.SYNCHRONIZED
    else:
        return {'errMsg': 'PCB进程创建错误！'}, 400
    precursor = set(precursor_list)
    # 创建新进程
    sys.createPCB(pid, time, ram, priority, prop, precursor)
    return sys.pcbQueue.toJson(), 200


@app.route('/os/get_main_memory')
def getMainMemory():
    print('内存：'+str(sys.mainMemory.toJson()))
    return sys.mainMemory.toJson(), 200


@app.route('/os/get_queue')
def getQueue():
    return sys.getQueue(),200



@app.route('/os/suspend', methods=['POST'])
def suspendPCB():
    form = request.get_json(silent=True)
    print('挂起进程表单：' + str(form))
    pid = int(form['form']['pid'])
    sys.checkSuspend(pid)
    return sys.pcbQueue.toJson(), 200

@app.route('/os/run')
def run():
    print(111)
    flag = sys.process()
    if not flag:
        return {'errMsg': '无可运行程序，请手动检查！'}, 400
    print('所有进程：' + str(sys.pcbQueue.toJson()))
    return sys.pcbQueue.toJson(), 200


if __name__ == '__main__':
    app.run(debug=True)
