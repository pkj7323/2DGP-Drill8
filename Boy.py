import math

from pico2d import *

from state_machine import StateMachine, time_out, space_down, right_down, right_up, left_up, left_down


#상태를 클래스를 통해서 정의 한다.
class Idle:
    @staticmethod#decolator 데코레이터 장식? 함수의 기능을 바꾼다.
    def enter(obj,e):
        if left_up(e) or right_down(e):
            obj.action =2
        elif right_up(e) or left_down(e):
            obj.action = 3
        obj.start_time = get_time()
        obj.frame = 0
        #상태에 필요한 초기화
    @staticmethod
    def exit(obj,e):
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
    def enter(obj,e):
        if obj.dir == -1:
            obj.action = 2
        else:
            obj.action = 3

    @staticmethod
    def exit(obj,e):
        pass

    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 8

    @staticmethod
    def draw(obj):
        if obj.dir == -1:
            obj.image.clip_composite_draw(obj.frame * 100, obj.action * 100, 100, 100, math.radians(-90), '', obj.x,
                                          obj.y - 25, 100, 100)
        else:
            obj.image.clip_composite_draw(obj.frame * 100, obj.action * 100, 100, 100, math.radians(90), '', obj.x,
                                          obj.y - 25, 100, 100)
class Run:
    @staticmethod
    def enter(obj,e):
        # 초기 방향을 설정함
        if right_down(e) or left_up(e):
           obj.dir = 1
           obj.action = 1
        elif right_up(e) or left_down(e):
           obj.dir = -1
           obj.action = 0
        obj.frame = 0


    @staticmethod
    def exit(obj,e):
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
        self.state_machine.start(Idle)#초기상태가 idle,Sleep
        self.state_machine.set_transitions(
            {

                Idle : { time_out : Sleep ,right_down : Run, right_up : Run, left_up : Run, left_down : Run},
                Sleep : { space_down : Idle, right_down : Run, right_up : Run, left_up : Run, left_down : Run },
                Run : {right_up:Idle, left_up: Idle, right_down : Idle, left_down : Idle}
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
