from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #日志记录

"""
功能:技能学习
更新日志: 2024-11-12 14:53:24
描述:
    学习技能
"""

class TaskSkillsLearning(TaskLogic):
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

    def task_打开技能界面(self):
        self.node_current = "task_打开技能界面"

        if self.node_counter >= 5:  # 计数器大于等于5,退出
            logger.info("没有技能需要学习")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能学习完成"
            return "task_finish"

        elif "技能界面" in self.interface_info:
            logger.info("技能界面")
            self.node_current = "task_技能学习"
            self.node_counter = 0  # 重置计数器
            return "task_finish"

        elif "主界面" in self.interface_info:
            self.key_press("K", delay_time=2)
        else:
            self.interface_closes()
            
        self.node_counter += 1  # 计数器加一

    def task_技能学习(self):
        self.node_current = "task_技能学习"

        if self.node_counter >= 5:  # 计数器大于等于5,退出
            logger.info("没有技能需要学习")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能学习完成"
            return "task_finish"

        if self.find_data_from_keys_list_click(["确定"],self.word_handle_data,delay_time=1):
                self.node_counter =0 #重置计数器
                logger.info("确定技能升级")

        elif "技能界面" in self.interface_info:
            key_list=["resource/images_info/other/技能升级.png"]
            if self.find_data_from_keys_list_click(key_list,self.image_data,delay_time=1):
                logger.info("点击升级标志")
                self.mouse_move(1122,634,delay_time=1)

        elif self.interface_info in ["主界面"]:#说明可能误操作
            self.key_press("K", delay_time=2)
        else:
            self.interface_closes()

        self.node_counter += 1  # 计数器加一


    def task_技能学习完成(self):
        self.node_current = "task_技能学习完成"

        if "主界面" in self.interface_info:
            self.ls_progress="task_finish"
            return "task_finish"
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_打开技能界面": self.task_打开技能界面,
            "task_技能学习": self.task_技能学习,
            "task_技能学习完成": self.task_技能学习完成,

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
            self.task_打开技能界面()
        elif self.handle_task():
            pass


task_skills_learning_data={
    "word": {
        "确定":{
            "scope": (608, 433, 708, 482),
            "con": 0.8,
            "model":0,
            "offset": (0, 0),
            "use": "技能学习",
            "enable":True,
        },
    },
    "image": {
        r"resource/images_info/other/技能升级.png": {
            "scope": (453,206,949,637),
            "model": 1,
            "con": 0.8,
            "enable": True
        },  # 技能升级
    },

}