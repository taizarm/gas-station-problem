from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_route('index_view', '/')

    config.add_static_view('static', 'gas_station_problem:static/', cache_max_age=3600)
    config.add_static_view('deform-static', 'deform:static/')

    config.scan()
    return config.make_wsgi_app()
