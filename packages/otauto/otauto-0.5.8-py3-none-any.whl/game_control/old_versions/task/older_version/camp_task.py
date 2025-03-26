# from basic_function.parent_module import *
import time

#测试
from basic_function.vnc.vnc_tools import *
from public_function.public_function import *
from public_function.public_resources import *

"""
更新日志:2024-9-27 21:26:48

"""

class Camp_Task(TaskModule):
    """
    更新日志:2024-9-14 09:26:09
    阵营任务模块:
    :py:win32模块
    :td_hwnd:游戏窗口句柄
    :dic_resource:资源字典
    :debug:调试模式
    :loop_count:循环次数
    """

    def __init__(self, py, td_hwnd, dic_resource, debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters)
        self.accepted_task_list_flag = False #已领取任务标志,默认为false
        self.camp_task_finish_flag = False #阵营任务完成标志,默认为false
        self.accepted_task_list = [] #已领取任务列表
        self.completed_task = []  # 已完成的任务
        self.current_task=None #记录当前执行的任务
        # fixme,假如在做这个任务时候的时候,要记录下来,避免多个任务换来换去,设计一个列表来记录当前任务

    def 任务领取(self):#todo,任务未找到,怎么处理
        """阵营任务领取"""

        tasks_to_handle = ["清理细作","精锐都尉","探查敌情", "探查粮仓", "探查通路", "探查刀魔"]#任务列表
        accepted_task_list=[] # 已领取任务列表

        if "游戏主界面" in  self.game_interface[0]:
            logger.info("当前在游戏主界面")
            if self.dic_word_hand:
                for key,value in self.dic_word_hand.items():
                    if "开启了阵营" in key :#关闭提示
                        self.ls_progress="任务中"
                        self.execute_coordinates=value[0][:2]
                        return True

            if self.dic_word_ocr:
                for  key, value in self.dic_word_ocr.items():
                    for task in tasks_to_handle:
                        if task in key :#任务在列表中
                            accepted_task_list.append(task)

            if accepted_task_list:
                logger.warning("阵营任务已接")
                self.accepted_task_list_flag=True
                return accepted_task_list

            self.ls_progress="任务中" #任务中

            if not self.accepted_task_list_flag:#避免重复领取任务
                # self.keyboard_str="m" # 按键触发
                self.py.key_press("M")
                self.execute_delay_time=2 #延迟时间
                self.gets_stuck_flag = False #卡屏功能关闭
                return True

        if "地图界面" in self.game_interface[0]:
            #任务顺序:打开自动寻路界面,筛选npc功能,寻找任务领取人,领取前面5个任务
            if self.dic_image_hand and "res/dtws/camp_task/地图_npc.bmp" in self.dic_image_hand:#打开自动寻路界面
                self.execute_coordinates=self.dic_image_hand["res/dtws/camp_task/地图_npc.bmp"][0][:2]
                return True

            if self.dic_word_hand and "寻路" in self.dic_word_hand:#筛选npc功能
                res_image_dic = self.py.find_image_vnc("res/dtws/camp_task/自动寻路_已勾选.bmp", 958, 207, 1099, 285)
                # print(res_image_dic)
                if res_image_dic:
                    coordinates = res_image_dic["res/dtws/camp_task/自动寻路_已勾选.bmp"]
                    coordinate_list = [] # 创建一个新的列表来存储过滤后的坐标
                    for coordinate in coordinates:
                        if len(coordinates) == 1 and (1030 < coordinate[0] < 1070 and 260 < coordinate[1] < 292):
                            self.py.mouse_drag(1109,337,1108,451,30)#拖动
                            time.sleep(1)

                            if get_value_from_key("义军图腾",self.dic_image_hand):
                                if self.py.ocr_vnc_click("义军任务",947,305,1086,543):#寻找义军任务领取人
                                    self.error_List.append(0)
                                    logger.info("前往义军任务领取人")
                                    time.sleep(10)
                            elif get_value_from_key("唐军图腾",self.dic_image_hand):
                                if self.py.ocr_vnc_click("唐军任务",947,305,1086,543):#寻找义军任务领取人
                                    self.error_List.append(0)
                                    logger.info("前往唐军任务领取人")
                                    time.sleep(10)
                            return True
                        elif not (1030 < coordinate[0] < 1070 and 260 < coordinate[1] < 292):
                            coordinate_list.append(coordinate)
                    if coordinate_list:
                        logger.info("剔除活动选择")
                        # print(coordinate_list)
                        for x, y, con in coordinate_list:
                            self.py.mouse_left_click(x, y)
                            time.sleep(1)

        if "任务领取板界面" in self.game_interface[0]: #todo,领取前面5个任务
            #[('（25级）【战斗】清理细作', 442, 247, 0.984), ('（25级）【后勤】探查敌情', 442, 273, 0.985), ('（25级）【后勤】探查粮仓', 443, 297, 0.969), ('（25级）【后勤】探查通路', 442, 319, 0.987), ('（25级）【后勤】探查刀魔', 442, 343, 0.985)]
            #[('（25级）【战斗】清理细作（接）', 443, 249, 0.974), ('（25级）【后勤】探查敌情（接', 443, 273, 0.979), ('25级）【后勤】探查粮仓（接）', 444, 297, 0.979), ('25编', 443, 322, 0.789), ('忙【后勤】探查通路（接）', 465, 319, 0.922), ('（25级）【后勤】探查刀魔（接）', 441, 342, 0.976)]
            res_ocr = self.py.ocr_vnc(433,244,638,362)  # 识别阵营任务, 领取前面5个任务
            # print(res_ocr)
            if res_ocr:
                for task in tasks_to_handle:
                    for text, x, y, _ in res_ocr :
                        if task in text and "接" in text:#任务已接
                            accepted_task_list.append((task, x, y))
                        elif task in text and "接" not in text: #任务未接
                            self.mouse_left_click_op(x, y)
                            time.sleep(1)
                            self.py.ocr_vnc_click("领取", 791, 702, 855, 727)
            # print(accepted_task_list)
            if len(accepted_task_list) == 5: #前5个任务都领取完毕
                self.execute_coordinates=self.game_interface[1:]
                logger.warning("阵营任务领取完毕")
                return True
    def 任务完成(self):
        if self.dic_word_hand and "可以提升" in self.dic_word_hand:
            logger.warning("可以提升爵位了")
            self.py.mouse_left_click(self.dic_word_hand["可以提升"][0][0], self.dic_word_hand["可以提升"][0][1])
            self.camp_task_finish_flag = True #阵营任务完成
            return True

    def task_精锐都尉(self):
        logger.info("精锐都尉")
        if self.accepted_task_list == ["精锐都尉"]:
            self.camp_task_finish_flag = True  # 阵营任务完成
            logger.info("交付任务,精锐都尉任务完成")
            return "task_finish"

    def task_清理细作(self):
        """主要作用是卡流程,有一个标志位,表示任务可以交付"""
        logger.info("清理细作")
        if self.accepted_task_list==["清理细作"]:
            self.camp_task_finish_flag=True #阵营任务完成
            logger.info("交付任务,清理细作任务完成")
            return "task_finish"
    def task_探查敌情(self):
        """查找字和颜色,如果字识别不到,则判断颜色"""
        logger.info("探查敌情")
        task_finish_flag = False  # 任务完成标志
        key_word_list_tasking = ["侦查:敌军粮车(未完成)","侦查:敌军粮车(完成)"]
        result_dict = self.get_items_from_keys(key_word_list_tasking, "dic_word_ocr")
        logger.debug(f"{result_dict}")
        if result_dict:
            for key, value in result_dict.items():
                if "未完成" in key and not self.role_info["寻路状态"]:
                    self.mouse_left_click_op(*value[:2], 30)
                    break
                if "完成" in key:
                    task_finish_flag = True
                    break

        if task_finish_flag and self.get_value_from_key_operation("点击交付", "dic_word_ocr"):  #
            logger.info("交付任务,探查敌情任务完成")
            return "task_finish"
    def task_探查粮仓(self):
        logger.info("探查粮仓")
        task_finish_flag = False  # 任务完成标志
        key_word_list_tasking = ["梨花唐1(未完成)", "梨花唐1(完成)", "梨花义1(未完成)","梨花义1完成",
                                 "梨花义1(完成)"]
        result_dict = self.get_items_from_keys(key_word_list_tasking, "dic_word_ocr")
        logger.debug(f"{result_dict}")
        if result_dict:
            for key, value in result_dict.items():
                if "未完成" in key and not self.role_info["寻路状态"]:
                    self.mouse_left_click_op(*value[:2], 30)
                    break
                if "完成" in key:
                    task_finish_flag = True
                    break

        if task_finish_flag and self.get_value_from_key_operation("点击交付", "dic_word_ocr"):  #
            logger.info("交付任务,探查粮仓任务完成")
            return "task_finish"
    def task_探查通路(self):
        logger.info("探查通路")
        task_finish_flag = False  # 任务完成标志
        key_word_list_tasking = ["梨花唐2(未完成)", "梨花唐2(完成)", "梨花义2(未完成)","梨花义2未完成)",
                                 "梨花义2(完成)"]
        result_dict = self.get_items_from_keys(key_word_list_tasking, "dic_word_ocr")
        logger.debug(f"{result_dict}")
        if result_dict:
            for key, value in result_dict.items():
                if "未完成" in key and not self.role_info["寻路状态"]:
                    self.mouse_left_click_op(*value[:2], 30)
                    break
                if "完成" in key:
                    task_finish_flag = True
                    break

        if task_finish_flag and self.get_value_from_key_operation("点击交付", "dic_word_ocr"):  #
            logger.info("交付任务,探查通路任务完成")
            return "task_finish"

    def task_探查刀魔(self):#todo
        logger.info("探查刀魔")
        task_finish_flag = False  # 任务完成标志
        key_word_list_tasking = ["梨花唐3(未完成)","梨花唐3(完成)","梨花义3(未完成)","梨花义3(完成)"]
        result_dict = self.get_items_from_keys(key_word_list_tasking, "dic_word_ocr")
        logger.debug(f"{result_dict}")
        if result_dict:
            for key ,value in result_dict.items():
                if "未完成" in key and not self.role_info["寻路状态"]:
                    self.mouse_left_click_op(*value[:2],30)
                    break
                if "完成" in key:
                    task_finish_flag = True
                    break

        if task_finish_flag and self.get_value_from_key_operation("点击交付", "dic_word_ocr"):  #
            logger.info("交付任务,探查刀魔任务完成")
            return "task_finish"

    def 任务操作(self):
        if self.camp_task_finish_flag:
            logger.info("阵营任务已完成")
            self.ls_progress = "任务完成"
            self.program_result = "task_finish"
            self.task_name="阵营"
            return True

        if not self.camp_task_finish_flag:
            if not self.任务完成(): #任务未完成,且任务领取列表为空
                self.accepted_task_list=self.任务领取()#["清理细作", "探查敌情", "探查粮仓", "探查通路", "探查刀魔","挑战义军"]
                print(self.accepted_task_list)

                if type(self.accepted_task_list) !=list: #todo,
                    pass

                elif len(self.completed_task)>0 and len(self.accepted_task_list)==0:#任务都完成,领取任务列表为空
                    self.camp_task_finish_flag=True
                    return True

                elif type(self.accepted_task_list)==list and len(self.accepted_task_list)>0:
                    if "探查敌情" in self.accepted_task_list :
                        logger.info("探查敌情任务已领取")
                        self.current_task="探查敌情"
                        if self.task_探查敌情()=="task_finish":
                            self.completed_task.append("探查敌情")
                            self.accepted_task_list.remove("探查敌情")
                            self.current_task=None

                    elif "探查粮仓" in self.accepted_task_list:
                        logger.info("探查粮仓任务已领取")
                        self.current_task="探查粮仓"
                        if self.task_探查粮仓()=="task_finish":
                            self.completed_task.append("探查粮仓")
                            self.accepted_task_list.remove("探查粮仓")
                            self.current_task=None

                    elif "探查通路" in self.accepted_task_list:
                        logger.info("探查通路任务已领取")
                        self.current_task="探查通路"
                        if self.task_探查通路()=="task_finish":
                            self.completed_task.append("探查通路")
                            self.accepted_task_list.remove("探查通路")
                            self.current_task=None

                    elif "探查刀魔" in self.accepted_task_list:
                        logger.info("探查刀魔任务已领取")
                        self.current_task="探查刀魔"
                        if self.task_探查刀魔()=="task_finish":
                            self.completed_task.append("探查刀魔")
                            self.accepted_task_list.remove("探查刀魔")
                            self.current_task=None

                    elif "清理细作" in self.accepted_task_list:
                        logger.info("清理细作任务已领取")
                        self.current_task="清理细作"
                        if self.task_清理细作()=="task_finish":
                            self.completed_task.append("清理细作")
                            self.accepted_task_list.remove("清理细作")

                    elif "精锐都尉" in self.accepted_task_list:
                        logger.info("精锐都尉任务已领取")
                        self.current_task="精锐都尉"
                        if self.task_精锐都尉()=="task_finish":
                            self.completed_task.append("精锐都尉")
                            self.accepted_task_list.remove("精锐都尉")

#任务资源
dic_camp_tasks={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        # 2: (621,64,724,93, 0.8),#目标体信息
        # "":(522,437,596,464,0.8,-25,21),#琴心
        "寻路":(998,167,1083,191,0.8),#自动寻路
        "开启了阵营":(462,344,625,368,0.8,242,131),#开启阵营提示
        "可以提升":(466,375,647,405,0.8,232,73),#阵营任务可以完成
        },
    "image": {
        "res/dtws/camp_task/地图_npc.bmp":(1088,563,1153,618,0.8),#地图npc
        "res/dtws/camp_task/义军图腾.bmp":(647,813,687,853,0.8),#义军图腾
        "res/dtws/camp_task/唐军图腾.bmp":(647,813,687,853,0.8),#唐军图腾
        # "res/dtws/main_task/商城.bmp":(1195,24,1243,87,0.8)
        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        "蜀山":True
    },
     "color": {
        #  1: (440,180), #点位
         "2df9f9": (1291, 326),#敌军粮车(未完成)
         "21b7b7": (1286, 331),#敌军粮车(未完成)
         "dd130e": (1323,326),#敌军粮车(未完成)
        },
    "mutil_colors":{
        "梨花唐1(未完成)":{"colors":{"2df9f9":(1286,325),
                            "27d8d8":(1296,327),
                            "1ea6a6":(1298,334),
                            "ed140f":(1317,330),
                          },
                    "scope":(1238,322,1371,450),
                    "tolerance":25},
        "梨花唐1(完成)":{"colors":{"2df9f9":(1286,297),
                            "27d8d8":(1296,295),
                            "1ea6a6":(1298,302),
                            "33cc33":(1318,300),
                          },
                    "scope":(1183,288,1357,320),
                    "tolerance":25},
        "(未完成)":{"colors":{"dd130e":(1324,360),
                            "cd110d":(1339,356),
                            "be100c":(1344,367),
                            "ed140f":(1356,365),
                          },
                    "scope":(1281,318,1381,471),
                    "tolerance":25},
        "敌军粮车":{"colors":{"2ae8e8":(1258,358),
                            "21b7b7":(1286,363),
                            "1ea6a6":(1305,365),
                            "2df9f9":(1301,368),
                          },
                    "scope":(1246,304,1311,468),
                    "tolerance":25},
        "一个爵位(未完成)":{"colors":{"2df9f9":(1255,330),
                                    "27d8d8":(1269,326),
                                    "2ae8e8":(1287,333),
                                    "24c7c7":(1304,335),
                                    "ed140f": (1324,330),
                                    "cd110d": (1339,324),
                                    "ae0f0b": (1359,335),
                                      },
                        "scope":(1176,257,1391,348),
                        "tolerance":25},
        "点击交付":{"colors":{"dd7600":(1201,286),
                            "ff8800":(1218,282),
                            "bb6400":(1232,276),
                            "ee7f00":(1247,331),},
                "scope":(1182,272,1276,337),
                "tolerance":20},
        "(已完成)":{"colors":{"228822":(1383,277),
                                          "33cc33":(1385,284),
                                          "29a329":(1396,279),
                                          "1f7a1f":(1405,285),},
                                "scope":(1186,273,1387,324),
                                "tolerance":20},

        "梨花":{"colors":{"27d8d8":(1252,293),
                        "2df9f9":(1256,300),
                        "24c7c7":(1267,294),
                        "2ae8e8":(1269,301),
                          },
                        "scope":(1181,285,1391,555),
                        "tolerance":20},
        "苏三":{"colors":{"cc6d00":(1267,342),
                        "884900":(1276,347),
                        "995200":(1284,342),
                        "ff8800":(1284,351),},
                "scope":(1180,249,1394,340),
                "tolerance":20},
        "箱子":{"colors":{'f0e8df': (1211,391),  # 主颜色
                        '2df9f9': (1268,390),
                        'cd110d': (1380,394),},
                "scope":(1179,249,1394,557),
                "tolerance":20}
        }
    }

# #资源合并
camp_merged_dict=merge_dicts(dic_camp_tasks,public_res)
# print(camp_merged_dict)
#阵营任务信息
task_background_scope=(1177,251,1395,552)
camp_task_text_alternative_parameters=task_background_scope

# #测试
# #窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#窗口类名
# win_title = "vnc_dtws_v1 "#窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = "127.0.0.1"
# vnc_port = 5901  # 默认 VNC 端口，根据实际情况可能有所不同
# vnc_password = "ordfe113"
#
#
#
# def run():
#     #初始化VNCtools,单线程
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port,vnc_password)
#     # 主任务运行
#     task=Camp_Task(py,win_hwnd[0],camp_merged_dict,True,50,camp_task_text_alternative_parameters)
#     res=task.run()
#     print(res)
#
# run()