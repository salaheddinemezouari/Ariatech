{
    'name': 'Timesheet Tags',
    'version': '1.0',
    'summary': 'Timesheet Tags',
    'sequence': 1,
    'description': """
    Application to manage timesheet tags
    """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
        'base', 'hr_timesheet'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/Tags.xml',
        'views/Timesheet.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',

}
