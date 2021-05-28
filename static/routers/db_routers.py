


class Route_meineDB:
    route_app_labels = {'huftrends'}

    def db_for_read(self, model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'meineDB'
        return None


class Route_default:
    route_app_labels = {'admin',
                        'auth',
                        'contenttypes',
                        'sessions', 
                        'messages',
                        'staticfiles',
                        'django_plotly_dash',}

    def db_for_read(self, model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    def db_for_write(self, model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    def allow_migrate(self, model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
    def allow_relation(self, model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None



    