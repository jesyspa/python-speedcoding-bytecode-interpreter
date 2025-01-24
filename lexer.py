import re
from collections import namedtuple

Choices = namedtuple('Choices', ['set', 're'])
Token = namedtuple('Token', ['type', 'value'])

def choice_re(options):
    return Choices(set(options), '|'.join(options))

INSTRUCTIONS = choice_re(['jump', 'store', 'load', 'print', 'add', 'mul', 'read'])
TARGETS = choice_re(['reg', 'mem', 'const', 'indmem'])
COMPARISONS = choice_re(['zero', 'pos', 'neg'])
ARGUMENT_RE = r'-?\d+'

TOKEN_RE = f'{INSTRUCTIONS.re}|{TARGETS.re}|{COMPARISONS.re}|{ARGUMENT_RE}'
TOKEN_RE_COMPILED = re.compile(TOKEN_RE)

def annotate(raw_token):
    if raw_token in INSTRUCTIONS.set:
        return Token('INSTRUCTION', raw_token)
    elif raw_token in TARGETS.set:
        return Token('TARGET', raw_token)
    elif raw_token in COMPARISONS.set:
        return Token('COMPARISON', raw_token)
    else:
        return Token('LITERAL', int(raw_token))

def lex(program):
    return [annotate(raw_token) for raw_token in TOKEN_RE_COMPILED.findall(program)]

