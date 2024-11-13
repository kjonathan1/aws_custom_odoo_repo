from odoo import http
from odoo.http import request


class ConnectionController(http.Controller):
    @http.route('/connection', type='http', auth='public', website=True)
    def connection_page(self, **kwargs):
        return http.request.render('gestion_marches.connection')
