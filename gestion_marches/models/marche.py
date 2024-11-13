from odoo import models, fields, api

class Marche(models.Model):
    _name = 'gestion_marches.marche'
    _description = 'Informations sur les marchés publics et privés'

    name = fields.Char(string='Nom')
    type_marche_id = fields.Many2one('gestion_marches.type_marche', string="Type_marche", required=True)
    institution_id = fields.Many2one('gestion_marches.institution', string="Institution", required=True)
    libelle = fields.Char(string="Libelle", required=True)
    object_id = fields.Many2one('gestion_marches.object', string="Object")
    description = fields.Text(string='Description')
    enveloppe_previsionnelle = fields.Float(string="Enveloppe_previsionnelle")
    devise_id = fields.Many2one('gestion_marches.devise', string="Devise")
    delais = fields.Char(string="Delais")
    contact = fields.Char(string="Contact")
    date_publication = fields.Date(string='Date_publication')
    date_expiration = fields.Date(string='Date_expiration', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Pièces', required=True)
    domaine_id = fields.Many2many('gestion_marches.domaine', string="Domaine")
    localite = fields.Char(string="Localite", required=True)
    institution_domain_id = fields.Many2one('gestion_marches.institution_domain', string="Institution_domain", required=True)
   




class Domaine(models.Model):
    _name = 'gestion_marches.domaine'
    _description = 'Informations sur les Domaines de marchés publics et privés'

    name = fields.Char(string='Domaine')

class Type_marche(models.Model):
    _name = 'gestion_marches.type_marche'
    _description = 'Informations sur les Types marches'

    name = fields.Char(string='Type_marche', required=True)

class Institution(models.Model):
    _name = 'gestion_marches.institution'
    _description = 'Informations sur les institution'

    name = fields.Char(string='Institution', required=True)
    institution_domain_id = fields.Many2one('gestion_marches.institution_domain', string="Domaine Institution")

    
class Devise(models.Model):
    _name = 'gestion_marches.devise'
    _description = 'Informations sur la devise'

    name = fields.Char(string='Devise')


class DomaineInstitution(models.Model):
    _name = 'gestion_marches.institution_domain'
    _description = 'Domaine Institution'

    name = fields.Char(string='Institution_domain', required=True)    


class Object(models.Model):
    _name = 'gestion_marches.object'
    _description = 'Informations sur les objets'

    name = fields.Char(string='Object')            



class User(models.Model):
    _name='gestion_marches.user'
    _description='Informations sur les utilisateurs'

    nom = fields.Char(String='Nom')
    prenom = fields.Char(String='Prenom')
    adresse = fields.Char(String='Adresse', required=True)
    mot_de_passe = fields.Char(String='Mot_de_passe', required=True)
