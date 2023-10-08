from OS.PCBQueue import *
from OS.MainMemory import *

class Processor:
    def __init__(self):
        self.__processorNum = ProcessorNum  # 处理机个数

    def process(self, pcb_queue: PCBQueue, ready_queue:list):
        finish = []  # 返回结束的进程的pid
        # 从就绪队列中取出前几个分配给对应处理机进行一步运行
        for i in range(self.__processorNum):
            if i < len(ready_queue):
                # 获取pcb并使该pcb运行一步
                pcb = pcb_queue.getPCBByPID(ready_queue[i])
                if pcb.process():
                    finish.append(pcb.getPID())
        return finish


