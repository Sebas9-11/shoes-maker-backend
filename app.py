from config.db import app
from api.apiemployee import employee_route

app.register_blueprint(employee_route)

if __name__ == '__main__':    
    app.run(debug=True)
