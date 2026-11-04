"""Synthetic applications, CSV loading, and reproducible comparison cases."""

from collections import Counter
import csv
from decimal import Decimal
from io import StringIO
from time import perf_counter

from credidsl import (
    ACTIONS, DEFAULT_POLICY, VARIABLES, DataError, analyze, decide, validate_application,
)

COLUMNS = ("id", *VARIABLES)
MAX_CASES = 1000
CSV_SIZE = 128 * 1024


def synthetic_cases():
    return [
        (
            str(i + 1),
            {
                "puntaje": 500 + (i * 47) % 351,
                "ingreso_mensual": 1200 + (i * 137) % 2800,
                "ratio_deuda": Decimal((i * 13) % 81) / 100,
            },
        )
        for i in range(100)
    ]


def read_cases(raw):
    if len(raw) > CSV_SIZE:
        raise DataError("El archivo CSV supera el límite de 128 KB.")
    try:
        stream = StringIO(raw.decode("utf-8-sig"), newline="")
    except UnicodeDecodeError as error:
        raise DataError("Guarda el archivo CSV con codificación UTF-8.") from error

    reader = csv.DictReader(stream, strict=True)
    cases, identifiers = [], set()
    try:
        if not reader.fieldnames or sorted(reader.fieldnames) != sorted(COLUMNS):
            raise DataError(f"El CSV debe contener estas columnas: {', '.join(COLUMNS)}.")
        for row in reader:
            line = reader.line_num
            if len(cases) >= MAX_CASES:
                raise DataError(f"El CSV admite hasta {MAX_CASES} solicitudes.")
            if None in row or any(value is None for value in row.values()):
                raise DataError(f"Fila {line} del CSV incompleta o con columnas adicionales.")
            case_id = row["id"].strip()
            if not case_id or case_id in identifiers or len(case_id) > 40:
                raise DataError(f"Fila {line}: el identificador debe ser único y tener de 1 a 40 caracteres.")
            try:
                application = validate_application(row)
            except DataError as error:
                raise DataError(f"Fila {line}: {error}") from error
            identifiers.add(case_id)
            cases.append((case_id, application))
    except csv.Error as error:
        raise DataError(f"Formato CSV inválido cerca de la fila {reader.line_num}.") from error
    if not cases:
        raise DataError("El CSV debe contener al menos una solicitud ficticia.")
    return cases


def simulate(policy_a, cases, policy_b=None):
    start = perf_counter()
    rows = []
    for case_id, application in cases:
        a = decide(policy_a, application)
        b = decide(policy_b, application) if policy_b else None
        rows.append({
            "id": case_id, "application": application, "a": a, "b": b,
            "changed": b is not None and a.action != b.action,
        })

    def totals(key):
        counts = Counter(row[key].action for row in rows)
        return {action: counts[action] for action in ACTIONS}

    return {
        "rows": rows, "cases": len(rows), "counts_a": totals("a"),
        "counts_b": totals("b") if policy_b else None,
        "changed": sum(row["changed"] for row in rows),
        "elapsed_ms": (perf_counter() - start) * 1000,
    }


def validation_study():
    """Compare both configurations on the same labeled policies without executing them."""
    fixtures = [
        ("Política válida", DEFAULT_POLICY, None),
        ("Política válida con paréntesis", DEFAULT_POLICY.replace("puntaje >= 650", "(puntaje >= 650 O puntaje == 600)"), None),
        ("Carácter inválido", DEFAULT_POLICY.replace(">= 650", "@ 650"), "léxico"),
        ("Falta ENTONCES", DEFAULT_POLICY.replace("ENTONCES APROBAR", "APROBAR"), "sintáctico"),
        ("Falta la decisión por defecto", DEFAULT_POLICY.rsplit("\n", 1)[0], "sintáctico"),
        ("Variable desconocida", DEFAULT_POLICY.replace("puntaje", "puntajee"), "semántico"),
        ("Umbral de tipo incorrecto", DEFAULT_POLICY.replace(">= 650", ">= 650.5"), "semántico"),
        ("Umbral fuera de rango", DEFAULT_POLICY.replace("<= 0.35", "<= 1.20"), "semántico"),
        ("Nombre de regla repetido", DEFAULT_POLICY.replace("perfil_elegible", "deuda_alta"), "semántico"),
        ("Prioridad no positiva", DEFAULT_POLICY.replace("PRIORIDAD 10", "PRIORIDAD 0"), "semántico"),
    ]
    rows = []
    for label, source, expected in fixtures:
        base = analyze(source, check_semantics=False)
        full = analyze(source)
        rows.append({
            "label": label, "expected": expected,
            "base": base.diagnostics[0].stage if base.diagnostics else None,
            "full": full.diagnostics[0].stage if full.diagnostics else None,
        })

    def measure(configuration):
        return {
            "detected": sum(bool(r["expected"] and r[configuration]) for r in rows),
            "missed": sum(bool(r["expected"] and not r[configuration]) for r in rows),
            "false_rejections": sum(bool(not r["expected"] and r[configuration]) for r in rows),
        }

    return {"rows": rows, "base": measure("base"), "full": measure("full")}
