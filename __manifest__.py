# -*- coding: utf-8 -*-
{
    'name': "Projet_Est",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','project'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/department.xml',
        'wizard/select_wizard.xml',
        'wizard/validate_wizard.xml',
        # 'wizard/voire_avencement.xml',
        'views/student.xml',
        'views/project.xml',
        'views/menus.xml',
        'data/sequence.xml',
        'data/mails.xml',
        'views/res_users.xml',
        'views/project_project.xml',
        'views/avencement.xml',
        # 'views/avencement_kanaban_attachment.xml',
        'views/stage.xml',
        'views/stage_home.xml',
        'views/teacher.xml',
        'views/avencement.xml',
        # 'views/Stage/kankan_test.xml'
        # 'views/Stage/Stagiaire_form.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
