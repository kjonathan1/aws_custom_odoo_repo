# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'nafa',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Backend sercice',
    'description': """
        Backend sercice
    """,
    'depends': [
        'base',
        'portal',
        'utm',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        # 'security/res_groups.xml',
        # 'security/ir_rules.xml',

        # 'report/account_invoice_report_views.xml',

        # 'data/ir_cron.xml',
        'data/ir_sequence_data.xml',

        # Define views before their references
        'views/job.xml',

        'views/menu.xml',  # Last because referencing actions defined in previous files
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
