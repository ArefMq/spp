

class Godel:
    def __init__(self, verbosity):
        self.verbose = verbosity
        self.code = None

    def open(self, filename):
        with open(filename) as f:
            godel = int(f.read())
        self.code = Godel.decode(godel)

    def save(self, filename, code=None):
        if code is None:
            code = self.code

        godel = Godel.encode(code)

        with open(filename, 'w') as f:
            f.write(str(godel))

    @staticmethod
    def encode(code):
        factors = []
        for line in code:
            coded_inst = Godel.encode_instruction(line)
            factors.append(coded_inst)
        factors.reverse()
    
        result = 1
        counter = 1
        while True:
            counter += 1
            if not Godel.is_prime(counter):
                continue
    
            result *= counter ** factors.pop()
            if len(factors) == 0:
                break
        return result

    @staticmethod
    def decode(number):
        factors = Godel.get_factors(number + 1)
        factors = [factors[prime_number] for prime_number in factors]

        result = []
        for p in factors:
            result.append(Godel.decode_instruction(p))
        return result

    @staticmethod
    def encode_instruction(line):
        instruction, label = Godel.separate_label(line)
        label_code = Godel.get_label_code(label)
        instruction_code = Godel.get_instruction_code(instruction)
        return Godel.pair_encode(label_code, instruction_code)

    @staticmethod
    def get_label_code(label):
        if not label:
            return 0
        CHAR = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
        return (int(label[1:]) - 1) * 5 + CHAR[label[0]] + 1

    @staticmethod
    def get_var_code(var):
        if var == 'y':
            return 0
        chr = 0 if var[0] == 'x' else 1
        return (int(var[1:]) - 1) * 2 + chr + 1

    @staticmethod
    def get_instruction_code(instruction):
        inst_part = instruction.split(' ')
        if inst_part[0] == 'if' and \
                inst_part[2] == '!=' and \
                inst_part[3] == '0' and \
                inst_part[4] == 'goto' and \
                len(inst_part) == 6:
            var_code = Godel.get_var_code(inst_part[1])
            label_code = Godel.get_label_code(inst_part[5])
            return Godel.pair_encode(label_code + 2, var_code)
    
        if inst_part[1] == '<-' and inst_part[0] == inst_part[2]:
            if len(inst_part) == 3:
                var_code = Godel.get_var_code(inst_part[0])
                return Godel.pair_encode(0, var_code)
            elif inst_part[4] == '1' and len(inst_part) == 5:
                if inst_part[3] == '+':
                    var_code = Godel.get_var_code(inst_part[0])
                    return Godel.pair_encode(1, var_code)
    
                if inst_part[3] == '-':
                    var_code = Godel.get_var_code(inst_part[0])
                    return Godel.pair_encode(2, var_code)

    @staticmethod
    def separate_label(line):
        if not line.startswith('['):
            return line, None
    
        index = line.find(']')
        return line[index + 1:].strip(), line[1:index]
    
    @staticmethod
    def decode_instruction(number):
        label_code, ins_pair = Godel.pair_decode(number)
        ins_code, var_code = Godel.pair_decode(ins_pair)
        label = '' if not label_code else ('[%s] ' % Godel.get_label_name(label_code))
        return '%s%s' % (label, Godel.get_composed_instruction(ins_code, Godel.get_var_name(var_code)))
    
    @staticmethod
    def get_var_name(index):
        if index == 0:
            return 'y'
        index -= 1
        return '%s%d' % ('x' if index % 2 == 0 else 'z',
                         index / 2 + 1)
    
    @staticmethod
    def get_label_name(index):
        CHARS = ['a', 'b', 'c', 'd', 'e']
        index -= 1
        return '%s%d' % (CHARS[index % 5], index / 5 + 1)
    
    @staticmethod
    def get_composed_instruction(ins_code, var):
        if ins_code == 0:
            return '%s <- %s' % (var, var)
        if ins_code == 1:
            return '%s <- %s + 1' % (var, var)
        if ins_code == 2:
            return '%s <- %s - 1' % (var, var)
        label = Godel.get_label_name(ins_code - 2)
        return 'if %s != 0 goto %s' % (var, label)
    
    @staticmethod
    def pair_decode(number):
        number += 1
        x = Godel.get_factors(number).get(2, 0)
    
        number /= 2 ** x
        number -= 1
        y = number / 2
        return x, y
    
    @staticmethod
    def pair_encode(x, y):
        res = (2 ** x) * (2 * y + 1) - 1
        return res if res > 0 else 0
    
    
    @staticmethod
    def get_factors(n):
        i = 2
        result = {}
        while True:
            c = 0
            while n % i == 0:
                c = c + 1
                n = n / i
    
            if Godel.is_prime(i):
                result[i] = c
    
            i = i + 1
            if n == 1:
                return result
    
    @staticmethod
    def is_prime(n):
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True
