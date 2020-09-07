#!/usr/bin/python3

import unittest
import contextlib
import os
import requests
import ssl
import tempfile
import OpenSSL.crypto #pip install pyopenssl
import random
import string

from pliance_py_sdk import ClientFactory, ApiException

@contextlib.contextmanager
def pfx_to_pem(pfx_path, pfx_password):
    ''' Decrypts the .pfx file to be used with requests. '''
    t_pem = 'temp.pem'
    f_pem = open(t_pem, 'wb')
    pfx = open(pfx_path, 'rb').read()
    p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
    f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
    ca = p12.get_ca_certificates()
    if ca is not None:
        for cert in ca:
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))

    f_pem.close()
    return t_pem


class TestSum(unittest.TestCase):

    def randomString(self, stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))    

    def createFactory(self):
        return ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')

    def createClient(self):
        factory = self.createFactory()

        return factory.create('Adam Furtenbach', '1337')

    def test_bad_request(self):        
        client = self.createClient()

        person = {
            'personReferenceId': self.randomString(),
        }

        try:
            response = client.view_person(person)
            self.assertTrue(False)
        except ApiException as error:
            return

    def test_ping_no_cert(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local-no-cert.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')
        res = client.ping({})

        self.assertEqual(res['message'], 'Pong')

    def test_ping(self):
        client = self.createClient()
        res = client.ping({})

        self.assertEqual(res['message'], 'Pong') 

    def test_register_person(self):
        client = self.createClient()
        id = self.randomString()
        res = self.createPerson(client, id)

        self.assertTrue(res['success'])

    def test_archive_person(self):
        client = self.createClient()
        id = self.randomString()
        self.createPerson(client, id)
        
        res = self.archivePerson(client, id)

        self.assertTrue(res['success'])        


    def test_unarchive_person(self):
        client = self.createClient()
        id = self.randomString()
        self.createPerson(client, id)
        self.archivePerson(client, id)

        command = {
            'personReferenceId': id,
        }       

        res = client.unarchive_person(command)

        self.assertTrue(res['success'])

    def test_delete_person(self):
        client = self.createClient()
        id = self.randomString()
        self.createPerson(client, id)

        command = {
            'personReferenceId': id,
        }       

        res = client.delete_person(command)

        self.assertTrue(res['success'])

    def test_view_person(self):
        client = self.createClient()
        id = self.randomString()
        self.createPerson(client, id)

        command = {
            'personReferenceId': id,
        }       

        res = client.view_person(command)

        self.assertTrue(res['success'])

    def test_search_person(self):
        client = self.createClient()
        id = self.randomString()
        self.createPerson(client, id)

        command = {
            'query': 'Osama',
        }       

        res = client.search_person(command)

        self.assertTrue(res['success'])        

    def test_classify_person(self):
        client = self.createClient()
        id = self.randomString()
        person = self.createPerson(client, id)
        match = person['data']['hits'][0][0]

        command = {
            'personReferenceId': id,
            'aliasId': match['aliasId'],
            'matchId': match['matchId'],
            'classification': 'FalsePositive'
        }       

        res = client.view_person(command)

        self.assertTrue(res['success'])

    def test_watchlist_person_v1(self):
        client = self.createClient()
        id = self.randomString()
        person = self.createPerson(client, id)
        match = person['data']['hits'][0][0]

        command = {
            'id': match['matchId'],
            'firstName': "Osama",
            'lastName': "bin Laden",
        }       

        res = client.watchlist_person(command)

        self.assertTrue(res['success'])

    def test_watchlist_person_v2(self):
        client = self.createClient()
        id = self.randomString()
        person = self.createPerson(client, id)
        match = person['data']['hits'][0][0]

        command = {
		    'matchId': match['matchId'],
		    'personReferenceId': id,
        }       

        res = client.watchlist_person_v2(command)

        self.assertTrue(res['success'])

    def test_feed(self):
        client = self.createClient()

        command = {
        }       

        res = client.feed(command)

        self.assertTrue(res['success'])

    def test_saveWebhook(self):
        client = self.createClient()

        command = {
            'enabled': True,
            'url': "https://url",
            'secret': "secret",
        }       

        res = client.save_webhook(command)

        self.assertTrue(res['success'])

    def test_getWebhook(self):
        client = self.createClient()

        command = {
        }       

        res = client.get_webhook(command)

        self.assertTrue(res['success'])

###

    def test_register_company(self):
        client = self.createClient()
        id = self.randomString()
        res = self.createCompany(client, id)

        self.assertTrue(res['success'])

    def test_archive_company(self):
        client = self.createClient()
        id = self.randomString()
        self.createCompany(client, id)
        
        res = self.archiveCompany(client, id)

        self.assertTrue(res['success'])        


    def test_unarchive_company(self):
        client = self.createClient()
        id = self.randomString()
        self.createCompany(client, id)
        self.archiveCompany(client, id)

        command = {
            'companyReferenceId': id,
        }       

        res = client.unarchive_company(command)

        self.assertTrue(res['success'])

    def test_delete_company(self):
        client = self.createClient()
        id = self.randomString()
        self.createCompany(client, id)

        command = {
            'companyReferenceId': id,
        }       

        res = client.delete_company(command)

        self.assertTrue(res['success'])

    def test_view_company(self):
        client = self.createClient()
        id = self.randomString()
        self.createCompany(client, id)

        command = {
            'companyReferenceId': id,
        }       

        res = client.view_company(command)

        self.assertTrue(res['success'])

    def test_search_company(self):
        client = self.createClient()
        id = self.randomString()
        self.createCompany(client, id)

        command = {
            'query': 'Daesong',
        }       

        res = client.search_company(command)

        self.assertTrue(res['success'])        

    def test_classify_company(self):
        client = self.createClient()
        id = self.randomString()
        company = self.createCompany(client, id)
        match = company['data']['hits'][0][0]

        command = {
            'companyReferenceId': id,
            'aliasId': match['aliasId'],
            'matchId': match['matchId'],
            'classification': 'FalsePositive'
        }       

        res = client.view_company(command)

        self.assertTrue(res['success'])

    def test_watchlist_company(self):
        client = self.createClient()
        id = self.randomString()
        company = self.createCompany(client, id)
        match = company['data']['hits'][0][0]

        command = {
		    'matchId': match['matchId'],
		    'companyReferenceId': id,
        }       

        res = client.watchlist_company(command)

        self.assertTrue(res['success'])

    def createCompany(self, client, id):
        command = {
            'name': 'Korea Daesong Bank',
            'companyReferenceId': id,
        }

        return client.register_company(command)

    def archiveCompany(self, client, id):
        command = {
            'companyReferenceId': id,
        }       

        return client.archive_company(command)

    def createPerson(self, client, id):
        command = {
            'firstName': 'Osama',
            'lastName': 'bin Laden',
            'personReferenceId': id,
        }

        return client.register_person(command)

    def archivePerson(self, client, id):
        command = {
            'personReferenceId': id,
        }       

        return client.archive_person(command)

if __name__ == '__main__':
    pfx_to_pem('client.pfx', [])
    unittest.main()
