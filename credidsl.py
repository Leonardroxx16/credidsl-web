"""Compilation and execution of the CrediDSL policy defined in CrediDSL.g4."""

from dataclasses import dataclass
from decimal import Decimal
import operator
import re

from antlr4 import CommonTokenStream, InputStream, Token
from antlr4.error.ErrorListener import ErrorListener

from generated.CrediDSLLexer import CrediDSLLexer
from generated.CrediDSLParser import CrediDSLParser


ACTIONS = ("APROBAR", "RECHAZAR", "REVISION_MANUAL")
DEFAULT_POLICY = """REGLA deuda_alta PRIORIDAD 20
SI ratio_deuda > 0.50 ENTONCES RECHAZAR

REGLA perfil_elegible PRIORIDAD 10
SI puntaje >= 650 Y ingreso_mensual >= 1800 Y ratio_deuda <= 0.35
ENTONCES APROBAR

POR_DEFECTO REVISION_MANUAL"""
DEMO_VARIANT = DEFAULT_POLICY.replace("puntaje >= 650", "puntaje >= 700")
MAX_POLICY_LENGTH = 16_000
MAX_TOKENS = 1_200
MAX_NESTING = 32

OPERATORS = {
    ">=": operator.ge, "<=": operator.le, ">": operator.gt,
    "<": operator.lt, "==": operator.eq, "!=": operator.ne,
}


@dataclass(frozen=True)
class Variable:
    label: str
    integer: bool
    maximum: int | None = None

    def restriction(self):
        return f"de 0 a {self.maximum}, inclusive" if self.maximum is not None else "mayor o igual a 0"


VARIABLES = {
    "puntaje": Variable("Puntaje", integer=True, maximum=1000),
    "ingreso_mensual": Variable("Ingreso mensual", integer=False),
    "ratio_deuda": Variable("Proporción de deuda", integer=False, maximum=1),
}


@dataclass(frozen=True)
class Diagnostic:
    stage: str
    message: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class Lexeme:
    kind: str
    text: str
    line: int
    column: int

    @classmethod
    def from_token(cls, token):
        return cls(CrediDSLLexer.symbolicNames[token.type], token.text, token.line, token.column + 1)

    def error(self, message):
        return Diagnostic("semántico", message, self.line, self.column)


@dataclass(frozen=True)
class Comparison:
    variable: Lexeme
    operator: str
    literal: Lexeme


@dataclass(frozen=True)
class Logical:
    operator: str
    operands: tuple["Condition", ...]


Condition = Comparison | Logical


@dataclass(frozen=True)
class Rule:
    name: Lexeme
    priority: Lexeme
    condition: Condition
    action: str


@dataclass(frozen=True)
class Policy:
    rules: tuple[Rule, ...]
    fallback: str


@dataclass(frozen=True)
class Analysis:
    tokens: tuple[Lexeme, ...] = ()
    tree: str = ""
    diagnostics: tuple[Diagnostic, ...] = ()
    policy: Policy | None = None

    @property
    def accepted(self):
        return not self.diagnostics


@dataclass(frozen=True)
class Decision:
    action: str
    rules: tuple[str, ...]
    reason: str


class DataError(ValueError):
    """The synthetic application does not match the variable catalog."""


class DiagnosticsListener(ErrorListener):
    def __init__(self, stage):
        self.stage = stage
        self.diagnostics = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if self.stage == "léxico":
            index = recognizer._tokenStartCharIndex
            character = recognizer.inputStream.getText(index, index)
            message = f"Carácter no reconocido {character!r}."
        else:
            expected = recognizer.getExpectedTokens().toString(
                recognizer.literalNames, recognizer.symbolicNames
            ).replace("<EOF>", "fin de la política")
            found = (
                "el fin de la política" if offendingSymbol.type == Token.EOF
                else repr(offendingSymbol.text)
            )
            message = f"Se esperaba {expected} y se encontró {found}."
        self.diagnostics.append(Diagnostic(self.stage, message, line, column + 1))


def _expression(ctx):
    terms = [_conjunction(ctx.con())]
    tail = ctx.eo()
    while tail.O():
        terms.append(_conjunction(tail.con()))
        tail = tail.eo()
    return terms[0] if len(terms) == 1 else Logical("O", tuple(terms))


def _conjunction(ctx):
    terms = [_atom(ctx.atom())]
    tail = ctx.cy()
    while tail.Y():
        terms.append(_atom(tail.atom()))
        tail = tail.cy()
    return terms[0] if len(terms) == 1 else Logical("Y", tuple(terms))


def _atom(ctx):
    if ctx.exp():
        return _expression(ctx.exp())
    return Comparison(
        Lexeme.from_token(ctx.ID().getSymbol()), ctx.op().getText(),
        Lexeme.from_token(ctx.num().start),
    )


def _build_rule(ctx):
    return Rule(
        Lexeme.from_token(ctx.ID().getSymbol()), Lexeme.from_token(ctx.ENTERO().getSymbol()),
        _expression(ctx.exp()), ctx.acc().getText(),
    )


def _build_policy(tree):
    rules = [_build_rule(tree.reg())]
    tail = tree.rest()
    while tail.reg():
        rules.append(_build_rule(tail.reg()))
        tail = tail.rest()
    return Policy(tuple(rules), tree.defecto().acc().getText())


def _check_condition(condition):
    if isinstance(condition, Logical):
        for item in condition.operands:
            yield from _check_condition(item)
        return

    name, literal = condition.variable, condition.literal
    spec = VARIABLES.get(name.text)
    if spec is None:
        yield name.error(f"La variable {name.text!r} no existe en el catálogo.")
        return
    if spec.integer and literal.kind != "ENTERO":
        yield literal.error(f"{spec.label} requiere un umbral entero.")
    if spec.maximum is not None and Decimal(literal.text) > spec.maximum:
        yield literal.error(f"El umbral de {name.text} debe ser {spec.restriction()}.")


def _check_policy(policy):
    seen = set()
    for rule in policy.rules:
        if rule.name.text in seen:
            yield rule.name.error(f"El nombre de regla {rule.name.text!r} está repetido.")
        seen.add(rule.name.text)
        if Decimal(rule.priority.text) <= 0:
            yield rule.priority.error("La prioridad debe ser un entero mayor que cero.")
        yield from _check_condition(rule.condition)


def analyze(source, *, check_semantics=True):
    """Return diagnostics and artifacts. Only the full pass returns an executable policy."""
    if len(source) > MAX_POLICY_LENGTH:
        return Analysis(diagnostics=(Diagnostic("entrada", f"El límite es de {MAX_POLICY_LENGTH} caracteres."),))
    lexer = CrediDSLLexer(InputStream(source))
    lexical = DiagnosticsListener("léxico")
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexical)
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = tuple(Lexeme.from_token(t) for t in stream.tokens if t.type != Token.EOF)
    if lexical.diagnostics:
        return Analysis(tokens, diagnostics=tuple(lexical.diagnostics))

    if len(tokens) > MAX_TOKENS:
        return Analysis(tokens, diagnostics=(Diagnostic("entrada", f"El límite es de {MAX_TOKENS} tokens."),))
    depth = 0
    for token in tokens:
        if token.kind == "PA":
            depth += 1
            if depth > MAX_NESTING:
                error = Diagnostic("entrada", f"El límite es de {MAX_NESTING} niveles de paréntesis.", token.line, token.column)
                return Analysis(tokens, diagnostics=(error,))
        elif token.kind == "PC":
            depth = max(0, depth - 1)

    parser = CrediDSLParser(stream)
    syntax = DiagnosticsListener("sintáctico")
    parser.removeErrorListeners()
    parser.addErrorListener(syntax)
    try:
        tree = parser.pol()
        if syntax.diagnostics:
            return Analysis(tokens, diagnostics=tuple(syntax.diagnostics))
        tree_text = tree.toStringTree(recog=parser)
    except RecursionError:
        error = Diagnostic("entrada", "La política contiene demasiadas reglas o condiciones anidadas.")
        return Analysis(tokens, diagnostics=(error,))

    if not check_semantics:
        return Analysis(tokens, tree_text)
    policy = _build_policy(tree)
    errors = tuple(_check_policy(policy))
    return Analysis(tokens, tree_text, errors, policy if not errors else None)


def validate_application(values):
    application = {}
    for name, spec in VARIABLES.items():
        raw = str(values.get(name, "")).strip()
        pattern = r"[0-9]+" if spec.integer else r"[0-9]+(?:\.[0-9]+)?"
        if not re.fullmatch(pattern, raw):
            kind = "un entero" if spec.integer else "un número con punto decimal"
            raise DataError(f"{spec.label} debe ser {kind}, {spec.restriction()}.")
        value = Decimal(raw)
        if spec.maximum is not None and value > spec.maximum:
            raise DataError(f"{spec.label} debe ser {spec.restriction()}.")
        application[name] = value
    return application


def _matches(condition, application):
    if isinstance(condition, Comparison):
        value = application[condition.variable.text]
        return OPERATORS[condition.operator](value, Decimal(condition.literal.text))
    checks = (_matches(operand, application) for operand in condition.operands)
    return all(checks) if condition.operator == "Y" else any(checks)


def decide(policy, application):
    matching = [rule for rule in policy.rules if _matches(rule.condition, application)]
    if not matching:
        return Decision(policy.fallback, (), "Ninguna regla coincide. Se aplica la decisión por defecto.")
    priority = max(Decimal(rule.priority.text) for rule in matching)
    winners = [rule for rule in matching if Decimal(rule.priority.text) == priority]
    names = tuple(rule.name.text for rule in winners)
    actions = {rule.action for rule in winners}
    if len(actions) > 1:
        return Decision("REVISION_MANUAL", names, f"Las reglas de prioridad {priority} indican decisiones distintas.")
    return Decision(winners[0].action, names, f"Las reglas indicadas coinciden y tienen la mayor prioridad ({priority}).")
