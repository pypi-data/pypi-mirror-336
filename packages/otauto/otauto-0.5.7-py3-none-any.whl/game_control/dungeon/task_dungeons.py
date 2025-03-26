import numpy as np
from PIL import Image

from otauto.a_star_v1 import PathFinder
from otauto.coordinate_converter import CoordinateConverter
from otauto.image_traits import ImageTraits
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import  dungeons_exit_dict, city_name,dungeons_node_dict



class TaskDungeons(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle,dungeons_name):
        super().__init__(vnc,vnc_port,queue_handle)
        self.node_flag = False #节点标识符
        self.moving_flag = False #移动模块标识符
        self.coordinate_node= None #节点坐标
        self.dungeons_name= dungeons_name # 副本名称
        self.ini_dungeons_dict = self.ini_handler.get_section_items(self.dungeons_name)  # 获取ini数据
        self.map_path= self.ini_dungeons_dict["map_path"] # 地图路径
        self.goal_list=dungeons_node_dict[f"{self.dungeons_name}"] # 节点列表
        self.target_colors_hex =self.ini_dungeons_dict["target_colors_hex"].split(",")   # 允许通行的颜色
        self.route_color = self.ini_dungeons_dict["route_color"].split(",")  # 惩罚值最低的颜色
        image2 = Image.open(self.map_path) # 读取图像
        self.image2_array = np.array(image2) # 将PIL图像转换为NumPy数组
        self.path_finder = PathFinder() # 创建一个PathFinder对象
        self.imagetraits = ImageTraits()  # 只使用 SIFT
        self.converter = CoordinateConverter(self.map_path) # 创建一个CoordinateConverter对象
        self.node_flag=False # 节点标识
        self.moving_flag=False # 移动标识
        self.exit_list=dungeons_exit_dict # 副本出口列表
        self.goal = (-1, -1) # 当前目标点
        self.goal_finish_list=[] # 已完成的节点列表
        self.target_point = None #目标点,和识别出来的起点最接近的节点
        self.goal_list_subscript=0 # 节点列表的下标
        self.boss_counter = 0 # boss计数器,避免未识别出来直接退出
        self.attack_range_num = 0 # 锁定次数


    def task_刷怪(self):
        logger.error("刷怪中")
        self.node_counter=0 #节点计数器初始化
        self.task_skill_attack() #刷怪

    def leave_dungeon(self):
        if self.find_data_from_keys_list_click(["离开"],self.word_handle_data,delay_time=10):
            logger.info("退出副本")

        elif self.boss_counter>=3: # boss计数器大于5,退出副本 (373, 74)
            logger.error("boss计数器大于3,退出副本")
            self.moving(dungeons_exit_dict[f"{self.dungeons_name}"]) # 移动

        elif self.find_data_from_keys_list_click([f"{self.dungeons_name}"],self.word_handle_data,delay_time=3):
            logger.error("副本已经刷完,退出副本")
            self.moving(dungeons_exit_dict[f"{self.dungeons_name}"]) # 移动

    def finish__dungeon(self):
        if self.find_data_from_keys_list_click(["物品","奖励"], self.word_handle_data, delay_time=2):
            logger.info("已领取奖励")

        if self.find_data_from_keys_list_click(["明日再来"], self.word_handle_data, delay_time=2):
            logger.info("该副本今天已经全部挑战完成")
            self.ls_progress = "task_finish"  # 模块运行结束
            return "task_finish"

        elif self.find_data_from_keys_list_click(["确定"], self.word_handle_data,delay_time=2):
            logger.info("已退出副本,回到城池")
            self.ls_progress="task_finish" #模块运行结束
            return "task_finish"

        elif self.map_name in city_name: # 如果在城池,退出副本
            logger.error("到了城池,退出副本")
            self.ls_progress = "task_finish"  # 模块运行结束
            return "task_finish"

    def equip_disassembly(self):
        """
        装备分解
        """
        pass

    def moving(self,node_list:list):
        """
         移动模块
         :node_list :节点列表
        """
        self.goal_list=node_list # 节点列表
        # 1应用特征比对方式获取坐标
        x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1的裁剪区域,不能更改
        image1_cropped = self.data_numpy[y1:y2, x1:x2]  # 裁剪
        imagetraits = ImageTraits()  # 只使用 SIFT
        traits_dict = imagetraits.draw_matches(image1_cropped, self.image2_array)  # 绘制匹配结果
        logger.error(f"当前位置:{traits_dict}")
        # 任务位置: {'num_inliers': 24, 'matches': 24, 'con': 1.0, 'role_position': (80, 334)}

        # 2根据起点和终点进行路径规划
        # 设置图像路径、起点、终点、目标颜色和路线颜色
        if traits_dict is not None and traits_dict["role_position"] != (-1, -1):
            start = traits_dict["role_position"]
            # goal = (94, 327)
            self.target_point = self.find_closest_and_remaining(self.goal_list, traits_dict["role_position"])
            self.goal = self.target_point[self.goal_list_subscript]

            logger.error(f"当前位置:{start},目标位置:{self.goal}")

            # 3根据坐标值进行路径规划
            # 检查 x 和 y 坐标的差是否都小于等于 2
            if abs(start[0] - self.goal[0]) <= 2 and abs(start[1] - self.goal[1]) <= 2:
                # 满足条件的代码块
                logger.success(f"当前位置:{start}在终点附近,切换成下一个节点")
                self.goal_finish_list.append(self.goal)  # 添加到已完成节点列表
                # 判断是否到了最后一个节点
                if len(self.target_point) == 1:
                    logger.error("到了最后一个节点,任务完成")
                    self.moving_flag = True
                else:
                    self.goal_list_subscript = 1
            else:
                # 4 进行路径规划,A星算法
                res_list = self.path_finder.find_path(self.map_path, start, self.goal, self.target_colors_hex,
                                                      self.route_color)
                """
                [(80, 335), (80, 334), (80, 333), (81, 333), (82, 333), (83, 333), (84, 333), (85, 333), (86, 333), (87, 333),
                (88, 333), (88, 332), (89, 332), (89, 331), (90, 331), (90, 330), (91, 330), (91, 329), (91, 328), (92, 328),
                (93, 328), (93, 327), (94, 327)]
                """
                logger.error(f"A星算法规划结果:{res_list}")
                # 输出结果
                if res_list:
                    # 每隔2个取1个
                    filtered_list = res_list[::3]
                    converted_points = self.converter.process_points(filtered_list)
                    logger.error(f"转换后的场景点击坐标列表：{converted_points}")
                    # [(810, 405), (720, 315), (855, 450), (855, 450), (810, 405), (810, 405), (765, 360), (810, 405)]
                    if converted_points:
                        for point in converted_points:
                            self.mouse_right_click(point[0], point[1], delay_time=0.4)
                        self.node_counter = 0  # 重置计数器
                        self.goal_list_subscript = 0  # 重置节点索引值
                        logger.error("已到达节点")  # todo:接上刷挂操作
                        self.key_press("tab")  # 切换到目标
                        # self.moving_flag = True # 移动标识
                        return True

    def task_on_hook(self):
        """
        挂机模块
        """
        logger.error("挂机模块")
        logger.error(f"节点信息:{self.goal_list}")
        logger.error(f"终点信息:{self.exit_list}")

        if self.finish__dungeon(): # 完成副本
            return "task_finish"
        else:
            self.leave_dungeon() # 退出副本

            if not self.node_flag:
                if self.target_info and self.target_info['name'] in ["铁枪", "歪嘴军师"]:
                    logger.error("目标锁定")
                    self.node_flag = True
                    self.node_counter=0 # 节点计数器初始化
                    self.attack_range_num=0 # 锁定次数初始化
                    return True
                elif self.target_info['lock']:
                    self.task_刷怪()
                    self.node_counter = 0  # 节点计数器初始化
                    self.attack_range_num = 0 # 锁定次数初始化
                    return True

                elif self.attack_range_num>3 and self.target_info["attack_range"]: #没有目标在攻击范围内,移动到目标节点
                    self.moving(self.goal_list)
                    self.attack_range_num = 0 # 锁定次数初始化
                    return True

                elif self.attack_range_num<=3 and self.target_info["attack_range"]:# 目标在攻击范围内,锁定目标次数少于3
                    self.key_press("tab")  # 切换到目标
                    self.node_counter = 0  # 节点计数器初始化
                    self.attack_range_num+=1 # 锁定次数加1
                    return True

            if self.node_counter>=10:
                logger.warning("寻路失败,点击小地图")
                self.mouse_right_click(1367, 112) #盲点击小地图

            elif self.node_counter>=5: #todo:说明a星寻路失败,启动节点寻路的方式

                if not self.target_info["driftlessness"] and not self.target_info["attack_range"]:  # 目标不在攻击范围内
                    if self.mutil_colors_data:
                        for key, value_data in self.mutil_colors_data.items():
                            if key in ["目标体_地图红点"]:
                                res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                                self.mouse_right_click(*res_tuple, delay_time=3)
                                return True
                elif self.target_info["driftlessness"]:
                    logger.error("无红点,特殊处理")

            if self.moving_flag and self.target_info["driftlessness"]:
                logger.error("到了终点附近,退去副本")
                self.boss_counter += 1  # 遇到boss次数


            if not self.moving_flag and self.goal_list: # 移动标识为False且节点列表不为空
                logger.error("移动模块")
                self.moving(self.goal_list) # 移动

            elif self.node_flag:
                logger.error("判断是否白名怪")
                self.node_flag = False
                if self.find_data_from_keys_list_click(["resource/images_info/main_task/收服标志.bmp"], self.image_data,
                                                       x3=20, y3=20, delay_time=15):
                    logger.warning("找到白名怪,收服中")
                    self.node_counter = 0  # 重置计数器
                    return True

                elif self.task_刷怪():
                    self.node_counter=0 # 重置计数器
                    return True
            self.node_counter += 1

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

        self.task_on_hook()


dungeons_data={
    "word": {
        "屠狼洞": {
            "scope": (517, 370, 810, 416),
            "con": 0.8,
            "offset": (183,71),
            "use": "每日签到",
            "unique": True,
            "enable": True,
        },
        "确定":{
            "scope": (647, 428, 760, 485),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "unique": True,
            "enable": True,
        },
        "明日再来": {
            "scope": (745, 368, 901, 405),
            "con": 0.8,
            "offset": (-47, 70),
            "use": "成长奖励",
            "unique": True,
            "enable": True,
        },
        "离开": {
            "scope": (558,587,633,618),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "enable": True,
        },
        "物品": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (185, 74),
            "use": "成长奖励",
            "unique": True,
            "enable": True,
        },
        "奖励": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "enable": True,
        },
    },
    "image": {
        r"resource/images_info/main_task/收服标志.bmp":{
            "scope":(659, 444, 772, 546),
            "con":0.8,
            "enable":True,
            "unique": True,
        },#奖励图标
    },
}

