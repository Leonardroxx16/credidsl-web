from flask import Flask, render_template, request
from credidsl import compile_rule, decide, demo, DEFAULT_RULE, DSLException

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html', default_rule=DEFAULT_RULE, result=None, error=None, values={})

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
        compiled = compile_rule(rule)
        decision = decide(compiled, application)
        result = {'name': compiled['name'], 'decision': decision, 'condition': 'Cumple' if decision != 'REVISION_MANUAL' else 'No cumple; pasa a revisión manual', 'rule': rule}
        return render_template('index.html', default_rule=DEFAULT_RULE, result=result, error=None, values=values)
    except (ValueError, DSLException) as exc:
        return render_template('index.html', default_rule=DEFAULT_RULE, result=None, error=str(exc), values=values), 400

@app.get('/api/health')
def health():
    return {'status': 'ok', 'app': 'CrediDSL', 'mode': 'academic-demo'}

@app.get('/api/demo')
def api_demo():
    return demo()

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
