# coding: utf-8

import unittest

from frontend.frontend import app
 
 
class FrontTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

 
    # executed after each test
    def tearDown(self):
        pass
 
 
    ########################
    #### helper methods ####
    ########################
     
    def login(self, name, firstname):
        return self.app.post(
            '/login',
            data=dict(name=name, firstname=firstname),
            follow_redirects=True
        )
     
    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )
 
    ###############
    #### tests ####
    ###############
 
    """Page d'accueil"""
    
    def test_index_get(self):
        response = self.app.get('/', follow_redirects=True)
        response2 = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
    """Page de login/logout"""
        
    def test_login_get(self):
        #L'utilisateur n'est pas connecté
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        self.login("Mikolov", "Thomas") #L'utilisateur est connecté
        response2 = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Bonjour Thomas Mikolov', response2.data)
        
        response3 = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response3.status_code, 200)
        self.logout()
        
        
    def test_login_post(self):
        #L'utilisateur se connecte avec des identifiants corrects
        response = self.login('Mikolov', 'Thomas')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bonjour Thomas Mikolov', response.data)
        
        #L'utilisateur se connecte avec des identifiants incorrects
        response2 = self.login('Poder', 'Solveig')
        self.assertEqual(response2.status_code, 401)
        self.assertIn(b'Mot de passe ou identifiant incorrect', response2.data)

 
 
if __name__ == "__main__":
    unittest.main()