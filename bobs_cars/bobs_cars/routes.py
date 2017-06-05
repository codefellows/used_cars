def includeme(config):
    config.add_static_view('static', 'bobs_cars:static')
    config.add_route('home', '/')
    config.add_route('car_info', '/info/{id:\w+}')
    config.add_route('new_car', '/new-car')
    config.add_route('edit_car', '/edit/{id:\w+}')
    config.add_route('car_sales', '/sales')