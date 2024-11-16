# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'clinic_facturation',
    'version': '1.0',
    'summary': 'GESTION DES CONSULTATIONS',
    'description': """
        GESTION DES HOPITAUX
        ====================
        Ce logiciel permet la gestion administrative, financiere et clinique des hopitaux
    """,
    'category': 'Sante',
    'website': 'https://www.esnformatic.com',
    'depends': ['stock', 'product'],
    'data': [
        'security/clinic.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/paperformat.xml',
        # 'report/reports.xml',
        # 'report/reportcaisse.xml',
        # 'report/reportcaisseduplicata.xml',
        # 'report/reportfactureass.xml',
        # 'report/etatevaluation.xml',
        # 'report/etatligneevaluation.xml',
        # 'report/etatdepense.xml',
        # 'report/etatmedecin.xml',
        # 'report/etatpararticle.xml',
        # 'report/reportordonance.xml',
        # 'report/observationmedical.xml',
        'views/clinic.xml',
        'views/params.xml',
        'views/assurance.xml',
        'views/etat.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
