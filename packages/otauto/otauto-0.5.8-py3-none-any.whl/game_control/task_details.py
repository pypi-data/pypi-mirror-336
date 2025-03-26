from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

class TaskDetails(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle):
        super().__init__(vnc,vnc_port,queue_handle)

    def task_01(self):
        pass
    def task_02(self):
        pass
    def task_03(self):
        pass
    def handle_task(self):
        task_methods = {
            'task_01': self.task_01,
            'task_02': self.task_02,
            'task_03': self.task_03,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

    def task_details(self):
        """
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器
        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        函数写入这里
        """
        logger.success(f"任务详情:{self.__class__.__name__}")
        logger.success(f"节点信息:{self.node_current}")

        if not self.node_current:
            pass
        elif self.handle_task():
            pass


name_change_data={
    "word": {
        # 30: {
        #     "scope": (608, 225, 1006, 691),
        #     "con": 0.8,
        #     "offset": (0, 0),
        #     "use": "成长奖励",
        #     "unique": True,
        #     "enable": True,
        # },  # 每日签到
        # "高级特权":{
        #     "scope": (580,485,739,539),
        #     "con": 0.8,
        #     "offset": (0, 0),
        #     "use": "每日签到",
        #     "enable":True,
        # },#每日签到

    },
    "image": {
        # r"resource/images_info/other/奖励图标.bmp":{
        #     "scope":(1036, 41, 1254, 112),
        #     "con":0.8,
        #     "enable":True
        #     "unique": True,
        # },#奖励图标

    },
}