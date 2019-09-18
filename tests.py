import unittest
import contextlib
import os
import requests
import ssl
import tempfile
import OpenSSL.crypto #pip install pyopenssl

from pliance_py_sdk import ClientFactory

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
    def test_ping(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')
        res = client.ping()

        self.assertEqual(res['message'], 'Pong')

    def test_register_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'firstName': 'Osama',
            'lastName': 'bin laden',
            'personReferenceId': 'reference-id'
        }

        res = client.registerPerson(person)

        self.assertEqual(res['status'], 'Success')

    def test_view_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'personReferenceId': 'reference-id'
        }

        res = client.viewPerson(person)

       # print(res)
        self.assertEqual(res['data']['personReferenceId'], 'reference-id')

    def test_classify_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'personReferenceId': 'reference-id',
            'matchId': 'EuSanction-833',
            'aliasId': 'a1be37af314c0cc35c5f9f4124f5f6aa0c050fbe5846e020ae17c0fe02c8c55e',
            'classification': 'FalsePositive'
        }

        res = client.classifyPersonMatch(person)

        self.assertEqual(res['status'], 'Success')

    def test_search_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        query = {
            'query': 'Osama bin',
            'page': {
                'size': 10,
                'no': 1
            },
            'filter': {
                'isSanction': True
            }
        }

        res = client.searchPerson(query)


        self.assertEqual(res['data']['result'][0]['personReferenceId'], 'reference-id')

    def test_archive_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'personReferenceId': 'reference-id'
        }

        res = client.archivePerson(person)

        self.assertEqual(res['status'], 'Success')

    def test_unarchive_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'personReferenceId': 'reference-id'
        }

        res = client.unarchivePerson(person)

        self.assertEqual(res['status'], 'Success')

    def test_delete_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        person = {
            'personReferenceId': 'reference-id'
        }

        res = client.deletePerson(person)

        self.assertEqual(res['status'], 'Success')


    def test_register_company(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        company = {
            'name': 'Plisec',
            'companyReferenceId': 'comp-reference-id',
            'identity': {
                'identity': '559161-4275',
                'country': 'sv'
            }
        }

        res = client.registerCompany(company)

        self.assertEqual(res['status'], 'Success')

    def test_view_company(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        company = {
            'companyReferenceId': 'comp-reference-id'
        }

        res = client.viewCompany(company)

        self.assertEqual(res['data']['companyReferenceId'], 'comp-reference-id')

    def test_search_company(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        query = {
            'query': 'Pliesec',
            'page': {
                'size': 10,
                'no': 1
            },
            'filter': {
                'isSanction': True
            }
        }

        res = client.searchCompany(query)

        self.assertEqual(res['data']['result'][0]['companyReferenceId'], 'comp-reference-id')

    def test_archive_company(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        company = {
            'companyReferenceId': 'comp-reference-id'
        }

        res = client.archiveCompany(company)

        self.assertEqual(res['status'], 'Success')

    def test_archive_company(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        company = {
            'companyReferenceId': 'comp-reference-id'
        }

        res = client.unarchiveCompany(company)

        self.assertEqual(res['status'], 'Success')

    def test_delete_person(self):
        clientFactory = ClientFactory('2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',  'Demo', 'https://adam.pliance.io/', cert='temp.pem')
        client = clientFactory.create('Adam', '1')

        company = {
            'companyReferenceId': 'comp-reference-id'
        }

        res = client.deleteCompany(company)

        self.assertEqual(res['status'], 'Success')

if __name__ == '__main__':
    unittest.main()
