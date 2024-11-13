# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class ClinicEtat(models.TransientModel):
    _name = "clinic.etat"
    _description = "Etats"

    debut = fields.Datetime(string="Date de début", required=True)
    fin = fields.Datetime(string="Date de fin", default=fields.Date.today, required=True)
    
    def reportbilan(self):
        data = {'debut': self.debut, 'fin': self.fin }
    #     return self.env.ref('clinic.reportshist_id').report_action(self, data=data)

    def reportevaluation(self):
        data = {'debut': self.debut, 'fin': self.fin }
        return self.env.ref('clinic.reportevaluation_id').report_action(self, data=data)
    def reportligneevaluation(self):
        data = {'debut': self.debut, 'fin': self.fin }
        return self.env.ref('clinic.reportligneevaluation_id').report_action(self, data=data)
    def reportdepenses(self):
        data = {'debut': self.debut, 'fin': self.fin }
        return self.env.ref('clinic.reportdepense_id').report_action(self, data=data)
    def reportmedecin(self):
        data = {'debut': self.debut, 'fin': self.fin }
        return self.env.ref('clinic.reportmedecin_id').report_action(self, data=data)
    def reportpararticle(self):
        data = {'debut': self.debut, 'fin': self.fin }
        return self.env.ref('clinic.reportpararticle_id').report_action(self, data=data)
    
   
class ClinicAbstractetat(models.AbstractModel):
    _name = 'report.clinic.reportevaluation_template'
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []
        mt_espece = mt_om = mt_cheque = mt_autre = 0
        montant = montantpatient = montantass = 0
        TYPE_PAYEMENT = [('espece', 'Espèce'), ('orange-money', 'Orange Money'), ('cheque', 'Chèque'), ('autre', 'Autre')]
        for rec in self.env['clinic.evaluation'].search(domain):
            val = {
                'name': rec.name,
                'date': rec.date.strftime("%m/%d/%Y"),
                'montantpatient': rec.montantpatient,
                'montantass': rec.montantass,
                'montant': rec.montant,
                'typepayement': rec.typepayement,
                'typeevaluation': rec.typeevaluation,
                
                'user': self.env['res.users'].search([('id', '=', rec.create_uid.id)])[0].name
               
            }
            
            docs.append(val)
            montantpatient += rec.montantpatient
            montantass += rec.montantass
            montant += rec.montant
            if rec.typepayement == 'espece':
                mt_espece += rec.montantpatient
            if rec.typepayement == 'orange-money':
                mt_om += rec.montantpatient
            if rec.typepayement == 'cheque':
                mt_cheque += rec.montantpatient
            if rec.typepayement == 'autre':
                mt_autre += rec.montantpatient

        return {
            'docs': docs,
            'data': data,
            'mt_espece': mt_espece,
            'mt_om': mt_om,
            'mt_cheque': mt_cheque,
            'mt_autre': mt_autre,
            'montant' : montant,
            'montantass': montantass,
            'montantpatient': montantpatient
        }

class ClinicAbtractEvaluationDetail(models.AbstractModel):
    _name = 'report.clinic.reportligneevaluation_template'
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []
        mt_espece = mt_om = mt_cheque = mt_autre = 0
        montant = montantpatient = montantass = 0

        for rec in self.env['clinic.evaluation'].search(domain):
            for record in rec.ligne_evaluation:
                val = {
                    'name': rec.name,
                    'codepatient': rec.patient.reference,
                    'date': rec.date.strftime("%m/%d/%Y"),
                    'montantpatient': rec.montantpatient,
                    'montantass': rec.montantass,
                    'montant': rec.montant,
                    'typepayement': rec.typepayement,
                    'typeevaluation': rec.typeevaluation,
                    'user': self.env['res.users'].search([('id', '=', rec.create_uid.id)])[0].name,
                    'article': record.article.name,
                    'quantite': record.qte,
                    'montantl': record.montant
                }
                
                docs.append(val)
            montantpatient += rec.montantpatient
            montantass += rec.montantass
            montant += rec.montant
            

        return {
            'docs': docs,
            'data': data,
            'montant' : montant,
            'montantass': montantass,
            'montantpatient': montantpatient
        }


class ClinicAbtractDepense(models.AbstractModel):
    _name = 'report.clinic.reportdepense_template'
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []
        montant = 0

        for rec in self.env['clinic.depense'].search(domain):
            val = {
                    'name': rec.name,
                    'date': rec.date.strftime("%m/%d/%Y"),
                    'montant': rec.montant,
                    'motif': rec.motif,
                    'banque': rec.banque.name,
                    'type': rec.type,
                    'user': self.env['res.users'].search([('id', '=', rec.create_uid.id)])[0].name,
            }
                
            docs.append(val)
            montant += rec.montant
            

        return {
            'docs': docs,
            'data': data,
            'montant' : montant,
        }

class ClinicAbtractMedecin(models.AbstractModel):
    _name = 'report.clinic.reportmedecin_template'
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []
        for rec in self.env['clinic.medecin'].search([]):
            prestations = []
            for rec1 in self.env['clinic.evaluation'].search(domain):
                for rec2 in rec1.ligne_evaluation:
                    if rec.id in rec2.medecins.ids:

                        val = {
                                'name': rec1.name,
                                'date': rec1.date.strftime("%m/%d/%Y"),
                                'montant': rec2.montant,
                                'acte': rec2.article.name,
                                'nb': len(rec2.medecins.ids),
                                'user': self.env['res.users'].search([('id', '=', rec.create_uid.id)])[0].name,
                        }
                        prestations.append(val)
                
            docs.append({
                'medecin': rec.name,
                'prestations': prestations,
            })
            

        return {
            'docs': docs,
            'data': data,
        }


class ClinicAbtractBilanParArticle(models.AbstractModel):
    _name = 'report.clinic.reportbilanpararticle_template'
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []

        for rec in self.env['product.template'].search([]):
            
            montant = 0
            for rec1 in self.env['clinic.ligneevaluation'].search(domain):
                if rec.id == rec1.article.id:
                    montant += rec1.montant

            if montant > 0: 
                val = {
                    'name': rec.name,
                    'montant': montant,
                }
                
                docs.append(val)
                
        
            

        return {
            'docs': docs,
            'data': data,
        }