{
    'name': 'ZIS Crowdfunding',
    'version': '1.0',
    'category': 'Crowdfunding',
    'summary': 'Platform ZIS (Zakat, Infak, Shodaqoh)',
    'depends': ['base', 'web', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/zis_menu.xml',
        'views/zis_campaign_views.xml',
        'views/zis_donation_views.xml',
        'views/zis_distribution_views.xml',
        'views/zis_category_views.xml',
        'views/zis_website_templates.xml',
    ],
    'installable': True,
    'application': True,
}