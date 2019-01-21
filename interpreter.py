from settings import *


class UnknownInstruction(Exception):
    pass


class Interpreter:
    def __init__(self, filename=None, verbosity=False):
        self.label_lut = {}
        self.memory_map = {}
        self.code = None
        self.line_counter = 0
        self.verbosity = verbosity

        if filename:
            self.open(filename)

    def run(self, input_list=None):
        if isinstance(input_list, list):
            for x_id, x_val in enumerate(input_list):
                self.memory_map['x%d' % x_id] = x_val

        self.line_counter = 0
        while self.line_counter < len(self.code):
            self.process_line()
            self.debug_print('result counter= %d' % self.line_counter)
            self.debug_print('---------------------------------------------')

    def process_line(self):
        if self.is_comment(self.current_line()):
            self.line_counter += 1
            return

        instruction, label = self.separate_label(self.current_line())

        if label:
            self.label_lut[label] = self.line_counter

        self.debug_print('mem= %s' % self.memory_map)
        jump = self.exec_instruction(instruction)

        if jump is not None:
            self.line_counter = jump
        else:
            self.line_counter += 1

    def exec_instruction(self, instruction):
        self.debug_print('instruction= %s' % instruction)
        inst_part = instruction.split(' ')

        try:
            if inst_part[0] == 'if' and \
                    inst_part[2] == '!=' and \
                    inst_part[3] == '0' and \
                    inst_part[4] == 'goto':
                return self.exec_if_statement(inst_part[1], inst_part[5])

            if inst_part[1] == '<-' and inst_part[0] == inst_part[2] and inst_part[4] == '1':
                if inst_part[3] == '+':
                    return self.exec_incr(inst_part[0])
                if inst_part[3] == '-':
                    return self.exec_decr(inst_part[0])
        except IndexError:
            raise UnknownInstruction(instruction)

        raise UnknownInstruction(instruction)

    def exec_incr(self, variable):
        if variable in self.memory_map:
            self.memory_map[variable] += 1
        else:
            self.memory_map[variable] = 1

    def exec_decr(self, variable):
        if variable in self.memory_map and self.memory_map[variable] > 1:
            self.memory_map[variable] -= 1
        else:
            self.memory_map[variable] = 0

    def exec_if_statement(self, variable, label):
        if self.memory_map.get(variable) != 0:
            self.debug_print('   - yes')
            return self.find_line_of_label(label)
        return None

    def current_line(self):
        if self.line_counter < len(self.code):
            return self.code[self.line_counter]

    @staticmethod
    def is_comment(line):
        return not line or line.startswith(COMMENT_CHAR)

    @staticmethod
    def separate_label(line):
        if not line.startswith('['):
            return line, None

        index = line.find(']')
        return line[index + 1:].strip(), line[1:index]

    def find_line_of_label(self, label):
        if label in self.label_lut:
            return self.label_lut[label]
        for idx, line in enumerate(self.code):
            _, s_label = self.separate_label(self.current_line())
            if s_label:
                self.label_lut[s_label] = idx
            if s_label == label:
                return idx
        return int('inf')

    def open(self, filename):
        with open(filename, 'r') as f:
            code = f.readlines()
        self.code = [x.lower().strip() for x in code]

    def debug_print(self, msg):
        if self.verbosity:
            print(msg)
