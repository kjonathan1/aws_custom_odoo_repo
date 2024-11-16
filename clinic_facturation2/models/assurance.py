# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

class ClinicAssurance(models.Model):
    _name = "clinic.assurance"
    _description = "Assurance"
        
    name = fields.Char('Société Assurance', required=True)
    adresse = fields.Char('Adresse')
    phone = fields.Char('Téléphone')
    ifu = fields.Char('IFU')
    rccm = fields.Char('RCCM')
    regime = fields.Char('Régime fiscal')
    division = fields.Char('Division fiscale')

class ClinicFactureAss(models.Model):
    _name = "clinic.factureass"
    _description = "Fcturation des assurance"
    TYPE_EVALUATION = [('consultation', 'Consultation'), ('examen', 'Examen'), ('hospitalisation', 'Hospitalisation'), ('intervention', 'Intervention')]
   
    
    def faire(self):
        self.write({'state':'fait'})
    
    def brouillon(self):
        for rec in self:
            for record in rec.ligne_factureass:
                for evaluation in self.env['clinic.evaluation'].search([('id', '=', record.evaluation.id)]):
                    evaluation.stateass = 'brouillon'
                record.unlink()

            # mouvelines = self.env['clinic.lignefactureass'].search([('idfactureass', '=', rec.id)])
            # mouvelines.unlink()
            rec.write({'state':'brouillon'})
    
    def annuler(self):
        self.write({'state':'annule'})
        
    @api.depends('ligne_factureass.montantass', 'ligne_factureasspaie.montant')
    def get_montant(self):
        for rec in self:
            for record in rec.ligne_factureass:
                rec.montantth += record.montantass
            for record in rec.ligne_factureasspaie:
                rec.montantnet = record.montant

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('clinic.factureass') or _('New')
        vals['name'] = sequence
        result = super(ClinicFactureAss, self).create(vals)
        return result

    def preparer_facture(self):
        for rec in self:
            if rec.typeevaluation:
                domain = [('state', '=', 'valide'), ('stateass', '=', 'brouillon'), ('date', '>=', rec.debut),('date', '<=', rec.fin),('assurance', '=', rec.assurance.id),('typeevaluation', '=', rec.typeevaluation)]
            else:
                domain = [('state', '=', 'valide'), ('stateass', '=', 'brouillon'), ('date', '>=', rec.debut),('date', '<=', rec.fin),('assurance', '=', rec.assurance.id)]
            
            montantass = 0
            for record in self.env['clinic.evaluation'].search(domain):
                montantass += record.montantass
                prestations = ''
                for record2 in record.ligne_evaluation:
                    prestations += str(record2.article.name) + ', '
                val = {
                    'idfactureass': rec.id,
                    # 'idevaluation': record.id,
                    'evaluation': record.id,
                    'patient': record.patient.id,
                    'telephone': record.patient.telephone,
                    'reference': record.patient.reference,
                    'numficheas': record.numficheas,
                    'prestation': prestations,
                    'montant': record.montant,
                    'montantass': record.montantass,
                    'tauxass': record.tauxass
                }
                rec.ligne_factureass.create(val)
                record.stateass = 'valide'
            rec.montantth = montantass
            rec.state = 'valide'


    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string='Code Fact. assurance', readonly=True, index=True)
    assurance = fields.Many2one('clinic.assurance', string='Assurance', required=True)
    typeevaluation = fields.Selection(TYPE_EVALUATION, string='Motif', required=True)
    debut = fields.Datetime(string="Date début", required=True)
    fin = fields.Datetime(string="Date fin", default=fields.Date.today, required=True)

    montantth = fields.Float(string='Montant théorique', )
    montantnet = fields.Float(string='Montant Payé', )
    commentaire = fields.Char(string='Commentaire')
    
    state = fields.Selection([('brouillon','Proforma'), ('valide','Facturé'),('paye','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    ligne_factureass = fields.One2many('clinic.lignefactureass','idfactureass', string="Details Facture Assurance")
    ligne_factureasspaie = fields.One2many('clinic.lignefactureasspaiement','idfactureass', string="Details Paiements Factures Assurance")
    

class ClinicLigneFactureAss(models.Model):
    _name = "clinic.lignefactureass"
    _description = "Details sur les Factures d'assurance"
                         
    idfactureass = fields.Many2one('clinic.factureass', string='ID Factureass')
    evaluation = fields.Many2one('clinic.evaluation', string='Evaluation')
    patient = fields.Many2one('clinic.patient', string='Patient')
    telephone = fields.Char(string='Téléphones', )
    reference = fields.Char(string='Code Patient')
    numficheas = fields.Char(string='N° Fiche assurance')
    prestation = fields.Char(string='Prestation')
    montant = fields.Float('Montant', store=True)
    montantass = fields.Float('Montant Assurance', store=True)
    tauxass = fields.Float('Taux assurance %', store=True)

class ClinicFactureAssPaiement(models.Model):
    _name = "clinic.factureasspaiement"
    _description = "Details sur les paiements des Factures d'assurance"
                         
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('clinic.factureasspaiement') or _('New')
        vals['name'] = sequence
        result = super(ClinicFactureAssPaiement, self).create(vals)
        return result

    def valider(self):
        for rec in self:
            for record in rec.factures:
                for rec3 in record.ligne_factureass:
                    for rec4 in self.env['clinic.evaluation'].search([('id', '=', rec3.evaluation.id)]):
                        rec4.stateass = 'regler'
                record.state = 'paye'
            rec.state='valide'
        
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.depends('factures')
    def get_montantth(self):
        for rec in self:
            montantth = 0
            cpt = 0
            for record in rec.factures:
                if cpt == 0:
                    montantth +=  record.montantth
                    rec.assurance = record.assurance.id
                if cpt > 0:
                    if rec.assurance.id == record.assurance.id:
                        montantth +=  record.montantth
                    else:
                        raise UserError('Veuillez choisir des factures de la meme assurance.')
                cpt+=1
            rec.montantth = montantth
            
    
    name = fields.Char(string='Code Paiement', readonly=True, index=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    factures = fields.Many2many('clinic.factureass', string='Factures', required=True, domain=[('state', '=', 'valide')])
    montantth = fields.Float(string='Montant theorique', compute=get_montantth, store=True)
    montantnet = fields.Float(string='Montant net')
    assurance = fields.Many2one('clinic.assurance', string='Assurance')
    banque = fields.Many2one('clinic.banque', string='Banque', required=True)
    reference = fields.Char(string='Reference de paiement') #ex: N° cheque
    commentaire = fields.Char(string='Commentaure') 
    state = fields.Selection([('brouillon','Brouillon'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')

class ClinicLigneFactureAssPaiement(models.Model):
    _name = "clinic.lignefactureasspaiement"
    _description = "Details sur les paiements des Factures d'assurance"
                         
    idfactureass = fields.Many2one('clinic.factureass', string='ID Factureass')
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    montant = fields.Float(string='Montant')
    reference = fields.Char(string='Reference') #ex: N° cheque

