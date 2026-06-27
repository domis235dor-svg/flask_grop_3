from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    celsius = None
    fahrenheit = None

    if request.method == 'POST':
        celsius = float(request.form.get('celsius'))
        fahrenheit = celsius * 9 / 5 + 32

    return render_template(
        'temperature.html',
        celsius=celsius,
        fahrenheit=fahrenheit
    )


app.run(debug=True)



    