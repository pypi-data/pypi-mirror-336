from threading import Thread

# implementation based on https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread 
class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try: 
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout = None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret