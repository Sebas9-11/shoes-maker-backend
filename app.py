from config.db import app
from api.apirol import rol_route
from api.apiemployee import employee_route
from api.apiproducts import products_route

app.register_blueprint(rol_route)
app.register_blueprint(employee_route)
app.register_blueprint(products_route)

if __name__ == '__main__':    
     app.run(debug=True)
