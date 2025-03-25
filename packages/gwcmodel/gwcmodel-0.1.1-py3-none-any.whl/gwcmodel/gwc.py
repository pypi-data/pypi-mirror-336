import requests

class GWCModel:
    def __init__(self, api_key, access_token):
        self.base_url = "https://api.gwcindia.in/v1"
        self.api_key = api_key
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'Authorization': f'Bearer {self.access_token}'            
        })

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)
    
    def _post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {'error': str(e), 'response': response.text}

    # 🔹 GET Methods
    def profile(self):
        return self._get('profile')
        
    def balance(self):
        return self._get('balance')
    
    def positions(self):
        return self._get('positions')    
            
    def holdings(self):
        return self._get('holdings')

    def orderbook(self):
        return self._get('orderbook')

    def tradebook(self):
        return self._get('tradebook')

    def logout(self):
        return self._get('logout')

    # 📘 Post Methods
    def exitposition(self,data):
        return self._post('exitposition', data=data)

    def orderhistory(self, data):
        return self._post('orderhistory', data=data)

    def placeorder(self, data):
        return self._post('placeorder', data=data)

    def placeboorder(self, data):
        return self._post('placeboorder', data=data)

    def placecoorder(self, data):
        return self._post('placecoorder', data=data)

    def modifyorder(self, data):
        return self._post('modifyorder', data=data)

    def modifyboorder(self, data):
        return self._post('modifyboorder', data=data)

    def modifycoorder(self, data):
        return self._post('modifycoorder', data=data)

    def cancelorder(self, data):
        return self._post('cancelorder', data=data)
    
    def exitboorder(self, data):
        return self._post('exitboorder', data=data)
    
    def exitcoorder(self, data):
        return self._post('exitcoorder', data=data)
    
    def positionconversion(self, data):
        return self._post('positionconversion', data=data)
    
    def getquote(self, data):
        return self._post('getquote', data=data)
    
    def fetchsymbol(self, data):
        return self._post('fetchsymbol', data=data)    