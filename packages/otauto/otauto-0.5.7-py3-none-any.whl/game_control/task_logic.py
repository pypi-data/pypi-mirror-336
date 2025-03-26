import math
import random
import re
import time
from datetime import datetime
from otauto.docker_fdv1 import SyncGRPCTritonRunner
import numpy as np

import yaml
from fuzzywuzzy import process
from loguru import logger

from otauto.clent_ppocr import OCRClient
from otauto.image_matcher import ImageMatcher
from otauto.ini_file_operationv2 import INIFileHandler  # ini文件操作对象
from otauto.mongodb_v2 import MongoDBHandler
from otauto.myemailv2 import EmailHandler # 邮件发送对象
from otauto.redis_main import RedisHashManager # redis操作对象
from otauto.coordinate_conversion import way_finding_node, coordinate_point_conversion
from resource.parameters_info.basic_parameter_info import gear_name_point_dict, \
    skill_快捷键_dict, state_points_dict, vnc_port_win_tille_dict  # vnc端口标题名对照表

from otauto.imagefinder_v4 import ImageFinder

"""
功能:任务流程模块
日期:2025-2-12 10:22:07
描述:
    1. Redis用于窗口之间的通讯,更新ui的实时信息
    2. MongoDB用于存储任务信息,角色信息,奖励领取
    3. INI用于存储任务配置信息
    4. VNC用于获取屏幕数据,进行任务流程
"""

class TaskLogic:
    """
    vnc: vnc对象
    vnc_port: vnc端口
    """
    def __init__(self,vnc,vnc_port,queue_handle):

        self.vnc = vnc # vnc对象
        self.latest_result = {}  # 线程处理结果
        self.vnc_port = vnc_port # vnc端口
        self.queue_handle = queue_handle # 队列对象
        self.role_name = None #角色名
        self.role_name_data = None # 角色名数据
        self.role_hp = None #角色血量
        self.role_mp = None #角色蓝量
        self.role_rp = None #角色红量
        self.role_level = None #角色等级
        self.role_gang = None  # 角色帮派
        self.bound_currency = None # 角色绑定货币
        self.unbound_currency = None # 角色未绑定货币
        self.role_running = None #角色是否在移动
        self.role_swap_gear = None #角色是否在换装
        self.role_combating = None #角色是否在战斗
        self.role_factions= None    #角色阵营
        self.role_scoring="-1" #角色评分
        self.role_loading = None #画面是否在加载
        self.role_healing_resurgence = None #角色是否在复活
        self.target_info = None #目标信息
        self.map_name = None #地图名称
        self.map_position = None #地图位置
        self.task_info = None #任务信息
        self.gear_info_data = None # 装备信息
        self.pet_info_data = None # 宠物信息
        self.summons_info = None # 召唤物信息
        self.summons_info_data = None # 召唤物信息
        self.interface_info = None #界面信息
        self.data_numpy = None # numpy数据
        self.update_time_data = None # 数据更新时间
        self.diff_time = 0 # 数据更新时间差
        self.redis_dict = {}  # Redis信息字典

        self.word_acquire_data={} # 词条信息
        self.word_handle_data={} # 词条处理信息
        self.color_acquire_data={} # 颜色信息
        self.color_handle_data= {} # 颜色处理信息
        self.image_data={} # 图片信息
        self.yolo_data={} # yolo信息
        self.mutil_colors_data ={} # 多颜色信息
        self.unique_data = {} # 特有信息

        self.redis_handler=RedisHashManager() #redis操作对象
        self.ini_handler=INIFileHandler() #ini操作对象
        self.image_finder = ImageFinder()  # 创建 ImageFinder 实例
        self.image_matcher = ImageMatcher() # 创建 ImageMatcher 实例
        self.mongodb_handler=MongoDBHandler() # mongodb操作对象
        self.email_handler=EmailHandler() # 邮件操作对象
        self.ocrclient_handler = OCRClient()  # ocr操作对象
        # self.colored_logger = ColoredLogger() # 创建 ColoredLogger 对象

        self.date=self.get_current_date() # 获取当前日期
        self.last_email_time = 0  # 初始化上次发送邮件的时间

        self.task_name=self.__class__.__name__ # 获取任务名称

        self.ini_data_dict = self.ini_handler.get_section_items(vnc_port_win_tille_dict[self.vnc_port]) # 获取ini数据
        """
        {'vnc_ip': '192.168.110.245',
        'vnc_port': '5901',
        'vnc_window': '001',
        "facility_num":"001"
        'role_name': '多情温暖,无双战士,未知,未知',
        'role_sect': '少林',
        'role_id': '448681260,448761260,002,003',
        'team_duty': '1',
        'team_designation': '1',
        'team_member': '002,003,004,005'
        }
        """
        self.team_designation=self.ini_data_dict ["team_designation"] # 获取队伍番号
        self.team_duty = self.ini_data_dict["team_duty"] # 获取队伍职责
        self.role_name_str = self.ini_data_dict .get("role_name")  # 获取角色名称
        self.role_sect=self.ini_data_dict .get("role_sect") # 获取角色门派
        #多情温暖,无双战士,未知,未知
        self.redis_key = f"team:{self.team_designation}:{self.team_duty}:{self.vnc_port}"  # redis哈希值:team:1:1:5901
        self.redis_value= {
            "task_name":self.task_name, # 任务名称
            "task_message":"none", # 任务信息
            "health_degree":"-1", # 生命值
            "role_name": self.role_name, # 角色名称
            "real_time_position":"none,-1,-1", # 实时位置
            "team_status":"-1", # 队伍状态
            "schedule": "-1", # 进度器
            "interactor": " -1", # 交互器
            "updated_at": -1, # 更新时间
        }
        self.previous_collection_team = {}  # 用于跟踪上一个状态
        self.role_id=None # mongodb查询条件,设计为role_id
        self.mongodb_query={} # mongodb查询条件,设计为role_id

        self.update_time_handling=-1 #操作更新时间
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,task_get,task_running
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器

        self.update_arg_flag=False # 更新参数标识
        self.update_role_info_flag=False # 更新角色标识
        self.update_role_gear_flag=False # 更新角色装备标识
        self.update_role_pet_flag = False   # 更新角色宠物标识
        self.update_role_summons_flag = False   # 更新角色召唤物标识
        self.update_role_summons_flag = False   # 更新角色召唤物标识
        self.update_role_basic_info_flag = False # 更新角色基础信息标识

        self.role_gear_dict={"武器": [-1, -1],# (进阶等级,强化等级)
                             "头盔": [-1, -1],# (进阶等级,强化等级)
                             "衣服": [-1, -1],# (进阶等级,强化等级)
                             "护手": [-1, -1],# (进阶等级,强化等级)
                             "腰带": [-1, -1],# (进阶等级,强化等级)
                             "鞋子": [-1, -1],# (进阶等级,强化等级)
                             "项链": [-1, -1],# (进阶等级,强化等级)
                             "玉佩": [-1, -1],# (进阶等级,强化等级)
                             "戒指上": [-1, -1],# (进阶等级,强化等级)
                             "戒指下": [-1, -1],# (进阶等级,强化等级)
                             "护身符左": [-1, -1],# (进阶等级,强化等级)
                             "护身符右": [-1, -1],# (进阶等级,强化等级)
                            }

        self.gear_usage_count = 0 # 坐标计数器

        docker_container_list = ["ppocr-fastapi", "fd_yolo", "fd_ocr"]
        data_dict = self.ini_handler.get_multiple_sections_items(docker_container_list)
        logger.success(f"获取到的docker容器列表:{data_dict}")
        """
        {'ppocr-fastapi': {'ip': 'localhost', 'port': '5060'}, 
            'fd_yolo': {'ip': 'localhost', 'port': '8010'}, 
            'fd_ocr': {'ip': 'localhost', 'port': '8000'}
         }
        """
        self.ppocr_fastapi_ip = data_dict["ppocr-fastapi"]["ip"]
        self.ppocr_fastapi_port = data_dict["ppocr-fastapi"]["port"]
        self.fd_yolo_ip = data_dict["fd_yolo"]["ip"]
        self.fd_yolo_port = data_dict["fd_yolo"]["port"]
        self.fd_ocr_ip = data_dict["fd_ocr"]["ip"]
        self.fd_ocr_port = data_dict["fd_ocr"]["port"]
        self.category_name = self.yaml_label()  # yolo文件标签

        self.role_map_position = (1336, 149)  # 角色地图坐标
        self.skill_状态技能_last_time = 0 #记录上次释放状态技能的时间
        if self.role_sect in ["少林"]:
            self.skill_快捷键_dict=skill_快捷键_dict["少林"]
        elif self.role_sect in ["蜀山"]:
            self.skill_快捷键_dict=skill_快捷键_dict["蜀山"]
        elif self.role_sect in ["凌云","凌云寨"]:
            self.skill_快捷键_dict=skill_快捷键_dict["凌云"]
        elif self.role_sect in ["天煞"]:
            self.skill_快捷键_dict=skill_快捷键_dict["天煞"]

        self.skill_普通高频=self.skill_快捷键_dict["普通高频技能"]
        self.skill_普通延迟=self.skill_快捷键_dict["普通延迟技能"]
        self.skill_怒气技能=self.skill_快捷键_dict["怒气技能"]
        self.skill_状态技能=self.skill_快捷键_dict["状态技能"]
        self.skill_加血技能=self.skill_快捷键_dict["加血技能"]
        self.skill_召唤技能=self.skill_快捷键_dict["召唤技能"]
        self.coord = [0, 0]  # 坐标,用于寻路
        self.real_time_tuple_record = (0,0) #坐标记录,用于寻路
        self.real_time_coordinate_list=[] #实时坐标记录,用于寻路时候点击了未移动的情况处理

    def yaml_label(self, yaml_path: str = "config/label.yaml"):
        """
        查找指定目录及其子目录下所有的YAML文件（.yaml 或 .yml）
        :param yaml_path: 目录路径
        :return: None
        """
        # 加载yaml文件,读取标签
        if yaml_path:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                logger.success(f"yaml文件加载成功:{data['names']}")
                return data['names']
        else:
            logger.error("未找到yaml文件,请检查config/yolo_yaml是否存在yaml文件")
            return False

    def find_closest_point(self,a_ls, b):
        """
        找到列表中与给定点最近的点。
        参数：
        a_ls (list of tuples): 一个包含二维坐标点的列表，每个点表示为一个元组 (x, y)。
        b (tuple): 一个二维坐标点，表示为元组 (x, y)，我们要找出与这个点最近的点。

        返回：
        tuple: 列表中与点 b 最近的点，表示为元组 (x, y)。
        """
        closest_point = None
        min_distance = float('inf')  # 初始化为无穷大

        for point in a_ls:
            # 计算距离
            distance = math.sqrt((point[0] - b[0]) ** 2 + (point[1] - b[1]) ** 2)
            # 更新最近的点
            if distance < min_distance:
                min_distance = distance
                closest_point = point
        return closest_point

    def perform_mouse_action(self, action, points, x3, y3, delay_time):
        """
        执行指定的鼠标操作。

        :param action: 鼠标操作类型，1-左击，2-双击，3-右击，4-移动
        :param points: 点击坐标列表，包含X和Y坐标
        :param x3: 点击时的X坐标（可选）
        :param y3: 点击时的Y坐标（可选）
        :param delay_time: 点击延迟时间
        :return: 返回True，表示操作已执行
        """
        # 根据不同的操作类型执行相应的鼠标操作
        if action == 1:
            self.mouse_left_click(*points, x3=x3, y3=y3, delay_time=delay_time)  # 左击
        elif action == 2:
            self.mouse_double_left_click(*points, x3=x3, y3=y3, delay_time=delay_time)  # 双击
        elif action == 3:
            self.mouse_right_click(*points, x3=x3, y3=y3, delay_time=delay_time)  # 右击
        elif action == 4:
            self.mouse_move(*points)  # 移动鼠标到指定位置

        return True  # 操作执行完毕，返回True

    def find_closest_and_remaining(self,node_list, point):
        """
        找到与给定点最近的点，并返回该点及其后面的所有元素。
        A星寻路模块有关

        :param node_list: 包含节点坐标的列表
        :param point: 参考点，格式为 (x, y)
        :return: 包含最近点及其后面元素的列表
        """

        def euclidean_distance(p1, p2):
            """计算两个点之间的欧几里得距离。"""
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        # 初始化最小距离和最近的点索引
        min_distance = float('inf')
        closest_index = -1

        # 遍历节点列表，计算每个点到给定点的距离
        for index, node in enumerate(node_list):
            distance = euclidean_distance(node, point)
            if distance < min_distance:
                min_distance = distance
                closest_index = index

        # 使用切片保留最近的点及其后面的所有元素
        return node_list[closest_index:]


    def mouse_move(self, x, y, delay_time=0.1):
        """
        移动鼠标到指定位置
        :param x: x坐标
        :param y: y坐标
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_move(x, y)
        time.sleep(delay_time)

    def mouse_left_click(self, x, y, x3: int = 0, y3: int = 0, delay_time=0.1):  # 鼠标左键点击
        """
        鼠标左键点击
        :param x: x坐标
        :param y: y坐标
        :param x3: x坐标偏移量
        :param y3: y坐标偏移量
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_left_click(x, y, x3, y3,delay_time)

    def mouse_double_left_click(self, x, y, x3: int = 0, y3: int = 0, delay_time=0.1):
        """
        鼠标左键双击
        :param x: x坐标
        :param y: y坐标
        :param x3: x坐标偏移量
        :param y3: y坐标偏移量
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_double_left_click(x, y, x3, y3,delay_time)

    def mouse_right_click(self, x, y, x3: int = 0, y3: int = 0, delay_time=0.1):  # 鼠标右键点击
        """
        鼠标右键点击
        :param x: x坐标
        :param y: y坐标
        :param x3: x坐标偏移量
        :param y3: y坐标偏移量
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_right_click(x, y, x3, y3,delay_time)

    def mouse_drag(self, x1, y1, x2, y2, step: int = 20):
        """
        鼠标拖拽
        :param x1: 起始x坐标
        :param y1: 起始y坐标
        :param x2: 结束x坐标
        :param y2: 结束y坐标
        :param step: 拖拽步长
        """
        self.vnc.mouse_drag(x1, y1, x2, y2, step)

    def mouse_up(self, button, delay_time=0.1):
        """
        鼠标释放
        :param button: 鼠标按键 1左键 3 右键
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_up(button)
        time.sleep(delay_time)

    def mouse_down(self, button, delay_time=0.1):
        """
        鼠标按下
        :param button: 鼠标按键 1左键 3 右键
        :param delay_time: 延迟时间
        """
        self.vnc.mouse_down(button)
        time.sleep(delay_time)

    def key_press(self, key, delay_time=0.1):  # 按键
        """
        按下键盘键
        :param key: 键值
        :param delay_time: 延迟时间
        """
        self.vnc.key_press(key, delay_time)

    def key_down(self, key, delay_time=0.1):  # 按键
        """
        按下键盘键
        :param key: 键值
        :param delay_time: 延迟时间
        """
        self.vnc.key_down(key, delay_time)

    def key_up(self, key, delay_time=0.1):  # 按键
        """
        按下键盘键
        :param key: 键值
        :param delay_time: 延迟时间
        """
        self.vnc.key_up(key, delay_time)

    def text_input(self,text,delay_time=0.1):
        """
        文本输入,只支持字母和数字输入
        :param text: 文本内容
        :param delay_time: 延迟时间
        :return:
        """
        result_list=list(text) # 将字符串转换为列表
        for text in result_list:
            self.key_press(text,delay_time)

    def set_gear_entry(self,dict_a: dict):
        """
        根据字典中的键值对,设置 gear_装备的值
        :param dict_a: 字典，键为字符串，值为元组
        :return: [3,2] # 假设初始值为 [0, 0]
        """
        res = [0, 0]
        # 遍历字典中的每一个键
        for key in dict_a.keys():
            # 检查是否包含 "阶" 关键字
            if "阶" in key:
                # 提取数字
                match = re.search(r'(\d+)', key)
                if match:
                    res[0] = int(match.group(1))  # 将阶数录入到 self.gear_武器[0]
            else:
                # 使用正则表达式提取 + 后的数字
                match = re.search(r'\+(\d)', key)
                if match:
                    plus_number = int(match.group(1))
                    if 1 <= plus_number <= 8:
                        res[-1] = plus_number  # 将 +1 到 +8 的数字录入到 self.gear_武器[-1]
        return res

    def set_correct_term(self,input_word,correct_words ,threshold=70):
        """
        使用模糊匹配找到最相似的词
        :param input_word: 输入的词
        :param correct_words: 正确的词列表
        :param threshold: 相似度阈值
        :return: 纠正后的词
        """
        try:
            result = process.extractOne(input_word, correct_words)
            # 若相似度超过阈值则返回纠正后的词，否则返回原词
            logger.success(f"set_correct_term result: {result}")
            return result[0] if result[1] > threshold else input_word
        except Exception as e:
            logger.error(f"set_correct_term error: {e}")

    def get_current_date(self):
        # 获取当前日期和时间
        now = datetime.now()
        # 提取年、月、日
        year = now.year
        month = now.month
        day = now.day
        return f"{year}/{month}/{day}"

    def find_word_scope(self,x1, y1, x2, y2,model:int=1):
        """
        局域文字识别,可以选用去除背景色的功能
        :param x1: 截图区域左上角x坐标
        :param y1: 截图区域左上角y坐标
        :param x2: 截图区域右下角x坐标
        :param y2: 截图区域右下角y坐标
        :param model:ocr模型选择
        :return [('无双战士', 222, 59, 0.894), ('雇佣剑客', 72, 73, 0.983)]
        """
        res_texts=[] # 识别结果
        # 区域截图
        clipped_arr = self.data_numpy[y1:y2, x1:x2]
        # clipped_arr = self.capture_region_as_numpy(x1, y1, x2, y2)

        if model == 1 :
            # 直接调用 ppocr_detect 处理裁剪区域
            res_dict = self.ocrclient_handler.run(clipped_arr, url_ip=self.ppocr_fastapi_ip, url_port=self.ppocr_fastapi_port)  # 使用裁剪的区域进行高精度识别
            # logger.success(f"高精度模型识别结果:{res_dict}")
            if res_dict:
                # 使用列表推导式优化代码
                res_texts = [(key, int(value[0]+x1), int(value[1]+y1), round(value[4], 3)) for key, values in res_dict.items() for value in values]

        # 处理 model == 0 的图像
        if np.any(clipped_arr) and model == 0:  # 检查 combined_image_model_0 是否有内容
            model_name = "pp_ocr"
            model_version = "1"
            url = self.fd_ocr_ip + f":{self.fd_ocr_port}"
            runner = SyncGRPCTritonRunner(url, model_name, model_version)

            # 裁剪过的图片识别
            im = np.array([clipped_arr, ])
            result = runner.Run([im, ])
            batch_texts = result['rec_texts']
            batch_scores = result['rec_scores']
            batch_bboxes = result['det_bboxes']

            for i_batch in range(len(batch_texts)):
                texts = batch_texts[i_batch]
                scores = batch_scores[i_batch]
                bboxes = batch_bboxes[i_batch]
                for i_box in range(len(texts)):
                    # 将坐标点列表拆分为x和y坐标的列表
                    x_coords = bboxes[i_box][::2]  # 每隔一个元素取一个,即所有x坐标
                    y_coords = bboxes[i_box][1::2]  # 从第一个y坐标开始,每隔一个元素取一个
                    x_min = int(min(x_coords))
                    y_min = int(min(y_coords))
                    text = (texts[i_box].decode('utf-8'), int(x_min+x1), int(y_min+y1), float(round(scores[i_box], 3)))
                    res_texts.append(text)
            # logger.info(f"模型0识别结果:{res_texts}")
        return res_texts

    def find_image_scope(self,image_path,x1,y1,x2,y2,con:float=0.8,model:int=0):
        """
        局域图片识别,可以选用去除背景色的功能
        :param image_path: 图片路径
        :param x1: 截图区域左上角x坐标
        :param y1: 截图区域左上角y坐标
        :param x2: 截图区域右下角x坐标
        :param y2: 截图区域右下角y坐标
        :param con: 置信度
        :param model:模型选择
        :return
        """
        sub_images_dict={} # 小图字典
        sub_images_dict_ac={}
        try:
            # 使用切片裁剪数组
            if self.data_numpy.any():
                if model == 0 : # 如果模型类型为0且启用状态为True
                    sub_images_dict.update({image_path:(x1, y1, x2, y2, con)})

                    # 查找小图在大图中的位置
                    results = self.image_finder.find(self.data_numpy, sub_images_dict)
                    # logger.success(f"图片识别结果:{sub_images_dict},{results}")
                    return results
                if model == 1 : # 如果模型类型为1且启用状态为True
                    sub_images_dict_ac.update({image_path:(x1, y1, x2, y2, con)})
                    results_ac=self.image_matcher.match_sub_images(self.data_numpy, sub_images_dict_ac)
                    # logger.success(f"图片识别结果:{results_ac},{results_ac}")
                    return results_ac
            return {}
        except Exception as e:
            logger.error(f"find_image_scope函数出错:{e}")
            return {}


    def find_word_from_acquire_num(self,key_num):
        """
        找出文字资源中,指定识别范围的所有结果
        :param key_num: 识别范围的标志:1~999的数字
        :return: 包含所有匹配项的字典或者{}
        """
        # 使用字典推导式提取最后一个元素为key_num的键值对
        word_data= {key: value for key, value in self.word_acquire_data.items() if value[-1] == key_num}
        if word_data:
            return word_data
        else:
            return {}

    def find_data_from_keys_list(self, key_text_list: list, dict_name) -> dict:
        """
        self.image_data,self.word_handle_data
        self.word_acquire_data,self.word_acquire_data
        self.color_acquire_data,self.color_handle_data
        self.mutil_colors_data,self.yolo_data
        :param key_text_list: 要在字典中查找的键文本列表
        :param dict_name: 要查找的字典名称,
        :return: 包含所有匹配项的字典
        """
        def find_items_in_dict(dictionary):
            items = {}
            if dictionary:
                for key, value in dictionary.items():
                    for key_text in key_text_list:
                        if key_text in key:
                            items[key] = value
            return items if items else None

        result = find_items_in_dict(dict_name)

        if not result and self.mutil_colors_data and dict_name != self.mutil_colors_data :
            result = find_items_in_dict(self.mutil_colors_data)
        return result

    def find_data_from_keys_list_click(self, key_text_list: list, dict_name, x3: int = 0, y3: int = 0, delay_time=0.1,
                                       action: int = 1,random_pro:bool=False):
        """
        只点击找到的第一个的位置
        self.image_data,self.word_handle_data
        self.word_acquire_data,self.word_acquire_data
        self.color_acquire_data,self.color_handle_data
        self.mutil_colors_data,self.yolo_data
        :param key_text_list: 要在字典中查找的键文本列表
        :param dict_name: 要查找的字典名称,
        :param x3: x3坐标
        :param y3: y3坐标
        :param delay_time: 延迟时间
        :param action: 1:鼠标左点击 2:鼠标左双点击 3: 鼠标右点击 4:鼠标移动
        :param random_pro bool
        :return: True or False
        """
        res = self.find_data_from_keys_list(key_text_list, dict_name)
        details_res=None # 默认为None
        if res:
            logger.success(f"find_data_from_keys_list_click result: {res}")
            if len(res)>=2 and random_pro: #随机选择一个
                num=random.randint(0,len(res)-1)
                details_res = res.get(key_text_list[num])
            else:
                for key_text in key_text_list:
                    if key_text in res:
                        details_res = res.get(key_text)

                logger.success(f"find_data_from_keys_list_click details_res: {details_res}")

            # 检查 details_res 的类型
            #{'65%': (720, 645, 0.999)}
            if isinstance(details_res, dict) and 'scope' in details_res:
                points_list = details_res['scope']

                # 确保 points_list 非空并且是一个列表
                if points_list and isinstance(points_list, list) and len(points_list) > 0:
                    points = (points_list[0][0], points_list[0][1])
                else:
                    logger.error("points_list is empty or not a list.")
                    return False
            elif isinstance(details_res, tuple) and len(details_res) == 3:
                # 直接从元组中提取坐标
                points = (details_res[0], details_res[1])
            else:
                return False

            # 进行鼠标操作
            if action == 1:
                self.mouse_left_click(*points, x3=x3, y3=y3, delay_time=delay_time)
                return True
            elif action == 2:
                self.mouse_double_left_click(*points, x3=x3, y3=y3, delay_time=delay_time)
                return True
            elif action == 3:
                self.mouse_right_click(*points, x3=x3, y3=y3, delay_time=delay_time)
                return True
            elif action == 4:
                self.mouse_move(*points)
                return True
        else:
            pass

        return False


    def find_data_from_all_keys_list(self, key_text_list, dict_name):
        """
        根据提供的部分键名从指定的字典中查找对应的值。全部匹配即返回 True 而不执行点击操作。
        :param key_text_list: 字典里key的关键列表
        :param dict_name: 字典，注意格式
        :return: True or False
        """
        # 获取匹配的结果字典
        result_dict = self.find_data_from_keys_list(key_text_list, dict_name)

        # 判断是否全部匹配成功
        if result_dict and len(result_dict) >= len(key_text_list):
            for key in key_text_list:
                # 检查 key 是否在结果字典的键中
                if not any(key in k for k in result_dict.keys()):
                    return False
            # 如果都匹配成功，返回 True
            return True
        # 如果有任何一个键未匹配成功，返回 False
        return False

    def queue_message(self, message: dict):
        """
        self.queue_message({"image": {'resource/images_info/camp_task/唐军图腾.bmp': {"enable": False}}}) # 参数关闭

        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        注意格式为:
        {"word": {"标签": {"enable": False}},
         "image": {"图片路径": {"enable": False}},
         "mutil_colors": {"文字": {"enable": False}}
         }
         主要是更新参数中,是否只使用一次,避免没必要的计算
        :param message: 字典,格式如上 {"image": {'resource/images_info/camp_task/唐军图腾.bmp': {"enable": False}}}
        """
        self.queue_handle.put(message)
        logger.error(f"线程队列信息更新{message}")

    def redis_find_team_info(self,team_key):
        """
        查询队伍信息
        :param team_key:  team:1:1:5901
        """
        return self.redis_handler.get_hash(team_key)

    def redis_find_team_designation_and_number(self,team_designation,team_duty):
        """
        查询队伍番号和职责都符合的文档
        :param team_designation:  队伍番号
        :param team_duty:  队伍职责
        :return:
        """
        keys = self.redis_handler.scan_keys(f'team:{team_designation}:{team_duty}:*')
        # logger.info(f"keys:{keys}")
        res_dict=self.redis_find_team_info(keys[0])
        logger.info(f"redis_find_team_designation_and_number:{res_dict}")
        return res_dict

    def redis_update_info(self,task_message: str=None, team_status: str =" -1", schedule: str = "-1", interactor: str = "-1"):
        """
        更新队伍信息，并在有变化时推送到数据库。
        :param task_message: 任务信息
        :param team_status: 组队状态, 默认值:-1 未组队:0 已组队:1 等待组队:2
        :param schedule: 进度器, 默认值:-1,"tld","fms","csg"
        :param interactor: 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4
        """
        real_time_position = "none,-1,-1" # 默认值,实时位置
        role_hp = "-1" # 默认值,角色生命值

        if self.map_name !="none" and self.map_position !="-1,-1":  # 检查是否有实时位置
            real_time_position = f"{self.map_name}, {self.map_position}"

        if self.role_hp !="-1" :
            role_hp = self.role_hp

        # 更新 collection_team 字典
        self.redis_value["task_message"] = task_message
        self.redis_value["health_degree"] = role_hp
        self.redis_value["real_time_position"] = real_time_position
        self.redis_value["team_status"] = team_status
        self.redis_value["schedule"] = schedule
        self.redis_value["interactor"] = interactor
        self.redis_value["updated_at"] = int(time.time())

        # 只比较需要的字段
        current_team_info = {
            "task_message": self.redis_value["task_message"],
            "health_degree": self.redis_value["health_degree"],
            "real_time_position": self.redis_value["real_time_position"],
            "team_status": self.redis_value["team_status"],
            "schedule": self.redis_value["schedule"],
            "交互器": self.redis_value["interactor"],
        }

        changes = {}

        if self.previous_collection_team:
            previous_team_info = {
                "task_message": self.previous_collection_team["task_message"],
                "health_degree": self.previous_collection_team["health_degree"],
                "real_time_position": self.previous_collection_team["real_time_position"],
                "team_status": self.previous_collection_team["team_status"],
                "schedule": self.previous_collection_team["schedule"],
                "interactor": self.previous_collection_team["interactor"],
            }

            # 检查 collection_team 是否有变化
            for key in current_team_info:
                if current_team_info[key] != previous_team_info[key]:
                    changes[key] = current_team_info[key]

            if changes:
                logger.info(f"redis_value 更新:{changes}" )
                # 更新数据库时只发送变化的字段
                self.redis_handler.set_hash(self.redis_key, self.redis_value)
                # 更新上一个状态为当前状态
                self.previous_collection_team = self.redis_value.copy()
        else:
            # 如果是首次更新，直接更新数据库
            logger.info(f"redis_key:{self.redis_key}")
            logger.info(f"collection_team:{self.redis_value}" )

            self.redis_handler.set_hash(self.redis_key, self.redis_value)
            self.previous_collection_team = self.redis_value.copy()

    def mongodb_set_query(self):
        """
        查询mongodb数据的条件
        """

        role_name = self.ini_data_dict["role_name"] # 角色名称
        role_id= self.ini_data_dict["role_id"] # 角色id
        # 以 "," 分割字符串
        role_name_list = role_name.split(',')
        parole_id_list = role_id.split(',')

        position_role_name = role_name_list.index(self.role_name) # 查找 self.role_name 的位置
        mongodb_query=parole_id_list[position_role_name] # 获取角色id

        logger.success(f"角色名称:{self.role_name}")
        logger.success(f"ini信息:{self.ini_data_dict}")
        logger.success(f"mongodb_query:{mongodb_query}")

        return mongodb_query

    def mongodb_update_facility(self):
        """
        更新设备信息
        set_facility = {"vnc_port": None, # vnc端口
                       "vnc_ip": None, # vnc ip
                       "role_id": None, # 角色id
                       "role_name":None, # 角色名称
                       "facility_num":None, # 设备编号
                       "updated_at":None, # 更新时间
                       }
        """
        facility={
            "vnc_port": self.vnc_port, # vnc端口
            "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
            "role_id": self.role_id, # 角色id
            "role_name": self.role_name, # 角色名称
            "facility_num": self.ini_data_dict.get("facility_num"), # 设备编号
            "updated_at": int(time.time()), # 更新时间
        }
        if not self.mongodb_handler.update_check_recent("facility",time_window=86000): # 检查是否需要更新设备信息
            logger.success(f"更新设备信息:{facility}")
            self.mongodb_handler.update_document_one("facility",self.mongodb_query,facility)
        else:
            logger.success(f"设备信息无需更新")

    def mongodb_update_role(self):
        """
        更新角色信息
        set_role = {"vnc_port": None, # vnc端口
                   "vnc_ip": None,  # vnc ip
                   "role_id": None, # 角色id
                   "role_name":None, # 角色名称
                   "role_level": None, # 等级
                   "role_sect": None, # 角色门派
                   "role_factions": None, # 角色阵营
                   "role_gang" : None, # 角色帮派
                   "role_scoring":None, # 角色评分
                   "role_position":None, # 角色位置
                   "bound_currency":None, # 绑定的货币
                   "unbound_currency":None, # 未绑定的货币
                   "updated_at":None, # 更新
                   }
        """
        real_time_position = "none,-1,-1" # 默认值,实时位置
        if self.map_name !="none" and self.map_position !="-1,-1":  # 检查是否有实时位置
            real_time_position = f"{self.map_name}, {self.map_position}"


        role = {"vnc_port": self.vnc_port, # vnc端口
                "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
                "role_id": self.role_id, # 角色id
                "role_name": self.role_name, # 角色名称
                "role_level": self.role_level,  # 等级
                "role_sect": self.ini_data_dict.get("role_sect"),  # 角色门派
                "role_factions": self.role_factions,  # 角色阵营
                "role_gang": self.role_gang,  # 角色帮派
                "role_scoring": self.role_scoring,  # 角色评分
                "role_position": real_time_position,  # 角色位置
                "bound_currency": self.bound_currency,  # 绑定的货币
                "unbound_currency": self.unbound_currency,  # 未绑定的货币
                "updated_at": int(time.time()),  # 更新时间
        }

        if not self.mongodb_handler.update_check_recent("facility",time_window=3600): # 1小时更新1次
            logger.success(f"更新角色信息:{role}")
            self.mongodb_handler.update_document_one("facility",self.mongodb_query,role)
        else:
            logger.success(f"角色信息无需更新")

    def mongodb_update_task_current(self,task_current:str):
        """
        更新任务信息,注意task_finish是添加
        set_task = {"vnc_port": None, # vnc端口
                   "vnc_ip": None, # vnc ip
                   "role_id": None, # 角色id
                   "role_name":None, # 角色名称
                   "task_current": None,  # 当前任务
                   "task_finish": None, # 完成任务,是个列表
                   "date": None,  # 任务日期,用于每日初始化这个集合
                   "updated_at":None, # 更新
                   }
        :param task_current: 当前任务
        """
        task = {"vnc_port": self.vnc_port, # vnc端口
                "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
                "role_id": self.role_id, # 角色id
                "role_name": self.role_name, # 角色名称
                "task_current": task_current,  # 当前任务
                "date": self.date,  # 任务日期,用于每日初始化这个集合
                "updated_at":int(time.time()), # 更新
               }
        logger.success(f"更新当前任务信息:{task}")
        self.mongodb_handler.update_document_one("task",self.mongodb_query,task)

    def mongodb_update_task_finish(self, task_finish:str):
        """
        更新任务信息,注意task_finish是添加
        set_task = {"vnc_port": None, # vnc端口
        :param task_finish: 已完成的任务
        """
        task = {
               "task_finish": task_finish, # 完成任务,是个列表
               }
        logger.success(f"更新已完成任务信息:{task}")
        res_dict=self.mongodb_handler.find_document_one("task", self.mongodb_query)
        # logger.success(f"更新前数据:{res_dict}")
        task_finish_list=res_dict.get('task_finish',[])
        if task_finish not in task_finish_list:
            self.mongodb_handler.update_document_one("task", self.mongodb_query, task, operator="$push")

    def mongodb_update_exception(self, exception_num:int,email_enable:bool=False):
        """
        更新异常信息
        99: "win桌面" ,
        98: "登陆选择界面",
        97: "登陆账号密码界面",
        96: "服务器选择界面",
        95: "角色选择界面",

        self.mongodb_update_exception(99,True)

        :param exception_num: 异常代码:
        :param email_enable: 是否发送邮件
        """
        error_msg={
            99: "win桌面" ,
            98: "登陆选择界面",
            97: "登陆账号密码界面",
            96: "服务器选择界面",
            95: "角色选择界面",
                }
        exception_info=error_msg.get(exception_num,"未知异常")
        exception = {"vnc_port": self.vnc_port, # vnc端口
                    "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
                    "role_id": self.role_id, # 角色id
                    "role_name": self.role_name, # 角色名称
                    "exception_num": exception_num,  # 异常代码
                    "exception_info": exception_info,  # 异常信息
                    "updated_at": int(time.time()),  # 更新
                    }
        logger.success(f"异常信息:{exception}")
        self.mongodb_handler.update_document_one("exception",self.mongodb_query,exception)
        if email_enable:
            current_time = time.time()
            # 检查是否已经过去了一小时
            if current_time - self.last_email_time >= 3600:  # 3600秒 = 1小时
                logger.success(f"发送邮件信息")
                self.email_handler.send_email_qq(f"{exception_num}:{exception_info}", self.data_numpy)
                self.last_email_time = current_time  # 更新最后发送时间


    def mongodb_update_gear(self):
        """
        更新装备信息
        set_gear = {"vnc_port": None, # vnc端口
                        "vnc_ip": None, # vnc ip
                        "role_id": None, # 角色id
                        "role_name":None, # 角色名称
                        "武器": None, #(进阶等级,强化等级)
                        "头盔": None, #(进阶等级,强化等级)
                        "衣服": None, #(进阶等级,强化等级)
                        "护手":None,   #(进阶等级,强化等级)
                        "腰带":None,   #(进阶等级,强化等级)
                        "鞋子": None, #(进阶等级,强化等级)
                        "项链": None, #(进阶等级,强化等级)
                        "玉佩": None, #(进阶等级,强化等级)
                        "戒指上": None, #(进阶等级,强化等级)
                        "戒指下":None, #(进阶等级,强化等级)
                        "护身符左": None, #(进阶等级,强化等级)
                        "护身符右":None,   #(进阶等级,强化等级)
                        "秘籍": None, #(进阶等级,强化等级)
                        "updated_at":None, # 更新
                        }
        """
        gear ={"vnc_port": self.vnc_port, # vnc端口
                    "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
                    "role_id": self.role_id, # 角色id
                    "role_name": self.role_name, # 角色名称
                     "updated_at": int(time.time()),  # 更新
                     }
        gear.update(self.role_gear_dict) # 和装备信息合并
        logger.success(f"更新当前任务信息:{gear}")
        self.mongodb_handler.update_document_one("gear",self.mongodb_query,gear)

    def mongodb_update_pet(self,pet_name:list):
        """
        更新宠物信息
        set_pet = {"vnc_port": None, # vnc端口
                 "vnc_ip": None, # vnc ip
                 "role_id": None, # 角色id
                 "role_name":None, # 角色名称
                  "pet_name" : None, # 宠物名称
                 "updated_at":None, # 更新
                 }
        :param pet_name: 宠物名称
        """
        pet = {"vnc_port": self.vnc_port, # vnc端口
                    "vnc_ip": self.ini_data_dict.get("vnc_ip"), # vnc ip
                    "role_id": self.role_id, # 角色id
                    "role_name": self.role_name, # 角色名称
               "pet_name": pet_name,  # 宠物名称
               "updated_at": int(time.time()),  # 更新
               }

        logger.success(f"更新当前任务信息:{pet}")
        self.mongodb_handler.update_document_one("pet",self.mongodb_query,pet)

    def message_to_log(self, word_dict: dict, items_per_line: int = 5):
        """
        # 记录日志
        logger.success(f"dic_word_ocr:\n{formatted_dict}")
        将字典或列表转换为字符串,并按每行指定数量进行换行
        :param word_dict: 字典或列表
        :param items_per_line: 换行的键值对数目
        :return: 格式化后的字符串
        """
        if word_dict is None:
            return ""

        formatted_items = []

        if isinstance(word_dict, dict):
            # 获取字典的键值对列表
            items = list(word_dict.items())
            # 分割成每行指定数量的键值对
            for i in range(0, len(items), items_per_line):
                formatted_items.append(', '.join([f"{k}: {v}" for k, v in items[i:i + items_per_line]]))

        elif isinstance(word_dict, list):
            # 分割列表并格式化
            for i in range(0, len(word_dict), items_per_line):
                formatted_items.append(', '.join([str(item) for item in word_dict[i:i + items_per_line]]))

        # 将分割后的内容连接成多行字符串
        formatted_dict = '\n'.join(formatted_items)
        return formatted_dict

    def data_info(self):
        data_pool = self.latest_result["data_cleansing"]  # 获取数据池
        """
        role_info_dict: {'name': '无双战士', 'HP': '4219/4219', 'MP': '983/983', 'RP': '-1', 'level': '30','role_factions': 'none', 'running': False, 'swap_gear': False, 'combating': False, 'loading': False, 'healing_resurgence': False}, 
        target_info_dict: {'name': '雇佣剑客', 'lock': True, 'attack_range': True, 'driftlessness': False}, coordinate_info_dict: {'map_name': '青城山', 'map_position': '-1,-1'}
        task_info_dict: {'【主线】简单的人（2': (1187, 259, 0.984, 4), '完成：悬赏任务（未完成）': (1203, 273, 0.967, 4), '交付人：王捕快': (1203, 291, 0.996, 4), '【阵营】【后勤】捕获毒蜂': (1185, 307, 0.949, 4), '寻物：捕获的毒蜂（0/5)': (1203, 320, 0.909, 4), '【新手任务】玲珑的故事': (1186, 339, 0.99, 4), '完成：玲珑副本（未完成）': (1203, 355, 0.97, 4), '【新手任务】试炼场的试炼': (1186, 371, 0.988, 4), '完成：试炼场（未完成）设': (1202, 384, 0.952, 4), '【新手任务】金装的诱惑': (1184, 401, 0.994, 4), '找人：名匠(未完成)': (1202, 417, 0.956, 4), '悬赏】悬赏任务白屏寨': (1195, 435, 0.992, 4), '排行': (1384, 445, 0.999, 4), '失败）【删除任务】': (1182, 451, 0.948, 4), '打倒：疑犯(0/1)': (1201, 465, 0.998, 4), '好友活动': (1209, 502, 0.981, 4), '系统': (1346, 502, 1.0, 4), '家': (1392, 510, 0.999, 4), '召回提醒': (1211, 517, 0.972, 4), '消息': (1346, 517, 1.0, 4)}, 
        interface_info_dict: {'主界面': (-1, -1)}, 
        processed_data_word_acquire: {'10.54': (22, 32, 0.971, 8), '送': (76, 34, 0.085, 8), '无双战士': (142, 41, 0.999, 1), '无双战士_1': (142, 41, 0.999, 8), '青城山': (1308, 51, 0.999, 7), '4219/4219': (121, 68, 0.992, 1), '4219/4219_2': (121, 68, 0.992, 8), '983/983': (144, 81, 0.999, 1), '983/983_3': (144, 81, 0.999, 8), '雇佣剑客': (661, 72, 0.994, 2), '0/100': (123, 90, 0.988, 1), '0/100_4': (123, 90, 0.988, 8), '30': (43, 122, 0.981, 9), '182,': (1307, 207, 0.908, 3), '69': (1344, 207, 0.999, 3), '【主线】简单的人（': (1187, 259, 0.984, 4), '2': (1314, 260, 0.998, 4), '完成：悬赏任务（未完成）': (1203, 273, 0.967, 4), '交付人：': (1203, 291, 0.996, 4), '王捕快': (1261, 291, 0.996, 4), '【阵营】【后勤】捕获毒蜂': (1185, 307, 0.949, 4), '寻物：捕获的毒蜂（0/5)': (1203, 320, 0.909, 4), '【新手任务】玲珑的故事': (1186, 339, 0.99, 4), '完成：玲珑副本（未完成）': (1203, 355, 0.97, 4), '【新手任务】试炼场的试炼': (1186, 371, 0.988, 4), '完成：试炼场（未完成）': (1202, 386, 0.952, 4), '设': (1392, 384, 0.995, 4), '【新手任务】金装的诱惑': (1184, 401, 0.994, 4), '找人：名匠(未完成)': (1202, 417, 0.956, 4), '悬赏】悬赏任务': (1195, 435, 0.995, 4), '白屏寨': (1330, 435, 0.992, 4), '失败）【删除任务】': (1182, 451, 0.948, 4), '排行': (1384, 445, 0.999, 4), '打倒：': (1201, 465, 0.999, 4), '疑犯(0/1)': (1246, 466, 0.998, 4), '好友': (1209, 502, 0.981, 4), '活动': (1277, 502, 1.0, 4), '系统': (1346, 502, 1.0, 4), '召回': (1211, 517, 0.972, 4), '提醒': (1278, 517, 0.999, 4), '消息': (1346, 517, 1.0, 4), '家': (1392, 510, 0.999, 4)}
        processed_data_word_handle: {}, 
        processed_data_color_acquire: {1: {'scope': (440, 180), 'rgb': (81, 109, 77)}, 2: {'scope': (923, 305), 'rgb': (20, 108, 98)}, 3: {'scope': (565, 462), 'rgb': (19, 79, 51)}}, 
        processed_data_color_handle: {'a3352e': {'scope': (616, 99), 'rgb': (46, 53, 163)}}
        processed_data_image: {'resource/images_info/main_task/商城.bmp': {'scope': [(1206, 59, 1227, 82, 1.0)]}, 'resource/images_info/main_task/冒险.bmp': {'scope': [(1399, 607, 1416, 628, 0.816), (1399, 608, 1416, 629, 0.998), (1399, 609, 1416, 630, 0.825)]}, 'resource/images_info/main_task/帮会.bmp': {'scope': [(1295, 672, 1319, 693, 0.998)]}, 'resource/images_info/main_task/角色.bmp': {'scope': [(838, 673, 854, 690, 0.999)]}, 'resource/images_info/main_task/技能.bmp': {'scope': [(889, 671, 904, 690, 1.0)]}, 'resource/images_info/camp_task/唐军图腾.bmp': {'scope': [(658, 834, 675, 853, 0.826)], 'ues': '唐军图腾'}}, processed_data_yolo: {'红色名称': {'scope': [(660, 68, 0.938)], 'offset': (0, 0), 'delay_time': 1.2, 'weight': 10}, '雇佣剑客': {'scope': [(267, 488, 0.929), (1169, 185, 0.909)], 'offset': (0, 0), 'delay_time': 1.2, 'weight': 10}, '红名怪': {'scope': [(236, 407, 0.809)], 'offset': (0, 0), 'delay_time': 1.2, 'weight': 10}},
        processed_data_mutil_colors: {'目标体_地图红点': {'scope': [(1323, 153), (1341, 160), (1344, 137), (1355, 142), (1357, 156)]}, '目标体血条': {'scope': [(664, 93), (725, 93)]}, '目标体等级': {'scope': [(585, 154), (586, 154)]}}
        """
        self.data_numpy = self.latest_result["numpy_data"]  # 获取numpy数据
        self.update_time_data = self.latest_result["uptime"]  # 获取更新时间

        self.diff_time=round(self.update_time_data-self.update_time_handling,3) # 计算数据更新时间差
        logger.error(f"数据更新时间差:{self.diff_time}") #计算数据的可信度
        if self.diff_time<-1:
            logger.error(f"数据不可信,休息{abs(self.diff_time)}秒")
            time.sleep(abs(self.diff_time))
            return False

        self.word_acquire_data=data_pool["processed_data_word_acquire"] # 获取文字信息
        self.word_handle_data=data_pool["processed_data_word_handle"] # 获取文字处理信息
        self.color_acquire_data=data_pool["processed_data_color_acquire"] # 获取颜色信息
        self.color_handle_data=data_pool["processed_data_color_handle"] # 获取颜色处理信息
        self.image_data=data_pool["processed_data_image"] # 获取图片信息
        self.yolo_data=data_pool["processed_data_yolo"] # 获取yolo信息
        self.mutil_colors_data=data_pool["processed_data_mutil_colors"] # 获取多颜色信息
        self.unique_data = data_pool["processed_data_unique"]  # 获取特有的信息

        self.role_name_data = data_pool["role_info_dict"]["name"]  # 获取角色信息
        self.role_hp = data_pool["role_info_dict"]["HP"]  # 获取血量信息
        self.role_mp = data_pool["role_info_dict"]["MP"]  # 获取蓝量信息
        self.role_rp = data_pool["role_info_dict"]["RP"]  # 获取耐力信息
        self.role_level = int(data_pool["role_info_dict"]["level"])  # 获取等级信息
        self.role_scoring = int(data_pool["role_info_dict"]["scoring"])  # 获取角色评分
        self.role_running = data_pool["role_info_dict"]["running"]  # 获取移动状态信息
        self.role_swap_gear = data_pool["role_info_dict"]["swap_gear"]  # 获取换装状态信息
        self.role_combating = data_pool["role_info_dict"]["combating"]  # 获取战斗状态信息
        self.role_loading = data_pool["role_info_dict"]["loading"]  # 获取加载状态信息
        self.role_healing_resurgence = data_pool["role_info_dict"]["healing_resurgence"]  # 获取复活状态

        self.target_info = data_pool["target_info_dict"]  # 获取目标信息
        self.map_name = data_pool["coordinate_info_dict"]["map_name"]  # 获取地图信息
        self.map_position = data_pool["coordinate_info_dict"]["map_position"]  # 获取地图位置信息
        self.task_info = data_pool["task_info_dict"]  # 获取任务信息
        self.gear_info_data=data_pool["gear_info_dict"] # 获取装备信息
        self.pet_info_data=data_pool["pet_info_dict"]  # 获取宠物信息
        self.summons_info_data=data_pool["summons_info_dict"]  # 获取召唤物信息
        self.interface_info = data_pool["interface_info_dict"]  # 获取界面信息

        logger.warning(f"==============================关键信息==========================================")
        logger.success(f"人物信息(self.role_name:str):{self.role_name}")
        logger.success(f"门派信息(self.role_sect:str):{self.role_sect}")
        logger.success(f"血量信息(self.role_hp:str):{self.role_hp}")
        logger.success(f"蓝量信息(self.role_mp:str):{self.role_mp}")
        logger.success(f"等级信息(self.role_level:int):{self.role_level}")
        logger.success(f"评分信息(self.role_scoring:int):{self.role_scoring}")
        logger.success(f"阵营信息(self.role_factions:str):{self.role_factions}")
        logger.success(f"耐力信息(self.role_rp:str):{self.role_rp}")
        logger.success(f"移动状态(self.role_running:bool):{self.role_running}")
        logger.success(f"换装状态(self.role_swap_gear:bool):{self.role_swap_gear}")
        logger.success(f"战斗状态(self.role_combating:bool):{self.role_combating}")
        logger.success(f"加载状态(self.role_loading:bool):{self.role_loading}")
        logger.success(f"复活状态(self.role_healing_resurgence:bool):{self.role_healing_resurgence}")
        logger.success(f"目标信息(self.target_info:dict):{self.target_info}")
        logger.success(f"地图信息(self.map_name:str):{self.map_name}")
        logger.success(f"地图位置(self.map_position:str):{self.map_position}")
        logger.success(f"任务信息(self.task_info:dict):{self.task_info}")
        logger.success(f"装备信息(self.role_gear_dic:dict):{self.role_gear_dict}")
        logger.success(f"宠物信息(self.pet_info_data:dict):{self.pet_info_data}")
        logger.success(f"召唤物信息(self.summons_info:dict):{self.summons_info}")
        logger.success(f"界面信息(self.interface_info:dict):{self.interface_info}")
        logger.warning(f"==============================数据信息==========================================")
        logger.success(f"特有信息(self.unique_data:dict):{self.message_to_log(self.unique_data,1)}")
        logger.success(f"文字信息(self.word_acquire_data:dict):{self.message_to_log(self.word_acquire_data)}")
        logger.success(f"文字处理信息(self.word_handle_data:list):{self.word_handle_data}")
        logger.success(f"颜色信息(self.color_acquire_data:dict):{self.message_to_log(self.color_acquire_data)}")
        logger.success(f"颜色处理信息(self.color_handle_data:dict):{self.message_to_log(self.color_handle_data)}")
        logger.success(f"图片信息(self.image_data:dict):{self.message_to_log(self.image_data,2)}")
        logger.success(f"yolo信息(self.yolo_data:dict):{self.message_to_log(self.yolo_data)}")
        logger.success(f"多颜色信息(self.mutil_colors_data:dict):{self.message_to_log(self.mutil_colors_data)}")
        logger.success(f"数据更新时间(self.update_time_data:float): {self.update_time_data}")
        logger.warning(f"==============================关键信息==========================================")



    def interface_closes(self):
        """界面关闭"""
        try:

            for key,value in self.interface_info.items():
                if key in "背包界面" :
                    self.key_press("b",delay_time=1)
                    return True
                if key not in ["主界面"]:
                    self.vnc.mouse_left_click(*value,delay_time=2)
                    return True
        except  Exception as e:
            logger.error(f"界面关闭失败:{e}")

    def role_info(self):
        """
        角色信息更新
        """
        self.ls_progress="task_running"
        logger.info("当前任务:角色信息更新")
        if self.node_counter >= 5 or (self.role_scoring !="-1" and not self.role_name):
            self.update_role_info_flag=True # 角色信息已更新,改变标志位
            self.node_counter = 0

        if not self.role_name:
            logger.success(f"名称数据:{self.role_name_data},ini名称数据:{self.role_name_str}")
            role_name_list=self.role_name_str.split(",")
            self.role_name=self.set_correct_term(self.role_name_data, role_name_list)

        if not self.role_factions:
            logger.info("当前任务:role_factions更新")
            res_dict = self.find_data_from_keys_list(["唐军图腾", "义军图腾"], self.image_data)
            logger.success(f"res_dict:{res_dict}")
            # {'resource/images_info/camp_task/唐军图腾.bmp': {'scope': [(658, 834, 675, 853, 0.826)], 'ues': '唐军图腾'}}
            if res_dict:
                for key, value in res_dict.items():
                    if value["ues"] == "唐军图腾":
                        self.role_factions = "唐军"
                    elif value["ues"] == "义军图腾":
                        self.role_factions = "义军"
            if self.role_factions :
                self.queue_message({"image": {'resource/images_info/camp_task/唐军图腾.bmp': {"enable": False},
                                              'resource/images_info/camp_task/义军图腾.bmp': {"enable": False},
                                              }})  # 参数关闭

        if self.role_scoring =="-1" and "主界面" in self.interface_info:
            logger.info("当前任务:role_scoring更新")
            self.vnc.key_press("c",delay_time=0.2) #打开角色信息界面
        elif self.role_scoring !="-1" and "角色信息界面" in self.interface_info:
            self.vnc.key_press("c",delay_time=0.2) #关闭角色信息界面
        else:
            self.interface_closes()

        self.node_counter += 1 # 节点计数器加1

    def role_gear(self):
        """
        角色装备更新
        """
        logger.info("当前任务:角色装备更新")
        # logger.success(f"角色装备已更新:{self.role_gear_dict}")

        if any(value == [-1,-1] for value in self.role_gear_dict.values()):
            if "角色信息界面" in self.interface_info:
                logger.success("角色信息界面,读取角色装备信息")
                # 遍历装备属性
                for gear,value in self.role_gear_dict.items():
                    if value == [-1, -1]:
                        self.gear_usage_count += 1  # 增加使用计数
                        if self.gear_info_data:
                            if self.gear_usage_count > 5:# 超过5次，重置为默认值
                                self.role_gear_dict[f'{gear}']=[0,0]
                                self.gear_info_data=None # 重置数据
                                self.gear_usage_count=0 # 重置使用计数
                                self.vnc.mouse_move(701+random.randint(-10,10),273+random.randint(-10,10))
                                time.sleep(2)
                                return True
                            else:
                                self.role_gear_dict[f'{gear}']=self.set_gear_entry(self.gear_info_data)
                                self.gear_info_data = None  # 重置数据
                                self.gear_usage_count = 0  # 重置使用计数
                                self.vnc.mouse_move(701 + random.randint(-10, 10), 273 + random.randint(-10, 10))
                                time.sleep(2)
                                return True
                        else:
                            self.vnc.mouse_move(*gear_name_point_dict[gear])  # 移动鼠标到装备位置
                            time.sleep(2)
                            return True

            elif "主界面" in self.interface_info:
                self.vnc.key_press("c", delay_time=0.2)  # 打开角色信息界面
        else:
            if "角色信息界面" in self.interface_info:
                self.vnc.key_press("c", delay_time=0.2)  # 关闭角色信息界面
            elif "主界面" in self.interface_info:
                self.mongodb_update_gear() # 更新角色装备信息
                self.update_role_gear_flag=True # 角色装备已更新,改变标志位
                self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭


    def role_pet(self):
        """
        角色宠物更新
        """
        self.ls_progress = "task_running"
        logger.info("当前任务:角色宠物更新")
        if self.node_counter>=5: # 节点计数器大于等于5
            self.update_role_pet_flag = True # 角色宠物已更新,改变标志位
            self.node_counter=0 # 重置节点计数器
            self.queue_message({"word": {12: {"enable": False}}})  # 参数关闭

        if "武将界面" in self.interface_info and self.pet_info_data:
            #{'铁枪': (1026, 593, 0.998, 12), '歪嘴军师': (1009, 617, 0.998, 12)}
            pet_name_list = list(self.pet_info_data.keys())
            self.mongodb_update_pet(pet_name_list) # 更新mongodb角色宠物信息
            self.update_role_pet_flag=True # 角色宠物已更新,改变标志位
            self.node_counter=0 # 重置节点计数器
            self.queue_message({"word": {12: {"enable": False}}})  # 参数关闭
            self.vnc.key_press("p", delay_time=0.2)  # 关闭武将信息界面

        elif "主界面" in self.interface_info:
            self.vnc.key_press("p",delay_time=0.2) #打开武将信息界面
            self.update_time_handling=int(time.time()) # 更新时间

        self.node_counter+=1 # 节点计数器加1

    def sum_pet(self):
        """
        角色召唤物更新
        """
        self.ls_progress = "task_running"
        logger.info("当前任务:角色召唤物更新")

        if self.summons_info_data:
            self.summons_info=list(self.summons_info_data.keys())[0]

    def role_basic_info(self):
        if not self.update_role_info_flag: # 获取角色信息
            self.role_info()
        # elif not self.update_role_gear_flag: # 获取角色装备信息
        #     self.role_gear()
        # elif not self.update_role_pet_flag: # 获取角色宠物信息
        #     self.role_pet()
        # elif self.update_role_info_flag and self.update_role_gear_flag and self.update_role_pet_flag:
        #     if not self.role_id:
        #         self.role_id = self.mongodb_set_query()  # mongodb查询条件,设计为role_id
        #         self.mongodb_query = {"role_id": self.role_id}  # mongodb查询条件
        #         self.mongodb_update_facility()  # 更新设备信息,设定更新间隔是24小时
        #
        #     if self.role_scoring:
        #         self.mongodb_update_role()  # 更新角色信息,设定更新间隔是1小时
        elif self.update_role_info_flag: #todo:不是调试的时候注销该行
            self.update_role_basic_info_flag = True  # 角色基础信息已更新,改变标志位
            logger.success("角色基础信息更新完成")
            return True

    def task_target_hunting(self):
        """
        目标寻找
        目标信息(self.target_info:dict):{'name': 'none', 'lock': False, 'attack_range': True, 'driftlessness': False}
        """
        if self.target_info:
            if self.target_info["driftlessness"]: #小地图范围内无目标
                return False
            elif self.target_info["attack_range"]:#目标在攻击范围内
                self.key_press("tab") #切换到目标
            elif not self.target_info["driftlessness"] and not self.target_info["attack_range"]: #目标不在攻击范围内
                if self.mutil_colors_data:
                    for key,value_data in self.mutil_colors_data.items():
                        if key in ["目标体_地图红点"]:
                            res_tuple=self.find_closest_point(value_data["scope"], self.role_map_position)
                            self.mouse_right_click(*res_tuple,delay_time=3)
            elif self.target_info["lock"]: #目标锁定,任务完成
                return True
    def task_普通高频技能(self):
        """
        职业的基本攻击技能
        """
        for skill_num in self.skill_普通高频:
            self.key_press(f"{skill_num}", delay_time=0.2)
    def task_普通延迟技能(self):
        # 随机选择的数量，确保不超过 numbers 的长度
        if len(self.skill_普通延迟)>=2:
            num_to_select = random.randint(2, len(self.skill_普通延迟))
            selected_elements = random.sample(self.skill_普通延迟, num_to_select)  # 随机抽样
            for skill_num in selected_elements:
                self.key_press(f"{skill_num}", delay_time=1)
        else:
            self.key_press(f"{self.skill_普通延迟[0]}",delay_time=0.6)
    def task_怒气技能(self):
        skill_num = random.sample(self.skill_怒气技能, 1) # 随机选择一个元素
        self.key_press(f"{skill_num[0]}", delay_time=0.2)
    def task_状态技能(self):
        for skill_num in self.skill_状态技能:
            if skill_num != "-1":
                self.mouse_left_click(*state_points_dict[skill_num], delay_time=1.5)
                self.mouse_move(838,797)
    def task_加血技能(self):
        for skill_num in self.skill_加血技能:
            if skill_num != "-1":
                self.key_press(f"{skill_num}", delay_time=0.6)
    def task_召唤技能(self):
        for skill_num in self.skill_召唤技能:
            if skill_num != "-1":
                self.key_press(f"{skill_num}", delay_time=0.6)
    def task_加血值判断(self):
        """
        血量百分比太小
        """
        if self.role_hp: #存在怒气值
            # 使用 split() 方法将字符串分割为列表
            ls = self.role_hp.split("/")
            # 将字符串列表转换为整数列表
            int_list = [int(num) for num in ls]
            # 计算百分比
            percentage = int((int_list[0] / int_list[1]) * 100)
            logger.info(f"{int_list},血量百分比:{percentage}")
            if percentage<60:
                logger.error("血量过低")
                return True
        else:
            return False
    def task_怒气值判断(self):
        if self.role_rp: #存在怒气值
            # 使用 split() 方法将字符串分割为列表
            ls = self.role_rp.split("/")
            # 将字符串列表转换为整数列表
            int_list = [int(num) for num in ls]
            if int_list[0]>=60:
                return True
        else:
            return False
    def task_skill_release(self):
        if self.task_加血值判断():
            if self.role_sect in ["少林"]:
                self.task_加血技能() #  释放加血技能
            else:
                self.key_press("_",delay_time=0.3) #血瓶

        if abs(int(time.time())-self.skill_状态技能_last_time)>=28*60: # 状态技能间隔为28分钟
            self.task_状态技能() # 释放状态技能
            self.skill_状态技能_last_time=int(time.time())

        if self.task_怒气值判断():
            self.task_怒气技能() # 释放怒气技能

        self.task_普通高频技能() # 释放普通高频技能

        self.task_普通延迟技能() # 释放普通延迟技能
    def task_skill_attack(self):
        """
        技能攻击
        """
        if self.target_info:
            if self.target_info["lock"]: # 锁定目标
                self.task_skill_release()
            elif self.target_info["driftlessness"]:  # 小地图范围内无目标
                return "task_wait"
            elif self.target_info["attack_range"]:  # 目标在攻击范围内
                self.key_press("tab")  # 切换到目标
            elif not self.target_info["driftlessness"] and not self.target_info["attack_range"]:  # 目标不在攻击范围内
                if self.mutil_colors_data:
                    for key, value_data in self.mutil_colors_data.items():
                        if key in ["目标体_地图红点"]:
                            res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                            self.mouse_right_click(*res_tuple, delay_time=3)

    #todo : 节点寻路,待优化
    def way_finding_node_op(self,coordinate_node_list: list, range_num: int = 50, debug: bool = False,difference:int=6,threshold:int=3,record_num:int=6):
        """
        示例代码:
            #节点坐标
            coordinate_node = [(118, 100), (116, 104), (113, 111), (111, 120),(112,125),(113,129),(113,135),(112,141),(109,150),(106,156),
                               (103,161),(101,168),(99,175),(99,181),(96,188),(91,196),]
            #节点坐标处理
            coordinate_node_dispose=insert_intermediate_points_on_line(coordinate_node)
            print(coordinate_node_dispose)
            way_finding_node_op(coordinate_node_dispose,debug=True)

        :param coordinate_node_list: 节点坐标
        :param range_num: 寻路次数
        :param debug: 是否开启调试信息
        :param difference: 坐标差值
        :param threshold: 坐标阈值,起点坐标和节点坐标之间距离调整
        :param record_num: 记录坐标次数,用于特殊寻路处理
        :return: 寻路结果 1:完成 0:未完成 -1 :失败
        """
        result = []  # 寻路结果
        # 使用 split 方法分割字符串，并将结果转换为整数
        x, y = map(int, self.map_position.split(','))
        self.coord = [x,y] #坐标信息,坐标是否改变

        if len(self.real_time_coordinate_list)>=record_num :# 记录6次坐标
            if len(set(self.real_time_coordinate_list))==1:#如果6次坐标都一样,则说明坐标没有变化
                logger.error("寻路失败,启动特殊寻路模式!!!")
                self.real_time_coordinate_list = []  # 清空列表
                return -1
            else:
                self.real_time_coordinate_list = []  # 清空列表

        for i in range(range_num):
            real_time_tuple_dispose = (-1, -1)
            real_time_tuple = self.coord # 获取当前坐标
            logger.error(f"识别出来的{real_time_tuple}")
            logger.error(f"记录的上次的坐标为{self.real_time_tuple_record}")

            """避免识别错误或者识别不全的情况下出现鼠标点击距离过大的问题"""

            if isinstance(real_time_tuple, tuple) and len(real_time_tuple) == 2 and all(isinstance(i, int) for i in real_time_tuple) and real_time_tuple != (0, 0):# 情况1,比较和节点坐标是否在误差范围内
                real_time_tuple_x, real_time_tuple_y = real_time_tuple
                for coordinate_node_x, coordinate_node_y in coordinate_node_list:
                    if abs(real_time_tuple_x - coordinate_node_x) <= 20 and abs(
                            real_time_tuple_y - coordinate_node_y) <= 20:
                        real_time_tuple_dispose = real_time_tuple  # 说明该坐标点可以使用
                        self.real_time_tuple_record = tuple(self.coord)  # 记录坐标
                        logger.debug(f"寻路实时坐标可用{real_time_tuple_dispose}")
                        break

            #情况2,实时坐标没有匹配成功,启用模块坐标比较
            if real_time_tuple_dispose==(-1, -1) and self.coord and all(isinstance(x, int) for x in self.coord[:2]) :
                for coordinate_node_x, coordinate_node_y in coordinate_node_list:
                    if abs(coordinate_node_x - self.coord[0]) <= 20 and abs(coordinate_node_y - self.coord[1]) <= 20: #比较和模块坐标是否在误差范围内
                        real_time_tuple_dispose = tuple(self.coord[:2]) # 说明该坐标点可以使用
                        self.real_time_tuple_record = tuple(self.coord[:2])  # 记录坐标
                        logger.debug(f"模块坐标可用{real_time_tuple_dispose}")
                        break

            #情况3,模块坐标没有匹配成功,启用之前坐标比较
            if real_time_tuple_dispose==(-1, -1) and self.real_time_tuple_record !=(0,0):
                real_time_tuple_dispose = self.real_time_tuple_record  # 用回之前保存的坐标点
                logger.debug(f"启用之前坐标点{real_time_tuple_dispose}")

            if real_time_tuple_dispose ==(-1, -1) :#都识别失败
                logger.error("坐标无法匹配")
                self.real_time_coordinate_list.append((0,0))

            if real_time_tuple_dispose != (-1, -1):
                logger.error(f"寻路已处理的实时坐标可用{real_time_tuple_dispose}")
                result = way_finding_node(real_time_tuple_dispose, coordinate_node_list,difference,threshold)  # 计算路径

            if debug:
                logger.debug(f"实时坐标{real_time_tuple}")
                logger.debug(f"寻路结果{result}")
                logger.debug(f"坐标记录:{self.real_time_coordinate_list}")

            if result and len(result) == 1:
                x1, y1 = result[0]  # 起点坐标
                if abs(x1 - coordinate_node_list[-1][0]) <= 3 and abs(y1 - coordinate_node_list[-1][1]) <= 3:
                    logger.info(f"已经到达目的地")
                    return 1
                else:  # 最后一个节点时候,特殊处理
                    x_point, y_point = coordinate_point_conversion(x1, y1, coordinate_node_list[-1][0],
                                                                   coordinate_node_list[-1][1], debug=True)
                    if (x_point, y_point) != (0, 0):
                        self.mouse_right_click(x_point, y_point, delay_time=0.5)  # 右键点击移动
                        self.real_time_coordinate_list.append(result[0])  # 记录坐标点,重复点击处理

            elif result and len(result) == 2:
                x1, y1 = result[0]  # 起点坐标
                x2, y2 = result[1]  # 目标坐标
                if (x2,y2)==coordinate_node_list[-1]:#说明是最后一个节点
                    if abs(x1 - x2) <= 3 and abs(y1 - y2) <= 3:
                        logger.info(f"已经到达目的地")
                        return 1
                else:#说明不是最后一个节点
                    x_point, y_point = coordinate_point_conversion(x1, y1, x2, y2, debug=True)
                    if (x_point, y_point) == (-1, -1):  # todo,怎么处理
                        pass
                    elif (x_point, y_point) != (0, 0):
                        self.mouse_right_click(x_point, y_point, delay_time=0.3)  # 右键点击移动
                        self.real_time_coordinate_list.append(result[0])#记录坐标点,重复点击处理

            else:
                time.sleep(0.2)
        return 0


    def task_details(self):
        """
        任务详情:这里接入任务的具体操作内容
        """
        pass

    def task_flow(self):
        """
        任务流程
        """
        self.data_info() # 获取数据信息

        if not self.update_role_basic_info_flag:
            self.role_basic_info()

        if self.update_role_summons_flag: # 获取角色召唤物信息
            self.sum_pet()

        if self.update_role_basic_info_flag :
            self.task_details() # 任务详情


    def run(self,latest_result):
        """
        运行任务
        ls_progress="task_finish","task_fail","task_error","task_wait","task_get","task_running"
        :param latest_result: 数据结果
        任务结果:
        """
        self.latest_result=latest_result # 获取结果
        self.task_flow() # 任务流程
        self.update_time_handling=time.time() # 更新时间
        logger.success(f"任务进度:{self.ls_progress}")
        if self.ls_progress=="task_finish": # 任务完成
            return "task_finish"
        elif self.ls_progress=="task_fail": # 任务失败
            return "task_fail"
        elif self.ls_progress=="task_error" : # 任务错误
            return "task_error"
        elif self.ls_progress=="task_wait": # 任务等待
            return "task_wait"
        else:
            return "task_unknown" # 任务未知

