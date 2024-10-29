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
        print(f'Entering state {self.cur_state}')


    def update(self):
        self.cur_state.do(self.obj)
        if self.event_q:#리스트에 하나라도 있으면 true
            e = self.event_q.pop(0)

            for check_event , next_state in  self.transitions[self.cur_state].items():
                                            #트렌지션 테이블을 확인했는데 table에 키가 없으면 오류 발생
                if check_event(e): # 내가 원하는 상태에서
                    print(f'Exit from  {self.cur_state}')# 테이블을 잘 썻는가?
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    print(f'Enter into {self.cur_state}')# 테이블을 잘 썻는가?
                    self.cur_state.enter(self.obj)
                    return # 제대로 이벤트에 따른 상태변환 완료
            #이 시점에 도달하는 것은 event에 따른 전환을 못함
            print(f'        Warning: {e} not handled at state {self.cur_state}')
    def draw(self):
        self.cur_state.draw(self.obj)

    def add_event(self, event):
        self.event_q.append(event)
        print(f'    Debug: new event {event} added to event queue ')

    def set_transitions(self, transitions):
        self.transitions = transitions

