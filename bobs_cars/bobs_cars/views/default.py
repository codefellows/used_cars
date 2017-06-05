from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from bobs_cars.models import Car


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_page(request):
    """List car objects on the home page."""
    all_cars = request.dbsession.query(Car).order_by(Car.price)[::-1]
    return {'all_cars': all_cars}


@view_config(route_name='car_info', renderer='../templates/car_info.jinja2')
def car_info(request):
    """View the car info."""
    vin_num = int(request.matchdict['id'])
    one_car = request.dbsession.query(Car).get(vin_num)
    if not one_car:
        raise HTTPNotFound
    return {'car': one_car}


@view_config(route_name='new_car', renderer='../templates/new_car.jinja2')
def new_car(request):
    """Add a new car."""
    if request.method == "POST":
        data = request.POST
        new_car = Car(
            make=data['make'],
            year=int(data['year']),
            price=float(data['price']),
            model=data['model'],
            mileage=int(data['mileage']),
            condition=data['condition'],
            doors=int(data['doors']),
            color=data['color'],
            in_stock=True,
            description=data['description'],
        )
        request.dbsession.add(new_car)
        return HTTPFound(location=request.route_url('home'))
    return {}


@view_config(route_name='edit_car', renderer='../templates/edit_car.jinja2')
def edit_view(request):
    """This edits the car."""
    vin_num = int(request.matchdict['id'])
    one_car = request.dbsession.query(Car).get(vin_num)
    if not one_car:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'car': one_car
        }
    if request.method == "POST":
        data = request.POST
        one_car.make = data['make']
        one_car.year = int(data['year'])
        one_car.price = float(data['price'])
        one_car.model = data['model']
        one_car.mileage = int(data['mileage'])
        one_car.condition = data['condition']
        one_car.doors = int(data['doors'])
        one_car.color = data['color']
        one_car.in_stock = bool(data['in_stock'])
        one_car.description = data['description']
        request.dbsession.flush()
        return HTTPFound(request.route_url('car_info', id=one_car.vin_num))


@view_config(route_name='car_sales', renderer='../templates/sales.jinja2')
def car_sales(request):
    """Track sales for all cars sold."""
    sold_cars = request.dbsession.query(Car).filter(
        Car.in_stock is False
    ).all()
    amount = sum(request.dbsession.query(Car.price).filter(
        Car.in_stock is False
    ).all())
    makes = request.dbsession.query(Car.make).filter(
        Car.in_stock is False
    ).distinct().all()

    return {
        'total_sales': amount,
        'number_sold': len(sold_cars),
        'makes_sold': makes
    }
