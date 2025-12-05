from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('geotalentos.db')

def criar_banco():
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS jovem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER,
        localizacao TEXT,
        desempenho REAL,
        status TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS oportunidade (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        localizacao TEXT,
        status TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS curso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        instituicao TEXT,
        dataInicio TEXT,
        dataFim TEXT)''')
    conn.commit()
    conn.close()

criar_banco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jovens')
def listar_jovens():
    conn = conectar()
    cur = conn.cursor()
    cur.execute('SELECT * FROM jovem')
    jovens = cur.fetchall()
    conn.close()
    return render_template('jovens.html', jovens=jovens)

@app.route('/novo_jovem', methods=['GET', 'POST'])
def novo_jovem():
    if request.method == 'POST':
        dados = (request.form['nome'], request.form['idade'], request.form['localizacao'], request.form['desempenho'], request.form['status'])
        conn = conectar()
        cur = conn.cursor()
        cur.execute('INSERT INTO jovem (nome, idade, localizacao, desempenho, status) VALUES (?, ?, ?, ?, ?)', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_jovens'))
    return render_template('form_jovem.html')

@app.route('/excluir_jovem/<int:id>')
def excluir_jovem(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM jovem WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_jovens'))

@app.route('/editar_jovem/<int:id>', methods=['GET', 'POST'])
def editar_jovem(id):
    conn = conectar()
    cur = conn.cursor()
    if request.method == 'POST':
        dados = (request.form['nome'], request.form['idade'], request.form['localizacao'], request.form['desempenho'], request.form['status'], id)
        cur.execute('UPDATE jovem SET nome=?, idade=?, localizacao=?, desempenho=?, status=? WHERE id=?', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_jovens'))
    
    cur.execute('SELECT * FROM jovem WHERE id=?', (id,))
    jovem = cur.fetchone()
    conn.close()
    return render_template('form_jovem.html', jovem=jovem)

@app.route('/oportunidades')
def listar_oportunidades():
    conn = conectar()
    cur = conn.cursor()
    cur.execute('SELECT * FROM oportunidade')
    oportunidades = cur.fetchall()
    conn.close()
    return render_template('oportunidades.html', oportunidades=oportunidades)

@app.route('/nova_oportunidade', methods=['GET', 'POST'])
def nova_oportunidade():
    if request.method == 'POST':
        dados = (request.form['titulo'], request.form['descricao'], request.form['localizacao'], request.form['status'])
        conn = conectar()
        cur = conn.cursor()
        cur.execute('INSERT INTO oportunidade (titulo, descricao, localizacao, status) VALUES (?, ?, ?, ?)', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_oportunidades'))
    return render_template('form_oportunidade.html')

@app.route('/editar_oportunidade/<int:id>', methods=['GET', 'POST'])
def editar_oportunidade(id):
    conn = conectar()
    cur = conn.cursor()
    if request.method == 'POST':
        dados = (request.form['titulo'], request.form['descricao'], request.form['localizacao'], request.form['status'], id)
        cur.execute('UPDATE oportunidade SET titulo=?, descricao=?, localizacao=?, status=? WHERE id=?', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_oportunidades'))
    
    cur.execute('SELECT * FROM oportunidade WHERE id=?', (id,))
    oportunidade = cur.fetchone()
    conn.close()
    return render_template('form_oportunidade.html', oportunidade=oportunidade)

@app.route('/excluir_oportunidade/<int:id>')
def excluir_oportunidade(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM oportunidade WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_oportunidades'))

@app.route('/cursos')
def listar_cursos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute('SELECT * FROM curso')
    cursos = cur.fetchall()
    conn.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/novo_curso', methods=['GET', 'POST'])
def novo_curso():
    if request.method == 'POST':
        dados = (request.form['nome'], request.form['instituicao'], request.form['dataInicio'], request.form['dataFim'])
        conn = conectar()
        cur = conn.cursor()
        cur.execute('INSERT INTO curso (nome, instituicao, dataInicio, dataFim) VALUES (?, ?, ?, ?)', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_cursos'))
    return render_template('form_curso.html')

@app.route('/editar_curso/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    conn = conectar()
    cur = conn.cursor()
    if request.method == 'POST':
        dados = (request.form['nome'], request.form['instituicao'], request.form['dataInicio'], request.form['dataFim'], id)
        cur.execute('UPDATE curso SET nome=?, instituicao=?, dataInicio=?, dataFim=? WHERE id=?', dados)
        conn.commit()
        conn.close()
        return redirect(url_for('listar_cursos'))
    
    cur.execute('SELECT * FROM curso WHERE id=?', (id,))
    curso = cur.fetchone()
    conn.close()
    return render_template('form_curso.html', curso=curso)

@app.route('/excluir_curso/<int:id>')
def excluir_curso(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM curso WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_cursos'))



@app.route('/agente')
def agente_inteligente():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, desempenho, status FROM jovem")
    jovens = cur.fetchall()
    conn.close()

    recomendacoes = []
    for j in jovens:
        nome, desempenho, status = j
        if status.lower() == "bloqueado":
            recomendacao = "⚠️ Treinamento obrigatório do CETEN para desbloqueio"
        elif desempenho is None:
            recomendacao = "Sem dados suficientes para gerar recomendação"
        elif desempenho < 3:
            recomendacao = "Recomenda-se o curso de Aperfeiçoamento Profissional"
        elif desempenho < 4:
            recomendacao = "Recomenda-se o curso de Comunicação e Trabalho em Equipe"
        else:
            recomendacao = "Recomenda-se a Mentoria de Liderança e Empreendedorismo"
        recomendacoes.append((nome, desempenho, status, recomendacao))

    return render_template('agente.html', recomendacoes=recomendacoes)

if __name__ == '__main__':
    app.run(debug=True)
