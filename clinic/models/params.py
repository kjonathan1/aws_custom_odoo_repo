# -*- coding: utf-8 -*-
from typing import Sequence
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from datetime import datetime
from odoo.tools.enlettres import convlettres


class ClinicCompany(models.Model):
    _name = "res.company"
    _description = 'Companies'
    _inherit = "res.company"

    def compute_amount_text(self,montant):
        return convlettres(montant)

    def mtlettre(self,montant):
        return convlettres(montant)
    
    user_ids = fields.Many2many('res.users', 'res_company_users_hospi', 'cid', 'user_id', string='Accepted Users')


class ClinicProduct(models.Model):
    _inherit = "product.template"

    prixass = fields.Float(string='Prix Assurance')
    prix = fields.Float(string='Prix Ordinaire')
    quantite = fields.Float(string='Quantité disponible')
    taxes_id = fields.Many2many('account.tax', 'product_hospi_taxes', 'prod_hospi_id', 'tax_id', string='Customer Taxes')
    supplier_taxes_id = fields.Many2many('account.tax', 'product_hospi_supplier_taxes', 'prod_hospi_id', 'tax_id', string='Vendor Taxes')
    route_ids = fields.Many2many('stock.location.route', 'stock_route_product_hospi', 'product_hospi_id', 'route_id', string='Routes',)
    
    

class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Patients ou malades"

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('clinic.patient') or _('New')
        vals['reference'] = sequence
        result = super(ClinicPatient, self).create(vals)
        return result

    @api.depends('datenaissance')
    def get_age(self):
        for rec in self:
            if rec.datenaissance:
                rec.age = (fields.datetime.today - rec.datenaissance).year

    @api.depends('name')
    def get_patient_data(self):
        # t=0
        for rec in self:
            for evaluation in self.env['clinic.evaluation'].search([('patient', '=', rec.id)]):
                # raise UserError(evaluaion.id)
                for detail_consult in evaluation.ligne_carnet.search([('idevaluation', '=', evaluation.id)]):
                    rec.ligne_carnet.create({
                        'idevaluation': evaluation.id,
                        'maladies': detail_consult.maladies,
                        'temperature': detail_consult.temperature,
                        'pression_art': detail_consult.pression_art,
                        'commentaire':detail_consult.commentaire,
                    })
                    # code a revoir

    # creer un fonction pour imprimer le dossier patient
    #
    # def print_patient_history(self):
    #     for rec in self:
    #         docs = []
    #         ids = []
    #         for i in rec.ligne_evaluation:
    #             ids.append(i.devaluation)
    #         new_ids = list(dict.fromkeys(ids))
    #         doc = {}
    #         for i in new_ids:
    #             val = {}
    #             for j in rec.ligne_carnet.search(['idevaluation', '=', i]):
    #                 val = {
    #                     'tenperature': j.temperature
    #                 }
    #             doc.append({
    #                 'evaluation': 
    #             }) 




    
    name = fields.Char(string='Nom et Prénom(s)')
    telephone = fields.Char(string='Téléphones')
    reference = fields.Char(string='Référence')
    ndossier = fields.Char(string='N° Dossier')
    alergie = fields.Char(string='Alergie')
    sexe = fields.Selection([('masculin','Masculin'), ('feminin','Feminin'),('autre','Autre')], string='Sexe')

    tauxass = fields.Float("Dernier Taux-Assurance %", digits=(16,0))
    assurance = fields.Many2one('clinic.assurance', string='Derniere Assurance')
    
    email = fields.Char(string='Email')
    datenaissance = fields.Date(string='Date de naissance')
    lieunaissance = fields.Char(string='Lieu de naissance')
    age = fields.Float("Age Patient", digits=(16,0))

    ligne_carnet = fields.One2many('clinic.lignecarnet', 'idpatient', string="Details consultations")
    ligne_ordonance = fields.One2many('clinic.ligneordonance', 'idpatient', string="Details ordonances")
    ligne_examen = fields.One2many('clinic.ligneexamen', 'idpatient', string="Details examens")
    ligne_evaluation = fields.One2many('clinic.ligneevaluation','idpatient', string="Motif de consultation")



class ClinicMedecin(models.Model):
    _name = "clinic.medecin"
    _description = "Médécins"

    name = fields.Char(string='Nom et Prénom(s)')
    telephone = fields.Char(string='Téléphones')
    specialite = fields.Many2one('clinic.specialitemedecin', string='Spécialité')


class ClinicSpecialiteMedecin(models.Model):
    _name = "clinic.specialitemedecin"
    _description = "Spécialite du medecin"

    name = fields.Char(string='Spésialite')


class ClinicAssurance(models.Model):
    _name = "clinic.assurance"
    _description = "Agence d'assurances"

    name = fields.Char(string='Assurance')


class ClinicBanque(models.Model):
    _name = "clinic.banque"
    _description = "banque de depot de fonds"

    name = fields.Char(string='Banque')