from OS.PCB import *

'''
MainMemory主存类
checkAssignable：检查主存是否可分配内存给PCB，返回插入主存分区表的位置序号
insertPCB:插入新的PCB到__memory中
checkProcessable:判断是否有进程可以运行
removePCB:从主存中移除PCB
toJson:以Json格式返回内存分区表信息
__mergeMemory:合并空闲块
'''

class MainMemory:
    def __init__(self):
        # 内存分区表[[分区号，内存起始，内存大小，状态], ...]，OS对应的内存表项用-1表示，未分配内存表项用-2表示
        self.__memory =[[-1, 0, OSMemory, MemoryBlockState.OS_ASSIGNED],
                         [-2, OSMemory, Memory - OSMemory, MemoryBlockState.UNASSIGNED]]

    def toJson(self):
        jsonList = []
        for index, memoryBlock in enumerate(self.__memory):
            jsonList.append({
                'memory_PCB': memoryBlock[0],
                'start': memoryBlock[1],
                'length': memoryBlock[2],
                'memory_state': MemoryBlockStateDict[memoryBlock[3].name],
            })
        return {'main_memory': jsonList}

    def checkAssignable(self, pcb: PCB):
        # 在内存分区表中查找空闲块
        for index, memoryBlock in enumerate(self.__memory):
            # 找到未分配空间并检查大小是否够存PCB，返回插入内存分区表的位置
            if memoryBlock[3] == MemoryBlockState.UNASSIGNED and memoryBlock[2] >= pcb.getRam():
                return True, index  
        return False, -1
        
    def insertPCB(self, pcb: PCB, index: int):
        # 将PCB插入到__memory的memoryBlockNum位置上
        partition = self.__memory[index]   # 获取被划分块
        pcb_ram = pcb.getRam()  # 获取内存大小
        pcb_id = pcb.getPID()   # 获取PID
        pcb.setState(PCBState.ACTIVE_READY)  # 更新PCB状态
        # 内存长度正好相等
        if partition[2] == pcb_ram:
            partition[0] = pcb_id
            partition[3] = MemoryBlockState.ASSIGNED
        # 否则划分空闲块
        else:
            # 插入一块被划分出来的空闲块
            self.__memory.insert(index + 1,
                                 [-2, partition[1] + pcb_ram, partition[2] - pcb_ram, MemoryBlockState.UNASSIGNED])
            # 修改原空闲块为被分配
            partition[0] = pcb_id
            partition[2] = pcb_ram
            partition[3] = MemoryBlockState.ASSIGNED

    def removePCB(self, pcb: PCB,):
        # 从内存中移除PCB
        memoryBlockNum = 0
        pid = pcb.getPID()
        # 遍历内存块找到被删除的进程
        for index, value in enumerate(self.__memory):
            if value[0] == pid:
                memoryBlockNum = index
        self.__memory[memoryBlockNum][0] = -2
        self.__memory[memoryBlockNum][3] = MemoryBlockState.UNASSIGNED
        self.__mergeMemory()

    def __mergeMemory(self):
        # 合并未分配的内存空间，每次结束一个进程最多产生一段空闲内存
        flag = False
        memoryBlockToMergeList = []  # 记录要合并的第二块及其后内存块的位置
        for index, value in enumerate(self.__memory):
            pid = value[0]
            if pid == -2:  # 检测到未分配的内存空间（-2）
                if not flag:  # 第一次检测到未分配的内存空间（-2）
                    flag = True
                else:  # 不是第一次检测到未分配的内存空间（-2），即有连续的未分配空间
                    memoryBlockToMergeList.append(index)
            if pid != -2:  # 检测到已分配的内存空间（!=-2）
                flag = False
        if memoryBlockToMergeList:
            beginMemoryBlockNum = memoryBlockToMergeList[0] - 1  # 要合并的第一个内存块的位置
            for partition in memoryBlockToMergeList[::-1]:
                memoryBlockToMerge = self.__memory.pop(partition)  # 倒序pop
                self.__memory[beginMemoryBlockNum][2] += memoryBlockToMerge[2]  #累加大小





