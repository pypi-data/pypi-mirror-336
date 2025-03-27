import re

#類似於java的String
class ntsu_str(str):
    def __init__(self, arg:object):
        super(ntsu_str, self).__init__()
        self.string = arg.__str__()

    def end_with(self, var:str) -> bool:
        return self.string.endswith(var)

    def start_with(self, var:str) -> bool:
        return self.string.startswith(var)

    def replaceAll(self, bereplaced:str, replace: str) -> str:
        return self.string.replace(bereplaced, replace)

    def replaceFirst(self, pattern, replacement) -> str:
        return re.sub(pattern, replacement, self.string, count=1)

    def replaceEnd(self, pattern, replacement) -> str:
        return  re.sub(pattern + '$', replacement, self.string)

    def replaceAt(self, index: int, bereplaced: str, replace: str) -> str:
        pattern = re.escape(bereplaced)
        count = 0
        def replace_match(match):
            nonlocal count
            count += 1
            if count == index:
                return replace
            else:
                return match.group()
        return re.sub(pattern, replace_match, self.string, count=index)

    def has_digits(self) -> bool:
        return any(char.isdigit() for char in self.string)

    def count_str(self, c: str) -> int:
        return self.string.count(c)

    def spilit(self, sp: str) -> str:
        return sp.join(self.string.split(sp))

    def __len__(self):
        return len(self.string)

    def __str__(self):
        return self.string

    def __add__(self, value):
        if isinstance(value, str):
            self.string = self.string + value
            return self
        elif isinstance(value, ntsu_str):
            self.string = self.string + value.string
            return self
        raise TypeError(f'無法使用相加 {type(self)} + {type(value)}!')

    def __setattr__(self, name, value):
        if name == 'string':
            if isinstance(value, object):
                super(ntsu_str, self).__setattr__(name, value.__str__())
            else:
                raise TypeError

    def __eq__(self, other):
        if isinstance(other, ntsu_str):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        else:
            return False
