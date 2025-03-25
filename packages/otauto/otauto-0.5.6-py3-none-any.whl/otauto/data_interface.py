import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
import time # 用于暂停程序
import queue # 用于多线程间通信
# from concurrent.futures import ProcessPoolExecutor # 用于多进程

from loguru import logger # 用于日志记录
import asyncio # 用于异步编程

from otauto.data_cleansing import DataCleansing
from otauto.image_processing import ImageProcessor
from otauto.vnc_recognition import VNC_recognition

stop_event = threading.Event()  # 创建一个事件用于停止线程
data_ready_event = threading.Event()  # 用于通知数据准备好

class LimitedQueue:
    """
    一个有最大容量的队列
    :param max_size: 队列的最大容量
    """
    def __init__(self, max_size):
        self.queue = queue.Queue(maxsize=max_size)
    def put(self, item):
        if self.queue.full():
            self.queue.get()  # 移除最旧的项
        self.queue.put(item)
    def get(self):
        return self.queue.get()
    def size(self):
        return self.queue.qsize()
    def empty(self):
        return self.queue.empty()
    def __iter__(self):
        return iter(self.queue.queue)


result_queue = LimitedQueue(max_size=3)  # 设定队列最大容量为3


async def main(vnc: VNC_recognition, parameter_dict, queue_handle, interval: float = 0.6):
    """
    主函数
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param queue_handle: 线程队列
    :param interval: 截图间隔时间,默认为0.6秒
    """

    imageprocessor = ImageProcessor()
    data_cleansing = DataCleansing(parameter_dict)
    time.sleep(3)

    try:
        async for updated_image in vnc.async_capture_full_screen_as_numpy(interval, debug=False):
            if stop_event.is_set():
                stop_event.clear()  # 清除事件, 以便将来可以重新使用
                logger.success(f"数据线程收到停止信号,停止捕获。")
                return

            queue_msg = None

            if not queue_handle.empty():
                queue_msg = queue_handle.get()
                logger.info(f"收到线程队列信息: {queue_msg}")

                if "interval" in queue_msg:
                    new_interval = queue_msg["interval"]
                    logger.info(f"截图时间修改为: {new_interval}")
                    time.sleep(new_interval)
                    updated_image=None # 移除队列中的元素
                if "image" not in queue_msg and  "word" not in queue_msg and  "mutil_colors" not in queue_msg:
                    queue_msg=None # 移除队列中的元素

            if updated_image is not None:
                logger.success(f"数据线程启动成功, Updated image captured successfully!")
                res = imageprocessor.data_treating_bytes_area(parameter_dict, updated_image)
                res_dict = res["treating_data"]
                numpy_data = res["numpy_data"]
                res_data = data_cleansing.run(res_dict, numpy_data,queue_msg)
                logger.debug(f"data_cleansing result from main: {res_data}")

                finish_data = {
                    "data_cleansing": res_data,
                    "uptime": time.time(),
                    "numpy_data": res["numpy_data"],
                }
                result_queue.put(finish_data)
                data_ready_event.set()  # 通知 run_info 数据已准备好
            else:
                logger.warning("Failed to capture updated image.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        traceback.print_exc()  # 打印堆栈跟踪



def run_asyncio_in_thread(vnc: VNC_recognition, parameter_dict,queue_handle, interval: float = 0.6):
    """
    在线程中运行异步函数
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param queue_handle: 线程队列
    :param interval: 截图间隔时间,默认为0.6秒
    """
    asyncio.run(main(vnc, parameter_dict, queue_handle, interval))

def run_info(task_instance, loop_num: int = 20, delay_time: float = 0.6):
    """
    :param task_instance: 任务类的实例
    :param delay_time: 暂停时间 0.5-1秒,空载的时候最小0.5秒
    :param loop_num: 循环次数
    """
    i = 0
    time.sleep(5)

    if task_instance is None:
        logger.error("任务实例未提供.")
        return

    while True:
        time.sleep(delay_time) #todo : 这里添加暂停时间
        i += 1
        logger.info(f"程序运行中... 当前循环:{i}")

        if i >= loop_num:
            logger.success("程序运行到设置的最大数,发送停止信号.")
            stop_event.set()  # 设置停止事件
            return

        logger.info(f"队列大小: {result_queue.size()}")

        # 检查队列的大小
        if result_queue.size() > 1:
            # 清空队列
            while not result_queue.empty():
                result_queue.get()  # 逐个移除队列中的元素

        # 等待数据准备好
        data_ready_event.wait()  # 等待直到数据准备好
        data_ready_event.clear()  # 清除事件, 以便下次使用

        if not result_queue.empty():
            latest_result = result_queue.get()
            # 执行任务的 run 方法
            task_result = task_instance.run(latest_result) #todo:这里加其他结果
            if isinstance(task_result, str):
                if task_result in ["task_finish", "task_error", "task_fail", "task_wait"]:
                    logger.success(f"任务完成,发送停止信号.任务结果: {task_result}")
                    stop_event.set()  # 设置停止事件
                    return task_result  # 返回任务结果
            elif isinstance(task_result, dict):
                logger.success(f"任务完成,发送停止信号.任务结果: {task_result}")
                stop_event.set()  # 设置停止事件
                return task_result  # 返回任务结果
        else:
            logger.info("队列为空,没有结果可处理")

def run_in_process(vnc,parameter_dict, task_instance,queue_handle,loop_num:int=20,delay_time=0.5,interval: float = 0.6):
    """
    在进程中运行任务
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param task_instance: 任务类的实例
    :param queue_handle: 线程队列
    :param loop_num: 循环次数
    :param delay_time: 暂停时间,空载的时候最小0.5秒,不然数据不可信
    :param interval: 截图间隔时间,默认为0.6秒
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        executor.submit(run_asyncio_in_thread, vnc, parameter_dict, queue_handle,interval)  # 提交第一个任务,用于捕获图像,识别图像,处理数据
        future2 = executor.submit(run_info,task_instance,loop_num,delay_time)  # 提交第二个任务,用于处理数据,执行任务逻辑

        # 只获取 future2 的结果
        try:
            result = future2.result()  # 获取结果
            logger.success(f"任务完成: {result}")
        except Exception as e:
            logger.error(f"任务发生异常: {e}")
            traceback.print_exc()  # 打印堆栈跟踪

    return result


# if __name__ == "__main__":
#     # 使用进程池执行器运行任务
#     with ProcessPoolExecutor() as executor:
#         executor.submit(run_in_process, "192.168.110.245", 5901)  # 启动一个进程并运行 run_in_process
#         executor.submit(run_in_process, "192.168.110.245", 5902)
#         executor.submit(run_in_process, "192.168.110.245", 5903)
#         executor.submit(run_in_process, "192.168.110.245", 5904)