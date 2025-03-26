from basic_function.quest_module import *
"""
功能:
更新日志:
设计思路:
1.
2.
3.
4.
5.
6.
"""

class reward_天孤峰(Quest_Task):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,target_name_list:list=None):
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

        key_info = ["目标体红名", "目标体等级", "目标体_红名", "目标体_地图红点", ]

        # 节点坐标
        coordinate_node_天孤峰 = {(128,54):"res/dtws/reward_task/天孤峰_1.bmp",
                                (110,88):"res/dtws/reward_task/天孤峰_2.bmp",
                                (112, 127):"res/dtws/reward_task/天孤峰_3.bmp",}


        coor_dict_start = {"天孤峰": (133,43)}
        coor_dict_end = {"天孤峰": (128, 114)}

        map_name_list =["蜀南竹海","白屏寨","少林","天煞盟","青城山",]   # todo:进入副本的地点名称

        map_neme_dict=self.get_items_from_keys(map_name_list,"dic_word_ocr")
        if map_neme_dict: #如果识别到地图名称,则纠正地图名称
            logger.info(f"地图名称纠正成功:{map_neme_dict}")
            self.map_name=key = next(iter(map_neme_dict))

        if self.map_name and self.map_name in map_name_list :
            self.get_ocr_vnc_click("确定", 670, 440, 737, 465)
            logger.info("回到城池,副本任务完成")
            return "task_finish"

        elif self.node_finish_flag:#说明副本到了终点位置
            logger.info("副本已完成")

            if self.get_ocr_vnc_click("离开",558,587,633,618,delay_time=10):
                logger.info("退出副本")
                return True

            if self.get_value_from_key_operation("捕获成功", "dic_word_hand", delay_time=2):
                logger.info("副本完成")
                self.node_finish_flag = True
                return True

            if "游戏主界面" in self.game_interface[0]:
                self.key_press_op("M",delay_time=1)
            elif "地图界面" in self.game_interface[0]:
                if self.get_value_from_key_operation("出口","dic_word_hand",delay_time=25,mouse_button=3):
                    logger.info("点击地图出口")
                elif self.get_value_from_key_operation("res/dtws/reward_task/出口.bmp","dic_image_hand",delay_time=25,mouse_button=3):
                    logger.info("点击地图出口")

        elif not self.node_finish_flag:

            condition_1=self.get_items_from_keys( ["目标体红名", "目标体等级",  "目标体_地图红点",],"dic_mutil_colors")
            condition_2=self.get_items_from_keys( ["红色名称", "红名怪", ],"dic_yolo_ocr")

            if condition_1 or condition_2: #已锁定目标体
                logger.info("目标体出现")
                if self.get_items_from_all_keys([key_info[0], key_info[1]], "dic_mutil_colors"):  # 已锁定目标体
                    self.task_攻击目标()

                elif self.get_items_from_keys([key_info[2], key_info[3]], "dic_mutil_colors"):  # 出现目标体
                    self.task_目标识别()

            if not condition_1 and not condition_2: #未锁定目标体

                npc_name_list = ['res/dtws/reward_task/通缉犯.bmp', "res/dtws/reward_task/霸山虎.bmp",
                                 "res/dtws/reward_task/异族细作.bmp", "res/dtws/reward_task/血路独行.bmp",
                                 "res/dtws/reward_task/七窍玲珑.bmp",]
                if self.get_items_from_keys_operation(npc_name_list, "dic_image_hand", delay_time=5):
                    logger.info("捕获")
                    return True

                if self.get_value_from_key_operation("捕获成功", "dic_word_hand", delay_time=2):
                    logger.info("副本完成")
                    self.node_finish_flag = True
                    return True

                if  self.map_name in coor_dict_start: #根据坐标判断
                    value_x_end, value_y_end = coor_dict_end[self.map_name]
                    if self.coord and all(isinstance(x, int) for x in self.coord[:2]):
                        diff_x_end = abs(self.coord[0] - value_x_end)
                        diff_y_end = abs(self.coord[1] - value_y_end)
                        if diff_x_end < 10 and diff_y_end < 10 :
                            logger.info("副本完成")
                            self.node_finish_flag= True
                            return True

                logger.debug("未出现目标体,节点移动")
                if self.coord and all(isinstance(x, int) for x in self.coord[:2]):
                    for key, value in coordinate_node_天孤峰.items():
                        if abs(self.coord[0]-key[0])<15 and abs(self.coord[1]-key[1])<15: #判断是否在节点附近
                            self.get_value_from_key_operation(value,"dic_image_hand",delay_time=6)
                            return True

    def 任务操作(self):
        res_str=self.task_flow()
        if res_str=="task_finish":#任务完成
            logger.info("今天副本任务完成")
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

dic_reward_tasks={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        # 2: (621,64,724,93, 0.8),#目标体信息
        "捕获成功":(507,367,597,404,0.8,185,74),
        "出口":(403,510,623,673,0.8,45,-19),
        },
    "image": {
        "res/dtws/reward_task/天孤峰_1.bmp":(1256,74,1415,204,0.8,0,15),#小地图1
        "res/dtws/reward_task/天孤峰_2.bmp":(1256,74,1415,204,0.8),#小地图1
        "res/dtws/reward_task/天孤峰_3.bmp":(1256,74,1415,204,0.8),#小地图3
        "res/dtws/reward_task/通缉犯.bmp": (371, 136, 973, 696, 0.8, 16, 123),  # 场景
        "res/dtws/reward_task/霸山虎.bmp": (371, 136, 973, 696, 0.8, 18, 157),  # 场景
        "res/dtws/reward_task/异族细作.bmp":(371, 136, 973, 696, 0.8, 41, 145),  # 场景
        "res/dtws/reward_task/血路独行.bmp":(371, 136, 973, 696, 0.8, 18, 138),  # 场景
        "res/dtws/reward_task/七窍玲珑.bmp":(371, 136, 973, 696, 0.8, 22, 176),  # 场景
        "res/dtws/reward_task/出口.bmp": (403,510,623,673, 0.8, 36, -24),

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
quest_task_天孤峰_merged_dict=merge_dicts(dic_reward_tasks,quest_task_merged_dict) #todo:更改名称

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
task_天孤峰_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
quest_task_word_standard_dict={"海":"蜀南竹海","少":"少林","寨":"白屏寨","盟":"天煞盟","青":"青城山",}

# 过滤的关键字
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在
win_class = "VNCMDI_Window"#todo,窗口类名
win_title = "002 "#todo,窗口标题
win_hwnd=set_win(win_class,win_title)
vnc_server = "127.0.0.1" #todo,服务器地址
vnc_port = 5902  #todo, 默认 VNC 端口，根据实际情况可能有所不同
vnc_password = "ordfe113" #todo,密码,未设置的话可以注销此行

def run(target_name_list):
    #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
    py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
    # todo,注意参数名称更改
    task=reward_天孤峰(py,win_hwnd[0],quest_task_天孤峰_merged_dict,True,100,task_天孤峰_text_alternative_parameters,quest_task_word_standard_dict,target_name_list=target_name_list)
    res=task.run(classes=2,running_time=1,ero_num=10)
    print(res)

target_name_list=["圣火教徒","圣火教长",]

run(target_name_list)