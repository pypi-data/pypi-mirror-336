from task.older_version.camp_task import *  # 阵营任务
from game_role.role_skill_蜀山 import * #角色技能操作
from task.task_蜀山.reward_task_template import * #悬赏任务


class Main_Task(TaskModule):
    """
    更新日志:2024-8-8 19:47:00
    主线任务模块:
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    """

    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters)

        self.camp_task_finish = False #阵营任务是否完成
        self.camp_task=False #阵营任务为特殊任务,需要另外处理
        self.reward_task = False # 奖励任务
        self.reward_task_finish=False  # 奖励任务是否完成

    def 任务信息(self):  # todo
        """
        注意,字典的4为任务信息
        任务类型:跑腿任务,打怪任务
        """
        ls_task = []  # 存储任务信息初始化
        monsters_definition = ["名录", "打倒:豪猪王(0/1)","剑客","血衣首领","豪","猪","强盗","长乐子（","屠","牙","军师","寻物","打倒"]  # 打怪任务关键字
        errand_definition = ["杂货", "学习:技能(未完成)", "寻找","张守义（未" ,"开通","剑派驿站","龙虎禁军","明月（未","阵营（未","爵位（未","王捕快（未"]  # 跑腿任务关键字
        buy_definition = ["青龙丹","武器（未"]  # 购买任务关键字
        gather_definition = ["采集", "木料"]  # 采集任务关键字

        if self.map_name and "血衣镇" in self.map_name:#副本任务
            self.task_info.update({"副本任务": "血衣镇"})
        if self.map_name and "屠狼洞" in self.map_name:
            self.task_info.update({"副本任务": "屠狼洞"})
        if self.map_name and "凤鸣山" in self.map_name:
            self.task_info.update({"副本任务": "凤鸣山"})

        if self.dic_word_ocr:
            for key, value in self.dic_word_ocr.items():
                if 4 == value[-1]:  # 任务信息
                    ls_task.append((key, value[0], value[1]))

        if ls_task:  # 任务信息
            self.task_info.update({"任务节点": "未完成"})
            for task in ls_task:
                if "已完成" in task[0] or "(完成)" in task[0]:
                    self.task_info.update({"任务节点": "完成"})
                if "交付" in task[0]:
                    self.task_info.update({"交付人": task})
                if "主线" in task[0]:
                    self.task_info.update({"主线": task})

            # 构建正则表达式
            pattern = '|'.join(monsters_definition)
            # 使用列表推导式和正则表达式来筛选
            key_word=["剑客","名录"]#起冲突的地方
            res_dict=get_values_from_keys(key_word,self.dic_word_ocr)
            logger.info("名录,凤鸣山任务")
            if len(res_dict)>=2 :
                res_list=get_value_from_key("名录",res_dict)
                # print(res_list)
                if res_list:
                    self.task_info.update({"打怪任务":("名录",*res_list[:2]) })
                    return True

            res = [item for item in ls_task if re.search(pattern, item[0]) and "主线" not in item[0]]
            if res:
                self.task_info.update({"打怪任务": res[0]})
            res = list_traversal(ls_task, errand_definition)
            if res:
                self.task_info.update({"跑腿任务": res[0]})
            res = list_traversal(ls_task, gather_definition)  # 采集任务
            if res:
                self.task_info.update({"采集任务": res[0]})
            res = list_traversal(ls_task, buy_definition)  # 购买任务
            if res:
                self.task_info.update({"购买任务": res[0]})


    def 副本任务入口(self):
        pass
    def 打怪任务入口(self):
        pass
    def 跑腿任务入口(self):
        pass
    def 采集任务入口(self):
        pass
    def 购买任务入口(self):
        pass

    def 任务完成(self):
        if get_value_from_key("升到:30级(完成)",self.dic_word_ocr):
            # logger.warning("任务完成")
            self.ls_progress="任务完成"
            self.program_result = "task_finish"
            self.task_name="1-30级主线"
            return "task_finish"

    def 任务操作(self):
        """
        具体任务逻辑操作
        """
        task_phase_flag= False #阶段性任务是否完成
        
        if self.任务完成()=="task_finish":
            return True

        if self.reward_task:#todo,奖励任务,特殊任务
            if not self.reward_task_finish:
                logger.error("悬赏任务开启")
                self.ls_progress = "任务中"
                reward_task_info=Reward_Task(self.py, self.td_hwnd, reward_merged_dict, self.debug, self.loop_count, reward_task_text_alternative_parameters)
                if reward_task_info.run()=="task_finish":
                    self.task_info.update({"任务节点": "完成"})

        elif self.camp_task:#todo,阵营任务,特殊任务
            if self.camp_task_finish:


                if "爵位提升界面" in self.game_interface[0] :#提升爵位
                    if self.py.ocr_vnc_click("陪", 406, 494, 524, 526):
                        self.py.ocr_vnc_click("位", 671,635,752,664)
                    if self.py.ocr_vnc_click("确", 688,519,777,543):#界面关闭
                        self.py.mouse_left_click(self.game_interface[0:])
                        # print("任务完成")

                if "爵位领取界面" in self.game_interface[0] and "提升" in self.dic_word_hand:
                    self.gets_stuck_flag = False
                    self.execute_coordinates=self.dic_word_hand["提升"][0][:2]
                    self.execute_delay_time=2
                    return True
            if not self.camp_task_finish:
                logger.error("阵营任务开启")
                self.ls_progress="任务中"
                #notice,merged_dict为阵营任务的资源字典
                camp_task_info=Camp_Task(self.py, self.td_hwnd, camp_merged_dict, self.debug, self.loop_count,camp_task_text_alternative_parameters)
                # res= camp_task_info.run()
                # print(res)
                if camp_task_info.run()=="task_finish" and self.get_value_from_key_operation("拥有:一个爵位(未完成)","dic_word_ocr"):#阵营任务完成
                    self.camp_task_finish=True
                    return True

        elif not self.camp_task or not self.reward_task :#普通主线任务

            if self.get_value_from_key("完成:悬赏任务(完成)","dic_word_ocr"):#悬赏任务完成
                self.task_info.update({"任务节点": "完成"})

            if get_value_from_key("悬赏任务(未完成)",self.dic_word_ocr):#悬赏任务已接
                self.reward_task= True
                return True

            elif get_value_from_key("拥有:一个爵位(未完成)",self.dic_word_ocr):#阵营任务已接
                self.camp_task= True
                return True

            else:
                if self.dic_word_hand:
                    for key, value in self.dic_word_hand.items():
                        if "福利中心" in key:
                            # print(value)
                            self.py.mouse_left_click(value[0][0], value[0][1])
                            time.sleep(2)
                            self.py.mouse_left_click(value[0][0]+340, value[0][1]+10)
                            return True
                        if "武将收服" in key:#歪嘴军师任务
                            self.py.mouse_left_click(value[0][0], value[0][1])

                if self.task_info:#3种情况

                    if self.task_info["任务节点"] == "完成" or get_value_from_key("(已完成)",self.dic_mutil_colors):  # 任务节点完成
                        logger.debug("任务节点完成")
                        self.ls_progress = ["任务中"]
                        task_phase_flag = True

                    condition_1=len(self.task_info)==2 and [key for key in self.task_info]==["任务节点","主线"] and "游戏主界面" in self.game_interface[0]
                    condition_2=len(self.task_info)==3 and [key for key in self.task_info]==["任务节点","主线","交付人"] and "游戏主界面" in self.game_interface[0]
                    if condition_1 or condition_2:#不存在任务类型情况下
                        res_clor=self.py.colors_vnc("dd130e", 1249,275,1336,290)#单色范围查找红色
                        logger.warning(f"文字识别失败,启动颜色补充,查找到的颜色坐标为{res_clor}")
                        if res_clor :
                            self.ls_progress = ["任务中"]
                            self.execute_coordinates = res_clor[0]#红色未完成
                            return True

                    if self.task_info["任务节点"] == "未完成":  # 任务节点未完成
                        self.ls_progress = ["任务中"]
                        logger.info("任务节点_未完成测试点", f"{self.task_info, self.ls_progress}")

                    if self.gets_stuck or self.coord[-1]==True:  # 有任务信息,(画面无变化或者坐标未改变)
                        logger.info("任务流程测试点")

                        if self.game_interface[0] in ["对话界面" ,"奖励界面"]:  # 出现对话界面,注意这个要在前面
                            self.execute_coordinates = (self.game_interface[1], self.game_interface[2])
                            self.execute_delay_time = 1
                            logger.warning("对话界面,奖励界面")
                            return True

                        if task_phase_flag  and "游戏主界面" in self.game_interface[0]:  # 任务阶段性交付,在游戏主画面的情况下

                            res_dict=get_value_from_key("交付人", self.task_info)
                            if res_dict:
                                self.ls_progress = ["任务中"]
                                logger.error(f"交付人:{res_dict}")
                                self.execute_coordinates = (res_dict[1] + 60, res_dict[2] + 5)
                                return True

                        if "驿站界面" in self.game_interface:  # 出现驿站界面
                            if '你开通|了驿站' in self.dic_word_hand:  # 开通驿站
                                self.execute_coordinates = (self.dic_word_hand['你开通|了驿站'][0][:2])
                                self.ls_progress = ["任务中"]
                                self.execute_delay_time = 1
                                return True

                        for key, value in self.task_info.items():

                            if self.game_interface[0] in ["阵营界面"] and len(self.dic_word_hand) > 0:  # 加入阵营任务
                                res_ocr = self.py.ocr_vnc(671, 504, 776, 539)  # OCR识别
                                # print(res_ocr)
                                if res_ocr and "阵营" in res_ocr[0][0]:
                                    self.py.mouse_left_click(res_ocr[0][1], res_ocr[0][2])
                                    return True

                            if task_phase_flag and self.game_interface[0] in ["背包界面","商城界面"]:  # 任务阶段性背包
                                self.py.mouse_left_click(self.game_interface[1], self.game_interface[2])
                                return True

                            if task_phase_flag and "杂货界面" in self.game_interface:
                                for key_hand, value_hand in self.dic_word_hand.items():
                                    if key_hand in ["确"]:
                                        self.py.mouse_left_click(value_hand[0][0], value_hand[0][1])
                                        time.sleep(1)
                                        self.py.mouse_left_click(self.game_interface[1], self.game_interface[2])
                                        return True

                            # if task_phase_flag and key in "交付人" :  # 任务阶段性交付
                            #     self.ls_progress = ["任务中"]
                            #     self.execute_coordinates = (value[1] + 60, value[2] + 5)
                            #     logger.error(f"交付人:{value[0]}")
                            #     return True

                            if not task_phase_flag:#任务节点未完成
                                condition_3 = len(self.task_info) == 1 and [key for key in self.task_info] == ["主线"] and "游戏主界面" in self.game_interface[0]
                                if condition_3 and self.dic_color_hand :#继续主线
                                    self.ls_progress = ["任务中"]
                                    self.execute_coordinates = self.dic_color_hand["ff8800"]
                                    logger.warning(f"继续主线:{value[0]}")
                                    return True

                                if "主线" in key and "继续主线" in value[0] :
                                    self.ls_progress = ["任务中"]
                                    self.execute_coordinates = (value[1], value[2])
                                    logger.warning(f"继续主线:{value[0]}")
                                    return True

                                if "任务中" in self.ls_progress:
                                    alternatives_offer_flag = True  # 颜色备选方案,默认是开启的

                                    if key in ["副本任务"] :  # 血衣镇,屠狼洞,todo,副本任务中的操作未实现
                                        alternatives_offer_flag = False #颜色备选方案关闭
                                        logger.error(f"注意,副本任务中,{value}")
                                        if value in ["血衣镇"]:#todo
                                            logger.warning("血衣镇副本中")
                                            return True
                                        elif value in ["屠狼洞"]:#todo
                                            logger.warning("屠狼洞副本中")
                                            return True
                                        elif value in ["凤鸣山"]:#todo
                                            logger.warning("凤鸣山副本中")
                                            return True

                                        # self.ls_progress = ["任务完成"]

                                    elif key in ["打怪任务"] :  # 打怪任务中的操作
                                        logger.error("打怪任务")
                                        if self.skill_combos:#技能连击启动的
                                            logger.warning("技能连击启动")
                                            Role_Skill(self.py,self.td_hwnd,role_skill_蜀山_dict,True,20).run()

                                        alternatives_offer_flag = False  # 颜色备选方案关闭
                                        if "游戏主界面" in self.game_interface:  # 主界面
                                            if len(self.target_info) == 0:  # 没有目标体的情况
                                                self.execute_coordinates = (value[1], value[2])
                                                logger.warning(f"打怪任务,寻找目标体")
                                                return True

                                            if "寻物" in value[0] and "狼" in self.target_info["目标体"] :#夜魔天狼
                                                logger.warning("寻物,夜魔天狼攻击中")
                                                self.keyboard_str = "1"  # 攻击
                                                self.execute_delay_time = 2
                                                self.skill_combos = True  # 技能连击启用
                                                return True

                                            if len(self.target_info) > 0 and len(self.task_info)>0 and len(self.task_info["打怪任务"]) > 0:
                                                target_str=self.task_info["打怪任务"][0]
                                                print(self.target_info["目标体"],target_str)

                                                for target_name in self.target_info["目标体"]:
                                                    if target_name in target_str:  # 目标体是打怪任务的目标
                                                        self.keyboard_str = "1"  # 攻击
                                                        self.execute_delay_time = 2
                                                        self.skill_combos=True# 技能连击启用
                                                        logger.warning(f"打怪任务,攻击目标体:{self.target_info['目标体']}")
                                                        return True

                                                if "子" in self.target_info["目标体"] and get_value_from_key("小黑子",self.dic_word_hand):#移动到屠狼洞
                                                    logger.warning(f"打怪任务,凤鸣山副本开始")
                                                    self.gets_stuck_flag = False#判断画面卡顿功能关闭
                                                    res = self.py.ocr_vnc_click("进|入", 561,499,628,523)
                                                    if res:
                                                        time.sleep(10)
                                                    return True

                                                elif "枯树" in self.target_info["目标体"] and get_value_from_key("枯树",self.dic_word_hand):#移动到屠狼洞
                                                    logger.warning(f"打怪任务,屠狼牙副本开始")
                                                    self.gets_stuck_flag = False#判断画面卡顿功能关闭
                                                    res = self.py.ocr_vnc_click("进|入", 564,496,692,559)
                                                    if res:
                                                        time.sleep(2)
                                                        self.py.ocr_vnc_click("确|定", 627,443,695,468)
                                                        time.sleep(10)
                                                    return True

                                                elif "铁枪" in self.target_info["目标体"]:
                                                    if "血衣镇" in self.dic_word_hand:
                                                        self.execute_coordinates = (self.dic_word_hand['血衣镇'][0][:2])  # 移动到血衣镇
                                                        self.execute_delay_time = 10
                                                        logger.warning(f"打怪任务,移动到血衣镇")
                                                        return True

                                                elif self.target_blood_bar_flag:#只存在血条,但不是打怪任务的目标
                                                    self.keyboard_str = "esc"  # 取消目标
                                                    logger.warning(f"打怪任务,取消目标体:{self.target_info['目标体']}")
                                                    time.sleep(1)
                                                    return True

                                                else:
                                                    self.keyboard_str = "tab"  # 切换目标
                                                    logger.warning(f"打怪任务,切换目标体:{self.target_info['目标体']}")
                                                    return True

                                    elif key in ["采集任务"] :  # fixme,跑腿任务中的操作
                                        logger.error("采集任务")
                                        alternatives_offer_flag = False  # 颜色备选方案关闭
                                        if "游戏主界面" in self.game_interface:  # 主界面
                                            if self.get_value_from_key_operation("上等木料","dic_word_ocr",7,1):
                                                return True

                                    elif key in ["跑腿任务"] :  # todo
                                        logger.error("跑腿任务")
                                        alternatives_offer_flag = False  # 颜色备选方案关闭
                                        if "游戏主界面" in self.game_interface:  # 主界面
                                            self.execute_coordinates = (value[1]+30, value[2]+10)
                                            return True

                                        if  "爵位领取界面" in self.game_interface[0]:#爵位任务
                                            logger.error("爵位任务,寻找阵营任务领取人,跳转到阵营任务")
                                            self.execute_coordinates=(self.game_interface[1:])
                                            self.camp_task=True#阵营任务开启
                                            return True


                                        if self.game_interface[0] in["技能界面","杂货界面"] and len(self.dic_word_hand) > 0:
                                            logger.info(f"{self.game_interface[0]}")
                                            # 在其他需要操作的界面下,把画面卡顿功能关闭,这样不会卡住
                                            self.gets_stuck_flag = False
                                            for key_hand, value_hand in self.dic_word_hand.items():
                                                if key_hand in ["确", "琴心"]:
                                                    self.mouse_left_click_op(value_hand[0][0], value_hand[0][1],1)
                                                    return True

                                        if "技能界面" in self.game_interface:
                                            self.py.mouse_left_click(self.game_interface[1], self.game_interface[2])
                                            return True

                                    elif key in ["购买任务"] and "青龙丹" in value[0] :
                                        logger.warning("购买任务,青龙丹")
                                        alternatives_offer_flag = False  # 颜色备选方案关闭
                                        if "商城界面" in self.game_interface :#注意倒序
                                            # 定义可能的键列表
                                            keys_list = ["确", "购|买", "青龙丹", "经验道具", "游戏币"]

                                            # 遍历键列表，找到第一个存在的键并设置坐标
                                            for key_word in keys_list:
                                                if key_word in self.dic_word_hand:
                                                    self.execute_coordinates = (
                                                    self.dic_word_hand[key_word][0][0], self.dic_word_hand[key_word][0][1])
                                                    break

                                        if "游戏主界面" in self.game_interface and 'res/dtws/main_task/商城.bmp' in  self.dic_image_hand.keys() :
                                            self.execute_coordinates = (self.dic_image_hand['res/dtws/main_task/商城.bmp'][0][0],
                                                                      self.dic_image_hand['res/dtws/main_task/商城.bmp'][0][1])
                                            # 在其他需要操作的界面下,把画面卡顿功能关闭,这样不会卡住
                                            self.gets_stuck_flag = False

                                        return True

                                    elif (key in ["购买任务"] and "武器" in value[0]) or (key in ["主线"] and "紫" in value[0]) :
                                        logger.warning("购买任务,紫色武器进阶")
                                        alternatives_offer_flag = False  # 颜色备选方案关闭
                                        self.gets_stuck_flag = False#卡顿功能关闭
                                        if "游戏主界面" in self.game_interface[0]:
                                            self.py.ocr_vnc_click("武器",1245,271,1341,292)
                                            return True
                                        if "装备进阶界面" in self.game_interface[0]:
                                            if self.dic_mutil_colors and "装备进阶" in self.dic_mutil_colors:
                                                self.mouse_left_click_op(self.dic_mutil_colors["装备进阶"][0][0]+70, self.dic_mutil_colors["装备进阶"][0][1]+8,2)
                                            if self.py.ocr_vnc_click("进|阶",804,359,908,398):
                                                time.sleep(2)
                                            self.py.ocr_vnc_click("确|定", 630,439,695,465)
                                            time.sleep(2)
                                            self.mouse_left_click_op(self.game_interface[1], self.game_interface[2], 2)
                                            return True

                                    if alternatives_offer_flag:#颜色备选方案
                                        mutil_colors_跑腿任务_list = ["王捕快(未完成)"]  # 跑腿任务,多颜色识别关键字
                                        for key_mutil_colors in mutil_colors_跑腿任务_list:
                                            if key_mutil_colors in self.dic_mutil_colors:
                                                self.execute_coordinates= self.dic_mutil_colors[key_mutil_colors][0]
                                                return True




main_task_scope=(1193,273,1409,312)#主线任务识别范围

#主线资源
dic_main_tasks={
    "word": {
        "琴心":(522,437,596,464,0.8,-25,21),#琴心
        "确":(630,440,738,502,0.8),#技能确定,包裹确定
        "你开通|了驿站":(480,377,592,417,0.8,211,75),#开通了驿站
        "血衣镇":(558,594,721,630,0.8),#血衣镇副本
        "小黑子":(686,172,754,201,0.8),#凤鸣山副本
        "游戏币":(829,200,919,241,0.8,0,0,1,5),#游戏币道具
        "经验道具":(383,246,468,267,0.8,0,0,1,10),#经验道具
        "青龙丹":(312,274,377,305,0.8,105,48,1,15),#青龙丹
        "购|买":(445,343,530,378,0.8,21,8,1,20),#购买
        "阵营":(671,162,777,190,0.8,228,10),#阵营界面
        "装备进阶":(652,171,740,203,0.8,320,10),#装备进阶
        "武将收服":(462,365,591,420,0.8,243,70),#武将收服
        "领取":(670,171,768,202,0.8,214,7),#爵位领取人
        "提升":(562,588,702,616,0.8),#提升爵位
        "陪":( 406,494,524,526,0.8),#陪戎效士
        },
    "image": {
        "res/dtws/main_task/上等木料.bmp":(450,205,994,614,0.8),
        "res/dtws/main_task/商城.bmp":(1195,24,1243,87,0.8)
        },
    "yolo":{"豪猪":(0,0,0,0),
            "蜀山":True,
            "铁枪":True,
    },
     "color": {
        "dd130e":(1294,277),#未完成
        },
    "mutil_colors":{
            "装备进阶":{"colors":{'53c034': (450,492),  # 主颜色
                                '65ee5a': (446,491),
                                '54d136': (453,491),
                                '6cd35c': (449,499),
                                },
                        "scope":(420,213,582,584),
                        "tolerance":20},
            "(未完成)":{"colors":{'ed140f': (1324, 294),  # 主颜色
                                'be100c': (1340, 299),
                                'cd110d': (1356, 295),
                                'dd130e': (1359, 297),
                                },
                        "scope":(1175,254,1414,326),
                        "tolerance":10},
            "上等木料":{"colors":{"3d3930":(876,273),
                                "3b342f":(872,279),
                                "342e2a":(875,286),
                                "2a2121":(867,284),
                              },
                        "scope":(681,328,770,447),
                        "tolerance":10},
            "(已完成)":{"colors":{"228822":(1383,277),
                                  "33cc33":(1385,284),
                                  "29a329":(1396,279),
                                  "1f7a1f":(1405,285),},
                        "scope":main_task_scope,
                        "tolerance":30},
            "悬赏任务（未完成)":{"colors":{"2df9f9":(1260,279),
                                      "2ae8e8":(1274,287),
                                      "21b7b7":(1299,283),
                                      "ed140f":(1324,283)},
                            "scope":(1245,272,1368,290),
                            "tolerance":20},
            "交付人:王捕快":{"colors":{"ff8800":(1267,298),
                                      "ee7f00":(1287,301),
                                      "cc6d00":(1306,298),},
                            "scope":(1259,289,1311,308),
                            "tolerance":20},
            "王捕快(未完成)":{"colors":{"2df9f9":(1256,282),
                                      "24c7c7":(1291,282),
                                      "ed140f":(1309,282),},
                            "scope":(1244,272,1353,291),
                            "tolerance":15},
            # "拥有:一个爵位(未完成)":{"colors":{"2df9f9":(1255,282),
            #                             "157474":(1270,282),
            #                             "1b9595":(1287,283),
            #                             "21b7b7":(1302,288),},
            #                 "scope":(1202,273,1373,293),
            #                 "tolerance":10},
            "交付人:苏三":{"colors":{"ff8800":(1268,293),
                                  "bb6400":(1277,294),
                                  "995200":(1288,294),},
                        "scope":(1256,288,1298,308),
                        "tolerance":30},

            }
    }


#测试
#窗口设置,获取句柄,注意类名和标题必须同时存在
win_class = "VNCMDI_Window"#窗口类名
win_title = "vnc_dtws_v1 "#窗口标题
win_hwnd=set_win(win_class,win_title)
vnc_server = "127.0.0.1"
vnc_port = 5901  # 默认 VNC 端口，根据实际情况可能有所不同
vnc_password = "ordfe113"


#资源合并
merged_dict=merge_dicts(dic_main_tasks,public_res)
# print(merged_dict)

#阵营任务信息
task_background_scope=(1174,249,1424,340)#任务信息
main_task_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
# main_task_text_alternative_parameters=task_background_scope

def run():
    #初始化VNCtools,单线程
    py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
    # 主任务运行
    task=Main_Task(py,win_hwnd[0],merged_dict,True,200,main_task_text_alternative_parameters)
    res=task.run()
    print(res)

run()










