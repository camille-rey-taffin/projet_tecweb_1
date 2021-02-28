define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "/mnt/c/Users/china/Desktop/TAL_M2/s2/Technique_web/apidoc/apifinal/doc/main.js",
    "groupTitle": "/mnt/c/Users/china/Desktop/TAL_M2/s2/Technique_web/apidoc/apifinal/doc/main.js",
    "name": ""
  },
  {
    "type": "get",
    "url": "/logout",
    "title": "Logout utilisateur",
    "name": "get",
    "group": "Authentification",
    "description": "<p>Permet à un utilisateur de se déconnecter (invalide son token d'authentification).</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse Succès:",
          "content": "HTTP/1.1 200 OK\n{\n   \"message\" : \"successfully logged out\",\n   \"status\" : \"succes\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de se déconnecter alors qu'il n'est pas connecté sur une session valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de se déconnecter alors qu'il n'est pas connecté.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Authentification"
  },
  {
    "type": "post",
    "url": "/login",
    "title": "Login utilisateur",
    "name": "post",
    "group": "Authentification",
    "description": "<p>Permet à un utilisateur de s'authentifier en renvoyant un token d'authentification.</p>",
    "examples": [
      {
        "title": "Exemple de requête:",
        "content": "    endpoint: http://digidata.api.localhost/login\n\nbody:\n     {\n       \"name\": \"Poder\",\n       \"firstname\": \"Camille\"\n     }",
        "type": "json"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Nom de l'utilisateur à identifier.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "firstname",
            "description": "<p>Prénom de l'utilisateur à identifier.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse Succès:",
          "content": "HTTP/1.1 200 OK\n{\n   \"Token\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjAwMSIsImV4cCI6MTYxNDQ2NTc1NX0.srnWB-HluXla7rJwJYymyqjs2hydysk1yxD5xui_61I\",\n   \"User\": {\n      \"actif\": false,\n      \"actionnaire\": true,\n      \"anciennete\": 10,\n      \"conge\": 15,\n      \"fonction\": \"Directeur des representations vectorielles\",\n      \"id\": \"001\",\n      \"mise_a_jour\": \"2017-05-06 11:25:11.827000\",\n      \"missions\": [\n         \"Bruxelle\",\n         \"Paris\",\n         \"Pakistan\"\n      ],\n      \"nom\": \"Poder\",\n      \"prenom\": \"Camille\"\n      },\n   \"status\": \"success\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Requête incorrecte, les mauvais paramètres ont été passés.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>Utilisateur introuvable dans la BDD : le prénom ou le nom est erroné.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur400:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"wrong authentification fields ('name' and 'firstname' required)\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"Incorrect name and/or firstname\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Authentification"
  },
  {
    "type": "get",
    "url": "/data/search?name={name}&geonameid={geonameid}&asciiname={asciiname}&alternatename={alternatename}&reste_des_paramètres",
    "title": "Recherche de données filtrées",
    "name": "get",
    "group": "DataSearch",
    "description": "<p>Permet à un utilisateur d'effectuer une recherche en filtrant ave certains champs (au minimum un champ).</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "name",
            "description": "<p>Nom du point géographique (utf8).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "geonameid",
            "description": "<p>ID entier de l'enregistrement dans la base de données des noms géographiques.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "asciiname",
            "description": "<p>nom du point géographique en caractères ascii simples.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "alternatename",
            "description": "<p>noms alternatifs, séparés par des virgules, noms ascii automatiquement translittérés, attribut de commodité du tableau des noms alternatifs.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "latitude",
            "description": "<p>latitude en degrés décimaux.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "longitude",
            "description": "<p>longitude in decimal degrees.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_class",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_code",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "country_code",
            "description": "<p>Code pays ISO-3166 à 2 lettres, 2 caractères.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "cc2",
            "description": "<p>autres codes pays, séparés par des virgules, code pays ISO-3166 à 2 lettres.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin1_code",
            "description": "<p>fipscode (susceptible d'être modifié en code iso), voir les exceptions ci-dessous, voir le fichier admin1Codes.txt pour les noms d'affichage de ce code.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin2_code",
            "description": "<p>code pour la deuxième division administrative, un comté aux États-Unis, voir le fichier admin2Codes.txt.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin3_code",
            "description": "<p>code for third level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin4_code",
            "description": "<p>code for fourth level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "population",
            "description": "<p>bigint.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "elevation",
            "description": "<p>en mètres, nombre entier.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "dem",
            "description": "<p>modèle numérique d'élévation, srtm3 ou gtopo30, élévation moyenne de 3''x3'' (environ 90mx90m) ou 30''x30''.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "timezone",
            "description": "<p>le fuseau horaire iana id (voir le fichier timeZone.txt).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "modification_date",
            "description": "<p>date de la dernière modification au format aaaa-MM-jj.</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Les filtres de recherche ne correspondent pas à des champs de la BDD.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "412",
            "description": "<p>Aucun filtre de recherche n'est indiqué.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de consulter les données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de consulter les données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur400:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"wrong format (field does not exist in db)\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur412:",
          "content": "HTTP/1.1 412 Precondition failed\n{\n   \"message\" : \"missing parameter(s) for filtering\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "DataSearch"
  },
  {
    "type": "delete",
    "url": "/data/<geonameid>",
    "title": "Supprimer des données",
    "name": "delete",
    "group": "Data",
    "description": "<p>Permet à un utilisateur de supprimer un lieu de la base de données.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "geonameid",
            "description": "<p>ID entier de l'enregistrement dans la base de données des noms géographiques.</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse succès:",
          "content": "HTTP/1.1 200 OK\n{\n   \"message\" : \"{geonameid} successfully deleted\",\n   \"status\":\"succes\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Le paramètre geonameid est manquant.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>Le geonameid renseigné n'existe pas.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de supprimer des données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de supprimer des données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur400:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\": \"geonameid to modify is missing\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur404:",
          "content": "HTTP/1.1 404 Not Found\n{\n   \"message\" : \"{geonameid} does not exist in database\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Data"
  },
  {
    "type": "get",
    "url": "/data",
    "title": "Affichage des données",
    "name": "get",
    "group": "Data",
    "description": "<p>Permet à un utilisateur d'accéder à toutes les données en lecture.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse succès:",
          "content": "HTTP/1.1 200 OK\n{\"data\":[donnees_lieu1, donnees_lieu2...]}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de consulter les données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de consulter les données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Data"
  },
  {
    "type": "get",
    "url": "/data/<geonameid>",
    "title": "Affichage des données filtrées",
    "name": "get",
    "group": "Data",
    "description": "<p>Permet à un utilisateur d'accéder en lecture à tous les champs d'un lieu grâce à son geonameid.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "geonameid",
            "description": "<p>ID entier de l'enregistrement dans la base de données des noms géographiques.</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse succès:",
          "content": "HTTP/1.1 200 OK\n    {\"data\":{\"admin1_code\":\"84\",\n            \"admin2_code\":\"74\",\n            \"admin3_code\":\"744\",\n            \"admin4_code\":\"74058\",\n            \"alternatenames\":\"Rapenaz  Col de,Recon  Col de\",\n            \"asciiname\":\"Col de Recon\",\n            \"cc2\":\"CH\",\n            \"country_code\":\"FR\",\n            \"dem\":\"1733\",\n            \"elevation\":\"\",\n            \"feature_class\":\"T\",\n            \"feature_code\":\"PASS\",\n            \"geonameid\":\"2659086\",\n            \"latitude\":\"46.30352\",\n            \"longitude\":\"6.82838\",\n            \"modification_date\":\"2019-02-15\",\n            \"name\":\"Col de Recon\",\n            \"population\":\"0\",\n            \"timezone\":\"Europe/Paris\"}}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>Le geonameid renseigné n'existe pas.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de consulter les données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de consulter les données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur404:",
          "content": "HTTP/1.1 404 Not Found\n{\n   \"message\": \"message\": \"geonameid not found\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Data"
  },
  {
    "type": "post",
    "url": "/data/<geonameid>",
    "title": "Modifier les données",
    "name": "post",
    "group": "Data",
    "description": "<p>Permet à un utilisateur de modifier un ou plusieurs champs d'un lieu dans la base de données.</p>",
    "examples": [
      {
        "title": "Exemple de requête:",
        "content": "    endpoint: http://digidata.api.localhost/data/7777777\n\nbody:\n     {\n       \"name\": \"Nouveau nom\",\n       \"country_code\": \"nouveau code\",\n       ...(autres paramètres possibles)...\n     }",
        "type": "json"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "geonameid",
            "description": "<p>ID entier de l'enregistrement dans la base de données des noms géographiques.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "name",
            "description": "<p>Nom du point géographique (utf8).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "asciiname",
            "description": "<p>nom du point géographique en caractères ascii simples.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "alternatename",
            "description": "<p>noms alternatifs, séparés par des virgules, noms ascii automatiquement translittérés, attribut de commodité du tableau des noms alternatifs.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "latitude",
            "description": "<p>latitude en degrés décimaux.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "longitude",
            "description": "<p>longitude in decimal degrees.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_class",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_code",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "country_code",
            "description": "<p>Code pays ISO-3166 à 2 lettres, 2 caractères.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "cc2",
            "description": "<p>autres codes pays, séparés par des virgules, code pays ISO-3166 à 2 lettres.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin1_code",
            "description": "<p>fipscode (susceptible d'être modifié en code iso), voir les exceptions ci-dessous, voir le fichier admin1Codes.txt pour les noms d'affichage de ce code.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin2_code",
            "description": "<p>code pour la deuxième division administrative, un comté aux États-Unis, voir le fichier admin2Codes.txt.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin3_code",
            "description": "<p>code for third level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin4_code",
            "description": "<p>code for fourth level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "population",
            "description": "<p>bigint.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "elevation",
            "description": "<p>en mètres, nombre entier.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "dem",
            "description": "<p>modèle numérique d'élévation, srtm3 ou gtopo30, élévation moyenne de 3''x3'' (environ 90mx90m) ou 30''x30''.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "timezone",
            "description": "<p>le fuseau horaire iana id (voir le fichier timeZone.txt).</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse succès:",
          "content": "HTTP/1.1 200 OK\n{\n   \"message\" : \"{geonameid} successfully modified\"\n   \"status\" :\"succes\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-1",
            "description": "<p>Le paramètre geonameid est manquant.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-2",
            "description": "<p>Le(s) champ(s) à modifier n'a pas été précisé.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-3",
            "description": "<p>Le champ geonameid ne peut pas être modifié.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-4",
            "description": "<p>Un (ou plusieurs) des champs renseignés n'existe pas dans la BDD.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>Le geonameid renseigné n'existe pas.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie de modifier des données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie de modifier des données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur400-1:",
          "content": "HTTP/1.1 400-1 Bad Request\n{\n   \"message\": \"geonameid to modify is missing\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur400-2:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"missing data to modify\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur400-3:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"geonameid cannot be modified\",\n   \"status\" : \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur400-4:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"wrong format (field does not exist in db)\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur404:",
          "content": "HTTP/1.1 404 Not Found\n{\n   \"message\" : \"{geonameid} does not exist in database\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Data"
  },
  {
    "type": "put",
    "url": "/data/<geonameid>",
    "title": "Ajout de données",
    "name": "put",
    "group": "Data",
    "description": "<p>Permet à un utilisateur d'ajouter un nouveau lieu dans la base de données.</p>",
    "examples": [
      {
        "title": "Exemple de requête:",
        "content": "    endpoint: http://digidata.api.localhost/data/7777777\n\nbody:\n     {\n       \"name\": \"UnNomDeLieu\",\n       \"country_code\": \"FR\",\n       ...(autres paramètres possibles)...\n     }",
        "type": "json"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "geonameid",
            "description": "<p>ID entier de l'enregistrement dans la base de données des noms géographiques.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Nom du point géographique (utf8).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "asciiname",
            "description": "<p>nom du point géographique en caractères ascii simples.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "alternatename",
            "description": "<p>noms alternatifs, séparés par des virgules, noms ascii automatiquement translittérés, attribut de commodité du tableau des noms alternatifs.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "latitude",
            "description": "<p>latitude en degrés décimaux.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "longitude",
            "description": "<p>longitude in decimal degrees.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_class",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "feature_code",
            "description": "<p>voir http://www.geonames.org/export/codes.html.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "country_code",
            "description": "<p>Code pays ISO-3166 à 2 lettres, 2 caractères.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "cc2",
            "description": "<p>autres codes pays, séparés par des virgules, code pays ISO-3166 à 2 lettres.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin1_code",
            "description": "<p>fipscode (susceptible d'être modifié en code iso), voir les exceptions ci-dessous, voir le fichier admin1Codes.txt pour les noms d'affichage de ce code.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin2_code",
            "description": "<p>code pour la deuxième division administrative, un comté aux États-Unis, voir le fichier admin2Codes.txt.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin3_code",
            "description": "<p>code for third level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "admin4_code",
            "description": "<p>code for fourth level administrative division.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "population",
            "description": "<p>bigint.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "elevation",
            "description": "<p>en mètres, nombre entier.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "dem",
            "description": "<p>modèle numérique d'élévation, srtm3 ou gtopo30, élévation moyenne de 3''x3'' (environ 90mx90m) ou 30''x30''.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "timezone",
            "description": "<p>le fuseau horaire iana id (voir le fichier timeZone.txt).</p>"
          }
        ]
      }
    },
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>(bearer) Token d'authentification d'un utilisateur.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Réponse succès:",
          "content": "HTTP/1.1 200 OK\n{\n   \"message\" : \"new data {geonameid} successfully added\",\n   \"status\" : \"succes\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-1",
            "description": "<p>Le paramètre geonameid est manquant.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-2",
            "description": "<p>Le champ name n'a pas été précisé.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400-3",
            "description": "<p>Un (ou plusieurs) des champs renseignés n'existe pas dans la BDD.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "409",
            "description": "<p>Un lieu avec ce geonameid existe déjà.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "401",
            "description": "<p>L'utilisateur essaie d'ajouter des données mais sa session n'est plus valide.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>L'utilisateur essaie d'ajouter des données sans s'être authentifié.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Erreur400-1:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"message\" : \"geonameid to create is missing\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur400-2:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"missing 'name' field of data to create\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur400-3:",
          "content": "HTTP/1.1 400 Bad Request\n{\n   \"message\" : \"wrong format (field does not exist in db)\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur409:",
          "content": "HTTP/1.1 409 CONFLICT\n{\n   \"message\" : \"{geonameid} existe déjà\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur401:",
          "content": "HTTP/1.1 401 Unauthorized\n{\n   \"message\": \"invalid token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        },
        {
          "title": "Erreur403:",
          "content": "HTTP/1.1 403 Forbidden\n{\n   \"message\": \"missing token\",\n   \"status\": \"fail\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_backend.py",
    "groupTitle": "Data"
  }
] });
