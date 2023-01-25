{
    'name': 'Timesheet Tags',
    'version': '1.0',
    'summary': 'Timesheet Tags',
    'sequence': 1,
    'description': """
    Application to manage the some of purchase and sales
    """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
        'hr',
        'base',
        'resource',
        'purchase',
        'purchase_requisition',
        'product',
        'report_xlsx',
        'survey',
        'account'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/Tags.xml',
        'views/Timesheet.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}
