from basic_function.quest_module import *
"""
功能: 副本任务模版
更新日志: 2024-12-19 19:37:33
设计思路:
1.
2.
3.
4.
5.
6.
"""

class team_design(Quest_Task):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,target_name_list:list=None,queue=None,win_title:str="000"):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list,queue=queue,win_title=win_title)


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
        self.target_name_list = target_name_list #目标名称列表
        self.node_finish_flag = False #节点是否完成
        self.node_disassemble_flag = False #是否拆分装备
        self.node_first_flag = False #进入副本第一个节点,拆分装备


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
    1.等待组队
    2.组队完成
    3.集合
    4.包裹清理
    5.进入副本
    6.副本操作
    7.包裹清理
    """
    def process_merge_list(self,lst):
        """
        合并列表中相邻的键值对,
        如果两个键值对的y坐标之差小于5，则合并这两个键值对
        :param lst: 列表
        :return: 合并后的列表
        """
        i = 0
        while i < len(lst) - 1:
            value1 = lst[i]
            value2 = lst[i + 1]
            # 检查y坐标之差
            if abs(value1[2] - value2[2]) < 10:
                # 合并这两个值
                new_value = (
                    value1[0],  # 类别1
                    value2[0],  # 类别2
                    min(value1[1], value2[1]),  # 最小x坐标
                    max(value1[2], value2[2]),  # 最大y坐标
                    max(value1[3], value2[3]),  # 最大置信度
                )
                # 只有当类别不相同时才进行合并
                if new_value[0] != new_value[1]:
                    lst[i] = new_value
                    del lst[i + 1]
                    # 不重置i，继续检查当前i的下一个元素
                else:
                    i += 1  # 如果类别相同，继续下一个
            else:
                i += 1  # 如果y坐标之差大于5，继续下一个

        return lst

    def handle_node(self, node_name, target_number, click_coordinates, npc_conditions, map_name):
        """
        处理节点任务
        :param node_name: 节点名称
        :param target_number: 目标数字
        :param click_coordinates: 点击坐标
        :param npc_conditions: NPC条件
        :param map_name: 地图名称
        :return:
        """
        if node_name not in self.node_list:
            if self.get_ocr_vnc_click(node_name, *click_coordinates, delay_time=1):
                for i in range(3):
                    pages_list = self.find_ocr_vnc_scope(743, 530, 862, 574)
                    if pages_list:
                        page_info = pages_list[0][0]
                        actual_number = int(page_info.split('第')[1].split('/')[0])

                        if actual_number < target_number:
                            logger.info(f"实际数字 {actual_number} 小于目标数字 {target_number}，点击右边。")
                            for _ in range(target_number - actual_number):
                                self.mouse_left_click_op(871, 553, delay_time=0.5)

                        elif actual_number > target_number:
                            logger.info(f"实际数字 {actual_number} 大于目标数字 {target_number}，点击左边。")
                            for _ in range(actual_number - target_number):
                                self.mouse_left_click_op(738, 553, delay_time=0.5)

                        elif actual_number == target_number:
                            logger.info(f"实际数字 {actual_number} 等于目标数字 {target_number}，无需点击。")
                            self.node_flag = True
                            break

                if self.node_flag:
                    npc_list = self.find_ocr_vnc_scope(591, 262, 1010, 528)
                    logger.info(f"npc_list: {npc_list}")

                    if npc_list:
                        npc_list_dispose = self.process_merge_list(npc_list)
                        logger.info(f"npc_list_dispose: {npc_list_dispose}")

                        if npc_list_dispose:
                            for npc in npc_list_dispose:
                                if len(npc) >= 5 and any(
                                        condition in npc[0] for condition in npc_conditions) and map_name in npc[1]:
                                    self.process_npc(npc)

                    self.node_list.append(node_name)
                    self.node_flag = False  # 设置节点完成标志为false

    def process_npc(self, npc_info):
        if len(npc_info) >= 1:
            npc_name, npc_location, x, y = npc_info[:4]
            self.mouse_left_click_op(x, y, delay_time=1)
            self.get_ocr_vnc_click("自动寻路", 575, 535, 671, 569, delay_time=1)
            self.node_first_flag = True

    def task_成都驿站(self):
        """

        :return:
        """
        self.ls_progress="任务中"
        self.node_current="task_等待组队"

        if self.map_name:
            if "成都" in self.map_name:
                logger.info("在成都")
                self.node_current="task_装备拆解"
                self.mongodb_team_info_update(advancer=1) #更新数据库的进度器
            else:
                logger.info("不在成都")
                if "地图界面" in self.game_interface[0]:
                    logger.info("地图界面.选择任务领取人")
                    if self.get_ocr_vnc_click("传送", 855, 201, 926, 241, delay_time=1):
                        self.get_ocr_vnc_click("成都", 589, 401, 1013, 446, delay_time=1)
                        self.get_ocr_vnc_click("自动寻路", 570, 520, 670, 573, delay_time=3)

                    elif self.get_ocr_vnc_click("快捷搜索", 996, 559, 1080, 585, delay_time=1):
                        pass

                    elif self.get_value_from_key_operation("res/dtws/camp_task/地图_npc.bmp", "dic_image_hand",
                                                           delay_time=1):
                        pass

                elif "游戏主界面" in self.game_interface[0]:
                    self.key_press_op("M")
                else:
                    self.界面关闭()

    def task_装备拆解(self):
        self.ls_progress="任务中"
        self.node_current="task_装备拆解"

        if self.node_disassemble_flag:
            logger.info("装备拆解完成")
            self.node_current="task_装备拆解"

        elif "装备拆解界面" in self.game_interface[0] and self.node_first_flag:
            logger.info("装备拆解界面")
            self.error_List=[] #清空错误列表
            if self.node_disassemble_flag:
                self.mouse_left_click_op(*self.game_interface[1:],delay_time=1)

            elif not self.node_disassemble_flag :
                if self.get_ocr_vnc_click("拆解", 774, 528, 857, 556, delay_time=15):
                    self.node_disassemble_flag = True

        elif "地图界面" in self.game_interface[0] and not self.node_first_flag:
            logger.info("地图界面")
            if self.find_ocr_vnc_word("自动寻路", 739, 156, 875, 182):
                if self.node_list == ["功能"]:
                    logger.info("功能界面关闭")
                    self.node_counter = 10  # 重置节点计数器
                    close_list = self.get_value_from_key("res/dtws/other/快速搜索_关闭.png", "dic_image_hand")
                    if close_list:
                        logger.info(f"close_list:{close_list}")
                        sorted_data = sorted(close_list, key=lambda x: x[0])
                        for close_coord in sorted_data:
                            self.mouse_left_click_op(close_coord[0], close_coord[1], delay_time=1)

                # 调用处理函数
                self.handle_node("功能", 19, (736, 207, 799, 235), ["装备拆解", "装备拆解师"], "成都")

            elif self.get_ocr_vnc_click("快捷搜索", 996, 559, 1080, 585, delay_time=1):
                pass
            elif self.get_value_from_key_operation("res/dtws/camp_task/地图_npc.bmp", "dic_image_hand",
                                                   delay_time=1):
                pass

        elif "游戏主界面" in self.game_interface[0] and len(self.node_list) < 1:
            self.key_press_op("M")  # 打开地图


    def task_flow(self):
        pass

    def 任务操作(self):#todo,这里一般固定写法,
        self.task_装备拆解()
        # res_str=self.task_flow()
        # if res_str=="task_finish_all":#任务完成
        #     logger.info("今天副本任务全部完成")
        #     self.ls_progress = "任务完成"  # 模块运行结束
        #     self.task_name = "副本"
        #     self.program_result = "task_finish"
        # elif res_str=="task_finish_once":#任务完成
        #     logger.info("副本任务完成一次,继续挑战")#todo:写再次进入副本的逻辑


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

team_design_reward_tasks={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        # 2: (621,64,724,93, 0.8),#目标体信息
        # "屠狼洞中":(511,369,692,406,0.8,185,74),#屠狼洞中
        # "快捷":(994,560,1080,584,0.8,0,0,1,5),
        # "收藏":(550,199,616,234,0.8,0,0,1,10),
        # "悬赏令发布使":(578,261,783,350,0.8,0,0,1,15),
        # "自动寻路":( 581,536,663,559, 0.8,0,0,1,20),
        # "寻路":(998,167,1083,191,0.8),#自动寻路
        # "开启了阵营":(462,344,625,368,0.8,242,131),#开启阵营提示
        # "可以提升":(466,375,647,405,0.8,232,73),#阵营任务可以完成
        # "你确认使用":(514,372,680,401,0.8,143,73),#你确定使用悬赏令
        # "贼人":(564,587,852,615,0.8),#贼人进入副本
        # "币":(964,567,1048,643,0.8),#整理,说明在背包界面
        },
    "image": {
        # "res/dtws/reward_task/悬赏令_数目1.bmp":(547,255,599,298,0.8),#悬赏令_数目1
        # "res/dtws/main_task/商城.bmp":(1195,24,1243,87,0.8)
        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        # "蜀山":True,
        # "疑犯":True,
        },
    "color": {
        #  1: (440,180), #点位
        #  "2df9f9": (1291, 326),#敌军粮车(未完成)
        #  "21b7b7": (1286, 331),#敌军粮车(未完成)
        #  "dd130e": (1323,326),#敌军粮车(未完成)
        },
    "mutil_colors":{
            # "打倒:疑犯(0/1)":{"colors":{"1b9595":(1250,517),
            #                     "2ae8e8":(1259,523),
            #                     "2df9f9":(1267,520),
            #                     "1ea6a6":(1277,525),
            #                     "ae0f0b":(1293,521),
            #                     "cd110d":(1305,526),},
            #             "scope":(1177,251,1395,552),
            #             "tolerance":30},

        }
    }


#资源合并,保持开启
team_design_merged_dict=merge_dicts(team_design_reward_tasks,quest_task_merged_dict) #todo:更改名称

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
team_design_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
team_design_word_standard_dict={"客":"雇佣剑客","毒":"毒蜂","熊":"棕熊",}

# 过滤的关键字
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#todo,窗口类名
# win_title = "vnc_dtws_v1 "#todo,窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = "127.0.0.1" #todo,服务器地址
# vnc_port = 5901  #todo, 默认 VNC 端口，根据实际情况可能有所不同
# vnc_password = "ordfe113" #todo,密码,未设置的话可以注销此行
#
# def run(target_name_list):
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # todo,注意参数名称更改
#     task=Quest_Task(py,win_hwnd[0],team_design_merged_dict,True,100,task_name_text_alternative_parameters,quest_task_word_standard_dict,target_name_list=target_name_list)
#     res=task.run(classes=2,running_time=1)
#     print(res)
#
# target_name_list=["屠狼帮众","巨狼","屠狼帮精锐","屠狼帮狼卫","屠狼帮大长老","屠狼帮头目","屠狼帮巡逻兵","散财童子",]
#
# run(target_name_list)