from task.task_少林.quest_task_悬赏_少林 import *

"""
功能:悬赏任务
更新日志:2024-11-11 18:51:48
设计思路:
1,寻找悬赏令发布使
2,购买悬赏令
3,领取悬赏任务
4,寻找疑犯
5,副本操作,未写,暂时人工完成
6,任务交付
"""

class Reward_Task(TaskModule):
    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list)
        self.task_accepted_flag = False #任务是否已领取,默认为false
        self.camp_task_finish_flag = False #阵营任务完成标志,默认为false
        self.accepted_task_list = [] #已领取任务列表
        self.completed_task = []  # 已完成的任务
        self.node_current=None #当前节点
        self.node_next=None #下一个节点
        self.node_before=None #上一个节点
        self.node_list= []  # 节点:操作,列表
        self.task_counter = 0  # 任务计数

    """
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    :text_alternative_parameters: 文字识别,是否去除背景色
    :word_standard_dict: 文字标准字典
    :keywords_list: 关键词列表
    """

    def task_寻找悬赏令发布使(self):
        """
        1打开地图界面
        2选择自动寻路界面
        3点击快速搜索,
        4点击收藏选项,提前把白屏寨的悬赏令发布使和爵位领取人加入收藏,人工设置
        5选择悬赏令发布使
        6点击自动寻路
        7关闭世界地图界面
        8悬赏令发布使界面表示该节点已完成
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_寻找悬赏令发布使"

        if "悬赏令发布使界面" in self.game_interface[0]:
            self.error_List.append(0)
            logger.info("悬赏令发布使界面表示该节点已完成")
            self.node_current = "task_购买悬赏令"
            return "task_finish"

        elif "地图界面" in self.game_interface[0]:
            logger.info("地图界面.选择任务领取人")
            if self.find_ocr_vnc_word("自动寻路",746,152,866,191):
                colors = {"859dd3": (564, 215), "849cd0": (563, 216), "8298c5": (566, 224)}
                if self.py.mutil_colors_vnc(colors, 553, 204, 612, 229):  # 在收藏界面,选择任务领取人
                    logger.info("在收藏界面,选择任务领取人")
                    self.get_ocr_vnc_click("悬赏令发布使", 580, 259, 782, 527, delay_time=1)
                    if self.get_ocr_vnc_click("自动寻路", 570, 520, 670, 573, delay_time=1):
                        self.mouse_left_click_op(*self.game_interface[1:],delay_time=2)

                elif self.get_ocr_vnc_click("收藏", 549, 199, 622, 236, delay_time=1):
                    pass

            elif self.get_ocr_vnc_click("快捷搜索", 996, 559, 1080, 585, delay_time=1):
                pass

            elif self.get_value_from_key_operation("res/dtws/camp_task/地图_npc.bmp", "dic_image_hand", delay_time=1):
                pass

        elif "游戏主界面" in self.game_interface[0]:
            if not self.coord[-1]:
                time.sleep(3)
            elif self.coord[-1]:
                self.key_press_op("M")

        else:
            self.界面关闭()

    def task_购买悬赏令(self):
        """
        1点击购买悬赏令
        2选择悬赏令数目1,右键
        3关闭购买界面
        4背包界面有悬赏令,购买完成
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_购买悬赏令"

        if "背包界面" in self.game_interface[0]:
            logger.info("4背包界面有悬赏令,购买完成")
            if self.dic_mutil_colors and "悬赏令(绿)" in self.dic_mutil_colors or self.get_value_from_key("res/dtws/reward_task/背包_悬赏令.bmp","dic_image_hand"):
                self.error_List.append(0)
                self.node_current="task_领取悬赏任务"
                return "task_finish"

        elif "悬赏令发布使界面" in self.game_interface[0]:

            if self.get_ocr_vnc_click("购买", 556, 504, 689, 527):
                logger.info("点击购买")
            elif self.get_value_from_key_operation("res/dtws/reward_task/悬赏令_数目1.bmp","dic_image_hand",2,3):
                self.mouse_left_click_op(*self.game_interface[1:])
            elif self.get_value_from_key_operation("悬赏","dic_word_hand",2,3):
               self.mouse_left_click_op(*self.game_interface[1:])

            logger.info("测试点000")

        elif "游戏主界面" in self.game_interface[0]:
            logger.info("测试点")
            self.node_current="task_寻找悬赏令发布使"

        else:
            self.界面关闭()

    def task_领取悬赏任务(self):
        """
        1 点击悬赏令,右键
        2 点击悬赏任务,右键
        3 确定领取
        4任务界面出现"疑犯","悬赏"等关键字,领取完成
        :return:
        """
        self.ls_progress= "任务中"

        if self.get_value_from_key_operation("你确认使用", "dic_word_hand", 2, 1):
            time.sleep(0.5)
            if self.find_ocr_vnc_word("只能|接受", 598, 168, 845, 205):  # 说明任务次数已经使用完毕
                logger.info("任务次数已经使用完毕")
                self.task_counter = 99  # 任务次数已经使用完毕
                self.node_current = "task_交付任务"
                return True

        elif "背包界面" in self.game_interface[0] or self.get_value_from_key("币","dic_word_hand"):
            if self.get_value_from_key("疑犯(0/1)", "dic_word_ocr"):
                logger.debug("任务领取完成")
                self.mouse_left_click_op(*self.game_interface[1:])  # 关闭背包界面
                self.error_List.append(0)
                self.node_current = "task_寻找疑犯"
                return "task_finish"

            elif self.get_value_from_key_operation("res/dtws/reward_task/悬赏任务_绿色.bmp", "dic_image_hand", 2, 3):
                self.mouse_move_op(832, 450, 1)  # 鼠标移开位置

            elif self.get_value_from_key_operation("悬赏令(绿)", "dic_word_hand", 2, 3):
                pass

        elif "游戏主界面" in self.game_interface[0]:
            self.node_current="task_寻找悬赏令发布使"

    def task_寻找疑犯(self):
        """
        1,点击疑犯
        2,自动寻路中
        3,在疑犯附近查找疑犯
        4,进入副本
        :return:
        """
        self.ls_progress= "任务中"
        self.node_current = "task_寻找疑犯"

        if self.target_info and "悬赏" in self.target_info["目标体"]: #悬赏令发布使已选定
            self.key_press_op("esc") #关闭选择

        elif self.get_value_from_key("悬赏令发布使", "dic_word_hand"):#在任务npc附近
            self.get_value_from_key_operation("疑犯(0/1)","dic_word_ocr",x3=50,y3=5,delay_time=2)

        elif "疑犯界面" in self.game_interface[0]:
            logger.info("找到疑犯,准备进入副本")
            self.node_current= "task_副本操作"
            return "task_finish"

        elif "背包界面" in self.game_interface[0]:
            self.mouse_left_click_op(*self.game_interface[1:])

        elif "游戏主界面" in self.game_interface[0] and self.coord[-1] :

            if self.get_value_from_key_operation("【删除任务】","dic_word_ocr"):
                logger.info("删除任务,任务失败")
                self.node_current = "task_寻找悬赏令发布使"
                self.task_counter+=1 #任务失败计数

            elif  self.get_yolo_click("疑犯",delay_time=5):#坐标未变化
                logger.info("找到疑犯")

            elif self.get_ocr_vnc_click("疑|犯",270,120,1056,592,x3=17,y3=122,delay_time=2):#坐标未变化
                logger.info("找到疑犯")

            elif  self.get_value_from_key_operation("疑犯(0/1)", "dic_word_ocr",x3=50,y3=5,delay_time=2):#坐标未变化
                logger.info("找疑犯中")


    def task_副本操作(self,map_name_key):
        """
        1进入副本
        2触发技能攻击
        3抓取犯人
        4离开副本
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_副本操作"
        if "疑犯界面" in self.game_interface[0]:
            self.py.ocr_vnc_click("休想",556,576,798,627)
        if self.map_name in map_name_key or self.check_elements(self.coord):#地图名称或者坐标
            logger.info("副本操作中") #todo,增加判断是否在副本中

            task = reward_悬赏(self.py, self.td_hwnd, quest_task_悬赏_merged_dict, True, 100,
                               task_悬赏_text_alternative_parameters, task_悬赏_word_standard_dict)
            task.run(classes=2, running_time=1, ero_num=10)

            return "task_finish"

    def task_交付任务(self):
        """
        1,点击交付
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_交付任务"

        if "游戏主界面" in self.game_interface[0]:
            if self.get_items_from_all_keys_operation(["点击交付","疑犯(已完成)"], "dic_word_ocr",x3=37,y3=4,delay_time=1):
                return "task_finish"
        else:
            self.界面关闭()

    def check_elements(self,coor_list):
        """坐标为2位数一般是在副本中"""
        if all(isinstance(i, int) and 10 <= i < 100 for i in coor_list[:2]):
            return True
        return False

    def handle_task(self,map_name_key):
        task_methods = {
            'task_寻找悬赏令发布使': self.task_寻找悬赏令发布使,
            'task_购买悬赏令': self.task_购买悬赏令,
            'task_领取悬赏任务': self.task_领取悬赏任务,
            'task_寻找疑犯': self.task_寻找疑犯,
            'task_副本操作': lambda: self.task_副本操作(map_name_key),
            'task_交付任务': self.task_交付任务
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

    def task_flow(self):
        """
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
        self.ls_progress= "任务中"
        map_name_key = ["疑犯", "南荒毒沼", "荒野营地","破庙","全商盟货船","北隅冰原","玻届","茫野荒坟","天孤峰","全商盟货舱",] # 任务地图
        task_word_key=["疑犯(已完成)","疑犯(0/1)"] # 任务关键词
        logger.debug(f"{self.node_current}")

        if self.map_name  and "商盟" in self.map_name: #识别不准确的时候启用
            self.map_name = "全商盟货船"

        if self.task_counter>=10:#任务失败次数超过10次,今天放弃任务
            logger.info("任务失败次数超过10次,今天放弃任务")
            return "task_finish"

        elif self.map_name in map_name_key : #副本中
            self.task_副本操作(map_name_key)

        elif self.get_items_from_keys(task_word_key,"dic_word_ocr"):
            if self.get_value_from_key("疑犯(已完成)","dic_word_ocr"):
                if self.task_交付任务()=="task_finish":
                    return "task_finish"

            elif self.get_value_from_key("疑犯(0/1)","dic_word_ocr"):
                if self.map_name in map_name_key or "疑犯" in self.game_interface[0]: #在任务地图中,在疑犯界面
                    if self.task_副本操作(map_name_key)=="task_finish":
                        return "task_finish"
                else: #在找疑犯中
                    self.task_寻找疑犯()
        else:
            if not self.node_current:
                self.task_寻找悬赏令发布使()
            elif self.node_current: #继续任务节点
                self.handle_task(map_name_key)

    def 任务操作(self):

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
                self.ls_progress= "任务完成"
                self.task_name="悬赏"
                self.program_result="task_finish"


#任务资源
scope_背包悬赏令=(638,412,1173,560)
dic_reward_tasks={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        # 2: (621,64,724,93, 0.8),#目标体信息
        # "":(522,437,596,464,0.8,-25,21),#琴心
        "快捷":(994,560,1080,584,0.8,0,0,1,5),
        "收藏":(550,199,616,234,0.8,0,0,1,10),
        "悬赏令发布使":(578,261,783,350,0.8,0,0,1,15),
        "自动寻路":( 581,536,663,559, 0.8,0,0,1,20),
        "寻路":(998,167,1083,191,0.8),#自动寻路
        "开启了阵营":(462,344,625,368,0.8,242,131),#开启阵营提示
        "可以提升":(466,375,647,405,0.8,232,73),#阵营任务可以完成
        "你确认使用":(510,366,800,401,0.8,143,73),#你确定使用悬赏令
        "贼人":(564,587,852,615,0.8),#贼人进入副本
        "币":(964,567,1048,643,0.8),#整理,说明在背包界面
        "悬赏":(587,254,652,279,0.8,-29,18),#购买悬赏令
        },
    "image": {
        r"res/dtws/camp_task/地图_npc.bmp":(1088,563,1153,618,0.8),#地图npc
        "res/dtws/reward_task/悬赏令_数目1.bmp":(546,252,610,302,0.8),#悬赏令_数目1
        "res/dtws/reward_task/悬赏任务_绿色.bmp":(*scope_背包悬赏令,0.8),#悬赏任务_绿色
        "res/dtws/reward_task/悬赏任务_蓝色.bmp":(*scope_背包悬赏令,0.8),#悬赏任务_蓝色
        "res/dtws/reward_task/背包_悬赏令.bmp":(*scope_背包悬赏令,0.8), #背包_悬赏令
        # "res/dtws/main_task/商城.bmp":(1195,24,1243,87,0.8)
        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        "蜀山":True,
        "疑犯":True,
        },
    "color": {
        #  1: (440,180), #点位
         "2df9f9": (1291, 326),#敌军粮车(未完成)
         "21b7b7": (1286, 331),#敌军粮车(未完成)
         "dd130e": (1323,326),#敌军粮车(未完成)
        },
    "mutil_colors":{
            "【悬赏】":{"colors":{"dcad5c":(1188,484),
                                "987840":(1202,485),
                                "876b39":(1221,492),
                                "edbb63":(1233,486),
                                "fec86a":(1231,496),},
                        "scope":(1177,251,1395,552),
                        "tolerance":25},

            "打倒:疑犯(0/1)":{"colors":{"1b9595":(1250,517),
                                "2ae8e8":(1259,523),
                                "2df9f9":(1267,520),
                                "1ea6a6":(1277,525),
                                "ae0f0b":(1293,521),
                                "cd110d":(1305,526),},
                        "scope":(1177,251,1395,552),
                        "tolerance":30},

            "悬赏令(绿)":{"colors":{"cf3a38":(1071,467),
                                      "cdceda":(1061,477),
                                      "2b0c22":(1086,455),},
                            "scope":scope_背包悬赏令,
                            "tolerance":25},
            "悬赏任务(未完成)":{"colors":{"2ae8e8":(1255,282),
                                      "27d8d8":(1270,286),
                                      "2df9f9":(1303,284),
                                      "ed140f":(1324,282),},
                            "scope":(1200,276,1372,304),
                            "tolerance":20},
            "交付人:王捕快":{"colors":{"ff8800":(1267,298),
                                      "ee7f00":(1287,301),
                                      "cc6d00":(1306,298),},
                            "scope":(1259,289,1311,308),
                            "tolerance":20},
        }
    }

#资源合并
reward_merged_悬赏_dict=merge_dicts(dic_reward_tasks,public_res)

#悬赏任务信息
task_background_scope=(1177,251,1395,552)
reward_task_text_alternative_parameters=task_background_scope

#文字模糊匹配
reward_task_word_standard_dict={"疑犯":"疑犯(0/1)","犯":"疑犯(已完成)","交付":"点击交付","删":"【删除任务】",}

#测试
# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#窗口类名
# win_title = "002 "#窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = "127.0.0.1"
# vnc_port = 5902  # 默认 VNC 端口，根据实际情况可能有所不同
# vnc_password = "ordfe113"
#
# def run():
#     #初始化VNCtools,单线程
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # 主任务运行
#     task=Reward_Task(py,win_hwnd[0],reward_merged_悬赏_dict,True,80,reward_task_text_alternative_parameters,reward_task_word_standard_dict)
#     res=task.run()
#     print(res)
#
# run()