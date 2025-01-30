from collections import namedtuple
import re

Token = namedtuple('Token', ['type', 'value'])
Rule = namedtuple('Rule', ['name', 'regex', 'transform'])

def make_rule(name, pattern):
    return lambda transform: Rule(name, re.compile('^' + pattern), transform)

class Lexer:
    def __init__(self, rules, text):
        self.rules = rules
        self.text = text.lstrip()

    def next(self):
        for rule in self.rules:
            match = rule.regex.match(self.text)
            if match:
                assert match.group()
                self.text = self.text[match.end():].lstrip()
                return Token(rule.name, rule.transform(match))
        return None

    def next_as(self, rule_name):
        x = self.next()
        assert x.type == rule_name
        return x.value

    def all(self):
        while self:
            yield self.next()

    def __bool__(self):
        return bool(self.text)
