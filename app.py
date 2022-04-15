from lib import create_app

app = create_app() 


@app.route('/')
def home():
    return "Hello admin"

if __name__ == "__main__":
    app.run(debug=True)