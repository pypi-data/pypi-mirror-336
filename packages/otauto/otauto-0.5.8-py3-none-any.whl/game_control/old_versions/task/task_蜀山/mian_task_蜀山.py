from task.camp_task_template import *  # 阵营任务
from task.task_蜀山.quest_task_凤鸣山_蜀山 import *
from task.task_蜀山.quest_task_血衣镇_蜀山 import *
from task.task_蜀山.reward_task_template_蜀山 import * #悬赏任务
from task.camp_task_template import camp_task_word_standard_dict
from task.task_蜀山.quest_task_屠狼洞_蜀山 import *
from game_role.role_奖励领取 import * #奖励领取
from game_role.role_技能学习 import * #技能学习
from game_role.role_技能配置_蜀山 import * #技能配置
from game_role.role_装备进阶 import * #装备进阶

"""
更新日志:2024-11-17 17:09:47
手动关闭,除了拒绝交互,屏蔽队友,寻路不从驿站传送以外的功能,隐藏信息窗口,坐骑取消自动,回城图标放在最后一栏
手动加入,白屏寨的:悬赏令发布使,爵位领取人,唐军任务领取人,义军任务领取人,西域商团青城山接引人,在活动和任务栏里查找
"""

class Mian_Task_蜀山(TaskModule): #todo,修改任务名称
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,queue=None):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list,queue)
        self.task_accepted_flag = False #任务是否已领取,默认为false
        self.camp_task_finish_flag = False #阵营任务完成标志,默认为false
        self.accepted_task_list = [] #已领取任务列表
        self.completed_task = []  # 已完成的任务
        self.node_current=None #当前节点
        self.node_next=None #下一个节点
        self.node_before=None #上一个节点
        self.node_list= []  # 节点:操作,列表
        self.role_promotion_flag=False #角色能力提升标志,默认为false

        #实例化奖励领取实例
        self.award_Task = award_Task(self.py, self.td_hwnd, reward_merged_奖励领取_dict, True, 30,
                                              task_奖励领取_text_alternative_parameters,
                                              task_奖励领取_word_standard_dict)

        logger.info("主任务初始化完成")
    #todo,任务的总体流程,节点,修改
    """
    更新日志:2024-10-16 16:23:16
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    :text_alternative_parameters: 文字识别,是否去除背景色
    :word_standard_dict: 文字标准字典
    :keywords_list: 关键词列表
    """


    def combat_condition(self,first_skill_flag:bool=False,forced_attack=True,state_skill_flag=False):
        """
        战斗状态
        :param first_skill_flag: 是否使用先手技能,默认为False
        :param forced_attack: 是否强制攻击,默认为True
        :param state_skill_flag: 是否使用状态技能,默认为False
        :return:
        """
        if self.skill_combos:
            if self.skill_combos:  # 技能连击启动的
                logger.warning("技能连击启动")
                Role_Skill_蜀山(self.py, self.td_hwnd, role_skill_蜀山_dict, False, 20,forced_attack=forced_attack,first_skill_flag=first_skill_flag,state_skill_flag=state_skill_flag).run()
                self.skill_combos = False #技能连击结束,关闭技能连击

    def  role_promotion(self):
        """
        角色能力提升
        :return:
        """
        self.ls_progress ="任务中"

        award_flag=False #奖励领取标志
        skills_learn_flag=False #技能学习标志
        skills_set_flag=False #技能配置标志
        equipment_evolution_flag=False #装备进阶标志

        image_list=["res/dtws/main_task/武将图标.bmp","res/dtws/main_task/信息窗口隐藏.bmp"]
        self.get_value_from_key_operation(image_list[0], "dic_image_hand", x3=-10, y3=36,delay_time=1)

        if self.get_value_from_key("目标体等级","dic_mutil_colors"): #取消npc选择
            self.key_press_op("esc",delay_time=1)

        self.mouse_move_op(282,666,delay_time=1) #移动鼠标到信息窗口
        self.py.find_image_vnc(image_list[1], 0,763,28,789) #点击隐藏信息窗口
        if not award_flag:
            logger.info("奖励领取")

            self.award_Task.run(ero_num=10)
            award_flag=True

        if not  skills_learn_flag:
            logger.info("技能学习")
            task_技能学习(self.py,self.td_hwnd,reward_merged_技能学习_dict,True,50,task_技能学习_text_alternative_parameters,task_技能学习_word_standard_dict).run(ero_num=15)
            skills_learn_flag=True

        if not skills_set_flag:
            logger.info("技能配置")
            task_技能配置(self.py,self.td_hwnd,reward_merged_技能配置_dict,True,50,task_技能配置_text_alternative_parameters,task_技能配置_word_standard_dict).run(ero_num=15)
            skills_set_flag=True

        if not equipment_evolution_flag:
            logger.info("装备进阶")
            task_装备进阶(self.py,self.td_hwnd,reward_merged_装备进阶_dict,True,50,task_装备进阶_text_alternative_parameters,task_装备进阶_word_standard_dict).run(ero_num=10)
            equipment_evolution_flag=True

        if award_flag and skills_learn_flag and skills_set_flag and equipment_evolution_flag:
            Role_Skill_蜀山(self.py,self.td_hwnd,role_skill_蜀山_dict,True,10,).run() #todo:状态技能释放和开启自动,后面要更加职业不同更换
            return "task_finish"

    def task_继续主线(self):
        """
        1,对话界面点击对话
        2,一般都卡在对话界面
        :return:
        """

        self.ls_progress="任务中"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            self.get_value_from_key_operation("【主线】继续主线","dic_word_ocr")


    def task_拜见宁婉儿(self):
        """
        1,对话界面点击对话
        2,【主线】熟悉武器,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_拜见宁婉儿"

        if self.get_value_from_key("【主线】熟悉武器", "dic_word_ocr"):
            self.node_current = "task_熟悉武器"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:宁婉儿","拜见:宁婉儿(已完成)"],"dic_word_ocr",x3=83,y3=8):
                pass
            elif self.get_value_from_key_operation("寻找:宁婉儿(未完成)","dic_word_ocr",x3=35,y3=8):
                pass

    def task_熟悉武器(self):
        """
        1,寻找豪猪
        2,攻击豪猪
        3,交付任务
        4,【主线】打倒豪猪王,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_熟悉武器"

        if self.get_value_from_key("【主线】打倒豪猪王", "dic_word_ocr"):
            self.node_current = "task_打倒豪猪王"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif self.get_value_from_key_operation("福利中心", "dic_word_ocr",x3=337,y3=10,delay_time=1):
            logger.info("福利中心界面关闭")

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:宁婉儿","打倒:豪猪(已完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")
            elif (self.target_info and self.target_info["目标体"] == "豪猪")  or self.get_value_from_key("豪猪", "dic_mutil_colors"):
                logger.info("寻找到豪猪,开始攻击")
                self.target_info.update({"目标体": "豪猪"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启
            elif self.get_value_from_key_operation("打倒:豪猪(/5)","dic_word_ocr",x3=35,y3=8):
                logger.info("寻找豪猪中")

    def task_打倒豪猪王(self):
        """
        1,寻找豪猪王
        2,攻击豪猪
        3,交付任务王
        4,【主线】熟悉药品,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_打倒豪猪王"

        if self.get_value_from_key("【主线】熟悉药品", "dic_word_ocr"):
            self.node_current = "task_熟悉药品"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:宁婉儿","打倒:豪猪王(已完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")
            elif (self.target_info and self.target_info["目标体"] == "豪猪王")  or self.get_value_from_key("豪猪", "dic_mutil_colors"):
                logger.info("寻找到豪猪王,开始攻击")
                self.target_info.update({"目标体": "豪猪王"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启
            elif self.get_value_from_key_operation("打倒:猪王(0/1)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找豪猪王中")

    def task_熟悉药品(self):
        """
        1,寻找杂货商
        2,关闭各种界面
        3,【主线】门派的技能,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_熟悉药品"

        if self.get_value_from_key("【主线】门派的技能", "dic_word_ocr"):
            self.node_current = "task_门派的技能"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "背包界面" in self.game_interface[0]:
            self.mouse_left_click_op(*self.game_interface[1:])

        elif "杂货界面" in self.game_interface[0]:
            self.py.ocr_vnc_click("确定",671,469,738,494,x3=21,y3=7)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:宁婉儿","了解:杂货商(完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("了解:杂货商(未完成)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找杂货商中")


    def task_门派的技能(self):
        """
        1,打开技能界面
        2,学习技能
        3,关闭界面
        4,【主线】新的任务,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_门派的技能"

        if self.get_value_from_key("【主线】新的任务", "dic_word_ocr"):
            self.node_current = "task_新的任务"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "技能界面" in self.game_interface[0]:
            if self.get_value_from_key("学习:技能(完成)","dic_word_ocr"):
                self.mouse_left_click_op(*self.game_interface[1:],delay_time=1)

            elif self.get_value_from_key("学习:技能(未完成)", "dic_word_ocr"):
                colors = {'2cd530': (490,460),  '3ae652': (492,462),'75ffb9': (491,464)}
                if self.py.ocr_vnc_click("确",629,441,695,465,delay_time=1):
                    logger.info("技能学习完成")
                elif self.py.mutil_colors_vnc_click(colors,472,427,521,476,delay_time=1,x3=13,y3=-14):
                    logger.info("点击技能图标")

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:宁婉儿","学习:技能(完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("学习:技能(未完成)","dic_word_ocr",x3=38,y3=8):
                logger.info("打开技能界面")

    def task_新的任务(self):
        """
        1,寻路
        2,对话
        3,关闭界面
        4,【主线】剑客的挑战,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_新的任务"

        if self.get_value_from_key("【主线】剑客的挑战", "dic_word_ocr"):
            self.node_current = "task_剑客的挑战"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:张守义", "寻找:张守义(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:张守义(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找张守义中")


    def task_剑客的挑战(self):
        """
        1,寻找剑客
        2,攻击剑客
        3,交付任务
        4,【主线】驿站的功用,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_剑客的挑战"

        if self.get_value_from_key("【主线】驿站的功用", "dic_word_ocr"):
            self.node_current = "task_驿站的功用"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:张守义","打倒:剑客(已完成)"],"dic_word_ocr",x3=83,y3=12):
                logger.info("任务交付")

            elif (self.target_info and self.target_info["目标体"] == "剑客")  or self.get_value_from_key("贱客", "dic_mutil_colors"):
                logger.info("寻找到剑客,开始攻击")
                self.target_info.update({"目标体": "剑客"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启

            elif self.get_value_from_key_operation("打倒:剑客(/5)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找剑客中")


    def task_驿站的功用(self):
        """
        1,对话界面点击对话
        2,驿站界面操作
        3,【主线】能力的考察,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_驿站的功用"

        if self.get_value_from_key("【主线】能力的考察", "dic_word_ocr"):
            self.node_current = "task_能力的考察"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "驿站界面" in self.game_interface[0]:
            if self.get_value_from_key("开通:驿站(外)(完成","dic_word_ocr"):
               if self.py.ocr_vnc_click("确",653,423,777,487):
                   logger.info("驿站开通完成")
               elif self.mouse_left_click_op(*self.game_interface[1:],delay_time=1):
                   logger.info("点击关闭驿站界面")

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:张守义", "开通:驿站(外)(完成"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("开通:驿站(外)(未完", "dic_word_ocr", x3=50, y3=8):
                logger.info("前往驿站中")

    def task_能力的考察(self):
        """
        1,对话界面点击对话
        2,木材的识别,这里取巧,直接点击了任务附近.
        2,【主线】收服武将,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_能力的考察"

        if self.get_value_from_key("【主线】收服武将", "dic_word_ocr"):
            self.node_current = "task_收服武将"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:#notice,待优化

            if self.get_items_from_all_keys_operation(["交付人:张守义", "上等木料(已完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            else:
                if self.coord[-1] and self.get_value_from_key("采集:上等木料(/3)", "dic_word_ocr"):
                    if self.get_yolo_click("木料",delay_time=5):
                        logger.info("采集中")
                    else:
                        self.get_value_from_key_operation("采集:上等木料(/3)", "dic_word_ocr", x3=30, y3=3)

    def task_收服武将(self):#todo.血衣镇副本没有写
        """
        1,对话界面点击对话
        2,血衣镇副本操作
        2,【主线】武道灵的求助,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_收服武将"

        if self.get_value_from_key("【主线】武道灵的求助", "dic_word_ocr"):
            self.node_current = "task_武道灵的求助"
            award_Task(self.py, self.td_hwnd, reward_merged_奖励领取_dict, True, 30,
                       task_奖励领取_text_alternative_parameters, task_奖励领取_word_standard_dict).run(ero_num=10)

            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif self.map_name and "血衣镇" in self.map_name: #todo,血衣镇副本没有写
            logger.info("血衣镇副本中,配置操作信息")
            target_name_list=["断锋杀手","嗜血凶徒","残刃刺客","血衣首领","散财童子",]
            task=Quest_Task_血衣镇(self.py,self.td_hwnd,quest_task_血衣镇_merged_dict,True,100,task_血衣镇_text_alternative_parameters,quest_task_word_standard_dict,target_name_list=target_name_list)
            task.run(classes=2,running_time=1)

        elif "游戏主界面" in self.game_interface[0]:

            if self.get_items_from_all_keys_operation(["交付人:张守义", "打倒:血衣首领(已完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")

            elif self.get_value_from_key_operation("血衣镇","dic_word_hand",delay_time=10):
                logger.info("进入副本中")

            elif self.get_value_from_key_operation("打倒:血衣首领(0/1)", "dic_word_ocr", x3=30, y3=5):
                logger.info("前往副本地点中")


    def task_武道灵的求助(self):
        """
        1,对话界面点击对话
        2,驿站界面操作
        3,【主线】竹海的强盗,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_武道灵的求助"

        if self.get_value_from_key("【主线】竹海的强盗", "dic_word_ocr"):
            self.node_current = "task_竹海的强盗"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵", "寻找:武道灵(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:武道灵(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找:武道灵中")


    def task_竹海的强盗(self):
        """
        1,寻找强盗
        2,攻击强盗
        3,交付任务
        4,【主线】突如其来的隋军,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_竹海的强盗"

        if self.get_value_from_key("【主线】突如其来的隋军", "dic_word_ocr"):
            self.node_current = "task_突如其来的隋军"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵","打倒:强盗(已完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")

            elif (self.target_info and self.target_info["目标体"] == "强盗")  or self.find_ppocr_word_op("强盗",618, 63, 735, 97):
                logger.info("寻找到强盗,开始攻击")
                self.target_info.update({"目标体": "强盗"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启

            elif self.get_value_from_key_operation("打倒:强盗(/5)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找强盗中")

    def task_突如其来的隋军(self):
        """
        1,对话界面点击对话
        2,寻路
        3,【主线】危机,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_突如其来的隋军"

        if self.get_value_from_key("【主线】危机", "dic_word_ocr"):
            self.node_current = "task_危机"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵", "找人:龙虎禁军(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("找人:龙虎禁军(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("找人:龙虎禁军中")

    def task_危机(self):
        """
        1,对话界面点击对话
        2,寻路
        3,【主线】讨伐长乐子,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_危机"

        if self.get_value_from_key("【主线】讨伐长乐子", "dic_word_ocr"):
            self.node_current = "task_讨伐长乐子"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵", "找人:龙虎禁军(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("找人:龙虎禁军(未完成)", "dic_word_ocr", x3=35, y3=8):
                logger.info("找人:龙虎禁军中")

    def task_讨伐长乐子(self):
        """
        1,寻找长乐子
        2,攻击长乐子
        3,交付任务
        4,【主线】使用道具商城,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_讨伐长乐子"

        if self.get_value_from_key("【主线】使用道具商城", "dic_word_ocr"):
            self.node_current = "task_使用道具商城"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵","打倒:长乐子(已完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")

            elif (self.target_info and self.target_info["目标体"] == "长乐子")  or self.get_value_from_key("目标体长乐子", "dic_mutil_colors"):
                logger.info("寻找到长乐子,开始攻击")
                self.target_info.update({"目标体": "长乐子"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启

            elif self.get_value_from_key_operation("打倒:长乐子(0/1)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找长乐子中")
    def task_使用道具商城(self):
        """
        1,对话界面点击对话
        2,购买流程
        3,【主线】为百姓而战之路,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_使用道具商城"

        if self.get_value_from_key("【主线】为百姓而战之路", "dic_word_ocr"):
            self.node_current = "task_为百姓而战之路"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "商城界面" in self.game_interface[0]:
            if self.get_value_from_key("购买:青龙丹(完成)", "dic_word_ocr"):
                self.mouse_left_click_op(*self.game_interface[1:], delay_time=1)
                logger.info("点击关闭商城界面")

            elif self.get_value_from_key("购买:青龙丹(未完成)", "dic_word_ocr"):
                if self.py.ocr_vnc_click("确",629,440,696,466, delay_time=1): #确定
                    pass
                elif self.py.ocr_vnc_click("购|买",445, 343, 530, 378, delay_time=1): #购买
                    pass
                elif self.py.ocr_vnc_click("青龙丹",312, 274, 377, 305,delay_time=1): #青龙丹
                    pass
                elif self.py.ocr_vnc_click("经验道具",372,225,480,269, delay_time=1): #经验道具
                    pass
                elif self.py.ocr_vnc_click("游戏币",829,200,919,241,delay_time=1): #游戏币道具
                    pass

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:武道灵", "购买:青龙丹(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key("购买:青龙丹(未完成)", "dic_word_ocr"):
                self.get_value_from_key_operation("res/dtws/main_task/商城.bmp","dic_image_hand",delay_time=2)

    def task_为百姓而战之路(self):
        """
        1,对话界面点击对话
        2,寻路
        3,【主线】谁动了乞丐的馒头,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_为百姓而战之路"

        if self.get_value_from_key("【主线】谁动了乞丐的馒头", "dic_word_ocr"):
            self.node_current = "task_谁动了乞丐的馒头"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:明月", "寻找:明月(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:明月(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找:明月中")
    def task_谁动了乞丐的馒头(self):
        """
        1,对话界面点击对话
        2,寻路
        3,【主线】玲珑有难,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_谁动了乞丐的馒头"

        if self.get_value_from_key("【主线】玲珑有难", "dic_word_ocr"):
            self.node_current = "task_玲珑有难"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:疯乞丐", "寻找:疯乞丐(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:疯乞丐(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找:疯乞丐中")

    def task_玲珑有难(self):
        """
        1,对话界面点击对话
        2,寻路
        3,【主线】线索,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_玲珑有难"

        if self.get_value_from_key("【主线】线索", "dic_word_ocr"):
            self.node_current = "task_线索"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:赌鬼小王", "寻找:赌鬼小王(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:赌鬼小王(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找:赌鬼小王中")
    def task_线索(self):
        """
        1,对话界面点击对话
        2,加入流程
        3,【主线】虬髯大汉与屠狗帮,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_线索"

        if self.get_value_from_key("【主线】虬髯大汉与屠狗帮", "dic_word_ocr"):
            self.node_current = "task_虬髯大汉与屠狗帮"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif self.coord[-1] and self.find_ocr_vnc_word("推荐|义军|唐军",661,254,771,300,):
            self.coord[-1] and self.py.ocr_vnc_click("阵营",672,501,782,541, delay_time=1)

        elif self.coord[-1] and self.get_ocr_vnc_click("均衡",569,438,888,486,delay_time=1):
            self.coord[-1] and self.py.ocr_vnc_click("阵营",672,501,782,541, delay_time=1)

        elif self.coord[-1] and self.py.ocr_vnc_click("阵营",672,501,782,541, delay_time=1):
            pass

        elif self.coord[-1] and self.get_value_from_key_operation("加入:阵营(未完成)", "dic_word_ocr",x3=56,y3=8,delay_time=1):
            pass

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:虬髯大汉", "加入:阵营(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("加入:阵营(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("加入:阵营中")

    def task_虬髯大汉与屠狗帮(self):#todo,加上奖励领取,技能配置
        """
        1,对话界面点击对话
        2,屠狼牙副本操作
        2,【主线】紫装在手天下我有,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_虬髯大汉与屠狗帮"

        if not self.role_promotion_flag and (self.map_name and "屠狼洞" not in self.map_name):#角色提升
            if self.role_promotion()=="task_finish":
                self.role_promotion_flag=True

        if self.get_value_from_key("【主线】紫装在手天下我有", "dic_word_ocr"):
            self.node_current = "task_紫装在手天下我有"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif self.map_name and "屠狼洞" in self.map_name:
            logger.info("屠狼牙副本中,配置操作信息")
            target_name_list = ["屠狼帮众", "巨狼", "屠狼帮精锐", "屠狼帮狼卫", "屠狼帮大长老", "屠狼帮头目",
                                "屠狼帮巡逻兵", "散财童子", ]
            task = Quest_Task_屠狼洞(self.py, self.td_hwnd, quest_task_屠狼洞_merged_dict, True, 100,
                                     task_屠狼洞_text_alternative_parameters, quest_task_word_standard_dict,target_name_list=target_name_list)
            task.run(classes=2,running_time=1,ero_num=10)

        elif "游戏主界面" in self.game_interface[0]:

            if self.get_items_from_all_keys_operation(["交付人:虬髯大汉", "打倒:屠狼牙(已完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")

            elif self.target_info and self.target_info["目标体"] == "枯树":
                if self.py.ocr_vnc_click("确|定", 627, 443, 695, 468):
                    pass
                elif self.get_value_from_key_operation("枯树", "dic_word_hand", delay_time=10):
                    pass

            elif self.get_value_from_key_operation("打倒:屠狼牙(0/1)", "dic_word_ocr", x3=40, y3=5):
                logger.info("前往副本地点中")

    def task_紫装在手天下我有(self):
        """
        1,对话界面点击对话
        2,购买流程
        3,【主线】歪嘴的嘴,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_紫装在手天下我有"

        self.role_promotion_flag = False #角色提升标志初始化

        if self.get_value_from_key("【主线】歪嘴的嘴", "dic_word_ocr"):
            self.node_current = "task_歪嘴的嘴"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif "装备进阶界面" in self.game_interface[0]:
            if self.get_value_from_key("进阶:进阶紫色武器(完成)", "dic_word_ocr"):
                self.mouse_left_click_op(*self.game_interface[1:], delay_time=1)
                logger.info("点击关闭装备进阶界面")

            elif self.get_value_from_key("进阶:进阶紫色武器(未完成)", "dic_word_ocr"):
                if self.py.ocr_vnc_click("确定", 631, 442, 694, 465, delay_time=1):
                    pass
                elif self.py.ocr_vnc_click("进阶", 805, 360, 909, 395, delay_time=1):
                    pass

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:虬髯大汉", "进阶:进阶紫色武器(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")

            elif self.get_value_from_key_operation("进阶:进阶紫色武器(未完成)", "dic_word_ocr"):
                logger.info("打开进阶界面")


    def task_歪嘴的嘴(self):
        """
        1,对话界面点击对话
        2,屠狼牙副本操作
        2,【主线】紫装在手天下我有,该节点完成`
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_歪嘴的嘴"

        if self.get_value_from_key("【主线】十六级", "dic_word_ocr"):
            self.node_current = "task_十六级"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif self.map_name and "屠狼洞" in self.map_name:
            logger.info("屠狼牙副本中,配置操作信息")
            target_name_list = ["屠狼帮众", "巨狼", "屠狼帮精锐", "屠狼帮狼卫", "屠狼帮大长老", "屠狼帮头目",
                                "屠狼帮巡逻兵", "散财童子", ]
            task = Quest_Task_屠狼洞(self.py, self.td_hwnd, quest_task_屠狼洞_merged_dict, True, 100,
                                     task_屠狼洞_text_alternative_parameters, quest_task_word_standard_dict,
                                     target_name_list=target_name_list)
            task.run(classes=2, running_time=1,ero_num=10)

        elif "游戏主界面" in self.game_interface[0]:

            if self.get_items_from_all_keys_operation(["交付人:虬髯大汉", "抓获:歪嘴军师(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")

            elif self.target_info and self.target_info["目标体"] == "枯树":
                if self.py.ocr_vnc_click("确|定", 627, 443, 695, 468):
                    pass
                elif self.get_value_from_key_operation("枯树", "dic_word_hand", delay_time=10):
                    pass

            elif self.get_value_from_key_operation("抓获:歪嘴军师(未完成)", "dic_word_ocr", x3=40, y3=5):
                self.py.ocr_vnc_click("成功收服",589,374,673,399,x3=113,y3=74,delay_time=1)
                logger.info("前往副本地点中")

    def task_十六级(self):
        """
        1,对话界面点击对话
        2,【主线】黑风寨来客,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_十六级"

        if self.get_value_from_key("【主线】黑风寨来客", "dic_word_ocr"):
            self.node_current = "task_黑风寨来客"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:虬髯大汉", "升到:16级(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("升到:16级(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("请先刷屠狼洞副本,升级到十六级")

    def task_黑风寨来客(self):
        """
        1,对话界面点击对话
        2,【主线】密码信,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_黑风寨来客"

        if self.get_value_from_key("【主线】密码信", "dic_word_ocr"):
            self.node_current = "task_密码信"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:徐颖天", "寻找:徐颖天(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:徐颖天(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:徐颖天中")

    def task_密码信(self):
        """
        1,寻找夜魔天狼
        2,攻击夜魔天狼
        3,交付任务
        4,【主线】什么是江湖,该节点完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_密码信"

        if self.get_value_from_key("【主线】什么是江湖", "dic_word_ocr"):
            self.node_current = "task_什么是江湖"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand",x3=50,y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:徐颖天","寻物:密码信(已完成)"],"dic_word_ocr",x3=83,y3=8):
                logger.info("任务交付")

            elif (self.target_info and self.target_info["目标体"] == "夜魔天狼")  or self.get_value_from_key("目标体夜魔天狼", "dic_mutil_colors"):
                logger.info("寻找到夜魔天狼,开始攻击")
                self.target_info.update({"目标体": "夜魔天狼"}) #手动更新目标信息
                self.skill_combos = True #技能连击启动
                self.combat_condition() #战斗状态开启

            elif self.get_value_from_key_operation("寻物:密码信(0/1)","dic_word_ocr",x3=38,y3=8):
                logger.info("寻找夜魔天狼中")

    def task_什么是江湖(self):
        """
        1,对话界面点击对话
        2,【主线】青山不改绿水长流,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_什么是江湖"

        if self.get_value_from_key("【主线】青山不改绿水长流", "dic_word_ocr"):
            self.node_current = "task_青山不改绿水长流"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:徐颖天", "升到:20级(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("升到:20级(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("请先刷屠狼洞副本,升级到十六级")

    def task_青山不改绿水长流(self):
        """
        1,对话界面点击对话
        2,【主线】为了爵位,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_青山不改绿水长流"

        if self.get_value_from_key("【主线】为了爵位", "dic_word_ocr"):
            self.node_current = "task_为了爵位"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:苏三", "寻找:苏三(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:苏三(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:苏三中")

    def task_为了爵位(self):
        """
        1,对话界面点击对话
        2,完成阵营任务
        3,【主线】贱客剑客,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_为了爵位"

        if self.get_value_from_key("【主线】贱客剑客", "dic_word_ocr"):
            self.node_current = "task_贱客剑客"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:苏三", "拥有:一个爵位(完成)"], "dic_word_ocr", x3=83,
                                                      y3=8):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("拥有:一个爵位(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("寻找领取爵位任务npc中")
                if self.py.ocr_vnc_click("爵位领取人",663,170,782,206,delay_time=1,x3=213,y3=10):
                    logger.info("领取爵位任务")
                    # notice,merged_dict为阵营任务的资源字典,注意提前把npc加入收藏
                    camp_task_info = Camp_Task(self.py, self.td_hwnd, camp_merged_dict, self.debug, self.loop_count,
                                               camp_task_text_alternative_parameters,camp_task_word_standard_dict)
                    if camp_task_info.run(): #运行阵营任务
                        logger.info("阵营任务完成")
        else:
            self.界面关闭()


    def task_贱客剑客(self):
        """
               1,对话界面点击对话
               2,疯鸣山副本操作
               2,【主线】我想要四个包子,该节点完成
               :return:
               """

        self.ls_progress = "任务中"
        self.node_current = "task_贱客剑客"

        if not self.role_promotion_flag and (self.map_name and "凤鸣山" not in self.map_name) and not self.get_value_from_key("寻物:名录(已完成)","dic_word_ocr"):#角色提升
            if self.role_promotion()=="task_finish":
                self.role_promotion_flag=True

        if self.get_value_from_key("【主线】我想要四个包子", "dic_word_ocr"):
            self.node_current = "task_我想要四个包子"
            self.role_promotion_flag=False #角色提升后取消
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=50, y3=8)

        elif self.map_name and "凤鸣山" in self.map_name:
            logger.info("凤鸣山副本中,配置操作信息")
            target_name_list = ["凤鸣帮众", "凤鸣精锐", "凤鸣力士", "凤鸣刀卫", "凤鸣慕情", "凤鸣术士", "贱剑客",
                                "散财童子", ]
            task = Quest_Task_凤鸣山(self.py, self.td_hwnd, quest_task_凤鸣山_merged_dict, True, 100,
                                     task_凤鸣山_text_alternative_parameters, quest_task_word_standard_dict,
                                     target_name_list=target_name_list)
            task.run(classes=2, running_time=1,ero_num=10)

        elif "游戏主界面" in self.game_interface[0]:

            if self.get_items_from_all_keys_operation(["交付人:苏三", "寻物:名录(已完成)"], "dic_word_ocr", x3=80,
                                                      y3=5):
                logger.info("任务交付")

            elif self.get_value_from_key("寻物:名录(已完成)","dic_word_ocr"):
                self.get_value_from_key_operation("交付人:苏三","dic_mutil_colors",x3=20,y3=5)
                logger.info("任务交付")

            elif self.get_value_from_key("小黑子","dic_word_hand"):
                self.py.ocr_vnc_click("进|入", 561,499,628,523,delay_time=1)
                if self.py.ocr_vnc_click("次数", 509,363,722,411,x3=179,y3=73, delay_time=1):
                    logger.success("任务完成")
                    return "task_finish"
                else:
                    time.sleep(10)

            elif self.get_value_from_key_operation("寻物:名录(0/1)", "dic_word_ocr", x3=20, y3=2,delay_time=10):
                logger.info("前往副本地点中")

    def task_我想要四个包子(self):
        """
        1,对话界面点击对话
        2,【主线】简单的人1,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_我想要四个包子"

        self.role_promotion_flag=False #重置角色提升标记

        if self.get_value_from_key("【主线】简单的人(1)", "dic_word_ocr"):
            self.node_current = "task_简单的人1"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:苏三", "升到:25级(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("升到:25级(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("请先接取支线任务,升级到二十五级")

    def task_简单的人1(self):
        """
        1,对话界面点击对话
        2,【主线】简单的人(2),该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_简单的人1"

        if self.get_value_from_key("【主线】简单的人(2)", "dic_word_ocr"):
            self.node_current = "task_简单的人2"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:王捕快", "寻找:王捕快(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:王捕快(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:王捕快中")

    def task_简单的人2(self):
        """
        1,对话界面点击对话
        2,悬赏任务开启
        2,【主线】简单的人(3),该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_简单的人2"

        if self.get_value_from_key("【主线】简单的人(3)", "dic_word_ocr"):
            self.node_current = "task_简单的人3"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:王捕快", "完成:悬赏任务(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key("完成:悬赏任务(未完成)", "dic_word_ocr"):
                logger.info("悬赏任务接取中,跳转")
                reward_task_info = Reward_Task(self.py, self.td_hwnd, reward_merged_悬赏_dict, self.debug, self.loop_count,
                                               reward_task_text_alternative_parameters, reward_task_word_standard_dict)
                if reward_task_info.run(ero_num=10) == "task_finish":
                    logger.info("悬赏任务完成")

    def task_简单的人3(self):
        """
        1,对话界面点击对话
        2,【主线】乌部神老,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_简单的人3"

        if self.get_value_from_key("【主线】乌部神老", "dic_word_ocr"):
            self.node_current = "task_乌部神老"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:苏三", "寻找:苏三(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:苏三(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:苏三中")

    def task_乌部神老(self):
        """
        1,对话界面点击对话
        2,【主线】突变,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_乌部神老"

        if self.get_value_from_key("【主线】突变", "dic_word_ocr"):
            self.node_current = "task_突变"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:乌部神老", "寻找:乌部神老(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:乌部神老(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:乌部神老中")


    def task_突变(self):
        """
        1,对话界面点击对话
        2,【主线】乌部神老,该节点完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_突变"

        if self.get_value_from_key("【主线】伤", "dic_word_ocr"):
            self.node_current = "task_伤"
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["交付人:苏三", "寻找:苏三(完成)"], "dic_word_ocr", x3=83,
                                                      y3=3):
                logger.info("任务交付")
            elif self.get_value_from_key_operation("寻找:苏三(未完成)", "dic_word_ocr",x3=50, y3=8):
                logger.info("寻找:苏三中")


    def task_伤(self):
        """
        1,对话界面点击对话
        2,该节点完成,起号完成
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_伤"

        if self.get_items_from_keys(["升到:30级(完成)","交付人:小七"], "dic_word_ocr"):
            logger.error("恭喜你,起号完成")
            return "task_finish"

        if "对话界面" in self.game_interface[0]:
            self.get_value_from_key_operation("res/dtws/main_task/对话界面_对话点击.bmp", "dic_image_hand", x3=70, y3=8)

        elif "游戏主界面" in self.game_interface[0]:
           if self.get_value_from_key_operation("升到:30级(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("请先接取支线任务,升级到三十级")

    def handle_task(self):
        task_methods = {
            "task_继续主线":self.task_继续主线,
            'task_拜见宁婉儿': self.task_拜见宁婉儿,
            'task_熟悉武器': self.task_熟悉武器,
            "task_打倒豪猪王": self.task_打倒豪猪王,
            "task_熟悉药品": self.task_熟悉药品,
            "task_门派的技能": self.task_门派的技能,
            "task_新的任务": self.task_新的任务,
            "task_剑客的挑战": self.task_剑客的挑战,
            "task_驿站的功用": self.task_驿站的功用,
            "task_能力的考察": self.task_能力的考察,
            "task_收服武将": self.task_收服武将,
            "task_武道灵的求助": self.task_武道灵的求助,
            "task_竹海的强盗": self.task_竹海的强盗,
            "task_突如其来的隋军": self.task_突如其来的隋军,
            "task_危机": self.task_危机,
            "task_讨伐长乐子": self.task_讨伐长乐子,
            "task_使用道具商城": self.task_使用道具商城,
            "task_为百姓而战之路": self.task_为百姓而战之路,
            "task_谁动了乞丐的馒头": self.task_谁动了乞丐的馒头,
            "task_玲珑有难": self.task_玲珑有难,
            "task_线索": self.task_线索,
            "task_虬髯大汉与屠狗帮": self.task_虬髯大汉与屠狗帮,
            "task_紫装在手天下我有": self.task_紫装在手天下我有,
            "task_歪嘴的嘴": self.task_歪嘴的嘴,
            "task_十六级": self.task_十六级,
            "task_黑风寨来客": self.task_黑风寨来客,
            "task_密码信": self.task_密码信,
            "task_什么是江湖": self.task_什么是江湖,
            "task_青山不改绿水长流": self.task_青山不改绿水长流,
            "task_为了爵位": self.task_为了爵位,
            "task_贱客剑客": self.task_贱客剑客,
            "task_我想要四个包子": self.task_我想要四个包子,
            "task_简单的人1": self.task_简单的人1,
            "task_简单的人2": self.task_简单的人2,
            "task_简单的人3": self.task_简单的人3,
            "task_乌部神老": self.task_乌部神老,
            "task_突变": self.task_突变,
            "task_伤": self.task_伤,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

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
        self.ls_progress= "任务中" #固定写法
        real_time_position=None
        logger.debug(f"{self.node_current}")
        self.queue_massage(self.node_current)  # 队列信息
        if self.map_name and self.coord: #地图名称和坐标都存在的情况下
            real_time_position = f"{self.map_name}, {self.coord[0]}, {self.coord[1]}"
        self.db_handler.update_document_one("collection_task",{"句柄":self.td_hwnd}, {"任务状态":f"{self.node_current}","位置信息":real_time_position}) #更新任务状态到数据库

        task_word_key=["【主线】继续主线","【主线】拜见宁婉儿","【主线】熟悉武器","【主线】打倒豪猪王","【主线】熟悉药品","【主线】门派的技能",
                       "【主线】新的任务","【主线】剑客的挑战","【主线】驿站的功用","【主线】能力的考察","【主线】收服武将","【主线】武道灵的求助",
                       "【主线】竹海的强盗","【主线】突如其来的隋军","【主线】危机","【主线】讨伐长乐子","【主线】使用道具商城","【主线】为百姓而战之路",
                       "【主线】谁动了疯乞丐的馒头","【主线】玲珑有难","【主线】线索","【主线】虬髯大汉与屠狗帮","【主线】紫装在手天下我有",
                       "【主线】歪嘴的嘴","【主线】十六级","【主线】黑风寨来客","【主线】密码信","【主线】什么是江湖","【主线】青山不改绿水长流",
                       "【主线】为了爵位","【主线】贱客剑客","【主线】我想要四个包子","【主线】简单的人(1)","【主线】简单的人(2)","【主线】简单的人(3)",
                       "【主线】乌部神老","【主线】突变","【主线】伤"] # 主线任务关键词

        if self.get_value_from_key(task_word_key[0],"dic_word_ocr"): #【主线】继续主线
            self.task_继续主线()

        elif self.get_value_from_key(task_word_key[1],"dic_word_ocr"): #【主线】拜见宁婉儿
            self.task_拜见宁婉儿()

        elif self.get_value_from_key(task_word_key[2],"dic_word_ocr"): #【主线】熟悉武器
            self.task_熟悉武器()

        elif self.get_value_from_key(task_word_key[3],"dic_word_ocr"): #【主线】打倒豪猪王
            self.task_打倒豪猪王()

        elif self.get_value_from_key(task_word_key[4],"dic_word_ocr"): #【主线】熟悉药品
            self.task_熟悉药品()

        elif self.get_value_from_key(task_word_key[5],"dic_word_ocr"): #【主线】门派的技能
            self.task_门派的技能()

        elif self.get_value_from_key(task_word_key[6],"dic_word_ocr"): #【主线】新的任务
            self.task_新的任务()

        elif self.get_value_from_key(task_word_key[7],"dic_word_ocr"): #【主线】剑客的挑战
            self.task_剑客的挑战()

        elif self.get_value_from_key(task_word_key[8],"dic_word_ocr"): #【主线】驿站的功用
            self.task_驿站的功用()

        elif self.get_value_from_key(task_word_key[9],"dic_word_ocr"): #【主线】能力的考察
            self.task_能力的考察()

        elif self.get_value_from_key(task_word_key[10],"dic_word_ocr"): #【主线】收服武将
            self.task_收服武将()

        elif self.get_value_from_key(task_word_key[11],"dic_word_ocr"): #【主线】武道灵的求助
            self.task_武道灵的求助()

        elif self.get_value_from_key(task_word_key[12],"dic_word_ocr"): #【主线】竹海的强盗
            self.task_竹海的强盗()

        elif self.get_value_from_key(task_word_key[13],"dic_word_ocr"): #【主线】突如其来的隋军
            self.task_突如其来的隋军()

        elif self.get_value_from_key(task_word_key[14],"dic_word_ocr"): #【主线】危机
            self.task_危机()

        elif self.get_value_from_key(task_word_key[15],"dic_word_ocr"): #【主线】讨伐长乐子
            self.task_讨伐长乐子()

        elif self.get_value_from_key(task_word_key[16],"dic_word_ocr"): #【主线】使用道具商城
            self.task_使用道具商城()

        elif self.get_value_from_key(task_word_key[17],"dic_word_ocr"): #【主线】为百姓而战之路
            self.task_为百姓而战之路()

        elif self.get_value_from_key(task_word_key[18],"dic_word_ocr"): #【主线】谁动了乞丐的馒头
            self.task_谁动了乞丐的馒头()

        elif self.get_value_from_key(task_word_key[19],"dic_word_ocr"): #【主线】玲珑有难
            self.task_玲珑有难()

        elif self.get_value_from_key(task_word_key[20],"dic_word_ocr"): #【主线】线索
            self.task_线索()

        elif self.get_value_from_key(task_word_key[21],"dic_word_ocr"): #【主线】寻找线索
            self.task_虬髯大汉与屠狗帮()

        elif self.get_value_from_key(task_word_key[22],"dic_word_ocr"): #【主线】紫装在手天下我有
            self.task_紫装在手天下我有()

        elif self.get_value_from_key(task_word_key[23],"dic_word_ocr"): #【主线】歪嘴的嘴
            self.task_歪嘴的嘴()

        elif self.get_value_from_key(task_word_key[24],"dic_word_ocr"): #【主线】十六级
            self.task_十六级()

        elif self.get_value_from_key(task_word_key[25],"dic_word_ocr"): #【主线】黑风寨来客
            self.task_黑风寨来客()

        elif self.get_value_from_key(task_word_key[26],"dic_word_ocr"): #【主线】密码信
            self.task_密码信()

        elif self.get_value_from_key(task_word_key[27],"dic_word_ocr"): #【主线】什么是江湖
            self.task_什么是江湖()

        elif self.get_value_from_key(task_word_key[28],"dic_word_ocr"): #【主线】青山不改绿水长流
            self.task_青山不改绿水长流()

        elif self.get_value_from_key(task_word_key[29],"dic_word_ocr"): #【主线】为了爵位
            self.task_为了爵位()

        elif self.get_value_from_key(task_word_key[30],"dic_word_ocr"): #【主线】贱客剑客
            if self.task_贱客剑客()=="task_finish":
                return "task_finish"

        elif self.get_value_from_key(task_word_key[31],"dic_word_ocr"): #【主线】我想要四个包子
            self.task_我想要四个包子()

        elif self.get_value_from_key(task_word_key[32],"dic_word_ocr"): #【主线】简单的人1
            self.task_简单的人1()

        elif  self.get_items_from_keys([task_word_key[33],"完成:悬赏任务(未完成)"],"dic_word_ocr"): #【主线】简单的人2
            self.task_简单的人2()

        elif  self.get_value_from_key(task_word_key[34],"dic_word_ocr"): #【主线】简单的人3
            self.task_简单的人3()

        elif self.get_value_from_key(task_word_key[35],"dic_word_ocr"): #【主线】乌部神老
            self.task_乌部神老()

        elif self.get_value_from_key(task_word_key[36],"dic_word_ocr"): #【主线】突变
            self.task_突变()

        elif self.get_value_from_key(task_word_key[37],"dic_word_ocr"): #【主线】伤
            if self.task_伤()=="task_finish":
                return "task_finish"
        else:
            if not self.node_current:#判断当前节点为空,这里写任务开始
                pass #任务开始,打开任务界面,更新节点任务
            elif self.node_current: #继续任务节点
                self.handle_task()

    def 任务操作(self):#todo,这里一般固定写法,
        moving_flag = False  # 判断角色是否在移动中
        if not self.coord[-1]:  # 说明角色移动中
            res_data = self.find_colors_vnc("ffffff", 1262, 76, 1414, 208)  # 查看小地图上的移动标识
            res_dict = self.find_value_with_length(res_data, "ffffff")  # 获取颜色值,判断颜色表示是否大于4
            logger.debug(f"{res_dict}")
            if res_dict and res_dict["ffffff"]:  # 说明角色移动中
                logger.info("角色移动中,等待3秒")
                self.error_List.append(0)
                time.sleep(3)
                moving_flag = True
        if not moving_flag:
            if self.task_flow()=="task_finish":
                self.ls_progress= "任务完成" #模块运行结束
                self.task_name="1_30主线" #todo,任务名称
                self.program_result="task_finish" #todo,模块运行返回值,按需更改

        # #ui操作相关
        # key = 'running'  # 要匹配的键
        # matching_nodes = find_other_key_value(file_path_name, "句柄",str(self.td_hwnd), key)
        # logger.error(f"运行标志:{matching_nodes}")
        # if matching_nodes=="1":
        #     logger.debug("程序正常运行")
        #     """所有的节点需要接入这里才能运行,测试也是这里添加测试代码"""
        #     moving_flag = False  # 判断角色是否在移动中
        #     if not self.coord[-1]:  # 说明角色移动中
        #         res_data = self.find_colors_vnc("ffffff", 1262, 76, 1414, 208)  # 查看小地图上的移动标识
        #         res_dict = self.find_value_with_length(res_data, "ffffff")  # 获取颜色值,判断颜色表示是否大于4
        #         logger.debug(f"{res_dict}")
        #         if res_dict and res_dict["ffffff"]:  # 说明角色移动中
        #             logger.info("角色移动中,等待3秒")
        #             self.error_List.append(0)
        #             time.sleep(3)
        #             moving_flag = True
        #     if not moving_flag:
        #         if self.task_flow()=="task_finish":
        #             self.ls_progress= "任务完成" #模块运行结束
        #             self.task_name="1_30主线" #todo,任务名称
        #             self.program_result="task_finish" #todo,模块运行返回值,按需更改

        # elif matching_nodes=="0":
        #     logger.debug("程序需要停止终止")
        #     self.ls_progress= "任务完成"
        #     self.task_name="1_30主线"
        #     self.program_result="task_finish"



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
        "血衣镇": (558, 594, 721, 630, 0.8),  # 血衣镇副本
        "枯树":(678,163,772,209,0.8,-106,336),#屠狼洞副本
        "小黑子": (686, 172, 754, 201, 0.8),  # 凤鸣山副本
        # "悬赏令发布使":(578,261,783,350,0.8,0,0,1,15),
        },
    "image": {
        "res/dtws/main_task/商城.bmp":(1195,24,1243,87,0.8),#商城
        "res/dtws/main_task/武将图标.bmp":(569,731,628,778,0.8),#武将图标
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
            "交付人:宁婉儿":{"colors":{"f0e8df":(1226,295),
                                    "ff8800":(1271,298),
                                    "dd7600":(1286,301),
                                    "cc6d00":(1307,302),
                                    },
                        "scope":(1202,292,1314,307),
                        "tolerance":25},

            "交付人:苏三":{"colors":{"ff8800":(1268,294),
                                    "bb6400":(1266,299),
                                    "cc6d00":(1286,293),
                                    "dd7600":(1292,303),
                                    },
                        "scope":(1202,292,1314,307),
                        "tolerance":25},

            "豪猪":{"colors":{"c1ce3b":(667,75),
                            "c0d43a":(669,87),
                            "c7df3c":(684,79),
                            "bcd23a":(686,87),
                            },
                    "scope":(654,69,696,91),
                    "tolerance":25},

            "打倒:猪王(0/1)":{"colors":{"2df9f9":(1252,277),
                                        "27d8d8":(1273,283),
                                        "2ae8e8":(1286,281),
                                        "ed140f":(1307,280),
                                        },
                                "scope":(1246,272,1331,294),
                                "tolerance":25},

            "贱客":{"colors":{"b3c638":(665,75),
                            "c7df3c":(674,84),
                            "bbd139":(682,77),
                            "98a92f":(688,85),
                            },
                    "scope":(654,69,696,91),
                    "tolerance":25},

            "打倒:剑客(/5)":{"colors":{"2df9f9":(1252,278),
                                    "27d8d8":(1266,284),
                                    "ed140f":(1283,286),
                                    "be100c":(1305,282),
                                    },
                            "scope":(1245,272,1317,293),
                            "tolerance":25},

            "采集:上等木料(/3)":{"colors":{"2df9f9":(1255,283),
                                        "27d8d8":(1271,285),
                                        "24c7c7":(1302,284),
                                        "ed140f":(1337,285),
                                        },
                                "scope":(1249,273,1345,293),
                                "tolerance":25},

            "打倒:血衣首领(0/1)":{"colors":{"2df9f9":(1254,278),
                                        "27d8d8":(1271,281),
                                        "2ae8e8":(1281,287),
                                        "24c7c7":(1305,287),
                                        "cd110d":(1326,286),
                                        },
                                "scope":(1245,272,1347,292),
                                "tolerance":25},

            "打倒:屠狼牙(0/1)":{"colors":{"2df9f9":(1251,281),
                                        "27d8d8":(1273,283),
                                        "24c7c7":(1284,281),
                                        "cd110d":(1311,286),
                                        },
                                "scope":(1246,272,1334,292),
                                "tolerance":25},
            "目标体长乐子":{"colors":{"c7df3c":(664,80),
                                    "adc234":(683,81),
                                    "92a42c":(701,82),
                                    "a1b431":(700,79),
                                    },
                            "scope":(658,68,711,91),
                            "tolerance":25},

            "【主线】简单的人(1)":{"colors":{"fec86a":(1308,265),
                                        "dcad5c":(1318,263),
                                        "a98547":(1320,270),
                                        "cba055":(1330,269),
                                        },
                                "scope":(1303,252,1338,277),
                                "tolerance":25},

            "开通:驿站(外)(未完":{"colors":{"24c7c7":(1310,277),
                                        "2df9f9":(1356,285),
                                        "ed140f":(1384,282),
                                        "be100c":(1400,283),
                                        },
                                "scope":(1242,272,1414,294),
                                "tolerance":25},
            "寻物:名录(0/1)":{"colors":{"2df9f9":(1255,283),
                                        "2ae8e8":(1270,285),
                                        "ed140f":(1288,284),
                                        "cd110d":(1305,281),
                                        },
                                "scope":(1176,250,1362,306),
                                "tolerance":25},

        }
    }

#资源合并
"""
dic_reward_tasks:该模块资源
public_res:公共资源
"""
reward_merged_dict_蜀山=merge_dicts(dic_reward_tasks,public_res)

#任务信息,是否需要去除背景色
"""
task_background_scope:识别范围
1不启用背景色,默认是识别文字资源为数字4的资源
task_name_text_alternative_parameters=task_background_scope
2启用背景色,具体参数参考basic_function/parent_module.py里get_text_alternative方法
task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
"""
task_background_scope=(1177,251,1395,552)
task_蜀山_text_alternative_parameters=task_background_scope
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#文字模糊匹配
"""
字典形式,key为模糊匹配的关键字符串,key可以用"|"符号设置多关键字,value为标准字符串
如果需要合并请使用,参数参考public_function/public_function.py里merge_dicts方法
word_standard_dict=merge_dicts(task_name_word_standard_dict,public_dict)
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_word_standard_dict
"""
task_name_word_standard_dict={"继续":"【主线】继续主线",
                            "拜见":"【主线】拜见宁婉儿","宁":"寻找:宁婉儿(未完成)","儿":"寻找:宁婉儿(完成)","婉":"交付人:宁婉儿",
                            "器":"【主线】熟悉武器","豪":"打倒:豪猪(/5)","猪":"打倒:豪猪(已完成)",
                            "王":"【主线】打倒豪猪王","猪|王":"打倒:豪猪王(0/1)","豪|猪|王":"打倒:豪猪王(已完成)",
                            "药品":"【主线】熟悉药品","杂":"了解:杂货商(未完成)","货":"了解:杂货商(完成)",
                            "派":"【主线】门派的技能","技":"学习:技能(未完成)","能":"学习:技能(完成)",
                            "新":"【主线】新的任务","守":"寻找:张守义(未完成)","义":"寻找:张守义(完成)","张":"交付人:张守义",
                            "挑":"【主线】剑客的挑战","剑":"打倒:剑客(/5)","剑|客":"打倒:剑客(已完成)",
                            "功":"【主线】驿站的功用","站":"开通:驿站(外)(未完","驿":"开通:驿站(外)(完成",
                            "考":"【主线】能力的考察","木":"采集:上等木料(/3)","料":"上等木料(已完成)",
                            "将":"【主线】收服武将","衣":"打倒:血衣首领(0/1)","领":"打倒:血衣首领(已完成)",
                            "助":"【主线】武道灵的求助","灵":"寻找:武道灵(未完成)","道":"寻找:武道灵(完成)","武":"交付人:武道灵",
                            "竹":"【主线】竹海的强盗","强":"打倒:强盗(/5)","盗":"打倒:强盗(已完成)",
                            "其":"【主线】突如其来的隋军","禁":"找人:龙虎禁军(未完成)","虎":"找人:龙虎禁军(完成)",
                            "机":"【主线】危机",
                            "讨":"【主线】讨伐长乐子","乐":"打倒:长乐子(0/1)","长":"打倒:长乐子(已完成)",
                            "商":"【主线】使用道具商城","青":"购买:青龙丹(未完成)","丹":"购买:青龙丹(完成)",
                            "路":"【主线】为百姓而战之路","明":"寻找:明月(未完成)","月":"寻找:明月(完成)","明|月":"交付人:明月",
                            "馒":"【主线】谁动了疯乞丐的馒头","乞":"寻找:疯乞丐(未完成)","丐":"寻找:疯乞丐(完成)","疯":"交付人:疯乞丐",
                            "玲":"【主线】玲珑有难","赌":"寻找:赌鬼小王(未完成)","鬼":"寻找:赌鬼小王(完成)","小":"交付人:赌鬼小王",
                            "索":"【主线】线索","阵":"加入:阵营(未完成)","营":"加入:阵营(完成)","汉":"交付人:虬髯大汉",
                            "狗":"【主线】虬髯大汉与屠狗帮","牙":"打倒:屠狼牙(0/1)","狼":"打倒:屠狼牙(已完成)",
                            "有":"【主线】紫装在手天下我有","紫":"进阶:进阶紫色武器(未完成)","色":"进阶:进阶紫色武器(完成)",
                            "歪":"【主线】歪嘴的嘴","军":"抓获:歪嘴军师(未完成)","师":"抓获:歪嘴军师(完成)",
                            "六":"【主线】十六级","16":"升到:16级(未完成)","6级":"升到:16级(完成)",
                            "来":"【主线】黑风寨来客","徐":"寻找:徐颖天(未完成)","颖":"寻找:徐颖天(完成)","天":"交付人:徐颖天",
                            "码":"【主线】密码信","密":"寻物:密码信(0/1)","信":"寻物:密码信(已完成)",
                            "江":"【主线】什么是江湖","0级":"升到:20级(未完成)","20":"升到:20级(完成)",
                            "水":"【主线】青山不改绿水长流","三":"寻找:苏三(未完成)","苏":"寻找:苏三(完成)","三|苏":"交付人:苏三",
                            "为":"【主线】为了爵位","爵":"拥有:一个爵位(未完成)","位":"拥有:一个爵位(完成)",
                            "客":"【主线】贱客剑客","录":"寻物:名录(0/1)","名":"寻物:名录(已完成)",
                            "包":"【主线】我想要四个包子","5级":"升到:25级","25":"升到:25级(完成)",
                            "简":"【主线】简单的人(1)","捕":"寻找:王捕快(未完成)","快":"寻找:王捕快(完成)","王|捕":"交付人:王捕快",
                            "人":"【主线】简单的人(2)","悬":"完成:悬赏任务(未完成)","赏":"完成:悬赏任务(完成)",
                            "单":"【主线】简单的人(3)",
                            "部":"【主线】乌部神老","老":"寻找:乌部神老(未完成)","乌":"寻找:乌部神老(完成)","神":"交付人:乌部神老",
                            "突":"【主线】突变",
                            "伤":"【主线】伤","30级":"升到:30级(未完成)","30":"升到:30级(完成)","七":"交付人:小七",
                            }

# 倒序排列
task_蜀山_word_standard_dict_order = dict(sorted(task_name_word_standard_dict.items(), reverse=True))

# 过滤的关键字
"""
这里可以自定义,容易出错的关键词,一般不定义
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_keywords_list
"""
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#todo,窗口类名
# win_title = vnc_window#todo,窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = vnc_ip #todo,服务器地址
# vnc_port = int(vnc_port)  #todo, 默认 VNC 端口，根据实际情况可能有所不同
#
#
# def run():
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port)
#     # todo,注意参数名称更改
#     task=Mian_Task(py,win_hwnd[0],reward_merged_dict_主线,True,1200,task_主线_text_alternative_parameters,task_主线_word_standard_dict_order)
#     res=task.run()
#     logger.info(f"任务执行的结果是:{res}")
#
# run()