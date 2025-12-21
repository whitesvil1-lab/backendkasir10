from flask import Flask


print("FILE DIJALANKAN")  # <- PENTING

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

if __name__ == "__main__":
    print("MASUK MAIN")
    app.run(debug=True, host="127.0.0.1", port=8000)