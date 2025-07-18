class AppContext:
    def __init__(self):
        self._services = {}
    def set_service(self, name: str, service_instance):
        self._services[name] = service_instance
    def get_service(self, name: str):
        return self._services.get(name)
    def get_all_services(self) -> dict:
        return self._services
