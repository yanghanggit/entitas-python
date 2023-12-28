from collections import namedtuple
from entitas import Entity, Matcher, Context

print('hello python!')

Position = namedtuple('Position', 'x y')
Health = namedtuple('Health', 'value')
Movable = namedtuple('Movable', '')
context = Context()

for _ in range(1):
    entity = context.create_entity()
    entity.name = 'test1'
    entity.add(Position, 3, 7)
    entity.add(Movable)

for _ in range(1):
    entity = context.create_entity()
    entity.name = 'test2'
    entity.add(Health, 100)

entities = context.entities
for e in entities:
    print('e = ', e.name)
    if e.has(Position):
        print('entity.has(Position)')
    if e.has(Movable):
        print('entity.has(Movable)')
    elif e.has(Health):
        print('entity.has(Health)')


