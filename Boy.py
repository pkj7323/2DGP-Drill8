import math

from pico2d import *

from state_machine import StateMachine, time_out, space_down, right_down, right_up, left_up, left_down, start_event, \
    key_a_down, key_a_up


#상태를 클래스를 통해서 정의 한다.
class Idle:
    @staticmethod#decolator 데코레이터 장식? 함수의 기능을 바꾼다.
    def enter(obj,e):
        if left_up(e) or right_down(e):
            obj.action = 2
            obj.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            obj.action = 3
            obj.face_dir = 1
        else:
            if obj.dir == 1:
                obj.face_dir = 1
                obj.action = 3
            elif obj.dir == -1:
                obj.face_dir = -1
                obj.action = 2
        obj.dir = 0
        obj.start_time = get_time()
        obj.frame = 0
        #상태에 필요한 초기화
    @staticmethod
    def exit(obj,e):
        if space_down(e):
            obj.fire_ball()
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
        if start_event(e):
            if obj.face_dir == -1:
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
        if obj.face_dir == -1:
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
        if space_down(e):
            obj.fire_ball()
    @staticmethod
    def do(obj):
        obj.x += obj.dir * 5
        obj.frame = (obj.frame + 1) % 8
        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(obj.frame * 100, obj.action * 100, 100, 100, obj.x, obj.y)
class AutoRun:
    @staticmethod
    def enter(boy,e):
        if boy.dir == 0:
            boy.dir = 1
        if boy.dir == 1:
            boy.action = 1
        elif boy.dir == -1:
            boy.action = 0
        boy.frame = 0
        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        if boy.x > 800:
            boy.dir = -1
            boy.action = 0
        elif boy.x < 0:
            boy.dir = 1
            boy.action = 1
        boy.x += boy.dir * 15
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y,150,150)
        elif boy.dir == -1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y,150,150)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)#소년 객체의 스테이트머신 생성 만들때 소년의 레퍼런스를 넘겨줌
        self.state_machine.start(Idle)#초기상태가 idle,Sleep
        self.state_machine.set_transitions(
            {

                Idle : { time_out : Sleep ,right_down : Run, right_up : Run, left_up : Run, left_down : Run
                    , space_down: Idle,key_a_down : AutoRun, key_a_up : AutoRun},
                Sleep : { space_down : Idle, right_down : Run, right_up : Run, left_up : Run, left_down : Run,
                          key_a_down : AutoRun, key_a_up : AutoRun},
                Run : {right_up:Idle, left_up: Idle, right_down : Idle, left_down : Idle
                       ,space_down : Run,key_a_down : AutoRun, key_a_up : AutoRun},
                AutoRun : {time_out : Idle, right_down : Run, right_up : Run, left_up : Run, left_down : Run}
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

    def fire_ball(self):
        if self.face_dir == -1:
            pass
        elif self.face_dir == 1:
            pass