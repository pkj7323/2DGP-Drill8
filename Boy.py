import math

import pygame
from pico2d import *

from state_machine import StateMachine, time_out, space_down


#상태를 클래스를 통해서 정의 한다.
class Idle:
    @staticmethod#decolator 데코레이터 장식? 함수의 기능을 바꾼다.
    def enter(obj):
        obj.start_time = get_time()
    @staticmethod
    def exit(obj):
        pass
    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 8
        if get_time() - obj.start_time>3:
            obj.state_machine.add_event(('TIME_OUT',0))
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(obj.frame * 100, obj.action * 100, 100, 100, obj.x, obj.y)

class Sleep:
    @staticmethod  # decolator 데코레이터 장식? 함수의 기능을 바꾼다.
    def enter(obj):
        pass

    @staticmethod
    def exit(obj):
        pass

    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 8

    @staticmethod
    def draw(obj):
        obj.image.clip_composite_draw(obj.frame * 100, 300, 100, 100, 3.141592/2, '', obj.x, obj.y-25,100,100)

class Run:
    @staticmethod
    def enter(obj):
        # 초기 방향을 설정함
        obj.dir = 1
        obj.action = 3
        obj.frame = 0
        pass
    @staticmethod
    def exit(obj):
        pass
    @staticmethod
    def do(obj):
        obj.x += obj.dir * 5
        obj.frame = (obj.frame + 1) % 8
        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(obj.frame * 100, obj.action * 100, 100, 100, obj.x, obj.y)



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)#소년 객체의 스테이트머신 생성 만들때 소년의 레퍼런스를 넘겨줌
        self.state_machine.start(Run)#초기상태가 idle,Sleep
        self.state_machine.set_transitions(
            {

                Idle : { time_out : Sleep},
                Sleep : { space_down : Idle},
                Run : {} # Run 상태에서 전환하지 않겠다는 의미
            }
        )#dict전달 #함수이름이 똑같아야함 time_out,space_down

    def update(self):
        self.state_machine.update()

    def move(self):
        self.x += 10 * self.dir

    def handle_event(self, event):
        #event : 입력 이벤트
        #우리가 넘겨줄거 튜플 형식
        self.state_machine.add_event(('INPUT',event))

    def draw(self):
        self.state_machine.draw()
