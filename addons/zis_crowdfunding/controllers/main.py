from odoo import http
from odoo.http import request

class ZISController(http.Controller):
    
    @http.route('/zis-campaigns', type='http', auth='public', website=True)
    def zis_campaigns(self, **kwargs):
        campaigns = request.env['zis.campaign'].search([('state', '=', 'open')])
        return request.render('zis_crowdfunding.zis_campaign_page', {
            'campaigns': campaigns
        })
    
    @http.route('/donasi/<int:campaign_id>', type='http', auth='public', website=True)
    def zis_donation_form(self, campaign_id, **kwargs):
        campaign = request.env['zis.campaign'].browse(campaign_id)
        if not campaign.exists() or campaign.state != 'open':
            return request.not_found()
        return request.render('zis_crowdfunding.zis_donation_form', {
            'campaign': campaign
        })
    
    @http.route('/submit-donation', type='http', auth='public', methods=['POST'], csrf=True)
    def submit_donation(self, **post):
        campaign_id = post.get('campaign_id')
        donator_name = post.get('donator_name')
        amount = post.get('amount')
        donation_type = post.get('donation_type')
        
        if campaign_id and donator_name and amount:
            donation = request.env['zis.donation'].create({
                'campaign_id': int(campaign_id),
                'donator_name': donator_name,
                'amount': float(amount),
                'donation_type': donation_type
            })
        
        return request.redirect('/zis-campaigns')