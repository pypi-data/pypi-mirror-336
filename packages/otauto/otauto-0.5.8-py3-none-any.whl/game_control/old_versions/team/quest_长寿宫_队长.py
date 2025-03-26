import time

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

class quest_长寿宫_队长(Quest_Task):
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
        self.boss_name=[] #boss名称

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
    1:等待组队
    2:组队中
    3:清理包裹
    4:集合
    5:进入副本
    6:副本操作
    7:清理物品
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

    def is_correct_and_compare_70(self,s):
        """
        判断字符串是否为两个数字通过斜杠 / 分隔的形式，并比较两个数字的值。
        两边必须是数字。
        # 测试
            test_string1 = '1317/1317'
            result1 = is_correct_and_compare(test_string1)
            print(f"'{test_string1}' 格式正确且符合比较条件: {result1}")

            test_string2 = '1317/2634'
            result2 = is_correct_and_compare(test_string2)
            print(f"'{test_string2}' 格式正确且符合比较条件: {result2}")

            test_string3 = 'abc/123'
            result3 = is_correct_and_compare(test_string3)
            print(f"'{test_string3}' 格式正确且符合比较条件: {result3}")

            test_string4 = '123/'
            result4 = is_correct_and_compare(test_string4)
            print(f"'{test_string4}' 格式正确且符合比较条件: {result4}")
        :param s: 需要判断的字符串
        :return: 如果格式正确且符合条件返回 True，格式不正确或条件不满足返回 False
        """
        # 定义正则模式：确保斜杠两边都是数字
        pattern = r'^\d+/\d+$'

        # 检查格式是否正确
        if not re.match(pattern, s):
            return False

        # 分割字符串
        parts = s.split('/')

        # 转换为整数
        num1 = int(parts[0])
        num2 = int(parts[1])

        # 比较数值
        return num1 < num2 *0.7

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

            elif self.is_correct_and_compare_70(self.role_info["血量"]):
                logger.info("内功疗伤")
                for i in range(2):
                    self.key_press_op("9", delay_time=0.5)

        if not self.find_imagefinder_op("res/dtws/role_skill/破衲功ing.png",259, 55, 440, 111):
            logger.info("破衲功开启")
            self.find_imagefinder_click("res/dtws/role_skill/破衲功.png",777, 811, 897, 866)


    def task_combating(self): #todo:增益技能没有写
        """
        战斗中
        :return:
        """
        common_skill = (1,3, 5,6,8)
        anger_skill = (2,4,7)
        self.task_skill_release(common_skill, anger_skill)

        if self.role_info["血量"]:  # 血量
            if self.is_correct_and_compare(self.role_info["血量"]):
                logger.warning("血量低于50%,快速恢复")
                self.key_press_op("-", delay_time=1)


    def task_目标识别(self):
        """
        1,地图和场景内识别目标体
        2,识别到目标体在角色附近,该节点完成
        :return:
        """
        self.ls_progress="任务中"
        self.node_current="task_目标识别"
        self.target_position_map=[] #目标位置,小地图初始化
        self.target_position_scene=[] #目标位置,游戏场景初始化
        yolo_red_target_flag=False #yolo识别红名怪标记

        if self.lock_target_num>=4 :#说明场景内没有目标体出现
            self.lock_target_num=0
            return "task_fail"

        if len(self.node_coords)>=4 :
            logger.debug(f"节点坐标:{self.node_coords}")
            counter = Counter(map(tuple, self.node_coords))
            unique_lst = [list(item) for item, count in counter.items() if count == 1]# 保留出现一次的元素
            if unique_lst :
                logger.info("节点坐标相同,说明没有找到目标体")
                self.node_coords=[] #清空节点坐标
                return "task_fail"

        if "游戏主界面" in self.game_interface[0]:
            key_word=["目标体_地图红点","目标体_地图红点补充","目标体_红名"]
            res_dict=self.get_items_from_keys(key_word,"dic_mutil_colors")
            logger.debug(f"识别出的结果:{res_dict}")
            if res_dict and "目标体_地图红点" in res_dict:
                self.target_position_map = group_by_difference_first_elements(res_dict["目标体_地图红点"],threshold=5)
            elif res_dict and "目标体_地图红点补充" in res_dict:
                self.target_position_map = group_by_difference_first_elements(res_dict["目标体_地图红点补充"],threshold=5)

            if res_dict and "目标体_红名" in res_dict:
                self.target_position_scene = group_by_difference_first_elements(res_dict["目标体_红名"])

            if self.find_yolo(["红色名称"]): #目标体在游戏场景出现
                logger.info("yolo识别出目标")
                self.key_press_op("1")
                self.node_current = "task_攻击目标"
                self.node_coords.append(self.coord[:2]) #记录节点坐标
                self.lock_target_num=0
                self.lock_target_num_yolo = 0
                return "task_finish"

            if self.find_yolo(["红名怪"]): #目标体在游戏场景出现
                logger.info("yolo识别出目标")
                self.key_press_op("1")
                self.node_current = "task_攻击目标"
                self.node_coords.append(self.coord[:2]) #记录节点坐标
                self.lock_target_num=0

            red_target_list=self.get_value_from_key("红名怪","dic_yolo_ocr")
            if red_target_list:
                for red_target in red_target_list:
                    if abs(red_target[0]-self.role_position_scene[0])<300 or abs(red_target[1]-self.role_position_scene[1])<300:
                        logger.info(f"yolo识别出附近有目标")
                        self.lock_target_num_yolo +=1
                        red_target_list=True
                        break
            if not red_target_list: #yolo没有识别出目标,或者不在附近
                logger.info(f"yolo没有识别出目标,或者不在附近")
                self.get_yolo_click("红名怪",x3=21,y3=127,delay_time=1) #避免距离过远

            if self.target_position_scene: #目标体在游戏场景出现
                logger.info(f"目标体_红名:{self.target_position_scene}")
                scope=(681, 347, 757, 465)
                x,y=self.target_position_scene[0][0],self.target_position_scene[0][1]

                if scope[0]<x<scope[2] and scope[1]<y<scope[3]: #避免判断到自身
                    logger.info(f"只有角色在游戏场景内,识别到自身")
                    return "task_fail"
                else:
                    self.key_press_op("tab",delay_time=0.5)
                    self.lock_target_num+=1 #锁定目标体次数+1

            if self.target_position_map : #目标体在小地图出现
                logger.info(f"目标体_地图红点:{self.target_position_map}")
                if check_proximity(self.target_position_map,self.role_position_map,threshold=5):
                    logger.info("目标体在小地图出现,且在角色附近")
                    self.key_press_op("tab")
                    self.node_current = "task_攻击目标"
                    self.node_coords.append(self.coord[:2]) #记录节点坐标
                    self.lock_target_num=0
                    self.lock_target_num_yolo +=1
                    return "task_finish"

                if self.lock_target_num_yolo >=4: #说明可能存在攻击目标,但是没有识别出来
                    logger.info("可能存在攻击目标,但是超过了锁定距离")
                    self.mouse_right_click_op(*self.target_position_map[0],delay_time=0.5)
                    self.lock_target_num = 0 #重置锁定目标次数
                    self.lock_target_num_yolo = 0 #重置锁定目标次数
                    self.node_coords=[] #清空节点坐标
                    return "task_finish"

                res_data = self.find_colors_vnc("f3120a", 1262, 76, 1414, 208)  # 查看小地图上的红色标记
                res_dict = self.find_value_with_length(res_data, "f3120a")  # 获取颜色值,判断颜色表示是否大于4
                if res_dict and res_dict["f3120a"]:  # 说明角色移动中
                    logger.success("发现红色标记")
                    for key, vlue in res_data.items():
                        if key == "f3120a":
                            for vlue_key, vlue_value in vlue.items():
                                self.mouse_left_click_op(vlue_value[0][0], vlue_value[0][1], delay_time=1)
                                self.lock_target_num = 0  # 重置锁定目标次数
                                self.lock_target_num_yolo = 0  # 重置锁定目标次数
                                self.node_coords = []  # 清空节点坐标
                                self.queue_massage(task_message="识别目标", team_info=1, combat_info=3)  # 队列信息
                                self.mongodb_team_info_update(interactor=3)
                                time.sleep(5)  # 等待8秒
                                return "task_finish"

                else:
                    logger.info(f"目标体在小地图出现,但不在角色附近:{self.target_position_map}")
                    self.mouse_right_click_op(*self.target_position_map[0],delay_time=0.5)
                    self.lock_target_num = 0 #重置锁定目标次数
                    self.lock_target_num_yolo = 0 #重置锁定目标次数
                    self.node_coords=[] #清空节点坐标
                    self.queue_massage(task_message="识别目标", team_info=1, combat_info=3)  # 队列信息
                    self.mongodb_team_info_update(interactor=3)
                    time.sleep(8)  # 等待8秒
                    return "task_finish"


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
        coordinate_node_长寿宫 = [(67, 55), (69,57),(69,66),(69,77),(72, 77),(69,86), (65, 80), (69, 93), (70,98),
                                  (69, 108), (67, 117), (69, 129),(69,137),(64,144),(57,148),
                                  (69, 141), (59, 144),(58,155) ,(60, 155), (62, 163), (63,169),(62,176),(62, 178),
                                  (62,183),(63,193),(67,196),(72,196),(75, 198),(77,196),(83,196),(90,196),(97,196),
                                  (102,193),
                                  (103,196),(105,196),(109,196),(112, 195), (120, 189),(121,197) ,(122,189),(121,182),
                                  (120,175),(120,169),(120,162),(119,155),(120,148),(121,142),(121,134),(121,128),
                                  (120,121),(120,112),(121,104),(120,97),(119,88),(120,82),(119,79),(120,77),
                                  (121, 71), (119,64),(129, 63), (135,62) ,(141,62) ,(147,62),(152,62),(158,62),
                                  (164, 62), (172, 63), (174, 73),(174,79) ,(173, 82),(174,90),(173,99),(174,105),
                                  (173,110),(173,119),(173,126),(174,134),(173,138),(173,143),(174,151),(174,158),
                                  (173,167),(173,175),(174,180),(173,187),]

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

            if self.get_value_from_key("连续按|空格|挣脱控制","dic_word_hand"):#挣脱控制
                for i in range(3,5):
                    self.key_press_op("spacebar", delay_time=0.3)

            data_list=self.get_value_from_key("res/dtws/other/组队_摇骰子.png","dic_image_hand") #物品捡起
            if data_list:
                for data in data_list:
                    self.mouse_left_click_op(data[0], data[1], delay_time=0.5)

            res_dict=self.find_ppocr_op(626, 59, 770, 99) #找到boss
            if res_dict:
                for key,value in res_dict.items():
                    if key=="纳魂尊者":
                        self.boss_name.append("纳魂尊者")
                        logger.info("找到boss,纳魂尊者")
                        self.boss_name=list(set(self.boss_name))
                        self.mongodb_team_info_update(interactor=1)  # 交互器为1
                        self.task_combating()  # 释放技能
                        return True
                    elif key=="灭魂灵兽":
                        self.boss_name.append("灭魂灵兽")
                        logger.info("找到boss,灭魂灵兽")
                        self.boss_name = list(set(self.boss_name))
                        self.mongodb_team_info_update(interactor=1)  # 交互器为1
                        self.task_combating()  # 释放技能
                        return True
                    elif key=="摄魂玄女":
                        self.boss_name.append("摄魂玄女")
                        self.boss_name = list(set(self.boss_name))
                        logger.info("找到boss,摄魂玄女")
                        self.mongodb_team_info_update(interactor=1)  # 交互器为1
                        self.task_combating()  # 释放技能
                        return True

            if  self.get_items_from_all_keys([key_info[0],key_info[1]],"dic_mutil_colors") or self.find_yolo(
                    ["红色名称","红名怪"]):#已锁定目标体
                self.task_combating() #释放技能
                self.queue_massage(task_message="攻击目标",team_info=1,combat_info=1)  # 队列信息
                self.mongodb_team_info_update(interactor=1) #交互器为1
                return True

            elif self.get_items_from_keys([key_info[2],key_info[3]],"dic_mutil_colors"):#出现目标体
                self.task_目标识别() #识别目标
                self.queue_massage(task_message="识别目标", team_info=1, combat_info=2)  # 队列信息
                self.mongodb_team_info_update(interactor=2) #交互器为2
                return True

            else:
                self.queue_massage(task_message="识别目标", team_info=1, combat_info=3)  # 队列信息
                self.mongodb_team_info_update(interactor=3) #交互器为3
                time.sleep(8) #等待8秒

                logger.debug("未出现目标体,节点移动")
                coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_长寿宫)
                res_num = self.way_finding_node_op(coordinate_node_dispose, debug=True,range_num=5, threshold=4)
                if res_num == 1:
                    logger.success("长寿宫节点移动完成")
                    return True
                elif res_num == -1:
                    logger.error("长寿宫节点移动失败")
                elif res_num == 0:
                    logger.info("长寿宫节点移动中")

        else:
            self.界面关闭()

    def 任务操作(self):#todo,这里一般固定写法,
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
        # 2: (621,64,724,93, 0.8),#目标体信息
        "连续按|空格|挣脱控制":(363, 204, 675, 261,0.8),#连续按|空格|挣脱控制
        },
    "image": {
        "res/dtws/other/组队_摇骰子.png":(615, 390, 684, 651,0.8),#摇骰子
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
quest_长寿宫_队长_merged_dict=merge_dicts(dic_reward_tasks,quest_task_merged_dict) #todo:更改名称

#todo:任务信息,是否需要去除背景色,调试是打开
task_background_scope=(1177,251,1395,552)
quest_长寿宫_队长_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#todo:文字模糊匹配,调试时开启
quest_长寿宫_队长_word_standard_dict={"客":"雇佣剑客","毒":"毒蜂","熊":"棕熊",}

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
#     task=quest_长寿宫_队长(py,win_hwnd[0],quest_长寿宫_队长_merged_dict,True,100,quest_长寿宫_队长_text_alternative_parameters,quest_长寿宫_队长_word_standard_dict,target_name_list=target_name_list)
#     res=task.run(classes=2,running_time=1)
#     print(res)
#
# target_name_list=["屠狼帮众","巨狼","屠狼帮精锐","屠狼帮狼卫","屠狼帮大长老","屠狼帮头目","屠狼帮巡逻兵","散财童子",]
#
# run(target_name_list)