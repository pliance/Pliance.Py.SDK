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
        #print(response)
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
                'given_name': 'Adam Furtenbach',
                'sub': '1337',
                'id': 1
            }, self.secret, algorithm='HS256')
        return token

class PlianceClient:
    def __init__(self, factory, givenName, subject):
        self.factory = factory
        self.givenName = givenName
        self.subject = subject

    def ping(self):
        return self.__executeGet('ping')

    def registerPerson(self, person):
        return self.__executePut('PersonCommand', person)

    def viewPerson(self, person):
        return self.__executeGet('PersonQuery', payload=person)

    def classifyPersonMatch(self, person):
        return self.__executePost('PersonCommand/Classify', person)

    def searchPerson(self, query):
        return self.__executeGet('PersonQuery/search', payload=query)

    def archivePerson(self, person):
        return self.__executePost('PersonCommand/archive', person)

    def unarchivePerson(self, person):
        return self.__executePost('PersonCommand/unarchive', person)

    def deletePerson(self, person):
        return self.__executeDelete('PersonCommand', person)

    def registerCompany(self, company):
        return self.__executePut('CompanyCommand', company)

    def viewCompany(self, company):
        return self.__executeGet('CompanyQuery', payload=company)

    def searchCompany(self, query):
        return self.__executeGet('CompanyQuery/search', payload=query)

    def archiveCompany(self, company):
        return self.__executePost('CompanyCommand/archive', company)

    def unarchiveCompany(self, company):
        return self.__executePost('CompanyCommand/unarchive', company)

    def deleteCompany(self, company):
        return self.__executeDelete('CompanyCommand', company)

    def __executeGet(self, endpoint, payload=None):
        return self.factory.executeGet(endpoint, self.givenName, self.subject, payload=payload)

    def __executePut(self, endpoint, data):
        return self.factory.executePut(endpoint, data, self.givenName, self.subject)

    def __executePost(self, endpoint, data):
        return self.factory.executePost(endpoint, data, self.givenName, self.subject)

    def __executeDelete(self, endpoint, data):
        return self.factory.executeDelete(endpoint, data, self.givenName, self.subject)
