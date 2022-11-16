from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def predict():
    'checking CI/CD pipeline'
    return 'Testing CI/CD pipeline'

if __name__ == "__main__":
    app.run()