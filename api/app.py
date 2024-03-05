from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Adicionar
@app.route('/add', methods=['POST'])
def Add():
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    escricao = request.form['escricao']
    
    contato = request.form['contato']
    email = request.form['email']
    valor = request.form['valor']
    
    cidade = request.form['cidade']
    endereco = request.form['endereco']

    if nome and cnpj and escricao and contato and email and valor and cidade  and endereco:
        cursor = db.database.cursor()
        sql = "INSERT INTO condominio (nome, cnpj, escricao, contato, email, valor, cidade, endereco) VALUES (%s, %s, %s, %s,  %s, %s, %s, %s)"
        data = (nome, cnpj, escricao, contato, email, valor, cidade , endereco)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

#Listar Todos
@app.route('/', methods=['GET'])
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM condominio")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('admin-list.html', data=insertObject)

#Remover
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM condominio WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Editar
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    escricao = request.form['escricao']
    contato = request.form['contato']
    email = request.form['email']
    valor = request.form['valor']
    cidade = request.form['cidade']
    endereco = request.form['endereco']

    if nome and cnpj and escricao and contato and email and valor and cidade  and endereco:
        cursor = db.database.cursor()
        sql = "UPDATE condominio SET nome = %s, cnpj = %s, escricao = %s, contato = %s, email = %s, valor = %s, cidade = %s, endereco = %s WHERE id = %s"
        data = (nome, cnpj, escricao, contato, email, valor, cidade , endereco, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
    
