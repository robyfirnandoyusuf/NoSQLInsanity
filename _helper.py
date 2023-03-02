import requests
class Switch:
    def __init__(self, value):
        self.value = value
        self._entered = False
        self._broken = False
        self._prev = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False # Allows a traceback to occur

    def __call__(self, *values):
        if self._broken:
            return False
        
        if not self._entered:
            if values and self.value not in values:
                return False
            self._entered, self._prev = True, values
            return True
        
        if self._prev is None:
            self._prev = values
            return True
        
        if self._prev != values:
            self._broken = True
            return False
        
        if self._prev == values:
            self._prev = None
            return False
    
    @property
    def default(self):
        return self()
    
class WebAppTester:
    def __init__(self, url):
        self.url = url
    
    def is_up(self):
        try:
            # Send a GET request to the web application
            response = requests.get(self.url)

            # Check the status code of the response
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            # Handle any errors that occur while sending the request
            print("An error occurred while testing the web application")
            return False
    