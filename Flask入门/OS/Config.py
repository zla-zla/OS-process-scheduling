from enum import Enum

ProcessorNum = 2    # 处理机个数
Memory = 100        # 内存大小
OSMemory = 20       # OS占用内存大小
MaxTrack = 10       # 规定道数

class PCBState(Enum):
    CREATE = 0          # '进程创建'
    ACTIVE_READY = 1    # '活动就绪'
    STATIC_READY = 2    # '静止就绪'
    BLOCK = 3           # '阻塞状态'
    RUNNING = 4         # '进程运行'
    SUSPENDING = 5      # '进程挂起'
    EXIT = 6            # '进程结束'

class Property(Enum):
    INDEPENDENT = 0     # '独立进程'
    SYNCHRONIZED = 1    # '同步进程'


class MemoryBlockState(Enum):
    UNASSIGNED = 0      # 未分配
    ASSIGNED = 1        # 已分配
    OS_ASSIGNED = 2     # OS使用

PCBStateDict = {
    'CREATE': '进程创建',
    'ACTIVE_READY': '活动就绪',
    'STATIC_READY': '静止就绪',
    'RUNNING': '进程运行',
    'SUSPENDING': '进程挂起',
    'EXIT': '进程结束'
}

PropertyDict = {
    'INDEPENDENT': '独立进程',
    'SYNCHRONIZED': '同步进程'
}

MemoryBlockStateDict = {
    'UNASSIGNED': '未分配',
    'ASSIGNED': '已分配',
    'OS_ASSIGNED': '操作系统',
}