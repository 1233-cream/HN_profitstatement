from profit_flask import app

profit_app = app

if __name__ == '__main__':
    profit_app.run(port=8000,debug=True)