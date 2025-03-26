from game_role.role_skill_蜀山_v2 import *
from public_function.public_function import *
from public_function.public_resources import *
"""
功能:
更新日志:
设计思路:
"""

class task_职业(TaskModule): #todo,修改任务名称
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

    def task_职业判断(self):
        """
        1,对话界面点击对话
        2,完成条件,该节点完成
        :return:
        """
        self.ls_progress="任务中"
        self.node_current="task_职业判断"

        if "游戏主界面" in self.game_interface[0]:
            occupation_tuple=("职业_凌云","职业_蜀山","职业_天煞","职业_少林")
            for occupation in occupation_tuple:
                if self.get_value_from_key(occupation,"dic_image_hand"):
                    return occupation
            else:
                return "职业_未知"

    def handle_task(self):
        task_methods = {
            'task_职业判断': self.task_职业判断,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()


    def 任务操作(self):
        res=self.task_职业判断()
        if res:
            self.ls_progress= "任务完成" #模块运行结束
            self.task_name="职业判断"
            self.program_result=f"{res}" #todo,模块运行返回值,按需更改

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

scope_tuple=(660, 774, 766, 867,0.8)

dic_reward_tasks={
    "word": {
        # 4:(1177,251,1395,552,0.8),#任务信息,这里改写任务信息范围
        # "快捷":(994,560,1080,584,0.8,0,0,1,5),
        },
    "image": {
        # r"res/dtws/camp_task/地图_npc.bmp":(1088,563,1153,618,0.8),#地图npc
        "res/dtws/other/职业_凌云.png":scope_tuple,
        "res/dtws/other/职业_少林.png":scope_tuple,
        "res/dtws/other/职业_蜀山.png":scope_tuple,
        "res/dtws/other/职业_天煞.png":scope_tuple,
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
职业_merged_dict=merge_dicts(dic_reward_tasks,public_res)

#任务信息,是否需要去除背景色
"""
task_background_scope:识别范围
1不启用背景色,默认是识别文字资源为数字4的资源
task_name_text_alternative_parameters=task_background_scope
2启用背景色,具体参数参考basic_function/parent_module.py里get_text_alternative方法
task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能
"""
task_background_scope=(1177,251,1395,552)
task_职业_text_alternative_parameters=task_background_scope #todo,更改名称
# task_name_text_alternative_parameters=(*task_background_scope,task_background_list,40,True)#带有背景色去除功能,按需使用

#文字模糊匹配
"""
字典形式,key为模糊匹配的关键字符串,key可以用"|"符号设置多关键字,value为标准字符串
如果需要合并请使用,参数参考public_function/public_function.py里merge_dicts方法
word_standard_dict=merge_dicts(task_name_word_standard_dict,public_dict)
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_word_standard_dict
"""
task_职业_word_standard_dict={"疑犯":"疑犯(0/1)","犯":"疑犯(已完成)","交付":"点击交付" } #todo,更改名称

# 过滤的关键字
"""
这里可以自定义,容易出错的关键词,一般不定义
如果不定义,默认基础模块加载的是basic_function/word_processing.py里的basic_keywords_list
"""
# keywords_list = ['未完',"(完成","已完成","0/1"] #一般不用

#测试,取消下面注释即可测试

# 窗口设置,获取句柄,注意类名和标题必须同时存在
# win_class = "VNCMDI_Window"#todo,窗口类名
# win_title = "002 "#todo,窗口标题
# win_hwnd=set_win(win_class,win_title)
# vnc_server = "127.0.0.1" #todo,服务器地址
# vnc_port = 5902  #todo, 默认 VNC 端口，根据实际情况可能有所不同
#
#
# def run():
#     #todo,初始化VNCtools,单线程,vnc_password没有密码的话删除
#     py=VNCtools(win_hwnd[0],vnc_server,vnc_port)
#     # todo,注意参数名称更改
#     task=task_name(py,win_hwnd[0],reward_merged_dict,True,50,task_name_text_alternative_parameters,task_name_word_standard_dict)
#     res=task.run()
#     print(res)
#
# run()