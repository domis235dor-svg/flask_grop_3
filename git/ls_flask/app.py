from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/for_student')
def for_student():
 
    return render_template( template_name_or_list= 'for_student.html', name='dima')


app.run(debug=True)

