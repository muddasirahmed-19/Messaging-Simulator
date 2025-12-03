class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for obs in list(self._observers):
            try:
                obs.update(*args, **kwargs)
            except:
                pass

class Observer:
    def update(self, *args, **kwargs):
        raise NotImplementedError()
