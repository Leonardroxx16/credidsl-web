from flask import Flask, render_template, request
from credidsl import compile_rule, decide, evaluate, demo, DEFAULT_RULE, DSLException

app = Flask(__name__)


def render_page(result=None, error=None, values=None, status=200):
    return render_template(
        'index.html', default_rule=DEFAULT_RULE, result=result,
        error=error, values=values or {}
    ), status


@app.get('/')
def index():
    page, status = render_page()
    return page, status


@app.post('/evaluate')
def evaluate_rule():
    rule = request.form.get('rule', DEFAULT_RULE).strip()
    values = {
        'ingreso': request.form.get('ingreso', '1800').strip(),
        'score': request.form.get('score', '650').strip(),
        'endeudamiento': request.form.get('endeudamiento', '0.40').strip(),
        'moras': request.form.get('moras', '0').strip(),
    }
    try:
        application = {k: float(v) for k, v in values.items()}
        if application['endeudamiento'] < 0 or application['endeudamiento'] > 1:
            raise ValueError('El endeudamiento debe estar entre 0 y 1.')
        if application['moras'] < 0 or not application['moras'].is_integer():
            raise ValueError('El número de moras debe ser un entero no negativo.')
        compiled = compile_rule(rule)
        condition_passed = bool(evaluate(compiled['condition'], application))
        decision = decide(compiled, application)
        if condition_passed:
            explanation = f"La condición de la regla '{compiled['name']}' se cumple. Se devuelve la acción declarada: {compiled['action']}."
            condition_text = 'La condición se cumple; se aplica la acción declarada en la regla.'
        else:
            explanation = 'La condición de la regla no se cumple. En este prototipo, el resultado alternativo es REVISION_MANUAL.'
            condition_text = 'La condición no se cumple; el caso pasa a revisión manual.'
        result = {
            'name': compiled['name'], 'decision': decision,
            'condition': condition_text, 'condition_passed': condition_passed,
            'explanation': explanation, 'rule': rule
        }
        page, status = render_page(result=result, values=values)
        return page, status
    except (ValueError, DSLException) as exc:
        page, status = render_page(error=str(exc), values=values, status=400)
        return page, status


@app.get('/api/health')
def health():
    return {'status': 'ok', 'app': 'CrediDSL', 'mode': 'academic-demo'}


@app.get('/api/demo')
def api_demo():
    return demo()


if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
