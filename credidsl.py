"""
CrediDSL - prototipo académico para reglas de evaluación crediticia.
Solo utiliza datos sintéticos; no es un sistema para decisiones crediticias reales.
"""
import re
import time
import json
from dataclasses import dataclass

TOKEN_RE = re.compile(
    r'(?P<WS>\s+)|'
    r'(?P<GE>>=)|(?P<LE><=)|(?P<EQ>==)|(?P<NE>!=)|'
    r'(?P<GT>>)|(?P<LT><)|'
    r'(?P<AND>\bAND\b)|(?P<OR>\bOR\b)|'
    r'(?P<REGLA>\bREGLA\b)|(?P<SI>\bSI\b)|(?P<ENTONCES>\bENTONCES\b)|'
    r'(?P<APROBAR>\bAPROBAR\b)|(?P<RECHAZAR>\bRECHAZAR\b)|'
    r'(?P<REVISION_MANUAL>\bREVISION_MANUAL\b)|'
    r'(?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)|'
    r'(?P<NUMBER>\d+(?:\.\d+)?)|(?P<SEMI>;)|(?P<LPAREN>\()|(?P<RPAREN>\))'
)

VARIABLES = {"ingreso", "score", "endeudamiento", "moras"}
ACTIONS = {"APROBAR", "RECHAZAR", "REVISION_MANUAL"}
OPS = {">=", "<=", "==", "!=", ">", "<"}

class DSLException(Exception):
    pass

@dataclass
class Token:
    type: str
    value: str
    pos: int

def tokenize(source):
    tokens, pos = [], 0
    while pos < len(source):
        match = TOKEN_RE.match(source, pos)
        if not match:
            raise DSLException(f"Error léxico en posición {pos}: carácter {source[pos]!r}")
        kind, value = match.lastgroup, match.group()
        if kind != "WS":
            tokens.append(Token(kind, value, pos))
        pos = match.end()
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens, self.i = tokens, 0

    def peek(self, kind=None):
        if self.i >= len(self.tokens):
            return False if kind else None
        return self.tokens[self.i].type == kind if kind else self.tokens[self.i]

    def take(self, kind):
        token = self.peek()
        if token is None or token.type != kind:
            got = "fin de entrada" if token is None else f"{token.value!r}"
            raise DSLException(f"Error sintáctico: se esperaba {kind}, se encontró {got}")
        self.i += 1
        return token

    def parse(self):
        self.take("REGLA")
        name = self.take("IDENT").value
        self.take("SI")
        condition = self.parse_or()
        self.take("ENTONCES")
        action = self.take("APROBAR") if self.peek("APROBAR") else (
            self.take("RECHAZAR") if self.peek("RECHAZAR") else self.take("REVISION_MANUAL"))
        if self.peek("SEMI"):
            self.take("SEMI")
        if self.i != len(self.tokens):
            raise DSLException(f"Error sintáctico: token inesperado {self.tokens[self.i].value!r}")
        return {"name": name, "condition": condition, "action": action.value}

    def parse_or(self):
        node = self.parse_and()
        while self.peek("OR"):
            self.take("OR")
            node = ("OR", node, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_comparison()
        while self.peek("AND"):
            self.take("AND")
            node = ("AND", node, self.parse_comparison())
        return node

    def parse_comparison(self):
        if self.peek("LPAREN"):
            self.take("LPAREN")
            node = self.parse_or()
            self.take("RPAREN")
            return node
        variable = self.take("IDENT").value
        if variable not in VARIABLES:
            raise DSLException(f"Error semántico: variable no permitida {variable!r}")
        op_token = self.peek()
        if op_token is None or op_token.value not in OPS:
            raise DSLException("Error sintáctico: se esperaba un operador relacional")
        self.i += 1
        number = float(self.take("NUMBER").value)
        return ("CMP", variable, op_token.value, number)

def compile_rule(source):
    return Parser(tokenize(source)).parse()

def evaluate(node, data):
    kind = node[0]
    if kind == "CMP":
        _, variable, op, number = node
        if variable not in data:
            raise DSLException(f"Error semántico: falta el dato {variable!r}")
        value = float(data[variable])
        return {">=": value >= number, "<=": value <= number, "==": value == number,
                "!=": value != number, ">": value > number, "<": value < number}[op]
    if kind == "AND":
        return evaluate(node[1], data) and evaluate(node[2], data)
    if kind == "OR":
        return evaluate(node[1], data) or evaluate(node[2], data)
    raise DSLException("Nodo interno no reconocido")

def decide(compiled_rule, application):
    return compiled_rule["action"] if evaluate(compiled_rule["condition"], application) else "REVISION_MANUAL"

DEFAULT_RULE = (
    "REGLA elegibilidad SI ingreso >= 1800 AND score >= 650 "
    "AND endeudamiento <= 0.40 AND moras == 0 ENTONCES APROBAR;"
)

def demo():
    compiled = compile_rule(DEFAULT_RULE)
    cases = []
    # Dataset determinista y ficticio para reproducibilidad; no representa clientes reales.
    for i in range(100):
        cases.append({
            "id": i + 1,
            "ingreso": 1200 + ((i * 137) % 2800),
            "score": 500 + ((i * 47) % 351),
            "endeudamiento": ((i * 13) % 81) / 100,
            "moras": (i * 7) % 4
        })
    start = time.perf_counter()
    decisions = [decide(compiled, c) for c in cases]
    elapsed_ms = (time.perf_counter() - start) * 1000
    counts = {a: decisions.count(a) for a in ("APROBAR", "RECHAZAR", "REVISION_MANUAL")}
    return {"cases": len(cases), "counts": counts, "elapsed_ms": elapsed_ms, "rule": DEFAULT_RULE}

if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
