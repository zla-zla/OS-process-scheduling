from OS.PCB import PCB

'''
PCB队列类（保存所有PCB块）
getNextPID:自动生成PID
getPCBByPID:通过PID返回PCB
toJson:以Json格式返回
append:PCB入队列
setPCBSuccessor:用新的PCB更新队列中的PCB的后继
'''
class PCBQueue:
    def __init__(self):
        self.__pcbList = []  # 存PCB

    # 获取队列最后一个PCB的PID
    def getNextPID(self):
        return self.__pcbList[-1].getPID() + 1 if self.__pcbList else 0

    def getPCBByPID(self, pid: int):
        return self.__pcbList[pid]

    def toJson(self):
        pcb_list = []
        for pcb in self.__pcbList:
            pcb_list.append(pcb.toJson())
        return {'pcb_list': pcb_list}

    def append(self, pcb: PCB):
        self.__pcbList.append(pcb)
        self.setPCBSuccessor(pcb)

    def setPCBSuccessor(self, pcb: PCB):
        for i in pcb.getPrecursor():
            prePCB = self.getPCBByPID(i)
            prePCB.addSuccessor(pcb.getPID())
