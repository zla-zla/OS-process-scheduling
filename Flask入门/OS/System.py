from OS.Processor import *
'''
成员函数：
创建新的进程
挂起进程
解除进程挂起
处理器运行一步

获取PCB列表
获取四种队列
获取主存使用信息
获取处理器当前处理信息

'''

class System:
    def __init__(self):
        self.ready_queue = []       # 就绪队列
        self.backup_queue = []      # 后备队列
        self.block_queue = []       # 阻塞队列
        self.suspend_queue = []     # 挂起队列
        self.pcbQueue = PCBQueue()  # 总PCB信息
        self.mainMemory = MainMemory()  # 主存
        self.processor = Processor()    # 处理器类
        self.track = 0    # 作业道数

    def createPCB(self, pid: int, time: int, ram: int, priority: int, prop: Property, precursor: set, state=PCBState.CREATE):
        # 创建PCB块并加入PCB队列
        pcb=PCB(pid,time,ram,priority,prop,precursor,state)
        self.pcbQueue.append(pcb)
        # 检查是否能放入内存，如果不能则加进后备队类；如果可以则放入内存并检查前驱，如果前驱都完成了则添加进就绪队列，否则加进阻塞队列
        flag, index = self.mainMemory.checkAssignable(pcb)
        if flag:
            self.mainMemory.insertPCB(pcb, index)
            if(pcb.preFinish(self.pcbQueue)):
                self.ready_queue.append(pcb.getPID())
                self.track += 1
            else:
                self.block_queue.append(pcb.getPID())
        else:
            self.backup_queue.append(pcb.getPID())

    def process(self):
        # 就绪队列重新排序
        self.__sortReady()
        # 检查是否有进程可以运行，如果有将就绪队列丢进处理器模拟一步运行
        if len(self.ready_queue) > 0:
            finish = self.processor.process(self.pcbQueue, self.ready_queue)
            # 如果finish非空,即有进程结束;为空则跳过下两行
            for pid in finish:
                self.mainMemory.removePCB(self.pcbQueue.getPCBByPID(pid))  # 移出主存
                self.ready_queue.remove(pid)  # 移出就绪队列
                self.track -= 1
            # 有进程完成说明阻塞队列可能有进程可以进行了,检查阻塞队列
            self.__updateBlock()
            # 有进程移出内存说明后备队列可能有进程可以载入内存了,检查后备队列
            self.__updateBackup()
            return True
        else:
            return False  # 无进程可运行

    def getQueue(self):
        # 前端表格展示需要字典数组的形式
        dict = {}
        jsonList = []
        for pid in self.ready_queue:
            jsonList.append({'pid': pid})
        dict['ready_queue'] = jsonList
        jsonList = []
        for pid in self.backup_queue:
            jsonList.append({'pid': pid})
        dict['backup_queue'] = jsonList
        jsonList = []
        for pid in self.block_queue:
            jsonList.append({'pid': pid})
        dict['block_queue'] = jsonList
        jsonList = []
        for pid in self.suspend_queue:
            jsonList.append({'pid': pid})
        dict['suspend_queue'] = jsonList
        return dict

    def checkSuspend(self, pid: int):
        # 判断是要挂起还是解挂
        if pid in self.ready_queue or pid in self.block_queue:
            self.suspend(pid)
        elif pid in self.suspend_queue:
            self.unsuspend(pid)


    def suspend(self, pid: int):
        # 在就绪队列或者阻塞队列中找到该pid并移除，根据pid找到pcb在内存中移除，添加进挂起队列
        if pid in self.ready_queue:
            self.ready_queue.remove(pid)
            self.track -= 1  # 道数-1
        elif pid in self.block_queue:
            self.block_queue.remove(pid)
        pcb = self.pcbQueue.getPCBByPID(pid)
        self.mainMemory.removePCB(pcb)
        self.suspend_queue.append(pid)
        pcb.setState(PCBState.SUSPENDING)  # 设置挂起状态
        # 有进程挂起就有内存空闲，需要更新阻塞队列和后备队列
        self.__updateBlock()
        self.__updateBackup()

    def unsuspend(self, pid: int):
        # 解挂进程，将该进程移除挂起队列，检查是否能放入内存，如果不能则加进后备队列；如果可以则放入内存并检查前驱，如果前驱都完成了则添加进就绪队列，否则加进阻塞队列
        if pid in self.suspend_queue:
            self.suspend_queue.remove(pid)
            pcb = self.pcbQueue.getPCBByPID(pid)
            flag, index = self.mainMemory.checkAssignable(pcb)
            if flag:
                self.mainMemory.insertPCB(pcb, index)
                if (pcb.preFinish(self.pcbQueue)):
                    self.ready_queue.append(pcb.getPID())
                    self.track += 1
                else:
                    self.block_queue.append(pcb.getPID())
            else:
                self.backup_queue.append(pcb.getPID())



    def __updateBackup(self):
        for pid in self.backup_queue:
            pcb = self.pcbQueue.getPCBByPID(pid)
            flag, index = self.mainMemory.checkAssignable(pcb)
            # 如果可以分配内存
            if flag:
                self.backup_queue.remove(pid)
                self.mainMemory.insertPCB(pcb, index)
                if (pcb.preFinish(self.pcbQueue)):
                    self.ready_queue.append(pcb.getPID())
                    self.track += 1  # 道数+1
                else:
                    self.block_queue.append(pcb.getPID())

    def __updateBlock(self):
        for pid in self.block_queue:
            pcb = self.pcbQueue.getPCBByPID(pid)
            # 如果前驱完成且小于规定道数就加入就绪队列
            if pcb.preFinish(self.pcbQueue) and self.track < MaxTrack:
                self.block_queue.remove(pid)
                self.ready_queue.append(pid)

    # 就绪队列的排序
    def __sortReady(self):
        self.ready_queue = sorted(self.ready_queue, key=lambda pid: self.pcbQueue.getPCBByPID(pid).getPriority(),reverse=True)




