from basic_function.quest_module import *
"""
副本任务类模版
"""

class Quest_Task_凤鸣山(Quest_Task):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,target_name_list:list=None):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list,first_skill_flag=True,)

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
    """

    def task_特殊寻路(self):
        """
        坐标寻路识别的情况下
        :return:
        """
        way_dict={(96,95):"第二平台",  #第一座桥头
                  (85,118):"第二平台",  #第一座桥中间
                  (81, 131): "凤鸣慕情",  # 第一座桥尾
                  (74,153):"凤鸣慕情",  #凤鸣慕情
                  (101, 156): "第二座中间",  # 第二座中间
                  (122,170):"第二座桥头",  #第二座桥头
                  (157,154):"第二座中间",  #第二座中间
                  (186,165): "第二平台",  # 第二座中间
                  (149, 198): "boss",  # boss
                  }
        if self.coord and all(isinstance(x, int) for x in self.coord[:2]):#模块坐标存在的情况下
            for key,value in reversed(way_dict.items()): #倒序遍历
                if abs(self.coord[0]-key[0])<=20 and abs(self.coord[1]-key[1])<=20:#说明在范围内
                    self.get_value_from_key_operation(value,"dic_mutil_colors",delay_time=1)
                    logger.info(f"特殊寻路,{value}移动中")
                    return True
        else:
            return False


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

        # 节点坐标
        coordinate_node_凤鸣山 = [(119, 50), (113, 50), (103, 51), (97, 52), (90, 55), (89, 58), (87, 66), (89, 71),
                                  (92, 74), (95, 79), (96, 82), (101, 83),
                                  (98, 92), (95,98),(93, 103), (89, 111), (85, 120), (81, 130), (77, 140), (74, 147),
                                  (75, 152), (80, 154), (85, 152), (89, 152), (93, 155), (99, 157), (103, 157),
                                  (107, 159), (113, 159), (118, 158), (124, 157),
                                  (128, 157), (134, 156), (140, 156), (145, 156), (152, 156), (157, 155), (162, 155),
                                  (168, 154), (173, 154), (177, 154),
                                  (185, 153), (190, 154), (188, 158), (185, 163), (183, 173), (180, 181), (177, 185),
                                  (175, 191), (173, 196), (168, 199),
                                  (161, 199), (155, 199), (149, 200), (142, 200), (137, 201), (131, 202), (126, 203),
                                  (122, 202),(117,203),(113,203),(105,203),]


        coor_dict_start = {"凤鸣山": (119, 50)} #todo:副本起始坐标点
        coor_dict_end = {"凤鸣山": (122, 202)}  # todo:副本终点坐标点

        key_info = ["目标体红名", "目标体等级", "目标体_红名", "目标体_地图红点","凤鸣山上",]  # todo:判断关键词
        map_name_list =["白屏寨",]   # todo:进入副本的地点名称


        if self.get_ocr_vnc_click("奖励|物品", 698,439,782,462, delay_time=2):
                logger.info("已领取奖励")

        if self.map_name and self.map_name in "凤鸣山":#副本内
            if self.get_ocr_vnc_click("离开",556, 587, 637, 625,delay_time=10):
                logger.info("退出副本")

        if self.map_name and self.map_name in map_name_list:#城里,副本外

            if self.get_ocr_vnc_click("明日再来", 745,368,901,405, x3=-47,y3=68,delay_time=2):
                logger.info("该副本今天已经全部挑战完成")
                return "task_finish_all"

            elif self.get_ocr_vnc_click("确定",672,442,739,470,delay_time=2):
                logger.info("已退出副本,回到城池")
                return "task_finish_once"

            else:
                 logger.info("已退出副本,回到城池")
                 return "task_finish_all"

        elif self.node_finish_flag:#说明副本到了终点位置
            logger.info("副本已完成")

            if self.get_ocr_vnc_click("奖励", 698,439,782,462, delay_time=2):
                logger.info("已领取奖励")

            if self.get_ocr_vnc_click("确定", 672, 442, 739, 470, delay_time=2):
                logger.info("提示信息")

            if self.get_ocr_vnc_click("离开",558,587,633,618,delay_time=10):
                logger.info("退出副本")

            elif self.map_name == "凤鸣山":#todo:修改
                coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_凤鸣山,threshold=3)
                self.way_finding_node_op(coordinate_node_dispose,range_num=8,record_num=6)

        elif not self.node_finish_flag:#todo:修改

            if self.get_value_from_key_operation(key_info[4],"dic_word_hand"):
                logger.info("凤鸣山副本完成")
                self.node_finish_flag = True
                return True

            if (not self.node_current or self.node_current == "task_装备分解") and self.map_name in coor_dict_start:
                value_x_start, value_y_start = coor_dict_start[self.map_name]
                value_x_end, value_y_end = coor_dict_end[self.map_name]
                if self.coord and all(isinstance(x, int) for x in self.coord[:2]):
                    diff_x_start = abs(self.coord[0] - value_x_start)
                    diff_y_start = abs(self.coord[1] - value_y_start)
                    diff_x_end = abs(self.coord[0] - value_x_end)
                    diff_y_end = abs(self.coord[1] - value_y_end)
                    if diff_x_end < 10 and diff_y_end < 10 and not self.get_items_from_keys( ["目标体红名", "目标体等级",  "目标体_地图红点",],"dic_mutil_colors"):#到达boss附近,没有红点情况情况下
                        logger.info("副本完成")
                        self.node_finish_flag= True
                        return True

                    elif diff_x_start < 10 and diff_y_start < 10:
                        if self.task_装备分解()=="task_finish":
                            self.node_first_flag = True
                    else:
                        self.node_first_flag=True
                else:
                    self.node_first_flag=True

            if self.node_first_flag: #装备分解完成
                if self.find_yolo(["红名怪","红色名称"]):
                    logger.debug(f"yolo识别到目标体")
                    self.key_press_op("tab",delay_time=0.3)
                    self.key_press_op("1")
                    self.task_攻击目标()

                if  self.get_items_from_keys([key_info[0],key_info[1]],"dic_mutil_colors"):#已锁定目标体
                    self.task_攻击目标()
                elif self.get_items_from_keys([key_info[2],key_info[3]],"dic_mutil_colors"):#出现目标体
                    self.task_目标识别()
                else:#todo:未出现目标体,节点移动
                    logger.debug("未出现目标体,节点移动")
                    if self.map_name=="凤鸣山":
                        coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_凤鸣山)
                        res_num = self.way_finding_node_op(coordinate_node_dispose,debug=True, range_num=5,record_num=4)
                        if res_num == 1:
                            self.node_finish_flag = True
                            return True
                        elif res_num == -1:
                            logger.error("凤鸣山节点移动失败")
                            self.task_特殊寻路()
                        elif res_num == 0:
                            logger.info("凤鸣山节点移动中")

    def 任务操作(self):#todo,这里一般固定写法,
        res_str=self.task_flow()
        if res_str=="task_finish_all":#任务完成
            logger.info("今天副本任务全部完成")
            self.ls_progress = "任务完成"  # 模块运行结束
            self.task_name = "副本"
            self.program_result = "task_finish_all"
        elif res_str=="task_finish_once":#任务完成
            logger.info("副本任务完成一次,继续挑战")
            self.ls_progress = "任务完成"  # 模块运行结束
            self.task_name = "副本"
            self.program_result = "task_finish_one"


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

dic_reward_tasks={
    "word": {
        3:(1294,209,1373,236,0.8),#任务信息,这里改写任务信息范围
        # 2: (621,64,724,93, 0.8),#目标体信息
        "凤鸣山上":(506,364,696,407,0.8,185,74),#凤鸣山上
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
            "第二平台":{"colors":{"696e71":(1385,110),
                                "a5aeb2":(1390,106),
                                "898d88":(1390,104),
                                "909598":(1390,108),},
                        "scope":(1335,79,1412,160),
                        "tolerance":25},

            "凤鸣慕情":{"colors":{"9ba7ae":(1384,158),
                                "9eaab1":(1386,158),
                                "abb9bd":(1385,159),
                                "a7b6ba":(1384,159),},
                        "scope":(1335,79,1412,160),
                        "tolerance":25},

            "第二座桥头": {"colors": {"97a29d": (1404,176),
                                    "7a8787": (1404,174),
                                    "4b563e": (1401,176),
                                    "44503e": (1402,177), },
                         "scope": (1335, 79, 1412, 160),
                         "tolerance": 25},

            "第二座中间": {"colors": {"888e90": (1405,176),
                                    "acb0b4": (1403,176),
                                    "adb1b6": (1403,177),
                                    "a0a8ad": (1405,178), },
                         "scope": (1335, 79, 1412, 160),
                         "tolerance": 25},

            "boss":{"colors":{"5f636c":(1299,116),
                                "9498a1":(1298,115),
                                "c1c5ce":(1297,116),
                                "b9bec0":(1301,113),},
                        "scope":(1273,99,1373,180),
                        "tolerance":30},
            "出口":{"colors":{"7e858f":(1321,169),
                    "9da2a8":(1329,168),
                    "6e757f":(1342,167),
                    "676c72":(1322,177),},
            "scope":(1273,99,1373,180),
            "tolerance":30},

        }
    }


#资源合并,保持开启
quest_task_凤鸣山_merged_dict=merge_dicts(dic_reward_tasks,quest_task_merged_dict)

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
task_凤鸣山_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
quest_task_word_standard_dict={"客":"雇佣剑客","毒":"毒蜂","熊":"棕熊",}

# 过滤的关键字
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在

# win_class = "VNCMDI_Window"
# win_title = vnc_window
# win_hwnd=set_win(win_class,win_title)
# vnc_server = vnc_ip
# vnc_port = int(vnc_port)
#
# def run(target_name_list):
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port)
#     # todo,注意参数名称更改
#     task=Quest_Task_凤鸣山(py,win_hwnd[0],quest_task_凤鸣山_merged_dict,True,100,task_凤鸣山_text_alternative_parameters,quest_task_word_standard_dict,target_name_list=target_name_list)
#     res=task.run(classes=2,running_time=1,ero_num=10)
#     print(res)
#
# target_name_list=["凤鸣帮众","凤鸣精锐","凤鸣力士","凤鸣刀卫","凤鸣慕情","凤鸣术士","贱剑客","散财童子",]
#
# run(target_name_list)