from odoo import http
from odoo.http import request

class ContactForm(http.Controller):

    @http.route('/contact', type='http', auth='public', website=True)
    def send_contact(self, **post):
        # Extraire les données du formulaire
        name = post.get('name')
        email = post.get('email')
        subject = post.get('subject')
        message = post.get('message')

        # Logique pour traiter les données ou envoyer un email
        # ...

        return request.render('gestion_marches.contact')
