from basic_function.quest_module import *
"""
功能: 悬赏任务
更新日志: 2024-11-26 19:21:23
设计思路:
1.根据副本任务不同选择对应的节点
2.为任务加上保险功能,防止任务失败,开启保险以后还是失败就放弃任务
3.毒沼任务直接放弃

"""

class reward_悬赏(Quest_Task):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list)


        self.task_accepted_flag = False #任务是否已领取,默认为false
        self.camp_task_finish_flag = False #阵营任务完成标志,默认为false
        self.accepted_task_list = [] #已领取任务列表
        self.completed_task = []  # 已完成的任务
        self.node_current=None #当前节点
        self.node_next=None #下一个节点
        self.node_before=None #上一个节点
        self.node_list= []  # 节点:操作,列表
        self.role_position_map=(1336,149) #角色位置,小地图
        self.role_position_scene=(720,450) #角色位置,游戏场景
        self.target_position_map=[] #目标位置,小地图
        self.target_position_scene=[] #目标位置,游戏场景
        self.identification_target_flag=False #是否识别到目标
        self.find_the_target_flag=False #是否找到目标
        self.attack_a_target_flag=False #是否攻击目标
        self.target_name_list = None #目标名称列表
        self.node_finish_flag = False #节点是否完成
        self.node_disassemble_flag = False #是否拆分装备
        self.node_first_flag = False #进入副本第一个节点,拆分装备
        self.coord_end=None #节点结束坐标
        self.coordinate_node_image = None #节点坐标
        self.coordinate_node_image_list= [] #节点坐标列表
        self.node_counter=0 #节点计数器
        self.find_way_node=None #寻路节点
        self.start_node=None #起始节点
        self.insurance_flag = False #保险标志

    """
    更新日志:2024-10-16 16:23:16
    倒序的形式写节点任务:
    if 结束条件
    elif 流程3
    elif 流程2
    else 流程1
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    :text_alternative_parameters: 文字识别,是否去除背景色
    :word_standard_dict: 文字标准字典
    :keywords_list: 关键词列表
    :target_name_list: 目标名称列表
    """

    def task_data_茫野荒坟(self):
        """
        茫野荒坟配置信息
        :return:
        """
        return {
            "start_node":"res/dtws/reward_task/荒坟_地图起点.bmp",
            "find_way_node":[(55,50),(52,59),(55,65),(60,70),(66,72),(70,78),(73,85),(74,83),(79,80),(80,75),(78,70),],

            "coordinate_node" : {(47,62):"res/dtws/reward_task/荒坟_1.bmp",
                                        (56,78):"res/dtws/reward_task/荒坟_2.bmp",
                                        (80, 77):"res/dtws/reward_task/荒坟_3.bmp",
                                        (78, 70):"res/dtws/reward_task/荒坟_4.bmp",},
            "dic_reward_tasks" : {
                "word": {
                    "出口": (350,277,1100,666, 0.8, 55, -18),
                },
                "image": {
                    "res/dtws/reward_task/荒坟_1.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/荒坟_2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/荒坟_3.bmp": (371, 136, 973, 696, 0.8),  # 小地图3
                    "res/dtws/reward_task/荒坟_4.bmp": (371, 136, 973, 696, 0.8),  # 小地图4
                    "res/dtws/reward_task/出口.bmp": (350,277,1100,666, 0.8, 43, -24),
                },},
            "coor_dict": [(56, 50), (79, 75)],
            "target_name_list" : ["波斯武士", "圣火教长",],}

    def task_data_全商盟货船(self):
        """
        茫野荒坟配置信息
        :return:
        """
        return {
            "start_node":"res/dtws/reward_task/货船_地图起点.bmp", #在地图界面,起点.
            "find_way_node": [(213,139),(209,133),(209,127),(209,121),(175,137),(175,132),(175,127),(175,120),
                              (137,155),(137,149),(137,142),(137,135),(137,120)], #补充重要节点之间的路径

            "coordinate_node": {(239,133):"res/dtws/reward_task/货船_小地图1.bmp",
                                (207,119):"res/dtws/reward_task/货船_小地图2.bmp",
                                (175, 115):"res/dtws/reward_task/货船_小地图3.bmp",},
            "dic_reward_tasks": {
                "word": {
                    "出口": (489,323,1148,689, 0.8, -7, -10),
                },
                "image": {
                    "res/dtws/reward_task/货船_小地图1.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/货船_小地图2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图2
                    "res/dtws/reward_task/货船_小地图3.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图3
                    "res/dtws/reward_task/出口.bmp": (489,323,1148,689, 0.8, -18, -15),
                    "res/dtws/reward_task/出口_货船.bmp": (489,323,1148,689, 0.8, -18, -15),
                }, },
            "coor_dict": [(239,133), (134, 120)],
            "target_name_list": ["疾风强盗","缥缈不定",], }

    def task_data_破庙(self):
        """
        破庙配置信息
        :return:
        """
        return {
            "start_node":"res/dtws/reward_task/破庙_地图起点.bmp",

            "find_way_node": [(74,45),(74,53),(75,62),(75,71),(75,78),(76,89),(76,96),(77,105),(76,110),],

            "coordinate_node": {(74,43):"res/dtws/reward_task/破庙_小地图1.bmp",
                                (75,62):"res/dtws/reward_task/破庙_小地图2.bmp",
                                (76, 83):"res/dtws/reward_task/破庙_小地图3.bmp",},
            "dic_reward_tasks": {
                "word": {
                    "出口": (350,277,1100,666, 0.8, 30, -10),
                },
                "image": {
                    "res/dtws/reward_task/破庙_小地图1.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/破庙_小地图2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/破庙_小地图3.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图3
                    "res/dtws/reward_task/出口.bmp": (350,277,1100,666, 0.8, 17, -17),
                }, },
            "coor_dict": [(76,44), (77, 112)],
            "target_name_list": ["七祸临头","八方聚晦","九世灾星",] }

    def task_data_天孤峰(self):
        """
        天孤峰配置信息
        :return:
        """
        return {

            "start_node":"res/dtws/reward_task/天孤峰_地图起点.bmp", #在地图界面,起点.
            "find_way_node": [(132,38),(133,46),(127,53),(118,55),(110,62),(110,70),(111,78),(110,84),(108,94),
                              (103,105),(98,115),(94,128),(100,132),(105,133),(113,132),(119,131),
                              (122,126),(117,120),(119,115),(127,112)],

            "coordinate_node": {(128,54):"res/dtws/reward_task/天孤峰_1.bmp",
                                (110,88):"res/dtws/reward_task/天孤峰_2.bmp",
                                (112, 127):"res/dtws/reward_task/天孤峰_3.bmp",},
            "dic_reward_tasks": {
                "word": {
                    "出口": (350,277,1100,666, 0.8, 45, -19),
                },
                "image": {
                    "res/dtws/reward_task/天孤峰_1.bmp": (1256, 74, 1415, 204, 0.8, 0, 15),  # 小地图1
                    "res/dtws/reward_task/天孤峰_2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/天孤峰_3.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图3
                    "res/dtws/reward_task/出口.bmp": (350,277,1100,666, 0.8, 35, -30),
                }, },
            "coor_dict": [(133,43), (128, 114)],
            "target_name_list": ["圣火教徒","圣火教长",]}

    def task_data_北隅冰原(self):
        """
        北隅冰原配置信息
        :return:
        """
        return {
            "start_node":"res/dtws/reward_task/冰原_地图起点.bmp",#在地图界面,起点.
            "find_way_node": [(78,63),(84,63),(90,61),(98,61),(105,61),(110,65),(110,73),(103,84),(92,91),
                              (84,99),(84,107),(86,118),(92,120),],

            "coordinate_node": {(82,59):"res/dtws/reward_task/冰原_1.bmp",
                                    (110,64):"res/dtws/reward_task/冰原_2.bmp",
                                    (122,93):"res/dtws/reward_task/冰原_3.bmp",
                                    (95,89):"res/dtws/reward_task/冰原_4.bmp",},
            "dic_reward_tasks": {
                "word": {
                    "出口": (350,277,1100,666, 0.8, 37, -10),
                },
                "image": {
                    "res/dtws/reward_task/冰原_1.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/冰原_2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图2
                    "res/dtws/reward_task/冰原_3.bmp": (1256, 74, 1415, 204, 0.8,),  # 小地图3
                    "res/dtws/reward_task/冰原_4.bmp": (1256, 74, 1415, 204, 0.8,),  # 小地图4
                    "res/dtws/reward_task/出口.bmp": (350,277,1100,666, 0.8, 25, -20),
                }, },
            "coor_dict": [(75,58), (98, 119)],
            "target_name_list": ["波斯舞姬","波斯贵族",]}

    def task_data_南荒毒沼(self):
        """
        南荒毒沼配置信息
        :return:
        """
        return {
            "start_node":None,
            "find_way_node": [],

            "coordinate_node": {},
            "dic_reward_tasks": {
                "word": {
                    "出口": (440, 309, 820, 555, 0.8, 40, -17),
                },
                "image": {
                    "res/dtws/reward_task/出口.bmp": (440, 309, 820, 555, 0.8, 25, -20),
                }, },
            "coor_dict": [],
            "target_name_list": []}

    def task_data_荒野营地(self):
        """
        荒野营地配置信息
        :return:
        """
        return {
            "start_node": "res/dtws/reward_task/营地_地图起点.bmp", #地图起点
            "find_way_node": [(66,23),(67,31),(71,38),(77,40),(82,50),(81,62),(77,69),(70,78),(74,86),(74,93),(67,95),
                              (58,93),(55,85),(56,77),(59,69),(62,73),(56,68),(57,61),(53,54)],

            "coordinate_node":{
                    (66,22):"res/dtws/reward_task/营地_0.bmp",
                    (76,42):"res/dtws/reward_task/营地_1.bmp",
                    (79,72):"res/dtws/reward_task/营地_2.bmp",
                    (60, 86):"res/dtws/reward_task/营地_3.bmp",
                    (53, 51):"res/dtws/reward_task/通缉犯.bmp",},
            "dic_reward_tasks": {
                "word": {
                    "出口": (350,277,1100,666, 0.8, 18, -2),
                },
                "image": {
                    "res/dtws/reward_task/营地_0.bmp": (1256, 74, 1415, 204, 0.8),
                    "res/dtws/reward_task/营地_1.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图1
                    "res/dtws/reward_task/营地_2.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图2
                    "res/dtws/reward_task/营地_3.bmp": (1256, 74, 1415, 204, 0.8),  # 小地图3
                    "res/dtws/reward_task/出口.bmp": (350,277,1100,666, 0.8, 7, -10),
                }, },
            "coor_dict": [(66,22), (52, 54)],
            "target_name_list": ["黑水头领","黑水盗贼",]}

    def task_config_info(self):
        """信息配置"""
        map_name = ["全商盟货船","全商盟货舱","破庙", "天孤峰", "北隅冰原","茫野荒坟", "南荒毒沼", "荒野营地"]  # 7个地图

        # 地图与其配置方法的映射
        map_task_data = {
            "全商盟货舱": self.task_data_全商盟货船,
            "全商盟货船": self.task_data_全商盟货船,
            "破庙": self.task_data_破庙,
            "天孤峰": self.task_data_天孤峰,
            "北隅冰原": self.task_data_北隅冰原,
            "茫野荒坟": self.task_data_茫野荒坟,
            "南荒毒沼": self.task_data_南荒毒沼,
            "荒野营地": self.task_data_荒野营地,
        }


        if self.map_name  and "商盟" in self.map_name:
            self.map_name = "全商盟货船"

        # 判断当前地图是否在任务地图中
        if self.map_name in map_name:
            logger.info("当前地图：{}".format(self.map_name))
            # 如果当前地图有对应的配置方法，进行配置
            if self.map_name in map_task_data:
                # 获取任务数据
                task_data = map_task_data[self.map_name]()

                # 更新文字识别资源
                self.dic_resource["word"].update(task_data["dic_reward_tasks"]["word"])
                # 更新图片识别资源
                self.dic_resource["image"].update(task_data["dic_reward_tasks"]["image"])

                # 设置配置参数
                self.coord_end = task_data["coor_dict"] # 终点坐标
                self.coordinate_node_image = task_data["coordinate_node"]  # 重要节点坐标
                self.target_name_list = task_data["target_name_list"]  # 目标体名称列表
                self.find_way_node = task_data["find_way_node"]  # 寻路节点
                self.start_node=task_data["start_node"] # 起始节点

    def task_flow(self):
        """
        思路:根据识别出来的任务关键词进行节点操作,节点之间用self.node_current连在一起
            在识别失败的情况下,可以根据self.node_current执行当前节点操作.
        任务节点综合操作
        1判断任务关键词是否存在:
            1存在:
                1完成,退出
                2任务中:
                    1在任务地图中,副本操作
                    2在野外地图寻找疑犯中
            2 不存在:
                1查看当前节点:
                    1任务接取
                    2继续任务节点

        :return:
        """
        self.ls_progress = "任务中"
        logger.debug(f"{self.node_current}")

        key_info = ["目标体红名", "目标体等级", "目标体_红名", "目标体_地图红点",]

        map_name_list =["蜀南竹海","白屏寨","少林","天煞盟","青城山","鸣沙山",]


        self.task_config_info() #配置任务信息

        if self.map_name and (self.map_name in map_name_list or "竹海" in self.map_name) : #在副本外
            self.get_ocr_vnc_click("确定", 670, 440, 737, 465)
            logger.info("回到城池,副本任务完成")
            return "task_finish"

        elif self.node_finish_flag:#说明副本到了终点位置
            logger.info("副本已完成")

            if self.get_ocr_vnc_click("离开",558,587,633,618,delay_time=10) or self.get_items_from_keys_operation("离开","dic_word_hand",delay_time=10):
                logger.info("退出副本")

            elif self.get_value_from_key_operation("捕获成功", "dic_word_hand", delay_time=2):
                self.key_press_op("~", delay_time=1)  # 拾取物品")
                logger.info("副本完成")

            elif "游戏主界面" in self.game_interface[0]:
                self.key_press_op("M",delay_time=1)

            elif "地图界面" in self.game_interface[0]:
                if self.get_value_from_key_operation("出口","dic_word_hand",delay_time=25,mouse_button=3):
                    logger.info("点击地图出口")
                elif self.get_items_from_keys_operation(["res/dtws/reward_task/出口.bmp",'res/dtws/reward_task/出口_货船.bmp'],"dic_image_hand",delay_time=25,mouse_button=3):
                    logger.info("点击地图出口")

        elif not self.node_finish_flag:

            if self.map_name in ["南荒毒沼"]: #这个任务直接放弃
                self.node_finish_flag = True
                return True

            if self.get_value_from_key("疑犯(已完成)","dic_word_ocr"): #任务完成
                self.node_finish_flag = True
                return True

            condition_1=self.get_items_from_keys( ["目标体红名", "目标体等级",  "目标体_地图红点",],"dic_mutil_colors")
            condition_2=self.find_yolo( ["红色名称", "红名怪", ])

            if condition_1 or condition_2: #已锁定目标体
                logger.info("目标体出现")
                self.node_counter = 0  # 重置

                if self.get_items_from_all_keys([key_info[0], key_info[1]], "dic_mutil_colors"):  # 已锁定目标体
                    if self.map_name and self.map_name in ["破庙",]:
                        self.py.find_image_vnc_click("res/dtws/reward_task/蜀山普通攻击.bmp", 1198, 808, 1247, 858,
                                                     delay_time=1)

                    self.key_press_op("3", delay_time=0.5)
                    skill_num = random.randint(1, 2)
                    self.key_press_op(f"{skill_num}", delay_time=2)
                    if self.role_info["血量"]:  # 血量
                        if self.is_correct_and_compare(self.role_info["血量"]):
                            logger.warning("血量低于50%,快速恢复")
                            self.key_press_op("-", delay_time=1)
                        if not self.find_ppocr_word_op("狼|灵",125, 115, 193, 139):
                            self.mouse_left_click_op(806,832)

                    return True

                elif self.get_items_from_keys([key_info[2], key_info[3]], "dic_mutil_colors"):  # 出现目标体
                    self.task_目标识别()
                    return True

            elif not condition_1 and not condition_2: #未锁定目标体

                npc_name_list = ['res/dtws/reward_task/通缉犯.bmp', "res/dtws/reward_task/霸山虎.bmp",
                                 "res/dtws/reward_task/异族细作.bmp", "res/dtws/reward_task/血路独行.bmp",
                                 "res/dtws/reward_task/七窍玲珑.bmp","res/dtws/reward_task/不赦死囚.bmp",]
                if self.get_items_from_keys_operation(npc_name_list, "dic_image_hand", delay_time=5):
                    logger.info("捕获")
                    self.key_press_op("~", delay_time=1)  # 拾取物品")
                    self.node_counter=0 #重置计数器
                    return True

                if self.get_value_from_key_operation("npc","dic_mutil_colors",delay_time=1):#找到npc图标在小地图中
                    logger.info("找到npc图标,前往中")
                    return True

                count = Counter(self.coordinate_node_image_list) #统计经过的节点,计算频率
                exists = any(value > 5 for value in count.values())# 判断是否存在频次大于 4 的元素
                if exists:
                    logger.info("经过的节点大于5次")
                    if not self.insurance_flag:#保险功能未开启
                        if "游戏主界面" in self.game_interface[0]:
                            self.key_press_op("M",delay_time=1)
                        elif "地图界面" in self.game_interface[0]:
                            if self.py.find_image_vnc_click(self.start_node, 308,278,1138,660,delay_time=1):
                                self.mouse_left_click_op(*self.game_interface[1:]) #界面关闭
                                self.coordinate_node_image_list=[] #重置节点列表
                                self.node_counter = 0  # 重置计数器
                                self.insurance_flag=True #保险功能已开启
                                return True
                    else:
                        logger.info("保险功能已开启,放弃任务")
                        self.node_finish_flag = True
                        return True

                if self.node_counter==3:#移动一下人物
                    logger.info("移动一下人物")
                    self.mouse_right_click_op(814,440,delay_time=1)
                    self.node_counter+=1
                    return  True

                if 4<=self.node_counter<=6:
                    if len(set(self.coordinate_node_image_list))==len(self.coordinate_node_image):
                        logger.info("所有节点都经过")
                    else:#todo:['res/dtws/reward_task/营地_2.bmp', 'res/dtws/reward_task/营地_3.bmp'],回到起点
                        logger.info("未经过所有节点")
                        if not self.insurance_flag: #保险功能未开启
                            if "游戏主界面" in self.game_interface[0]:
                                self.key_press_op("M", delay_time=1)
                                return True
                            elif "地图界面" in self.game_interface[0]:
                                if self.py.find_image_vnc_click(self.start_node, 308, 278, 1138,660, delay_time=1,mouse_button=3):
                                    self.mouse_left_click_op(*self.game_interface[1:])  # 界面关闭
                                    self.coordinate_node_image_list = []  # 重置节点列表
                                    self.node_counter = 0  # 重置计数器
                                    self.insurance_flag = True  # 保险功能已开启
                                    return True
                        else: #保险功能已开启
                            logger.info("保险功能已开启,放弃任务")
                            self.node_finish_flag = True
                            return True

                if self.get_value_from_key_operation("捕获成功", "dic_word_hand", delay_time=2) or self.node_counter>=8:
                    logger.info("副本完成")
                    self.node_finish_flag = True
                    self.key_press_op("~", delay_time=1)  # 拾取物品")
                    self.node_counter=0 #重置计数器
                    return True

                if self.coord and all(isinstance(x, int) for x in self.coord[:2]): #根据坐标判断
                    if self.coord_end:
                        value_x_end, value_y_end = self.coord_end[1]
                        if abs(self.coord[0] - value_x_end) < 10 and abs(self.coord[1] - value_y_end) < 10 : #判断是否在终点附近
                            logger.info("在终点附近")
                            self.node_counter+=1
                            return True

                    for key, value in self.coordinate_node_image.items(): #判断是否在节点附近

                        if abs(self.coord[0]-key[0])<15 and abs(self.coord[1]-key[1])<15: #判断是否在节点附近
                            self.get_value_from_key_operation(value,"dic_image_hand",delay_time=6)
                            self.coordinate_node_image_list.append(value)
                            logger.debug(f"重要节点{self.coordinate_node_image_list}")
                            return True

                    if self.find_way_node: #判断节点是否存在
                        coordinate_node_dispose = insert_intermediate_points_on_line(self.find_way_node)
                        res_num = self.way_finding_node_op(coordinate_node_dispose,debug=True, range_num=5,record_num=4)
                        logger.debug("节点寻路中")
                        if res_num == 1:
                            self.node_counter+=1 #计数器加1
                            return True
                        elif res_num == -1:
                            logger.error("寻路移动失败")
                            self.node_counter+=1 #计数器加1
                            return True
                        elif res_num == 0:
                            logger.info("凤鸣山节点移动中")
                            self.node_counter=0 #计数器清零
                            return True
                else:
                    logger.error("未知触发")
                    self.node_counter+=1 #计数器加1

    def 任务操作(self):
        res_str=self.task_flow()
        if res_str=="task_finish":#任务完成
            logger.info("悬赏副本任务完成")
            self.ls_progress = "任务完成"  # 模块运行结束
            self.task_name = "副本"
            self.program_result = "task_finish"


#任务资源
"""
说明: 资源格式和参数说明
    x1:左上角x坐标值
    y1:左上角y坐标值
    x2:右下角x坐标值
    y2:右下角y坐标值
    con:置信度
    x3:x偏移值
    y3:y偏移值
    time:延迟时间
    weight:权重,值越大,优先级越高
    True/false:True为只判断,false为点击,默认为false

    "word":{"标签":(x1,y1,x2,y2,con,x3,y3,time,weight,true/false)}
            标签为数字的,在范围内识别出来的文字,文字模糊匹配功能,去出背景色识别功能,存入dic_word_ocr中
            标签为字符串的,在范围内识别出来的文字,存入dic_word_hand中
    "image":{"图片路径":(x1,y1,x2,y2,con,x3,y3,time,weight,true/false),#true为只判断,false为点击,默认为false}
            注意图片路径
    "yolo":{"类名":(x3,y3,time,weight),
            "类名":True,#True为只判断
            }
    "color": {
             1: (440,180), #点位颜色识别
             "2df9f9": (1291, 326),#点位颜色判断
            },
    "mutil_colors":{
                "文字":{"colors":{"dcad5c":(1188,484),#文字自定义,颜色点位,主颜色
                                    "987840":(1202,485),#颜色点位,副颜色
                                    "876b39":(1221,492),#颜色点位,副颜色
                                    "edbb63":(1233,486),#颜色点位,副颜色
                                    },
                            "scope":(1177,251,1395,552),#识别颜色范围
                            "tolerance":25}, #颜色误差,一般设置为20-30之间
"""

scene_scope=(226, 29, 1136, 761, 0.8,)
dic_reward_tasks={
    "word": {
        # 2: (621,64,724,93, 0.8),#目标体信息
        "离开":(550,582,653,622,0.8,16,5),
        "捕获成功":(507,367,597,404,0.8,185,74),
        },
    "image": {
        "res/dtws/reward_task/通缉犯.bmp": (*scene_scope, 16, 123),  # 场景
        "res/dtws/reward_task/霸山虎.bmp": (*scene_scope, 18, 157),  # 场景
        "res/dtws/reward_task/异族细作.bmp":(*scene_scope, 41, 145),  # 场景
        "res/dtws/reward_task/血路独行.bmp":(*scene_scope, 18, 138),  # 场景
        "res/dtws/reward_task/七窍玲珑.bmp":(*scene_scope, 22, 176),  # 场景
        "res/dtws/reward_task/不赦死囚.bmp": (*scene_scope, 22, 176),  # 场景
        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        # "蜀山":True,
        # "疑犯":True,
        },
    "color": {
        #  1: (440,180), #点位
        #  "2df9f9": (1291, 326),#敌军粮车(未完成)
        },
    "mutil_colors":{
            "npc":{"colors":{"f7eb2f":(1320,158),
                            "fbf5a7":(1317,160),
                            "aa792b":(1320,161),
                            "dac039":(1319,163),},
                        "scope":(1257,74,1415,205),
                        "tolerance":25},

        }
    }

#资源合并,保持开启
quest_task_悬赏_merged_dict=merge_dicts(dic_reward_tasks,quest_task_merged_dict) #todo:更改名称

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
task_悬赏_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
task_悬赏_word_standard_dict={"疑犯":"疑犯(0/1)","犯":"疑犯(已完成)","交付":"点击交付"}

# 过滤的关键字
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#todo,窗口类名
# win_title = "002 "#todo,窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = "127.0.0.1" #todo,服务器地址
# vnc_port = 5902  #todo, 默认 VNC 端口，根据实际情况可能有所不同
# vnc_password = "ordfe113" #todo,密码,未设置的话可以注销此行
#
# def run():
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # todo,注意参数名称更改
#     task=reward_悬赏(py,win_hwnd[0],quest_task_悬赏_merged_dict,True,100,task_悬赏_text_alternative_parameters,task_悬赏_word_standard_dict)
#     res=task.run(classes=2,running_time=1,ero_num=10)
#     print(res)
#
# run()