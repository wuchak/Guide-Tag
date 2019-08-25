from flask import Flask, render_template, request, redirect, url_for,flash
from wtforms import Form, TextAreaField, StringField, IntegerField, validators
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_DB'] = 'jsse'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '25601262'
mysql = MySQL(app)

@app.route('/')
def index():
    return tags()

@app.route('/tags')
def tags():
    cur = mysql.connection.cursor()
    cur.execute('SELECT tag_id FROM tags')
    tags_id = cur.fetchall()
    mysql.connection.commit()
    print(tags_id)
    cur.close()

    return render_template('tags.html', tags_id=tags_id)

def get_data(tag_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tags WHERE tag_id = %s',(tag_id,))
    tag_data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return tag_data

@app.route('/tag/<string:tag_id>')
def tag(tag_id):
    tag_data = get_data(tag_id)
    return render_template('tag.html', tag_data=tag_data[0])

@app.route('/usr_app/<string:tag_id>')
def usr_app(tag_id):
    tag_data = get_data(tag_id)
    to_app = [ tag_data[0]['tag_' + i] for i in ['id','info','name','type']]
    return repr(to_app)[1:-1]

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        result = request.form['search']
        try:
            return redirect(url_for('tag',tag_id=result))
        except Exception as e:
            return redirect(url_for('tags'))

class editForm(Form):
    tag_id = StringField(u'tag_id',[validators.required(),validators.length(min=5,max=50)])
    tag_name = StringField(u'tag_name',[validators.required(),validators.length(min=0,max=10)])
    tag_type = StringField(u'tag_type',[validators.required(),validators.length(min=0)])
    tag_info = TextAreaField(u'tag_info',[validators.required(),validators.length(min=0,max=40)])

@app.route('/submit')
def submit(data):
    return render_template('submit.html', data=data)

@app.route('/new',methods=['GET','POST'])
def new():
    form = editForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        tag_id = form.tag_id.data
        tag_name = form.tag_name.data
        tag_type = form.tag_type.data
        tag_info = form.tag_info.data

        cur = mysql.connection.cursor()
        cur.execute('SELECT tag_name FROM tags WHERE tag_id = %s', (tag_id,))    
        test = cur.fetchall()

        if test == () :
            cur.execute('INSERT INTO tags(tag_id, tag_name, tag_type, tag_info) VALUES(%s, %s, %s, %s)',
                    (tag_id, tag_name, tag_type, tag_info))
            mysql.connection.commit()
            cur.close()
            return tag(tag_id) 
        else:
            error = 'The TAG ID already exits'

    return render_template('new.html',form=form,error=error)

@app.route('/delete/<string:tag_id>')
def delete(tag_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tags WHERE tag_id = %s', (tag_id,))
    mysql.connection.commit()
    cur.close()
    #return redirect(url_for('submit',data=tag_id))
    return redirect(url_for('tags'))

@app.errorhandler(404)
def page_not_found(e):
    return '404'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')