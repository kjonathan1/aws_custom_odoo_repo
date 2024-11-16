# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ClinicPotiologie(models.Model):
    _name = "clinic.potiologie"
    _description = "Dose et rythme de prise des medicaments"

    name = fields.Char(string='Potiologie', required=True)

class ClinicMaladie(models.Model):
    _name = "clinic.maladie"
    _description = "Maladies ou patologies"

    name = fields.Char(string='Patologie', required=True)
    description = fields.Char(string='Description')


class ClinicMedicament(models.Model):
    _name = "clinic.medicament"
    _description = "medicament pharmacetique"

    name = fields.Char(string='Medicament', required=True)
    description = fields.Char(string='Description')


class ClinicLigneCarnet(models.Model):
    _name = "clinic.lignecarnet"
    _description = "Carnet pour recuiller les details des patologies retrouver chez le patient"

    idevaluation = fields.Many2one('clinic.evaluation', string='Evaluation')
    idpatient = fields.Many2one('clinic.patient', string='Patient')
    maladies = fields.Many2many('clinic.maladie', string='Maladies')
    signe_physique = fields.Char(string='Signe physique')
    signe_biologique = fields.Char(string='Signe Biologique')
    temperature = fields.Float('Temperature', digits=(16,0))
    poul = fields.Float('Poul', digits=(16,0))
    pression_art = fields.Float('Pression arterielle', digits=(16,0))
    commentaire = fields.Char(string='Commentaire')
    date = fields.Datetime(string="Date", default=fields.Datetime.today, required=True)
    # inclure des variables gardant les resultats d'examens et les exament prescrit a faire


class ClinicLigneOrdonance(models.Model):
    _name = "clinic.ligneordonance"
    _description = "Ordonnance pour patient"

    idevaluation = fields.Many2one('clinic.evaluation', string='Evaluation')
    idpatient = fields.Many2one('clinic.patient', string='Patient')
    medicament = fields.Many2one('clinic.medicament', string='Medicament')
    potiologie = fields.Many2one('clinic.potiologie', string='Potiologie', required=True)
    date = fields.Date(string="Date", default=fields.Date.today, required=True)

class ClinicLigneExamen(models.Model):
    _name = "clinic.ligneexamen"
    _description = "Cette clase recense les informations sur les exament medicaux faits par le patient le patient"

    idevaluation = fields.Many2one('clinic.evaluation', string='Evaluation')
    idpatient = fields.Many2one('clinic.patient', string='Patient')
    article = fields.Many2one('product.template', string='Prescriptions Examens')
    stateexam = fields.Selection([('brouillon','En cours'), ('valide','Fait'),('annule','Annulé')], string='Etat', default='brouillon')
    statepaye = fields.Selection([('brouillon','Non Soldé'), ('valide','Soldé')], string='Paiement', default='brouillon')
    resultat = fields.Char(string='Résultat')
    date = fields.Datetime(string="Date", default=fields.Datetime.today, required=True)
    