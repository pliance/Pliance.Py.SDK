import requests
import jwt
import datetime

class ClientFactory:
    def __init__(self, secret, issuer, url, cert=None):
        self.secret = secret
        self.issuer = issuer
        self.url = url
        self.cert = cert

    def create(self, givenName, subject):
        return PlianceClient(self, givenName, subject)

    def executePost(self, endpoint, data, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.post(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)
        return response.json()

    def executePut(self, endpoint, data, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.put(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)
        return response.json()

    def executeGet(self, endpoint, givenName, subject, payload=None):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.get(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)
        return response.json()

    def executeDelete(self, endpoint, payload, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.delete(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)
        return response.json()

    def __getJwt(self, givenName, subject):
        token = jwt.encode(
            {
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300),
                'aud': 'pliance.io',
                'iss': self.issuer,
                'given_name': givenName,
                'sub': subject
            }, self.secret, algorithm='HS256')
        return token

class PlianceClient:
    def __init__(self, factory, givenName, subject):
        self.factory = factory
        self.givenName = givenName
        self.subject = subject

    # @inject: methods
    def archive_company(self, command):
    	return self.__executePost('api/CompanyCommand/Archive', command)

    def archive_person(self, command):
    	return self.__executePost('api/PersonCommand/Archive', command)

    def classify_company_hit(self, command):
    	return self.__executePost('api/CompanyCommand/Classify', command)

    def classify_person_hit(self, command):
    	return self.__executePost('api/PersonCommand/Classify', command)

    def delete_company(self, command):
    	return self.__executeDelete('api/CompanyCommand', command)

    def delete_person(self, command):
    	return self.__executeDelete('api/PersonCommand', command)

    def feed(self, request):
    	return self.__executeGet('api/FeedQuery', request)

    def get_report(self, request):
    	return self.__executeGet('api/ReportQuery', request)

    def get_webhook(self, request):
    	return self.__executeGet('api/WebhookQuery', request)

    def ping(self, request):
    	return self.__executeGet('api/Ping', request)

    def register_company(self, command):
    	return self.__executePut('api/CompanyCommand', command)

    def register_person(self, command):
    	return self.__executePut('api/PersonCommand', command)

    def save_webhook(self, command):
    	return self.__executePut('api/WebhookCommand', command)

    def search_company(self, request):
    	return self.__executeGet('api/CompanyQuery/Search', request)

    def search_person(self, request):
    	return self.__executeGet('api/PersonQuery/Search', request)

    def unarchive_company(self, command):
    	return self.__executePost('api/CompanyCommand/Unarchive', command)

    def unarchive_person(self, command):
    	return self.__executePost('api/PersonCommand/Unarchive', command)

    def view_company(self, request):
    	return self.__executeGet('api/CompanyQuery', request)

    def view_person(self, request):
    	return self.__executeGet('api/PersonQuery', request)

    def watchlist_company(self, request):
    	return self.__executeGet('api/WatchlistQuery/Company', request)

    def watchlist_person(self, request):
    	return self.__executeGet('api/WatchlistQuery', request)

    def watchlist_person_v2(self, request):
    	return self.__executeGet('api/WatchlistQuery/v2', request)

    # @inject: !methods

    ## Internal
    def __executeGet(self, endpoint, payload=None):
        result = self.factory.executeGet(endpoint, self.givenName, self.subject, payload=payload)
        
        return self.__throw_on_error(result)

    def __executePut(self, endpoint, data):
        result = self.factory.executePut(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __executePost(self, endpoint, data):
        result = self.factory.executePost(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __executeDelete(self, endpoint, data):
        result = self.factory.executeDelete(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __throw_on_error(self, payload):
        if not payload['success']:
            raise ApiException(payload['message'])

        return payload

class ApiException(Exception):
    pass