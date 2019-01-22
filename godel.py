

class Godel:
    def __init__(self):
        pass

    def encode(self, code):
        pass

    def decode(self, number):
        factors = self.get_factors(number + 1)
        print factors
        factors = [factors[prime_number] for prime_number in factors]

        result = []
        for p in factors:
            result.append(self.decode_instruction(p))
        return result

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


if __name__ == "__main__":
    _code = [
        '[a1] y <- y + 1',
        'x0 <- x0 - 1',
        'if x0 != 0 goto a1',
    ]

    g = Godel()
    en = g.encode(_code)
    print en
    print '\n'.join(g.decode(en))
