# from basic_function.parent_module import *
import time

from game_role.role_skill_蜀山 import *
from basic_function.vnc.vnc_tools import *
from public_function.public_function import *
from public_function.public_resources import *

from  mongoDB.mongodb_v2 import * #数据库操作

"""
生产模式程序入口
更新日志:2024-12-18 18:42:41
功能:角色信息采集
"""

class task_execution(TaskModule):
    def __init__(self, py, td_hwnd, dic_resource, queue,debug=False, loop_count: int = 10,text_alternative_parameters:tuple=None,word_standard_dict:dict=None,keywords_list:list=None,):
        super().__init__(py, td_hwnd, dic_resource, debug, loop_count,text_alternative_parameters,word_standard_dict,keywords_list,)

        self.parcel_scope = None #包裹范围
        self.task_accepted_flag = False #任务是否已领取,默认为false
        self.camp_task_finish_flag = False #阵营任务完成标志,默认为false
        self.accepted_task_list = [] #已领取任务列表
        self.completed_task = []  # 已完成的任务
        self.node_current=None #当前节点
        self.node_next=None #下一个节点
        self.node_before=None #上一个节点
        self.node_list= []  # 节点:操作,列表
        self.node_flag = False #节点是否执行完成
        self.node_counter= 0 #节点计数器

        self.queue = queue #进程队列信息


        self.mongodb_query={} #mongodb查询条件

        self.collection_role = { "id": None, "角色名称": None, "等级": None,"职业": None, "角色评分": None,
                                 "战斗状态": None, "实时位置": None,  "饷银": None, "金币": None,"updated_at": 0}
    #todo,任务的总体流程,节点,修改
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
    def combat_condition(self,forced_attack=True):
        """
        战斗状态
        :param forced_attack: 是否强制攻击
        :return:
        """
        if self.skill_combos:
            if self.skill_combos:  # 技能连击启动的
                logger.warning("技能连击启动")
                Role_Skill(self.py, self.td_hwnd, role_skill_蜀山_dict, True, 20,forced_attack=forced_attack).run()
                self.skill_combos = False #技能连击结束,关闭技能连击

    def extract_keys_and_ids(self,dict_a):
        """
        从字典中提取键，如果键中包含方括号或中文引号，则拆分出词条和ID。

        示例字典:
        dict_a = {
            '断水不见「741751237': [[13, 11, 161, 24, 0.951]],
            '46级': [[11, 28, 51, 43, 0.999]]
        }

        :param dict_a: 包含词条和ID的字典
        :return: 提取出的扁平元组
        """
        result = []
        for key in dict_a.keys():
            # 检查是否包含方括号或中文引号
            if '[' in key or '「' in key:
                if '[' in key:
                    name, id_value = key.split('[', 1)  # 拆分方括号
                else:
                    name, id_value = key.split('「', 1)  # 拆分中文引号

                id_value = id_value.strip(']」')  # 去掉尾部的方括号或中文引号
                result.append(name)
                result.append(id_value)
            else:
                # 如果没有ID，直接添加词条
                result.append(key)  # 直接添加词条

        return tuple(result)

    def merge_keys(self,data):
        keys = list(data.keys())
        merged_keys = []

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                # 获取y1的值
                y1_1 = data[keys[i]][0][1]  # 获取第一个值的第二个元素
                y1_2 = data[keys[j]][0][1]  # 获取第二个值的第二个元素

                # 检查差值
                if abs(y1_1 - y1_2) < 6:
                    merged_keys.append((keys[i], keys[j]))

        return merged_keys

    def task_角色信息(self):
        """
        读取角色界面的信息
        :return:
        """
        self.ls_progress="任务中"
        self.node_current="task_角色信息"

        role_occupation=None #职业
        real_time_position=None #实时位置
        role_scoring=0 #角色评分

        if self.node_flag:
            level_str = self.collection_role["等级"]
            if level_str:
                logger.info(f"任务入口:角色信息更新成功,等级为{self.collection_role['等级']}")
                level_int = int(level_str.replace("级", ""))
                if level_int <= 30:
                    return "task_failed"

            self.node_current = "task_包裹信息"
            self.node_flag = False # 恢复节点标志
            return "task_finish"

        if "角色界面" in self.game_interface[0]:
            """
            collection_role = {"句柄":None,"端口": None,"ip": None, "id": None,"角色名称":None,"等级": None, "职业": None,"角色评分":None,
                            "战斗状态":None,"实时位置":None,"血量":None,"交互器":None,"饷银":None,"金币":None,"updated_at":None}
            """
            logger.info("角色界面,保存角色信息")
            game_role=self.find_ppocr_op(472, 219, 649, 278)#角色名称,id

            role_scoring_data=self.find_ppocr_op(882, 219, 1063, 252) #角色评分
            if self.get_value_from_key("res/dtws/other/蜀山图标.bmp","dic_image_hand",): #todo:其他职业这里更改
                role_occupation="蜀山"
            if self.map_name and self.coord: # 实时位置
                real_time_position=(self.map_name,self.coord[0],self.coord[1])


            logger.info(f"角色信息:{game_role},角色评分:{role_scoring_data}")
            #角色信息:{'寒冰温柔[456371254]': [[11, 1, 161, 22, 0.94]], '30级': [[12, 22, 53, 38, 0.999]]},角色评分:{'303': [[24, 5, 60, 25, 0.999]]}
            role_name,role_id,role_level=self.extract_keys_and_ids(game_role)
            if role_scoring_data:
                role_scoring=list(role_scoring_data.keys())[0]
            logger.info(f"角色名称:{role_name},角色id:{role_id},角色等级:{role_level},角色评分:{role_scoring}")
            self.collection_role={"角色名称":role_name,"等级":role_level,"角色评分":role_scoring,"id":role_id,
                                  "职业": role_occupation,"实时位置":real_time_position,} #更新角色信息
            self.mongodb_query={"id":role_id} #查询条件

            self.mouse_left_click_op(*self.game_interface[1:], delay_time=1) #界面关闭

            self.node_flag=True #节点完成

        elif "游戏主界面" in self.game_interface[0]:
            if self.coord[-1]:
                self.key_press_op("C")

        else:
            self.界面关闭()

    def task_包裹信息(self):
        """
        collection_role = {"饷银":None,"金币":None,}
        """
        self.ls_progress="任务中"
        self.node_current="task_包裹信息"

        if self.node_flag:
            self.node_flag=False # 恢复节点标志
            self.node_current="task_信息采集完成"

        elif self.game_interface[0]  in "背包界面":
           logger.info(f"包裹界面范围:{self.parcel_scope}")
           res_point=self.get_value_from_key("无双币","dic_word_hand")
           logger.info(f"无双币:{res_point}")
           #[(1169, 556, 0.994)]
           if res_point:
               x1,y1=res_point[0][0],res_point[0][1]+20
               x2,y2=res_point[0][0]+100,res_point[0][1]+70+20
               logger.info(f"无双币坐标:{x1,y1,x2,y2}")
               dict_data=self.find_ppocr_op(x1, y1, x2, y2)
               tupe_data=self.merge_keys(dict_data) #合并
               logger.info(f"数量:{tupe_data}")
               #[('银', '10'), ('金币', '6')]
               for data in tupe_data:
                   if "银" in data[0]:
                       self.collection_role["饷银"]=data[1]
                   if "币" in data[0] or "金" in data[0]:
                       self.collection_role["金币"]=data[1]

           self.mouse_left_click_op(*self.game_interface[1:], delay_time=1)  # 界面关闭
           self.node_flag=True #节点完成

        elif self.game_interface[0]  in "游戏主界面":
            self.key_press_op("B")

        else:
            self.界面关闭()

    def task_task_信息采集完成(self):
        self.ls_progress="任务中"
        self.node_current="task_信息采集完成"

        if self.node_flag: #节点完成
            self.node_flag=False # 恢复节点标志
            return "task_finish"

        elif self.game_interface[0]  in "游戏主界面":
            logger.info(f"角色信息:{self.collection_role}")

            if self.mongodb_query: #更新数据库
                self.collection_role["updated_at"]=int(time.time()) #更新时间
                self.db_handler.update_document_one("collection_role",self.mongodb_query, self.collection_role)
                self.node_flag=True #节点完成
        else:
            self.界面关闭()
    def handle_task(self):
        task_methods = {
            'task_角色信息': self.task_角色信息,
            'task_包裹信息': self.task_包裹信息,
            'task_信息采集完成': self.task_task_信息采集完成,
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
        logger.debug(f"当前节点:{self.node_current}")
        self.queue_massage(self.node_current) #队列信息

        if self.node_current in ["task_信息采集完成",]:
            if self.task_task_信息采集完成()=="task_finish":
                role_lever=self.collection_role["等级"]
                return {"task_finish":role_lever}
        elif not self.node_current or "task_角色信息" in self.node_current:
            if self.task_角色信息()=="task_failed":
                return {"task_finish":-2}
        else:
            self.handle_task()

    def 任务操作(self) -> None:
        """所有的节点需要接入这里才能运行, 测试也是这里添加测试代码"""
        dict_data = self.task_flow()

        if isinstance(dict_data, dict):
            # 从字典中获取任务完成状态
            role_level = dict_data.get("task_finish", -1)  # 默认值为 -1
            self.ls_progress = "任务完成"  # 模块运行结束
            self.task_name = "数据库"  # 任务名称
            self.program_result = role_level  # 模块运行返回值

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

dic_reward_tasks_execution={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        "无双币":(970,560,1080,600,0.8,),#无双币
        # "收藏":(550,199,616,234,0.8,0,0,1,10),

        },
    "image": {
        "res/dtws/other/蜀山图标.bmp":(419, 221, 470, 269,0.8),
        # "res/dtws/reward_task/悬赏令_数目1.bmp":(547,255,599,298,0.8),#悬赏令_数目1
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
reward_merged_dict_execution=merge_dicts(dic_reward_tasks_execution,public_res)

#任务信息,是否需要去除背景色
"""
task_background_scope:识别范围
1不启用背景色,默认是识别文字资源为数字4的资源
task_name_text_alternative_parameters=task_background_scope
2启用背景色,具体参数参考basic_function/parent_module.py里get_text_alternative方法
task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
"""
task_background_scope=(1177,251,1395,552)
task_execution_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#文字模糊匹配
"""
字典形式,key为模糊匹配的关键字符串,key可以用"|"符号设置多关键字,value为标准字符串
如果需要合并请使用,参数参考public_function/public_function.py里merge_dicts方法
word_standard_dict=merge_dicts(task_name_word_standard_dict,public_dict)
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_word_standard_dict
"""
task_name_word_standard_dict={"疑犯":"疑犯(0/1)","犯":"疑犯(已完成)","交付":"点击交付" }

# 过滤的关键字
"""
这里可以自定义,容易出错的关键词,一般不定义
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_keywords_list
"""
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用


# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#todo,窗口类名
# win_title = vnc_window#todo,窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = vnc_ip #todo,服务器地址
# vnc_port = int(vnc_port)  #todo, 默认 VNC 端口，根据实际情况可能有所不同
#
# def run():
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port)
#     task=task_execution(py,win_hwnd[0],reward_merged_dict,True,100,task_name_text_alternative_parameters,task_name_word_standard_dict)
#     res=task.run()
#     print(res)
#
# run()