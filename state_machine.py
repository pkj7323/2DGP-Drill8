from pico2d import *

def space_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0]=='TIME_OUT'


class StateMachine:
    def __init__(self,obj):
        self.obj = obj# 어떤 오브젝트를 위한 상태머신인지 저장해둠
        self.event_q = [] # 상태 이벤트 저장 리스트
    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서 그걸로 현재 상태를 정의


    def update(self):
        self.cur_state.do(self.obj)
        if self.event_q:#리스트에 하나라도 있으면 true
            e = self.event_q.pop(0)
            #이시점의 우리가 아는 정보는?
            # e
            # cur_state
            # 현재 상태와 련재 발생한 이벤트에 따라서 다음 상태를 결정하는 방법은?
            # 상태변환 테이블을 이용
            for check_event , next_state in  self.transitions[self.cur_state].items():#dict뽑아서
                if check_event(e): # 내가 원하는 상태에서
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    self.cur_state.enter(self.obj)
    def draw(self):
        self.cur_state.draw(self.obj)

    def add_event(self, event):
        self.event_q.append(event)

    def set_transitions(self, transitions):
        self.transitions = transitions

