# from basic_function.parent_module import *
import time

#测试
from basic_function.vnc.vnc_tools import *
from public_function.public_function import *
from public_function.public_resources import *

class Camp_Task(TaskModule):
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
        self.task_word_list=["探查敌情","探查粮仓","探查通路","探查刀魔","捕获毒蜂"]
        self.accepted_task_list=[] #已领取任务列表
    #todo,任务的总体流程,节点,修改
    """
    更新日志:2024-10-16 16:23:16
    流程:1,悬赏任务领取
        2,
        3,
        4,
        5,
        6,
        7,
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    :text_alternative_parameters: 文字识别,是否去除背景色
    :word_standard_dict: 文字标准字典
    :keywords_list: 关键词列表
    """

    def task_任务领取人(self): #todo,修改节点名称,并在说明中写具体操作顺序
        """
        1,打开地图
        2,自动寻路界面
        3,快速搜索
        4,收藏界面
        5,自动寻路
        6,关闭世界界面
        7,
        8,
        :return:
        """

        self.ls_progress="任务中"
        self.node_current="task_任务领取人"

        # if "悬赏令发布使界面" in self.game_interface[0]:#todo,完成条件,根据实际修改
        #     self.error_List.append(0)
        #     logger.info("5,")
        #     self.node_current = "task_node_name_02" #todo,修改节点名称,最后一个节点,删除
        #     return "task_finish"

        if "任务领取板界面" in self.game_interface[0]:
            res_task_list=self.find_ocr_vnc_scope(532, 277, 639, 398)
            # print(res_task_list)
            if res_task_list:
                for task_word in self.task_word_list:
                    for task_name, x, y, _ in res_task_list :
                        if task_word in task_name and "接" in task_name:#任务已接
                            self.accepted_task_list.append((task_word, x, y))
                        elif task_word in task_name and "接" not in task_name: #任务未接
                            self.mouse_left_click_op(x, y,delay_time=1)
                            self.get_ocr_vnc_click("领取", 778, 700, 875, 751,delay_time=1)
            self.accepted_task_list=list(set(self.accepted_task_list)) #去重
            if len(self.accepted_task_list) == 5: #5个任务都领取完毕
                self.mouse_left_click_op(*self.game_interface[1:],delay_time=1)
                logger.info("阵营任务领取完毕,关闭")

        elif "地图界面" in self.game_interface[0]:
            logger.info("地图界面.选择任务领取人")
            if self.get_ocr_vnc_click("收|藏",557, 207, 609, 232):
                logger.info("收藏界面")
                if self.get_value_from_key("res/dtws/camp_task/义军图腾.bmp","dic_image_hand"):
                    self.get_ocr_vnc_click("义军任务领取人", 580,259,782,527, delay_time=1)
                    self.get_ocr_vnc_click("自动寻路", 570,520,670,573, delay_time=1)

                elif self.get_value_from_key("res/dtws/camp_task/唐军图腾.bmp","dic_image_hand"):
                    self.get_ocr_vnc_click("唐军任务领取人", 580,259,782,527, delay_time=1)
                    self.get_ocr_vnc_click("自动寻路", 570, 520, 670, 573, delay_time=1)

            elif self.get_ocr_vnc_click("收藏", 549,199,622,236, delay_time=1):
                pass

            elif self.get_ocr_vnc_click("快捷搜索",996,559,1080,585,delay_time=1):
                pass

            elif self.get_value_from_key_operation("res/dtws/camp_task/地图_npc.bmp","dic_image_hand",delay_time=1):
                pass

        elif "游戏主界面" in self.game_interface[0]:
            self.key_press_op("M")

    def task_探查敌情(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """

        self.ls_progress = "任务中"
        self.node_current = "task_探查敌情"

        if "游戏主界面" in self.game_interface[0]:
            if self.get_value_from_key_operation("【点击交付】", "dic_word_ocr", x3=33,
                                                      y3=3,delay_time=1):
                logger.info("任务交付")
                self.get_ocr_vnc_click("确",670,466,738,493,delay_time=1)
                self.node_current = "task_探查粮仓"
                return "task_finish"

            elif self.get_value_from_key_operation("侦查:敌军粮车(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("侦查:敌军粮车中")

        else:
            self.界面关闭()

    def task_探查粮仓(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_探查粮仓"

        if "游戏主界面" in self.game_interface[0]:
            if self.get_value_from_key_operation("【点击交付】", "dic_word_ocr", x3=33,
                                                      y3=3,delay_time=1):
                logger.info("任务交付")
                self.get_ocr_vnc_click("确",670,466,738,493,delay_time=1)
                self.node_current = "task_探查通路"
                return "task_finish"

            elif self.get_value_from_key_operation("侦查:梨花1(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("侦查中")

    def task_探查通路(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_探查通路"

        if "游戏主界面" in self.game_interface[0]:
            if self.get_value_from_key_operation("【点击交付】", "dic_word_ocr", x3=33,
                                                 y3=3, delay_time=1):
                logger.info("任务交付")
                self.get_ocr_vnc_click("确", 670, 466, 738, 493, delay_time=1)
                self.node_current = "task_探查刀魔"
                return "task_finish"

            elif self.get_value_from_key_operation("侦查:梨花2(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("侦查中")

    def task_探查刀魔(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_探查刀魔"

        if "游戏主界面" in self.game_interface[0]:
            if self.get_value_from_key_operation("【点击交付】", "dic_word_ocr", x3=33,
                                                 y3=3, delay_time=1):
                logger.info("任务交付")
                self.get_ocr_vnc_click("确", 670, 466, 738, 493, delay_time=1)
                return "task_finish"

            elif self.get_value_from_key_operation("侦查:梨花3(未完成)", "dic_word_ocr", x3=50, y3=8):
                logger.info("侦查中")

    def task_爵位领取(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """
        self.ls_progress = "任务中"
        self.node_current = "task_爵位领取"

        if "爵位提升界面" in self.game_interface[0]:
            logger.info("爵位提升界面")
            if self.get_value_from_key("拥有:一个爵位(未完成)","dic_word_ocr"):
                if self.get_ocr_vnc_click("陪", 406, 494, 524, 526,delay_time=1):
                    self.get_ocr_vnc_click("位", 671, 635, 752, 664,delay_time=1)
                elif self.get_ocr_vnc_click("确", 688, 519, 777, 543,delay_time=1):  # 界面关闭
                    self.mouse_left_click_op(*self.game_interface[1:],delay_time=1)
            else:
                self.mouse_left_click_op(*self.game_interface[1:],delay_time=1)

        elif "游戏主界面" in self.game_interface[0]:
            logger.info("游戏主界面")
            if self.get_ocr_vnc_click("提升",549,575,716,628,delay_time=3):
                logger.info("打开爵位提升界面")

            elif self.get_value_from_key("拥有:一个爵位(完成)","dic_word_ocr"):
                self.get_ocr_vnc_click("确", 688, 519, 777, 543, delay_time=1)
                logger.info("爵位提升完成")
                return "task_finish"

            elif self.get_value_from_key_operation("拥有:一个爵位(未完成)", "dic_word_ocr",delay_time=1, x3=50,y3=8):
                logger.info("寻找爵位领取人")

    def handle_task(self):
        task_methods = {
            'task_任务领取人': self.task_任务领取人,
            'task_探查敌情': self.task_探查敌情,
            "task_探查粮仓": self.task_探查粮仓,
            "task_探查通路": self.task_探查通路,
            "task_探查刀魔": self.task_探查刀魔,
            "task_捕获毒蜂": self.task_爵位领取,


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
        logger.debug(f"{self.node_current}")

        task_word_key=["【阵营】【后勤】探查敌情","【阵营】【后勤】探查粮仓","【阵营】【后勤】探查通路","【阵营】【后勤】探查刀魔",
                       "【阵营】【后勤】捕获毒蜂",]

        if self.get_value_from_key_operation("可以提升","dic_word_hand"):
            if self.task_爵位领取()=="task_finish":
                return "task_finish"

        elif self.get_value_from_key(task_word_key[0], "dic_word_ocr"):  # 【阵营】【后勤】探查敌情
            self.task_探查敌情()

        elif self.get_value_from_key(task_word_key[1], "dic_word_ocr"):  # 【阵营】【后勤】探查粮仓
            self.task_探查粮仓()

        elif self.get_value_from_key(task_word_key[2], "dic_word_ocr"):  # 【阵营】【后勤】探查通路
            self.task_探查通路()

        elif self.get_value_from_key(task_word_key[3], "dic_word_ocr"):  # 【阵营】【后勤】探查刀魔
            self.task_探查刀魔()

        elif self.get_value_from_key(task_word_key[4], "dic_word_ocr"):  # 【阵营】【后勤】捕获毒蜂
            if self.task_爵位领取() == "task_finish":
                return "task_finish"

        else:
            if not self.node_current:#判断当前节点为空,这里写任务开始
                self.task_任务领取人()
            elif self.node_current: #继续任务节点
                self.handle_task()

    def 任务操作(self):#todo,这里一般固定写法,
        """所有的节点需要接入这里才能运行,测试也是这里添加测试代码"""
        moving_flag=False #判断角色是否在移动中
        if not self.coord[-1]:  # 说明角色移动中
            res_data = self.find_colors_vnc("ffffff", 1262, 76, 1414, 208)  # 查看小地图上的移动标识
            res_dict = self.find_value_with_length(res_data, "ffffff")  # 获取颜色值,判断颜色表示是否大于4
            logger.debug(f"{res_dict}")
            if res_dict and res_dict["ffffff"]:  # 说明角色移动中
                logger.info("角色移动中,等待3秒")
                self.error_List.append(0)
                time.sleep(3)
                moving_flag=True
        if not moving_flag:
            if self.task_flow() == "task_finish":
                self.ls_progress = "任务完成"  # 模块运行结束
                self.task_name = "阵营"  # todo,任务名称
                self.program_result = "task_finish"  # todo,模块运行返回值,按需更改


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
        "自动寻路":(756,157,846,184,0.8),#自动寻路
        "可以提升":(466,375,647,405,0.8,232,73),#阵营任务可以完成
        },
    "image": {
        r"res/dtws/camp_task/地图_npc.bmp":(1088,563,1153,618,0.8),#地图npc
        "res/dtws/camp_task/义军图腾.bmp":(649, 817, 691, 872,0.8),#义军图腾
        "res/dtws/camp_task/唐军图腾.bmp":(649, 817, 691, 872,0.8),#唐军图腾
        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        # "蜀山":True,
        },
    "color": {
        #  1: (440,180), #点位
        #  "2df9f9": (1291, 326),#敌军粮车(未完成)
        },
    "mutil_colors":{
            # "【悬赏】":{"colors":{"dcad5c":(1188,484),
            #                     "987840":(1202,485),
            #                     "876b39":(1221,492),
            #                     "edbb63":(1233,486),
            #                     "fec86a":(1231,496),},
            #             "scope":(1177,251,1395,552),
            #             "tolerance":25},
        }
    }

#资源合并
"""
dic_reward_tasks:该模块资源
public_res:公共资源
"""
camp_merged_dict=merge_dicts(dic_reward_tasks,public_res)

#任务信息,是否需要去除背景色
"""
task_background_scope:识别范围
1不启用背景色,默认是识别文字资源为数字4的资源
task_name_text_alternative_parameters=task_background_scope
2启用背景色,具体参数参考basic_function/parent_module.py里get_text_alternative方法
task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
"""
camp_background_scope=(1177,251,1395,552)
camp_task_text_alternative_parameters=camp_background_scope
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#文字模糊匹配
"""
字典形式,key为模糊匹配的关键字符串,key可以用"|"符号设置多关键字,value为标准字符串
如果需要合并请使用,参数参考public_function/public_function.py里merge_dicts方法
word_standard_dict=merge_dicts(task_name_word_standard_dict,public_dict)
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_word_standard_dict
"""
camp_task_word_standard_dict={"情":"【阵营】【后勤】探查敌情","粮":"侦查:敌军粮车(未完成)","车":"侦查:敌军粮车(完成)",
                                "仓":"【阵营】【后勤】探查粮仓","1":"侦查:梨花1(未完成)",
                                "通": "【阵营】【后勤】探查通路", "2": "侦查:梨花2(未完成)",
                                "刀": "【阵营】【后勤】探查刀魔", "3": "侦查:梨花3(未完成)",
                                "捕": "【阵营】【后勤】捕获毒蜂", "毒": "寻物:捕获的毒蜂(0/5)",
                                "为":"【主线】为了爵位","爵":"拥有:一个爵位(未完成)","位":"拥有:一个爵位(完成)",
                                "交|付":"【点击交付】",
                              }

# 过滤的关键字
"""
这里可以自定义,容易出错的关键词,一般不定义
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_keywords_list
"""
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
# def run():
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # todo,注意参数名称更改
#     task=Camp_Task(py,win_hwnd[0],camp_merged_dict,True,50,camp_task_text_alternative_parameters,camp_task_word_standard_dict)
#     res=task.run()
#     print(res)
#
# run()