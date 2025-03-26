import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

def tokenize(code):
    keywords = {'OPENQASM', 'include', 'qreg', 'creg', 'measure', 'gate', 'barrier', 'if', 'h', 'cx'}
    token_specification = [
        ('COMMENT',  r'//.*'),            # Single-line comment
        ('NUMBER',   r'\d+(\.\d*)?'),     # Integer or decimal number
        ('ID',       r'[A-Za-z_]\w*'),    # Identifiers
        ('OP',       r'[{}[\]();,->]'),   # Operators and punctuation
        ('SKIP',     r'[ \t\n]+'),        # Skip spaces and tabs
        ('MISMATCH', r'.'),               # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    match = get_token(code)
    while match is not None:
        type_ = match.lastgroup
        if type_ != 'SKIP' and type_ != 'COMMENT':
            val = match.group(type_)
            if type_ == 'ID' and val in keywords:
                type_ = val.upper()
            yield Token(type_, val)
        pos = match.end()
        match = get_token(code, pos)
    if pos != len(code):
        raise RuntimeError('Unexpected character %r on line %d' % (code[pos], code.count('\n', 0, pos) + 1))

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _consume(self, expected_type=None):
        token = self.tokens[self.pos]
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type} but got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.type == 'OPENQASM':
                self._consume('OPENQASM')
                version = self._consume('NUMBER').value
                ast.append(('OPENQASM', version))
                self._consume('OP')  # Consume the ';'
            elif token.type == 'QREG':
                self._consume('QREG')
                name = self._consume('ID').value
                self._consume('OP')  # Consume the '['
                size = int(self._consume('NUMBER').value)
                self._consume('OP')  # Consume the ']'
                self._consume('OP')  # Consume the ';'
                ast.append(('QREG', name, size))
            elif token.type == 'CREG':
                self._consume('CREG')
                name = self._consume('ID').value
                self._consume('OP')  # Consume the '['
                size = int(self._consume('NUMBER').value)
                self._consume('OP')  # Consume the ']'
                self._consume('OP')  # Consume the ';'
                ast.append(('CREG', name, size))
            elif token.type in {'H', 'CX'}:
                gate = token.type
                self._consume(gate)
                qubits = []
                while self.pos < len(self.tokens) and (self.tokens[self.pos].type != 'OP' or self.tokens[self.pos].value != ';'):
                    if self.tokens[self.pos].type == 'ID' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].value == '[':
                        qubit_name = self._consume('ID').value
                        self._consume('OP')  # Consume the '['
                        index = int(self._consume('NUMBER').value)
                        self._consume('OP')  # Consume the ']'
                        qubits.append((qubit_name, index))
                    self.pos += 1
                if self.pos < len(self.tokens):
                    self._consume('OP')  # Consume the ';'
                ast.append((gate, qubits))
            elif token.type == 'MEASURE':
                self._consume('MEASURE')
                qubit_name = self._consume('ID').value
                self._consume('OP')  # Consume the '['
                qubit_index = int(self._consume('NUMBER').value)
                self._consume('OP')  # Consume the ']'
                self._consume('OP')  # Consume the '->'
                creg_name = self._consume('ID').value
                self._consume('OP')  # Consume the '['
                creg_index = int(self._consume('NUMBER').value)
                self._consume('OP')  # Consume the ']'
                self._consume('OP')  # Consume the ';'
                ast.append(('MEASURE', (qubit_name, qubit_index), (creg_name, creg_index)))
            else:
                self.pos += 1  # Skip any unexpected tokens
        return ast


code = """
OPENQASM 2.0;

h q[0];
cx q[0], q[1];
measure q[0] ;
measure q[1] ;
"""
tokens = list(tokenize(code))
for token in tokens:
    print(token)

parser = Parser(tokens)
ast = parser.parse()
print(ast)
