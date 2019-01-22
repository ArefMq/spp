from settings import *
from interpreter import Interpreter, UnknownInstruction


class Compiler(Interpreter):
    def __init__(self, filename=None, verbosity=False):
        Interpreter.__init__(self, filename, verbosity)
        self.macro_map = {}
        if filename:
            self.compile()

    def compile(self):
        generated_code = []
        counter = 0
        while counter < len(self.code):
            current_line = self.code[counter]
            if current_line.startswith('@'):
                counter = self.extract_extensions(counter)
            elif not self.is_comment(current_line):
                instruction, label = self.separate_label(current_line)
                label = '[%s] ' % label if label else ''

                if self.is_atomic_instruction(instruction.strip()):
                    generated_code.append('%s%s' % (label, instruction))
                else:
                    new_instruction_set = self.replace_macro_usage(instruction)
                    if not new_instruction_set:
                        continue
                    new_instruction_set[0] = '%s%s' % (label, new_instruction_set[0])
                    generated_code.extend(new_instruction_set)
            counter += 1
        self.code = generated_code

    def extract_extensions(self, line_no):
        line = self.code[line_no]
        if line.startswith('@macro'):
            return self.extract_macro(line_no)
        raise UnknownInstruction

    def extract_macro(self, line_no):
        macro_definition = self.code[line_no].replace('@macro', '')
        signature = self.get_signature(macro_definition)

        line_no += 1
        macro_body = [macro_definition]
        while self.code[line_no] != '@end' and line_no < len(self.code):
            macro_body.append(self.code[line_no])
            line_no += 1

        self.macro_map[signature] = macro_body
        return line_no

    def replace_macro_usage(self, instruction):
        signature = self.get_signature(instruction)
        if signature not in self.macro_map:
            raise UnknownInstruction

        result = [i for i in self.macro_map[signature]]  # deep copy
        mem_map = self.create_memory_map(instruction, result[0])

        label_map = {}
        for line_id, line in enumerate(result):
            _, label = self.separate_label(line)
            if label and label not in label_map:
                label_map[label] = '%s_%s' % (label, generate_random_name())
            for key, value in label_map.items():
                result[line_id] = line.replace(key, value)

        result = '#'.join(result[1:])
        for key, value in mem_map.items():
            result = result.replace(key, value)
        result = result.split('#')

        result.insert(0, '# %s' % instruction)
        return result

    @staticmethod
    def is_atomic_instruction(instruction):
        if not instruction:
            return True

        inst_part = instruction.split(' ')

        try:
            if inst_part[0] == 'if' and \
                    inst_part[2] == '!=' and \
                    inst_part[3] == '0' and \
                    inst_part[4] == 'goto' and \
                    len(inst_part) == 6:
                return True

            return inst_part[1] == '<-' and inst_part[0] == inst_part[2] and inst_part[4] == '1' and \
                   (inst_part[3] == '+' or inst_part[3] == '-') and len(inst_part) == 5
        except IndexError:
            return False

    @staticmethod
    def create_memory_map(instruction, macro_instruction):
        macro_instruction = macro_instruction.replace('@macro', '').strip()
        result = {}
        for key, value in zip(instruction.split(' '), macro_instruction.split(' ')):
            if Compiler.is_variable(key) and Compiler.is_variable(value):
                result[value] = key
            elif not Compiler.is_variable(key) or not Compiler.is_variable(value):
                continue
            else:
                raise UnknownInstruction
        return result

    @staticmethod
    def is_variable(term):
        for c in term:
            if c not in VALID_VARIABLE_CHARS:
                return False
        return True

    @staticmethod
    def is_literal(term):
        try:
            _ = float(term)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_signature(instruction):
        result = []
        spl = instruction.split()
        for s in spl:
            if s.startswith('@'):
                continue
            elif Compiler.is_literal(s):
                result.append('l')
            elif Compiler.is_variable(s):
                result.append('v')
            else:
                result.append(s)
        return ' '.join(result)

    def save(self, filename, ignore_comments=False):
        result = ['# This is an Auto-Generated Code',
                  '# By SPP Compiler - (c) %s' % COPYRIGH_YEAR,
                  '# WebPage: %s' % GITHUB_URL,
                  '']
        result.extend(self.code)

        if ignore_comments:
            result = [line for line in result if line and not line.startswith('#')]

        with open(filename, 'w') as file_handel:
            file_handel.writelines('\n'.join(result))
