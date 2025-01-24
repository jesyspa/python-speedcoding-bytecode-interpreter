def assert_type(token, type, line):
    assert token.type == type, f'Error on line {line}, found {token}'

def parse(tokens):
    result = []
    for i in range(0, len(tokens), 3):
        line = 1 + i // 3
        try:
            a, b, c = tokens[i], tokens[i+1], tokens[i+2]
        except Exception as e:
            raise Exception(f'Error on line {line}: {e}')
        assert_type(a, 'INSTRUCTION', line)
        if a.value == 'jump':
            assert_type(b, 'COMPARISON', line)
        else:
            assert_type(b, 'TARGET', line)
        assert_type(c, 'LITERAL', line)
        result.append((a.value, b.value, c.value))
    return result
