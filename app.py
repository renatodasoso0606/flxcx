import os
import openpyxl
from flask import Flask, render_template, request, send_file
from datetime import datetime

app = Flask(__name__)

pagamentos = []
saidas = []


diretorio_atual = os.path.dirname(__file__)


subdiretorio_dados = 'dados'


pasta_excel = os.path.join(diretorio_atual, subdiretorio_dados)


if not os.path.exists(pasta_excel):
    os.makedirs(pasta_excel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_pagamento', methods=['POST'])
def registrar_pagamento():
    data_pagamento = request.form['data_pagamento']
    valor_entrada = float(request.form['valor_entrada'])
    pagamentos.append({'data': data_pagamento, 'valor': valor_entrada})
    salvar_em_excel(os.path.join(pasta_excel, 'pagamentos.xlsx'), pagamentos)
    return send_file(os.path.join(pasta_excel, 'pagamentos.xlsx'), as_attachment=True)

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida():
    data_saida = request.form['data_saida']
    valor_saida = float(request.form['valor_saida'])
    saidas.append({'data': data_saida, 'valor': valor_saida})
    salvar_em_excel(os.path.join(pasta_excel, 'saidas.xlsx'), saidas)
    return send_file(os.path.join(pasta_excel, 'saidas.xlsx'), as_attachment=True)

def salvar_em_excel(nome_arquivo, dados):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Data', 'Valor'])
    for dado in dados:
        ws.append([dado['data'], dado['valor']])
    wb.save(nome_arquivo)

if __name__ == '__main__':
    app.run(debug=True)
