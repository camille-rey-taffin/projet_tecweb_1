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
        resp1 = self.app.get('/', follow_redirects=True)
        resp2 = self.app.get('/index', follow_redirects=True)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)


        """Page de login"""

    def test_login_get(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.get('/login', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 200)

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté
        resp_logged = self.app.get('/login', follow_redirects=True)
        self.assertEqual(resp_logged.status_code, 200)
        self.assertIn('Bonjour Thomas Mikolov, vous êtes bien connecté(e) !', resp_logged.data.decode('utf-8'))

    def test_login_post(self):
        #L'utilisateur se connecte avec des identifiants corrects
        resp_ok = self.login('Mikolov', 'Thomas')
        self.assertEqual(resp_ok.status_code, 200)
        self.assertIn('Bonjour Thomas Mikolov, vous êtes bien connecté(e) !', resp_ok.data.decode('utf-8'))

        #L'utilisateur se connecte avec des identifiants incorrects
        resp_nok = self.login('Poder', 'Solveig')
        self.assertEqual(resp_nok.status_code, 401)
        self.assertIn('Mot de passe ou identifiant incorrect', resp_nok.data.decode('utf-8'))


        """Page de logout"""

    def test_logout_get(self):

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté
        resp_logged = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(resp_logged.status_code, 200)
        self.assertIn('Vous avez bien été déconnecté.', resp_logged.data.decode('utf-8'))

        self.logout() #L'utilisateur essaie de charger la page alors qu'il n'est pas connecté
        resp_notlogged = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 400)


        """Données"""

    """Recherches de données"""
    def test_dataSearch_get(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.get('/data/search', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté mais n'a encore rien recherché
        resp_logged = self.app.get('/data/search', follow_redirects=True)
        self.assertEqual(resp_logged.status_code, 200)
        self.assertNotIn('Résultats', resp_logged.data.decode('utf-8'))

        #L'utilisateur a rempli au moins un champ et cliqué sur le bouton "Rechercher"
        #Il y a trois résultats
        resp_data = self.app.get('/data/search', query_string=dict(name='Lucelle'), follow_redirects=True)
        self.assertEqual(resp_data.status_code, 200)
        self.assertIn('Résultats', resp_data.data.decode('utf-8'))
        self.assertEqual(resp_data.data.decode('utf-8').count("<tr>"), 4)

        #L'utilisateur remplit tous les champs mais il n'y a pas de résultats correspondant
        resp_nodata = self.app.get('/data/search', query_string=dict(geonameid="a", name="b", asciiname="c", alternatenames="d", latitude="e", longitude="f", feature_class="g", feature_code="h", country_code="i", cc2="j", admin1_code="k", admin2_code="l", admin3_code="m", admin4_code="n", population="o", elevation="p", dem="q", timezone="r", modification_date="s"), follow_redirects=True)
        self.assertEqual(resp_nodata.status_code, 200)
        self.assertIn('Aucun résultat', resp_nodata.data.decode('utf-8'))

    """Ajout de données"""
    def test_dataAdd_get(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.get('/data/add', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté mais n'a encore rien ajouté
        resp_logged = self.app.get('/data/add', follow_redirects=True)
        self.assertEqual(resp_logged.status_code, 200)
        self.assertIn('Ajout de données', resp_logged.data.decode('utf-8'))

    def test_dataAdd_post(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.post('/data/add', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur se connecte
        #L'utilisateur ajoute un lieu qui n'existait pas
        resp_addok = self.app.post('/data/add', data=dict(geonameid='111111', name="truc"), follow_redirects=True)
        self.assertEqual(resp_addok.status_code, 200)
        self.assertIn('L\'élément <a href="/data/111111">111111<a> a bien été créé', resp_addok.data.decode('utf-8'))
        self.app.delete('/data/111111', follow_redirects=True)
        #L'utilisateur essaie d'ajouter un lieu qui existe déjà
        resp_addnok = self.app.post('/data/add', data=dict(geonameid='2659815', name="Lucelle"), follow_redirects=True)
        self.assertEqual(resp_addnok.status_code, 409)
        self.assertIn("Un élément de geonameid 2659815 existe déjà", resp_addnok.data.decode('utf-8'))


    """Affichage, suppression ou modification d'un lieu"""
    def test_data_get(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.get('/data/2659815', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté et consulte un lieu qui existe
        resp_logged = self.app.get('/data/2659815', data=dict(modif=False), follow_redirects=True)
        self.assertEqual(resp_logged.status_code, 200)
        self.assertIn('2659815', resp_logged.data.decode('utf-8'))
        #L'utilisateur essaie de consulter un lieu qui n'existe pas
        resp_nodata = self.app.get('/data/111111', follow_redirects=True)
        self.assertEqual(resp_nodata.status_code, 404)
        self.assertIn("OOPS ! Ce lieu n'existe pas !", resp_nodata.data.decode('utf-8'))


    def test_data_post(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.post('/data/2659815', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté et modifie un lieu
        self.app.post('/data/add', data=dict(geonameid='111111', name="truc"), follow_redirects=True)
        resp_modif = self.app.post('/data/111111', data=dict(alternatenames="autre truc"), follow_redirects=True)
        self.assertEqual(resp_modif.status_code, 200)
        self.assertIn("autre truc", resp_modif.data.decode('utf-8'))
        self.app.delete('/data/111111', follow_redirects=True)

    def test_data_delete(self):
        #L'utilisateur n'est pas connecté
        resp_notlogged = self.app.delete('/data/111111', follow_redirects=True)
        self.assertEqual(resp_notlogged.status_code, 401)
        self.assertIn('Identification requise pour accéder aux données, veuillez vous identifier', resp_notlogged.data.decode('utf-8'))

        self.login("Mikolov", "Thomas") #L'utilisateur est connecté et supprime un lieu
        self.app.post('/data/add', data=dict(geonameid='111111', name="truc"), follow_redirects=True)
        resp_del = self.app.delete('/data/111111', follow_redirects=True)
        self.assertEqual(resp_del.status_code, 200)
        resp_deleted_data= self.app.get('/data/111111', follow_redirects=True)
        self.assertEqual(resp_deleted_data.status_code, 404)

if __name__ == "__main__":
    unittest.main()
