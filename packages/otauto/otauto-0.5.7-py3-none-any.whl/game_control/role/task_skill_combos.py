import random
import time

from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
"""
功能:技能连招
日期:2025-2-27 13:33:28
描述:
    普通高频技能
    普通延迟技能
    怒气技能
    状态技能
    加血技能
    技能释放权重:加血技能>状态技能>怒气技能>普通高频技能>普通延迟技能 
"""

class TaskSkillCombos:
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle):

        self.skill_状态技能_last_time = 0 #记录上次释放状态技能的时间
        if self.role_sect in ["少林"]:
            self.skill_快捷键_dict=skill_快捷键_dict["少林"]
        elif self.role_sect in ["蜀山"]:
            self.skill_快捷键_dict=skill_快捷键_dict["蜀山"]
        elif self.role_sect in ["凌云","凌云寨"]:
            self.skill_快捷键_dict=skill_快捷键_dict["凌云"]
        elif self.role_sect in ["天煞"]:
            self.skill_快捷键_dict=skill_快捷键_dict["天煞"]

        self.skill_普通高频=self.skill_快捷键_dict["普通高频技能"]
        self.skill_普通延迟=self.skill_快捷键_dict["普通延迟技能"]
        self.skill_怒气技能=self.skill_快捷键_dict["怒气技能"]
        self.skill_状态技能=self.skill_快捷键_dict["状态技能"]
        self.skill_加血技能=self.skill_快捷键_dict["加血技能"]
        self.skill_召唤技能=self.skill_快捷键_dict["召唤技能"]

    def task_普通高频技能(self):
        """
        职业的基本攻击技能
        """
        for skill_num in self.skill_普通高频:
            self.key_press(f"{skill_num}", delay_time=0.2)
    def task_普通延迟技能(self):
        # 随机选择的数量，确保不超过 numbers 的长度
        if len(self.skill_普通延迟)>=2:
            num_to_select = random.randint(2, len(self.skill_普通延迟))
            selected_elements = random.sample(self.skill_普通延迟, num_to_select)  # 随机抽样
            for skill_num in selected_elements:
                self.key_press(f"{skill_num}", delay_time=1)
        else:
            self.key_press(f"{self.skill_普通延迟[0]}",delay_time=0.6)
    def task_怒气技能(self):
        skill_num = random.sample(self.skill_怒气技能, 1) # 随机选择一个元素
        self.key_press(f"{skill_num[0]}", delay_time=0.2)
    def task_状态技能(self):
        for skill_num in self.skill_状态技能:
            if skill_num != "-1":
                self.mouse_left_click(*state_points_dict[skill_num], delay_time=1.5)
                self.mouse_move(838,797)
    def task_加血技能(self):
        for skill_num in self.skill_加血技能:
            if skill_num != "-1":
                self.key_press(f"{skill_num}", delay_time=0.6)
    def task_召唤技能(self):
        for skill_num in self.skill_召唤技能:
            if skill_num != "-1":
                self.key_press(f"{skill_num}", delay_time=0.6)
    def task_加血值判断(self):
        """
        血量百分比太小
        """
        if self.role_hp: #存在怒气值
            # 使用 split() 方法将字符串分割为列表
            ls = self.role_hp.split("/")
            # 将字符串列表转换为整数列表
            int_list = [int(num) for num in ls]
            # 计算百分比
            percentage = int((int_list[0] / int_list[1]) * 100)
            logger.info(f"{int_list},血量百分比:{percentage}")
            if percentage<60:
                logger.error("血量过低")
                return True
        else:
            return False

    def task_怒气值判断(self):
        if self.role_rp: #存在怒气值
            # 使用 split() 方法将字符串分割为列表
            ls = self.role_rp.split("/")
            # 将字符串列表转换为整数列表
            int_list = [int(num) for num in ls]
            if int_list[0]>=60:
                return True
        else:
            return False

    def task_skill_release(self):
        if self.task_加血值判断():
            if self.role_sect in ["少林"]:
                self.task_加血技能() #  释放加血技能
            else:
                self.key_press("_",delay_time=0.3) #血瓶

        if abs(int(time.time())-self.skill_状态技能_last_time)>=28*60: # 状态技能间隔为28分钟
            self.task_状态技能() # 释放状态技能
            self.skill_状态技能_last_time=int(time.time())

        if self.task_怒气值判断():
            self.task_怒气技能() # 释放怒气技能

        self.task_普通高频技能() # 释放普通高频技能

        self.task_普通延迟技能() # 释放普通延迟技能

    def task_skill_attack(self):
        """
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器
        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        函数写入这里
        """
        logger.success(f"任务详情:{self.__class__.__name__}")
        logger.success(f"节点信息:{self.node_current}")
        if self.target_info["lock"]: # 锁定目标
            self.task_skill_release()
        else:
            return "task_finish" #模块运行结束

state_points_dict={
"alt+1":(806,841),
"alt+2":(842,846),
"alt+3":(883,843),
}
skill_快捷键_dict={
    "少林":{
        "普通高频技能":["1"],
        "普通延迟技能":["3","5","6","8"],
        "怒气技能":["2","4","7"],
        "状态技能":["alt+2"],
        "加血技能":["9"],
        "召唤技能":["-1"],
    },
    "蜀山":{
        "普通高频技能":["1"],
        "普通延迟技能":["3","4","5","7"],
        "怒气技能":["2","8"],
        "状态技能":["alt+1","alt+2","alt+3"],
        "加血技能":["-1"],
        "召唤技能":["6"],
    },
    "凌云":{
        "普通高频技能":["1"],
        "普通延迟技能":["2"],
        "怒气技能":["8"],
        "状态技能":["-1"],
        "加血技能":["3"],
        "召唤技能": ["4","5"],
    },
    "天煞":{
        "普通高频技能":["1"],
        "普通延迟技能":["2","3","4","5"],
        "怒气技能":["6","7"],
        "状态技能":["-1"],
        "加血技能":["-1"],
        "召唤技能": ["-1"],
    },
}
