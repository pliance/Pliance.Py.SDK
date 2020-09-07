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



        #self.assertEqual(res['status'], 'Success')        

    # def test_ping(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     res = client.ping({})

    #     self.assertEqual(res['message'], 'Pong')            


    # def test_ping(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     res = client.ping({})

    #     self.assertEqual(res['message'], 'Pong')

    # def test_ping_not_cert(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local-no-cert.pliance.io/', cert=None)
    #     client = clientFactory.create('Adam', '1')
    #     res = client.ping({})

    #     self.assertEqual(res['message'], 'Pong')



    # def test_view_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     person = {
    #         'personReferenceId': 'reference-id'
    #     }

    #     res = client.viewPerson(person)

    #    # print(res)
    #     self.assertEqual(res['data']['personReferenceId'], 'reference-id')

    # def test_classify_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     id = self.randomString()
    #     registerPerson = {
    #         'firstName': 'Ebba',
    #         'lastName': 'Busch',
    #         'personReferenceId': id,
    #         'identity': {
    #             "country": "se"
    #         }
    #     }

    #     res = client.registerPerson(registerPerson)

    #     person = {
    #         'personReferenceId': id,
    #         'matchId': res['data']['hits'][0][0]['matchId'],
    #         'aliasId': res['data']['hits'][0][0]['aliasId'],
    #         'classification': 'FalsePositive'
    #     }

    #     res = client.classifyPersonHit(person)

    #     self.assertEqual(res['status'], 'Success')

    # def test_search_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     query = {
    #         'query': 'Osama bin',
    #         'page': {
    #             'size': 10,
    #             'no': 1
    #         },
    #         'filter': {
    #             'isSanction': True
    #         }
    #     }

    #     res = client.searchPerson(query)

    #     self.assertTrue(len(res['data']) > 0)

    # def test_archive_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     id = self.randomString()
    #     registerPerson = {
    #         'firstName': 'Osama',
    #         'lastName': 'bin laden',
    #         'personReferenceId': id
    #     }

    #     res = client.registerPerson(registerPerson)

    #     person = {
    #         'personReferenceId': id
    #     }

    #     res = client.archivePerson(person)

    #     self.assertEqual(res['status'], 'Success')

    # def test_unarchive_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     person = {
    #         'personReferenceId': 'reference-id'
    #     }

    #     res = client.unarchivePerson(person)

    #     self.assertEqual(res['status'], 'Success')

    # def test_delete_person(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     id = self.randomString()
    #     registerPerson = {
    #         'firstName': 'Osama',
    #         'lastName': 'bin laden',
    #         'personReferenceId': id
    #     }

    #     res = client.registerPerson(registerPerson)

    #     person = {
    #         'personReferenceId': id
    #     }

    #     res = client.deletePerson(person)

    #     self.assertEqual(res['status'], 'Success')


    # def test_register_company(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     company = {
    #         'name': 'Plisec',
    #         'companyReferenceId': 'comp-reference-id',
    #         'identity': {
    #             'identity': '559161-4275',
    #             'country': 'sv'
    #         }
    #     }

    #     res = client.registerCompany(company)

    #     self.assertEqual(res['status'], 'Success')

    # def test_view_company(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     company = {
    #         'companyReferenceId': 'comp-reference-id'
    #     }

    #     res = client.viewCompany(company)

    #     self.assertEqual(res['data']['companyReferenceId'], 'comp-reference-id')

    # def test_search_company(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')

    #     query = {
    #         'query': 'Pliesec',
    #         'page': {
    #             'size': 10,
    #             'no': 1
    #         },
    #         'filter': {
    #             'isSanction': True
    #         }
    #     }

    #     res = client.searchCompany(query)

    #     self.assertTrue(len(res['data']) > 0)

    # def test_archive_company(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     id = self.randomString()

    #     registerCompany = {
    #         'name': 'Plisec',
    #         'companyReferenceId': id,
    #         'identity': {
    #             'identity': '559161-4275',
    #             'country': 'sv'
    #         }
    #     }

    #     res = client.registerCompany(registerCompany)        

    #     company = {
    #         'companyReferenceId': id
    #     }

    #     res = client.archiveCompany(company)

    #     self.assertEqual(res['status'], 'Success')

    # def test_feed(self):
    #     clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 'Demo', 'https://local.pliance.io/', cert='temp.pem')
    #     client = clientFactory.create('Adam', '1')
    #     query = {}

    #     res = client.feed(query)        

    #     self.assertEqual(res['status'], 'Success')        

if __name__ == '__main__':
    pfx_to_pem('client.pfx', [])
    unittest.main()
