from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

class TaskEquipUpgrade(TaskLogic):
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
        self.last_points = [-1,-1] # 记录上一次点击的位置，防止重复点击

    def task_打开装备进阶界面(self):
        """
        1,对话界面点击对话
        2,完成条件,该节点完成
        :return:
        """
        self.node_current="task_打开装备进阶界面"
        if  self.node_counter>=3:#计数器大于等于5,退出
            logger.info("没有找到需要进阶的装备")
            self.node_counter=0 #重置计数器
            self.node_current="task_装备进阶完成"
            return "task_finish"

        elif "装备进阶界面" in self.interface_info:
            logger.info("装备进阶界面")
            self.node_current="task_装备进阶"
            self.node_counter=0#重置计数器
            return "task_finish"

        elif "角色信息界面" in self.interface_info:
            logger.info("角色信息界面")
            if self.find_data_from_keys_list_click(["resource/images_info/other/升级标志.bmp"],self.image_data,delay_time=3):
                logger.info("找到需要进阶的装备")
            else:
                self.node_counter+=1 #计数器加一

        elif "主界面" in self.interface_info:
            self.key_press("C",delay_time=2)

    def task_装备进阶(self):
        self.node_current = "task_装备进阶"

        if  self.node_counter>=5:#计数器大于等于5,退出
            logger.info("没有找到需要进阶的装备")
            self.node_counter=0 #重置计数器
            self.node_current="task_装备进阶完成"
            return "task_finish"

        elif "装备进阶界面" in self.interface_info:
            logger.info("装备进阶界面")
            if self.find_data_from_keys_list_click(["确"], self.word_handle_data, delay_time=1):
                logger.info("点击确定")
                self.node_counter=0 #重置计数器

            res_dict=self.find_data_from_keys_list(["resource/images_info/other/升级标志.bmp"],self.image_data)
            #{'resource/images_info/other/升级标志.bmp': {'scope': [(447, 377, 453, 390, 0.989), (574, 414, 580, 427, 0.828), (574, 234, 580, 247, 0.816)], 'model': 1, 'enable': True, 'unique': True}}
            if res_dict:
                logger.info("找到需要进阶的装备")
                if self.find_data_from_keys_list_click(["确"],self.word_handle_data, delay_time=1):
                    logger.info("点击确定")
                    self.node_counter = 0  # 重置计数器

                elif self.find_data_from_keys_list_click(["进阶"], self.word_handle_data, delay_time=1):
                    logger.info("点击进阶")

                elif self.find_data_from_keys_list_click(["立即制作"], self.word_handle_data, delay_time=2):
                    self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1)
                    logger.info("立即制作")
                else:
                    for key,value in res_dict.items():
                        res_list=value["scope"]
                        if len(res_list) == self.node_counter:  # 说明材料不够,退出
                            logger.info("材料不够,退出")
                            self.node_counter = 99  # 说明没有需要进阶的装备
                        for res in res_list:
                            if self.last_points !=[res[0],res[1]]:
                                self.mouse_left_click(res[0]+74,res[1]+3,delay_time=1)
                                self.mouse_move(648,453)
                                self.last_points=[res[0],res[1]]
                                self.node_counter += 1  # 计数器加一
                                break
            else:
                logger.info("没有找到需要进阶的装备")
                self.node_counter+=99 #说明没有需要进阶的装备

        elif self.interface_info in ["角色信息界面","主界面"]:#说明可能误操作
            logger.info(f"{self.interface_info}")
            self.node_current="task_打开装备进阶界面"
            return "task_finish"

    def task_装备进阶完成(self):
        self.node_current = "task_装备进阶完成"

        if "主界面" in self.interface_info:
            self.ls_progress = "task_finish"
            return "task_finish"
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_打开装备进阶界面": self.task_打开装备进阶界面,
            "task_装备进阶": self.task_装备进阶,
            "task_装备进阶完成": self.task_装备进阶完成,
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
            self.task_打开装备进阶界面()
        elif self.handle_task():
            pass


equip_upgrade_data={
    "word": {
        "确": {
            "scope": ( 612,426,707,478),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "unique": True,
            "enable": True,
        },
        "进阶":{
            "scope": (792, 344, 925, 416),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "enable":True,
            "unique": True,
        },
        "立即制作": {
            "scope": (786, 438, 892, 476,),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "unique": True,
            "enable": True,
        },
        "确定":{
            "scope": (615, 433, 705, 474),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "enable":True,
            "unique": True,
        },
    },

    "image": {
        r"resource/images_info/other/升级标志.bmp":{
            "scope":(420, 210, 583, 588),
            "con":0.8,
            "model":1,
            "enable":True,
            "unique": True,
        },#奖励图标
    },
}

