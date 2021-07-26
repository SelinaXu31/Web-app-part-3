from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscarsData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Male Oscar Awards'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarsImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, oscarAwards=result)


@app.route('/view/<int:oscar_id>', methods=['GET'])
def record_view(oscar_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarsImport WHERE id = %s', oscar_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', oscar=result[0])


@app.route('/edit/<int:oscar_id>', methods=['GET'])
def form_edit_get(oscar_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarsImport WHERE id = %s', oscar_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', oscar=result[0])


@app.route('/edit/<int:oscar_id>', methods=['POST'])
def form_update_post(oscar_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldAge'),
                 request.form.get('fldName'), request.form.get('fldMovie'), oscar_id)
    sql_update_query = """UPDATE tblOscarsImport t SET t.fldYear = %s, t.fldAge = %s, t.fldName = %s,
    t.fldMovie = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/oscarAwards/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Form')


@app.route('/oscarAwards/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldAge'), request.form.get('fldName'),
                 request.form.get('fldMovie'))
    sql_insert_query = """INSERT INTO tblOscarsImport (fldYear, fldAge, fldName, fldMovie) VALUES (%s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:oscar_id>', methods=['POST'])
def form_delete_post(oscar_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarsImport WHERE id = %s """
    cursor.execute(sql_delete_query, oscar_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscarAwards', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarsImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscarAwards/<int:oscar_id>', methods=['GET'])
def api_retrieve(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarsImport WHERE id = %s', oscar_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscarAwards/', methods=['POST'])
def api_add() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldYear'], content['fldAge'], content['fldName'], content['fldMovie'])
    sql_add_query = """INSERT INTO tblOscarsImport (fldYear, fldAge, fldName, fldMovie) VALUES (%s, %s, %s, %s) """
    cursor.execute(sql_add_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/oscarAwards/<int:oscar_id>', methods=['PUT'])
def api_edit(oscar_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/oscarAwards/<int:oscar_id>', methods=['DELETE'])
def api_delete(oscar_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarsImport WHERE id = %s """
    cursor.execute(sql_delete_query, oscar_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)