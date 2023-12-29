from collections import namedtuple
from entitas import Entity, Matcher, Context, Processors, ExecuteProcessor, ReactiveProcessor, GroupEvent, InitializeProcessor
import time


print('hello python!')

'''
全局变量
'''
running = True
frame_duration = 1 / 30  # 每帧所需时间（30帧每秒）


'''
全局函数
'''
def stop_running():
    global running
    running = False

'''
components
'''
Position = namedtuple('Position', 'x y')
Health = namedtuple('Health', 'value')
Movable = namedtuple('Movable', '')

'''
MyInitializeProcessor
'''
class MyInitializeProcessor(InitializeProcessor):

    def __init__(self, context):
        self._context = context
      
    def initialize(self):
        print('MyInitializeProcessor')

'''
MyExecuteProcessor
'''
class MyExecuteProcessor(ExecuteProcessor):

    def __init__(self, context):
        self._context = context
        self._execute_count = 0
       
    def execute(self):
        self._execute_count += 1
        print('MyExecuteProcessor = ', self._execute_count)
        if (self._execute_count > 30):
            stop_running()


'''
MyReactiveProcessor
'''
# class MyReactiveProcessor(ReactiveProcessor):

#     def __init__(self, context):
#         super().__init__(context)
#         self._context = context

#     def get_trigger(self):
#         return {Matcher(Position): GroupEvent.ADDED}

#     def filter(self, entity):
#         return entity.has(Position)

#     def react(self, entities):
#         for entity in entities:
#             print('111111')
#             #print(entity.get(EmptyComponent).name)
#             # print(entity.get(EmptyComponent).index)
           

'''
执行核心区间
'''
print("game start!!!!!")


context = Context()

processors = Processors()
processors.add(MyInitializeProcessor(context))
processors.add(MyExecuteProcessor(context))

processors.initialize()
processors.activate_reactive_processors()


while running:

    start_time = time.time()  # 获取当前时间

    processors.execute()
    processors.cleanup()

    end_time = time.time()  # 获取循环结束的时间
    elapsed = end_time - start_time  # 计算循环执行所花费的时间
    if elapsed < frame_duration:
        time.sleep(frame_duration - elapsed)  # 如果循环执行时间小于一帧所需时间，等待剩余时间
 

processors.clear_reactive_processors()
processors.tear_down()

print("game over!!!!!")



