import math
import time
from queue import Queue
from vstd import *


LOW_PULSE = False
HIGH_PULSE = True

low_pulses = 0
high_pulses = 0
sent_pulses: Queue['SentPulse'] = Queue()


class SentPulse:
    def __init__(self, pulse: bool, from_module: 'Module', to_module: 'Module'):
        self.pulse = pulse
        self.from_module = from_module
        self.to_module = to_module

    
    def resolve(self):
        self.to_module.handle_input(self.pulse, self.from_module)


    def __repr__(self) -> str:
        name = self.from_module.name
        name += ' -low-> ' if self.pulse == LOW_PULSE else ' -high-> '
        name += self.to_module.name
        return name



class Module:
    def __init__(self, name: str):
        self.name = name
        self.connected_out: list['Module'] = []
        self.connected_in: list['Module'] = []


    def connect_to(self, module: 'Module'):
        self.connected_out.append(module)
        module.connect_from(self)


    def connect_from(self, module: 'Module'):
        self.connected_in.append(module)


    def handle_input(self, pulse: bool, recived_from: 'Module'):
        global high_pulses
        global low_pulses

        if pulse == HIGH_PULSE:
            high_pulses += 1
        else:
            low_pulses += 1


    def send_pulse(self, pulse: bool):
        for module in self.connected_out:
            sent_pulses.put_nowait(SentPulse(pulse, self, module))


    def __repr__(self):
        name = self.name + ' -> '
        for module in self.connected_out:
            name += module.name + ', '

        return name
    


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state = LOW_PULSE

    
    def handle_input(self, pulse: bool, recived_from: Module):
        super().handle_input(pulse, recived_from)

        if pulse == LOW_PULSE:
            if self.state == LOW_PULSE:
                self.state = HIGH_PULSE
                self.send_pulse(HIGH_PULSE)
            else:
                self.state = LOW_PULSE
                self.send_pulse(LOW_PULSE)


    def __repr__(self):
        name = '%' + super().__repr__()
        return name
    


class Conjuntion(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state: dict[Module, bool] = dict()


    def connect_from(self, module: Module):
        super().connect_from(module)
        self.state[module] = LOW_PULSE


    def handle_input(self, pulse: bool, recived_from: Module):
        super().handle_input(pulse, recived_from)

        self.state[recived_from] = pulse

        if all(self.state[i] for i in self.state):
            self.send_pulse(LOW_PULSE)
        else:
            self.send_pulse(HIGH_PULSE)


    def __repr__(self):
        name = '&' + super().__repr__()
        return name



def get_input():
    modules: dict[str, Module] = dict()

    with open('day20.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().split()

            if line == []:
                break

            name = line[0]

            if name == 'broadcaster':
                modules[name] = Module(name)
                broadcaster = modules[name]

            elif name[0] == '%':
                name = name[1:]
                modules[name] = FlipFlop(name)

            elif name[0] == '&':
                name = name[1:]
                modules[name] = Conjuntion(name)

        file.close()

    with open('day20.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().split()

            if line == []:
                break

            name = line[0].removeprefix('%').removeprefix('&')
            module = modules[name]

            for i in range(2, len(line)):
                module_name = line[i].removesuffix(',')

                if not module_name in modules.keys():
                    modules[module_name] = Module(module_name)
                
                module.connect_to(modules[module_name])

    return modules, broadcaster



def press_button(modules: list[Module], broadcaster: Module):
    global low_pulses 
    low_pulses += 1 # (the button itself sends a low pulse)
    broadcaster.send_pulse(LOW_PULSE)

    while not sent_pulses.empty():
        sent_pulses.get().resolve()


def main():
    modules, broadcaster = get_input()

    for i in range(1000):
        press_button(modules, broadcaster)
    
    print('Low Pulses: ' + str(low_pulses) + '\nHigh Pulses: ' + str(high_pulses), '\n')

    return low_pulses * high_pulses


print(main())