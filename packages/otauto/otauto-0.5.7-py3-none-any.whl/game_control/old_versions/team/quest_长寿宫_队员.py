from basic_function.quest_module import *

"""
功能: 副本任务模版
更新日志: 2024-12-19 19:37:33
设计思路:

"""

class quest_长寿宫_队员(Quest_Task):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,target_name_list:list=None,queue=None,win_title:str="000",occupation=None):
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
        self.occupation=occupation #职业
        self.follow_flag=False #是否跟随
        self.assist_flag=False #是否协助
        self.last_team_dict = {} #队伍信息字典_历史记录

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
        self.queue_team_dict字典说明:
        "win_hand":游戏窗口句柄
        "task_name":任务名称
        "task_message":任务信息
        "position_info":实时位置信息
        "health_degree":血量
        "team_info":队伍信息 默认值:-1 未组队:0 已组队:1 等待组队:2
        "combat_info":战斗信息 默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动:3
    """

    def task_怒气值判断(self):
        self.ls_progress = "任务中"
        rage_flag=False
        logger.info("怒气值判断")
        if self.role_info :
            try:#避免报错停止运行11
                anger_ls = self.role_info["怒气"].split("/")
                if int(anger_ls[0]) >=60:#说明怒气值大于60
                    return True
            except Exception as e:
                pass
        elif self.get_value_from_key("怒气60+","dic_mutil_colors"):
            return True

        return rage_flag

    def task_skill_release(self,common_skill:tuple=(-1,-1),anger_skill:tuple=(-1,-1)):
        """
        技能释放
        :param common_skill:  普通技能
        :param anger_skill:   怒气技能
        :return:
        """
        if self.task_怒气值判断():
            if anger_skill != (-1,-1):
                num_rage =  random.choice(anger_skill)
                self.key_press_op(f"{num_rage}", delay_time=1.5)

        # 随机选择1到4个数字
        if common_skill != (-1,-1):
            num_to_select = random.randint(2, len(common_skill))
            # 随机选择不定数量的元素
            selected_numbers = random.sample(common_skill, num_to_select)
            # 打乱顺序
            random.shuffle(selected_numbers)
            self.key_press_op("1", delay_time=0.3)
            for skill_num in selected_numbers:
                self.key_press_op(f"{skill_num}", delay_time=1.5)

        self.key_press_op("~", delay_time=0.3)

        if self.role_info["血量"]:  # 血量
            if self.is_correct_and_compare(self.role_info["血量"]):
                logger.warning("血量低于50%,快速恢复")
                self.key_press_op("-", delay_time=1)

    def task_combating(self): #todo:增益技能没有写
        """
        战斗中
        :return:
        """
        self.key_press_op("f2", delay_time=0.5)
        self.key_press_op("f9", delay_time=1)
        self.key_press_op("F", delay_time=0.5)

        if self.occupation in ["职业_凌云",]:
            self.key_press_op("3", delay_time=2) #灵兽阵
            skill_num = random.randint(1, 3)
            self.key_press_op(f"{skill_num}", delay_time=1)
            self.key_press_op("~", delay_time=0.3)
            if not self.find_ppocr_word_op("狼|灵", 125, 115, 193, 139):
                self.key_press_op("9")

        elif self.occupation in ["职业_蜀山",]:
            common_skill = (1,3, 4, 5,6,7)
            anger_skill = (2, 8)
            self.task_skill_release(common_skill, anger_skill)

        elif self.occupation in ["职业_天煞",]:
            common_skill= (1,2,3,4,5)
            anger_skill = (6, 7,8)
            self.task_skill_release(common_skill, anger_skill)

        if self.role_info["血量"]:  # 血量
            if self.is_correct_and_compare(self.role_info["血量"]):
                logger.warning("血量低于50%,快速恢复")
                self.key_press_op("-", delay_time=1)


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
        coordinate_node_屠狼洞 = [(101, 52), (106, 55), (108, 65), (109, 76), (108, 81), (107, 86), (108, 95),
                                  (108, 100), (108, 106),(107,112) ,(111, 118), (107, 128), (109, 134),
                                  (108, 141), (108, 149), (110, 155), (117, 157), (124, 156), (132, 155),
                                  (139, 157), (143, 164), (144, 171), (143, 178), (142, 185),
                                  (134, 188), (124, 190), (118, 190), (112, 192), (108, 201), (108, 209),
                                  (109, 215), (108, 224), (100, 229), (94, 228), (87, 228),
                                  (83, 235), (84, 241), (83, 247), (85, 254), (86, 261), (86, 270), (85, 278),
                                  (85, 286), (86, 287), (84, 296), (85, 301), (78, 301), (69, 302)]

        key_info = ["目标体红名", "目标体等级", "目标体_红名", "目标体_地图红点",]  # todo:判断关键词

        if "游戏主界面" in self.game_interface[0]:
            if self.role_info["复活"]:  # 角色死亡
                self.py.mouse_left_click(*self.role_info["复活"])
                logger.success("角色复活成功")
                time.sleep(10)
                return True

            if self.get_ocr_vnc_click("饷银|物品|玉衡|奖励", 576, 433, 913, 478, delay_time=2):
                logger.info("已领取奖励")

            if self.get_ocr_vnc_click("确定", 672, 442, 739, 470, delay_time=2):
                logger.info("提示信息")

            if self.get_ocr_vnc_click("离开",558,587,633,618,delay_time=10):
                logger.info("退出副本")

            if self.get_value_from_key("连续按|空格|挣脱控制","dic_word_hand"): # 按空格键
                for i in range(3,6):
                    self.key_press_op("spacebar", delay_time=0.3)

            data_list=self.get_value_from_key("res/dtws/other/组队_摇骰子.png","dic_image_hand") #物品捡起
            if data_list:
                for data in data_list:
                    self.mouse_left_click_op(data[0], data[1], delay_time=0.5)

            if self.find_ppocr_word_op("纳魂尊者|灭魂灵兽|摄魂玄女",626, 59, 770, 99): #找到boss
                logger.info("找到boss")
                self.task_combating()
                self.follow_flag = False  # 跟随状态为False
                return True

            if self.get_items_from_all_keys([key_info[0],key_info[1]],"dic_mutil_colors") or self.find_yolo(["红色名称"]):  # 只要遇到红名或者等级,都进行战斗
                self.task_combating()
                self.follow_flag = False  # 跟随状态为False
                return True

            logger.error(f"职业:{self.occupation}")
            res=self.get_value_from_key("组队_离队标志", "dic_image_hand")
            if res:
                logger.info("离队中")
                self.key_press_op("f2", delay_time=1) #尝试选择队长
                if not self.find_imagefinder_op("res/dtws/other/组队_目标少林.png", 550, 81, 626, 175): #队长未选定
                    self.key_press_op("M", delay_time=1) #打开地图
                    if self.find_imagefinder_click("res/dtws/other/队友标志.bmp",288, 157, 1158, 710,delay_time=5,function=3): #点击队友标志
                        self.key_press_op("M", delay_time=10) #关闭地图

                    else:
                        logger.debug("未找到队友,节点移动")
                        # coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_屠狼洞)
                        # res_num = self.way_finding_node_op(coordinate_node_dispose, debug=True,range_num=5, threshold=4)
                        # if res_num == 1:
                        #     self.node_finish_flag = True
                        #     return True
                        # elif res_num == -1:
                        #     logger.error("屠狼洞节点移动失败")
                        # elif res_num == 0:
                        #     logger.info("屠狼洞节点移动中")
                else: #直接移动到队长
                    self.key_press_op("f9", delay_time=0.5)

            elif not res:
                logger.info("在队伍附近")

                if self.get_items_from_all_keys([key_info[0], key_info[1]], "dic_mutil_colors") or self.find_yolo(["红色名称"]):  # 只要遇到红名或者等级,都进行战斗
                    self.task_combating()
                    self.follow_flag = False  # 跟随状态为False

                # 查询本队队长的信息
                res_dict=self.mongodb_team_info_find_team_duty_and_number({"队伍番号": self.team_designation, "队伍职务": "1"})

                if  res_dict :
                    self.last_team_dict=res_dict # 队伍队列信息存入
                logger.info(f"队长信息last_team_dict:{self.last_team_dict}")
                if self.last_team_dict:
                    for key,vlue in self.last_team_dict.items():
                        if key=="实时位置" :
                            map,x,y=vlue
                            if map != "未知":
                                if self.map_name == map:  # 同一个地图
                                    # 假设 x 和 y 是目标坐标
                                    if self.coord and len(self.coord) == 3:
                                        coord_x, coord_y, _ = self.coord  # 提取坐标值

                                        # 检查 coord_x 和 coord_y 是否为 None
                                        if coord_x is None or coord_y is None:
                                            logger.warning("坐标的某个值为 None，无法进行计算。")
                                            return  # 早期返回

                                        # 检查地点是否相同
                                        if abs(coord_x - x) <= 3 and abs(coord_y - y) <= 3 and self.get_value_from_key('res/dtws/other/组队_目标少林.png',"dic_image_hand"):
                                            logger.info("跟随队长中")
                                            self.follow_flag = True
                                        # 检查是否启用自动跟随
                                        elif abs(coord_x - x) > 3 and abs(coord_y - y) > 3:
                                            logger.info("启用自动跟随")
                                            self.assist_flag = False  # 协助状态为 False
                                            self.follow_flag = False  # 跟随状态为 False
                                    else:
                                        logger.warning("坐标未定义或不完整，无法进行跟随判断。")
                                else:
                                    logger.error("队长移动到其他地图, 移动到队长位置")

                        if key == "交互器" :
                            if vlue==2:
                                logger.error("跟随中队长中")
                                self.queue_massage(task_message="跟随中队长中", team_info=1, combat_info=2)  # 队列信息
                                self.assist_flag=False # 协助状态为False
                                if not self.follow_flag:
                                    self.key_press_op("f2",delay_time=0.5)
                                    self.key_press_op("f9", delay_time=0.5)
                                if not self.find_imagefinder_op("res/dtws/other/组队_目标少林.png",550, 81, 626, 175):
                                    self.key_press_op("f2", delay_time=0.5)
                                    self.key_press_op("f9", delay_time=0.5)
                                else:
                                    logger.info("已跟随队长")
                            elif vlue==1:
                                logger.error("队长战斗中")
                                self.queue_massage(task_message="队长战斗中", team_info=1, combat_info=1)  # 队列信息
                                if not self.follow_flag:
                                    self.key_press_op("f2",delay_time=0.5)
                                    self.key_press_op("f9", delay_time=0.5)

                                if not self.get_items_from_all_keys([key_info[0],key_info[1]],"dic_mutil_colors"):#已锁定目标体
                                    self.assist_flag=False # 协助状态为False
                                    self.follow_flag = False  # 跟随状态为False
                                if not self.assist_flag: #队员协助中
                                    self.key_press_op("f2",delay_time=0.5)
                                    self.key_press_op("F", delay_time=0.5)
                                    self.task_combating()
                                    self.assist_flag=True # 协助状态为True
                                    self.follow_flag = False  # 跟随状态为False
                            elif vlue==3:
                                logger.error("移动中")
                                self.queue_massage(task_message="队长战斗中", team_info=1, combat_info=3)  # 队列信息
                                if not self.follow_flag:
                                    for i in range(2):
                                        self.key_press_op("f2", delay_time=0.5)
                                        self.key_press_op("f9", delay_time=0.5)
                                    self.follow_flag=True
                            elif vlue==0:
                                logger.error("未设置")

        else:
            self.界面关闭()

    def 任务操作(self):#todo,这里一般固定写法,
        #查询本队队长的信息
        res_str=self.task_flow()
        if res_str=="task_finish_all":#任务完成
            logger.info("今天副本任务全部完成")
            self.ls_progress = "任务完成"  # 模块运行结束
            self.task_name = "副本"
            self.program_result = "task_finish"
        elif res_str=="task_finish_once":#任务完成
            logger.info("副本任务完成一次,继续挑战")#todo:写再次进入副本的逻辑


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
        "连续按|空格|挣脱控制":(363, 204, 675, 261,0.8),#连续按|空格|挣脱控制
        },
    "image": {
        "res/dtws/other/组队_离队标志.png":(6, 187, 53, 370,0.8),#离队标志
        "res/dtws/other/组队_摇骰子.png":(615, 390, 684, 651,0.8),#摇骰子
        "res/dtws/other/组队_目标少林.png":(550, 81, 626, 175,0.8),#少林
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
quest_长寿宫_队员_merged_dict=merge_dicts(dic_reward_tasks,quest_task_merged_dict) #todo:更改名称

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
quest_长寿宫_队员_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
quest_长寿宫_队员_word_standard_dict={"客":"雇佣剑客","毒":"毒蜂","熊":"棕熊",}

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

# def run(target_name_list):
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # todo,注意参数名称更改
#     task=quest_长寿宫_队员(py,win_hwnd[0],quest_长寿宫_队员_merged_dict,True,100,quest_长寿宫_队员_text_alternative_parameters,quest_长寿宫_队员_word_standard_dict,target_name_list=target_name_list)
#     res=task.run(classes=2,running_time=1)
#     print(res)
#
# target_name_list=["屠狼帮众","巨狼","屠狼帮精锐","屠狼帮狼卫","屠狼帮大长老","屠狼帮头目","屠狼帮巡逻兵","散财童子",]
#
# run(target_name_list)