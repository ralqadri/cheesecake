from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/page', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        videolink = request.form.get('link')
        return '''
            <h1>link is {}</h1>
        '''.format(videolink)
    else:
        return render_template('index.html')


# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
