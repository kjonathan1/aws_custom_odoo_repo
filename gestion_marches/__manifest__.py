# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'gestion_marches',
    'version': '1.0',
    'category': 'sale', 
    'summary': """ Module de gestion d'informations sur les marches publics et prives.""",
    'description': """ Ce module permet de gérer les informations relatives aux marchés publics et privés. 
    Les administrateurs peuvent créer, afficher, éditer et supprimer des marchés, 
    tandis que les utilisateurs peuvent publier et visualiser des articles.""",
    'author': 'Admin',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',

         
        'views/marche_views.xml',
        'views/templates.xml',
        'views/contact.xml',
        'views/connection.xml',
        # 'views/recherche.xml',
        # 'views/contact_page_template.xml',
        # 'viesw/list_marches.xml',
        'views/menu.xml',
    ],

    
     

    'demo': [],
    'installable': True,
    'application': True,
    
    
    
    'license': 'LGPL-3',
 }
