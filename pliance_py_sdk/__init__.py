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
        response = requests.post(f'{self.url}api/{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)
        return response.json()

    def executePut(self, endpoint, data, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.put(f'{self.url}api/{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)
        return response.json()

    def executeGet(self, endpoint, givenName, subject, payload=None):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.get(f'{self.url}api/{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)
        return response.json()

    def executeDelete(self, endpoint, payload, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token.decode('utf-8')}
        response = requests.delete(f'{self.url}api/{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)
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

    def ping(self):
        return self.__executeGet('ping')

    # Person
    def registerPerson(self, command):
        return self.__executePut('PersonCommand', command)

    def viewPerson(self, query):
        return self.__executeGet('PersonQuery', payload=query)

    def searchPerson(self, query):
        return self.__executeGet('PersonQuery/Search', payload=query)

    def deletePerson(self, command):
        return self.__executeDelete('PersonCommand', command)

    def archivePerson(self, command):
        return self.__executePost('PersonCommand/Archive', command)

    def unarchivePerson(self, command):
        return self.__executePost('PersonCommand/Unarchive', command)

    def classifyPersonHit(self, command):
        return self.__executePost('PersonCommand/Classify', command)

    # Company
    def registerCompany(self, query):
        return self.__executePut('CompanyCommand', query)

    def viewCompany(self, query):
        return self.__executeGet('CompanyQuery', payload=query)

    def searchCompany(self, query):
        return self.__executeGet('CompanyQuery/Search', payload=query)

    def deleteCompany(self, command):
        return self.__executeDelete('CompanyCommand', command)

    def archiveCompany(self, command):
        return self.__executePost('CompanyCommand/Archive', command)

    def unarchiveCompany(self, command):
        return self.__executePost('CompanyCommand/Unarchive', command)

    def classifyCompanyHit(self, command):
        return self.__executePost('CompanyCommand/Classify', command)   

    def beneficiariesCompanyGraph(self, query):
        return self.__executePost('CompanyQuery/Graph/Beneficiaries', query)              

    # Feed
    def feed(self, query):
        return self.__executeGet('FeedQuery', payload=query)

    # Watchlist
    def watchlistPerson(self, query):
        return self.__executeGet('WatchlistQuery', payload=query)       

    def watchlistPerson_v2(self, query):
        return self.__executeGet('WatchlistQuery/v2', payload=query) 

    def watchlistCompany(self, query):
        return self.__executeGet('WatchlistQuery/Company', payload=query) 

    # Webhook
    def webhookGet(self, query):
        return self.__executeGet('WebhookQuery', payload=query)

    def webhookSave(self, command):
        return self.__executePut('WebhookCommand', command)

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