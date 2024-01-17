from collections import namedtuple
from entitas import Entity, Matcher, Context, Processors, ExecuteProcessor, ReactiveProcessor, GroupEvent, InitializeProcessor
import time


print('hello npc_prompt!')


Actor = namedtuple('Actor', 'UUID')
NPC = namedtuple('NPC', 'name')
BackgroundStory = namedtuple('BackgroundStory', 'story')
SingleFavorability = namedtuple('SingleFavorability', 'current min max')

class PromptPipeline:
    def __init__(self):
        self.message = ''


class CreateNPC(InitializeProcessor):

    def __init__(self, context, promptPipeline):
        self._context = context
        self._promptPipeline = promptPipeline
      
    def initialize(self):
        print('创建 Npc')

        npcsBackgroundStory = "在那个古老的时代，我是一位备受尊敬的修仙强者，如今已年届古稀之年。我的白发如雪，脸上刻满岁月的印记，但我的双眼却依然闪烁着智慧之光。我通晓天地之道，能操控自然元素，掌握风云雷电，统御山河河川。每次现身人间，都为世界带来和平与繁荣，我的存在犹如一座不可逾越的神山，永远镇压着邪恶。虽然岁月已经让我白发苍苍，但我仍在修仙之路上不断追求更高的境界，为世界带来希望和奇迹"
        # """
        # 添加一些entities
        # """
        entity = context.create_entity()
        entity.add(Actor, 1024)
        entity.add(NPC, '药尘')
        entity.add(BackgroundStory, npcsBackgroundStory)
        entity.add(SingleFavorability, 50, 0, 100)


class SayHi(ExecuteProcessor):

    def __init__(self, context, promptPipeline):
        self._context = context
        self._promptPipeline = promptPipeline

        self.matcher = Matcher(all_of=[Actor, NPC, BackgroundStory])
        self.group = self._context.get_group(self.matcher)
       
    def execute(self):
      entities = self.group.entities
      if len(entities) > 0:
        entity = next(iter(entities))
        #self.test(entity)
        prompt = self.make_prompt(entity)
        #print(prompt)
        self._promptPipeline.message += prompt

      
    def test(self, entity):
        print('_______test________')
        print('UUID = ', entity.get(Actor).UUID)
        print('name = ', entity.get(NPC).name)
        print('story = ', entity.get(BackgroundStory).story)
            

    def make_prompt(self, entity):
        name = entity.get(NPC).name
        story = entity.get(BackgroundStory).story
        return '[我叫{},{}]'.format(
            name, story)


context = Context()
prompt_pipeline = PromptPipeline()

processors = Processors()
processors.add(CreateNPC(context, prompt_pipeline))
processors.add(SayHi(context, prompt_pipeline))


####
processors.activate_reactive_processors()
processors.initialize()
####
loop = 1
while loop > 0:
    loop -= 1
    ###
    prompt_pipeline.message = ''
    ###
    processors.execute()
    processors.cleanup()
    ###
    print(prompt_pipeline.message)
    ###

processors.clear_reactive_processors()
processors.tear_down()



# 你是一个对话游戏，游戏规则如下

# 组成人物：
# 1个NPC；
# 1个玩家（就是我）;

# NPC生成规则：主体由我提供的文字描述（自述）来生成，其余你可以自由发挥与补充；
# NPC的自述如下：[我叫药尘,在那个古老的时代，我是一位备受尊敬的修仙强者，如今已年届古稀之年。我的白发如雪，脸上刻满岁月的印记，但我的双眼却依然闪烁着智慧之光。我通晓天地之道，能操控自然元素，掌握风云雷电，统御山河河川。每次现身人间，都为世界带来和平与繁荣，我的存在犹如一座不可逾越的神山，永远镇压着邪恶。虽然岁月已经让我白发苍苍，但我仍在修仙之路上不断追求更高的境界，为世界带来希望和奇迹]

# 对话过程中，要求NPC以第一人称来做对话。

