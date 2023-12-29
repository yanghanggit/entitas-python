from collections import namedtuple
from entitas import Entity, Matcher, Context, Processors, ExecuteProcessor, ReactiveProcessor, GroupEvent, InitializeProcessor
import time


print('hello python!')

'''
全局变量
'''
running = True
context = Context()

'''
全局函数
'''
def stop_running():
    global running
    running = False

'''
components
'''
EmptyComponent = namedtuple('EmptyComponent', 'name index')


'''
MyInitializeProcessor
'''
class MyInitializeProcessor(InitializeProcessor):

    def __init__(self, context):
        self._context = context
      
    def initialize(self):
        entity = self._context.create_entity()
        entity.add(EmptyComponent, 'empty', 1024)

'''
MyExecuteProcessor
'''
class MyExecuteProcessor(ExecuteProcessor):

    def __init__(self, context):
        self._context = context
       
    def execute(self):
        return
        #print('MyExecuteProcessor = ')


'''
MyReactiveProcessor
'''
class MyReactiveProcessor(ReactiveProcessor):

    def __init__(self, context):
        super().__init__(context)
        self._context = context

    def get_trigger(self):
        return {Matcher(EmptyComponent): GroupEvent.ADDED}

    def filter(self, entity):
        return entity.has(EmptyComponent)

    def react(self, entities):
        for entity in entities:
            print(entity.get(EmptyComponent).name)
            print(entity.get(EmptyComponent).index)
           

'''
正式执行
'''
print("game start!!!!!")

processors = Processors()
processors.add(MyInitializeProcessor(context))
processors.add(MyReactiveProcessor(context))
processors.add(MyExecuteProcessor(context))
processors.initialize()
processors.activate_reactive_processors()

frame_duration = 1 / 30  # 每帧所需时间（30帧每秒）
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



