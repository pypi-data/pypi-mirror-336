import time

from game_role.role_skill_蜀山_v2 import *
from public_function.public_function import *
from public_function.public_resources import *
"""
功能: 游戏基本设置
更新日志: 2024-12-25 18:37:39
设计思路:
1.
2.
3.
4.
5.
6.
"""

class game_setting(TaskModule):
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
        self.node_flag= False #节点是否完成,默认为false
        self.node_counter = 0 # 节点计数器

        logger.success(f"game_setting")
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

    def handle_node(self, node_name, target_number, click_coordinates, npc_conditions,map_name):
        """
        处理节点任务
        self.handle_node("功能", 26, (738, 203, 796, 229), ["爵位领取人", "悬赏令发布使"],"白屏寨")
        self.handle_node("任务", 19, (799, 202, 856, 231), ["西域商团青城山接引人"],"青城山")
        self.handle_node("活动", 24, (922, 203, 980, 229), ["唐军任务领取人", "义军任务领取人"],"白屏寨")
        :param node_name:  节点名称
        :param target_number:  目标数字
        :param click_coordinates:  点击坐标
        :param npc_conditions:  NPC条件
        :param map_name:
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
        if len(npc_info) >= 5:
            npc_name, npc_location, x, y = npc_info[:4]
            self.mouse_left_click_op(x, y, delay_time=1)
            self.get_ocr_vnc_click("收藏", 949, 527, 1052, 566, delay_time=1)
            self.get_ocr_vnc_click("确定", 674, 439, 739, 465, delay_time=1)


    def task_快捷键取消(self):
        """取消右侧快捷栏的快捷键"""
        self.ls_progress = "任务中"
        self.node_current = "task_快捷键取消"

        if self.node_counter>=5:
            self.node_current = "task_游戏设置"
            self.node_flag= False # 设置节点完成标志为false
            self.node_counter=0 # 重置节点计数器
            return "task_finish"

        elif self.get_value_from_key("按键设定","dic_word_hand"):
            logger.info("按键设定")
            # 筛选出最后一个元素为 99 的键值对
            result_dict = {key: value for key, value in self.dic_word_ocr.items() if value[-1] == 99}
            logger.info(f"result_dict:{result_dict}")
            condition_1=self.get_items_from_keys(['Alt-9','Alt-8',],"dic_word_ocr")
            condition_2=self.get_items_from_keys(['Alt-1','Alt-2',],"dic_word_ocr")
            logger.info(f"condition_1:{condition_1}")
            logger.info(f"condition_2:{condition_2}")
            if condition_1 and  condition_2:
                logger.info("找到快捷键")
                self.node_flag = True # 找到快捷键,设置节点完成标志为true
                # 定义需要点击的快捷键集合
                keys_to_click = {"Alt-2", "Alt-3", "Alt-5", "Alt-6", "Alt-7", "Alt-0", "Alt-1", "Alt-4", "Alt-8",
                                 "Alt-9"}
                set_the_number=0 # 设置的次数
                # 遍历结果字典，执行鼠标点击操作
                for key, value in result_dict.items():
                    if key in keys_to_click:
                        set_the_number+=1
                        x_offset = 10
                        y_offset = 5
                        self.mouse_left_click_op(value[0] + x_offset, value[1] + y_offset, delay_time=1)
                        self.get_ocr_vnc_click("取消设定", 634, 658, 715, 691, delay_time=1)

                if set_the_number>=10 or set_the_number>=len(result_dict):
                    logger.info("设置完成")
                    self.get_ocr_vnc_click("确定", 718, 656, 798, 693, delay_time=1)
                    self.node_counter=10 # 设置的次数改为10

            if not self.node_flag:
                self.py.mouse_drag(878, 289, 879, 360, 30)  # 拖动
                time.sleep(1)
                self.node_flag = True

        elif self.get_value_from_key_operation("按键设置","dic_word_hand",delay_time=1):
            logger.info("进入按键设置")

        elif "游戏主界面" in self.game_interface[0] and not self.get_value_from_key("系统菜单","dic_word_hand"):
            self.key_press_op("esc")

        self.node_counter+=1 # 节点计数器加1

    def task_游戏设置(self):
        """游戏设置"""
        self.ls_progress = "任务中"
        self.node_current = "task_游戏设置"

        if self.node_counter>=5:
            self.node_current = "task_npc收藏"
            self.node_flag= False # 设置节点完成标志为false
            self.node_counter=0 # 重置节点计数器
            return "task_finish"

        elif self.node_flag:
            self.get_ocr_vnc_click("恢复默认", 544, 535, 639, 568, delay_time=1)
            result_dict = {key: value for key, value in self.dic_word_ocr.items() if value[-1] == 98}
            # 定义需要点击的快捷键集合
            keys_to_click = {"关闭聊天", "关闭系统", "隐藏头盔", "隐藏披风", "隐藏神兵", "隐藏红包", "隐藏他人",
                             "隐藏召唤",}
            set_the_number = 0  # 设置的次数
            # 遍历结果字典，执行鼠标点击操作
            for key, value in result_dict.items():
                for key_tr in keys_to_click:
                    if key_tr in key:
                        set_the_number += 1
                        x_offset = 10
                        y_offset = 5
                        self.mouse_left_click_op(value[0] + x_offset, value[1] + y_offset, delay_time=1)
            if set_the_number >= 8 or set_the_number >= len(result_dict):
                logger.info("设置完成")
                self.get_ocr_vnc_click("确", 671, 536, 770, 571, delay_time=1)
                self.node_counter = 10  # 设置的次数改为10

        elif not self.node_flag:
            if self.get_value_from_key_operation("最低画质","dic_word_hand",delay_time=1):
                logger.info("选择最低画质")

            if self.get_value_from_key_operation("功","dic_word_hand",delay_time=1):
                logger.info("功能设定")
                self.node_flag= True # 设置节点完成标志为true

            elif self.get_value_from_key_operation("游戏设置","dic_word_hand",delay_time=1):
                logger.info("进入按键设置")

            elif "游戏主界面" in self.game_interface[0] and not self.get_value_from_key("系统菜单","dic_word_hand"):
                self.key_press_op("esc")

        self.node_counter+=1 # 节点计数器加1

    def task_npc收藏(self):
        """npc收藏"""
        self.ls_progress = "任务中"
        self.node_current = "task_npc收藏"

        if self.node_counter>=5 :
            self.get_value_from_key_operation("res/dtws/other/快速搜索_关闭.png", "dic_image_hand")
            self.node_current = "task_基础技能"
            self.node_flag= False
            self.node_counter=0
            return "task_finish"

        if self.get_value_from_key("系统菜单","dic_word_hand"):
            self.get_ocr_vnc_click("返回游戏",666, 513, 814, 551)

        elif "地图界面" in self.game_interface[0]:
            logger.info("地图界面")
            if self.find_ocr_vnc_word("自动寻路",739, 156, 875, 182):
                if self.node_list == ["功能","任务","活动"]:
                    logger.info("npc收藏完成,界面关闭")
                    self.node_counter = 10  # 重置节点计数器
                    close_list=self.get_value_from_key("res/dtws/other/快速搜索_关闭.png","dic_image_hand")
                    if close_list:
                        logger.info(f"close_list:{close_list}")
                        sorted_data = sorted(close_list, key=lambda x: x[0])
                        for close_coord in sorted_data:
                            self.mouse_left_click_op(close_coord[0], close_coord[1], delay_time=1)

                # 调用处理函数
                self.handle_node("功能", 26, (738, 203, 796, 229), ["爵位领取人", "悬赏令发布使"], "白屏寨")
                self.handle_node("任务", 19, (799, 202, 856, 231), ["西域商团青城山接引人"], "青城山")
                self.handle_node("活动", 24, (922, 203, 980, 229), ["唐军任务领取人", "义军任务领取人"], "白屏寨")

            elif self.get_ocr_vnc_click("收藏", 549, 199, 622, 236, delay_time=1):
                pass
            elif self.get_ocr_vnc_click("快捷搜索", 996, 559, 1080, 585, delay_time=1):
                pass
            elif self.get_value_from_key_operation("res/dtws/camp_task/地图_npc.bmp", "dic_image_hand", delay_time=1):
                pass

        elif "游戏主界面" in self.game_interface[0] and len(self.node_list)<3:
            self.key_press_op("M") # 打开地图

    def task_基础技能(self):
        """基础技能"""
        self.ls_progress = "任务中"
        self.node_current = "task_基础技能"

        if self.node_counter>=5:
            self.node_counter=0
            self.界面关闭()
            return "task_finish"

        if "技能界面" in self.game_interface[0]:
            logger.info("技能界面")
            if self.get_value_from_key("res/dtws/role_skill/蜀山_普通攻击.png","dic_image_hand"):
                self.py.mouse_drag(504,266,1224,832,30) # 技能栏拖动
                time.sleep(2)
                self.node_counter = 10

            elif self.get_ocr_vnc_click("综",405, 539, 435, 620,delay_time=1):
                logger.info("综合界面")

        if "游戏主界面" in self.game_interface[0]:
            if self.get_value_from_key("res/dtws/role_skill/回城.bmp","dic_image_hand"):
                self.py.mouse_drag(805,834,1261,833,30)
                time.sleep(2)
            self.key_press_op("K") # 打开技能栏

        self.node_counter+=1

    def handle_task(self):
        task_methods = {
            "task_快捷键取消":self.task_快捷键取消,
            'task_游戏设置': self.task_游戏设置,
            'task_npc收藏': self.task_npc收藏,
            "task_基础技能": self.task_基础技能,
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
        self.ls_progress = "任务中"
        logger.debug(f"{self.node_current}")
        self.queue_massage(self.node_current)  # 队列信息

        if not self.node_current:
            self.task_快捷键取消()
        elif "task_基础技能" in self.node_current :
            if self.task_基础技能() == "task_finish":
                return "task_finish"
        else:
            self.handle_task()


    def 任务操作(self):
        """所有的节点需要接入这里才能运行,测试也是这里添加测试代码"""
        if self.task_flow()=="task_finish":
            self.ls_progress= "任务完成" #模块运行结束
            self.task_name="game_setting"
            self.program_result="task_finish"


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
        99:(732, 253, 866, 646,0.8),#快捷键
        98:(551, 231, 891, 502,0.8),#功能设置
        # "快捷":(994,560,1080,584,0.8,0,0,1,5),
        "按键设置":(671, 447, 804, 477,0.8),
        "游戏设置":(672, 388, 807, 410,0.8,),
        "按键设定":(668, 173, 779, 204,0.8),
        "最低画质":(800, 249, 889, 286,0.8),
        "功":(521, 384, 555, 433,0.8),
        },
    "image": {
        r"res/dtws/camp_task/地图_npc.bmp":(1088,563,1153,618,0.8),#地图npc
        r"res/dtws/other/快速搜索_关闭.png":(1025, 110, 1168, 212,0.8),#关闭图标
        r"res/dtws/role_skill/回城.bmp":(775, 803, 835, 855,0.8),
        r"res/dtws/role_skill/蜀山_普通攻击.png":(466, 231, 533, 294,0.8),

        },
    "yolo":{
        # "豪猪":(0,0,0,0),
        # "蜀山":True,

        },
    "color": {
        #  1: (440,180), #点位
        #  "2df9f9": (1291, 326),#敌军粮车(未完成)
        #  "21b7b7": (1286, 331),#敌军粮车(未完成)
        #  "dd130e": (1323,326),#敌军粮车(未完成)
        },
    "mutil_colors":{
            "按键设置_滚动条":{"colors":{"7c8192":(878, 351),
                                "7a8091":(878, 358),
                                "767d8e":(878, 371),},
                        "scope":(865, 265, 887, 630),
                        "tolerance":25},

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

#资源合并
"""
dic_reward_tasks:该模块资源
public_res:公共资源
"""
game_setting_merged_dict=merge_dicts(dic_reward_tasks,public_res)

#任务信息,是否需要去除背景色
"""
task_background_scope:识别范围
1不启用背景色,默认是识别文字资源为数字4的资源
task_name_text_alternative_parameters=task_background_scope
2启用背景色,具体参数参考basic_function/parent_module.py里get_text_alternative方法
task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
"""
task_background_scope=(1177,251,1395,552)
task_game_setting_text_alternative_parameters=task_background_scope
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#文字模糊匹配
"""
字典形式,key为模糊匹配的关键字符串,key可以用"|"符号设置多关键字,value为标准字符串
如果需要合并请使用,参数参考public_function/public_function.py里merge_dicts方法
word_standard_dict=merge_dicts(task_name_word_standard_dict,public_dict)
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_word_standard_dict
"""
task_game_setting_word_standard_dict={"疑犯":"疑犯(0/1)","犯":"疑犯(已完成)","交付":"点击交付" }

# 过滤的关键字
"""
这里可以自定义,容易出错的关键词,一般不定义
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_keywords_list
"""
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用


# task=game_setting(py,win_hwnd[0],game_setting_merged_dict,True,50,task_game_setting_text_alternative_parameters,task_game_setting_word_standard_dict)
# res=task.run()
