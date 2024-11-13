from odoo import http
from odoo.http import request

class GestionMarchesController(http.Controller):

    @http.route(['/gestion_marches/templates'], type='http', auth="public", website=True)
    def recherche_marche(self, type_marche=None, **kwargs):
        # Rechercher les marchés par type
        domain = []
        if type_marche:
            domain = [('type_marche_id.name', 'ilike', type_marche)]
        
        marches = request.env['gestion_marches.marche'].sudo().search(domain)
        
        # Rendre la vue avec les résultats de recherche
        return request.render('gestion_marches.templates', {
            'marches': marches
        })
    

    

   

    
    # @http.route('/templates', type='http', auth='public', website=True)
    # def list_marches_public(self, **kw):
    #     # Récupérer tous les enregistrements de marchés
    #     marches = request.env['gestion_marches.marche'].sudo().search([])
    #     return request.render('gestion_marches.templates', {
    #         'marches': marches
    #     })
#  @http.route('/recherche', type='http', auth='public', website=True)
#     def list_marches_public(self, **kw):
#         # Initialiser les critères de recherche
#         domain = []
        
#         # Vérifier si le paramètre 'type' est fourni pour la recherche
#         if 'type_marche' in kw:
#             # Convertir le paramètre 'type' en minuscule pour la comparaison insensible à la casse
#             type_recherche = kw['type_marche'].strip().lower()
            
#             # Définir les types valides de marchés pour la recherche
#             valid_types = ['fournitures et services', 'prestations intellectuelles', 'travaux']
            
#             # Vérifier si le type est valide et faire la recherche correspondante
#             if type_recherche in [v.lower() for v in valid_types]:
#                 domain.append(('type_marche_id.name', '=', type_recherche))

#         # Rechercher les marchés en fonction du domaine
#         marches = request.env['gestion_marches.marche'].sudo().search(domain)
        
#         # Rendre la page avec les résultats
#         return request.render('gestion_marches.recherche', {
#             'marches': marches
#         })