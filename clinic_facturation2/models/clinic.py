# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ClinicDepense(models.Model):
    _name = "clinic.depense"
    _description = "Reccueil des depenses courantes"

    def valider(self):
        self.write({'state':'valide'})
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})
        
    antidate = fields.Date(string="Anti-Date", readonly=True, default=fields.Date.today)
    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    name = fields.Char(string='Code depense')
    montant = fields.Float(string='Montant', digits=(16,0))
    motif = fields.Char(string='Motif')
    commentaire = fields.Char(string='Commentaire')
    type = fields.Selection([
        ('achat_produit','Achat produits'),
        ('maintenance','Maintenance'),
        ('salaire_medecin','Salaire Medecin'),
        ('salaire_vacataire','Salaire Vacataire'),
        ('salaire_personnel','Salaire Personnel'),
        ('facture','Facture'),
        ('gazoile','Gazoile'),
        ('transfert','Transfert banque'), 
        ('divers','Divers'),
        ('autre','Autres'),
        ], 
        string='Type depense', required=True)
    banque = fields.Many2one('clinic.banque', string='Banque')
    state = fields.Selection([('brouillon','Brouillon'),('valide','Validé'),('annule','Annulé'),], 
        string='Etat', default='brouillon' ,track_visibility='onchange', readonly=True)

class ClinicRdv(models.Model):
    _name = "clinic.rdv"
    _description = "Reccueil des rendez-vous"

    def valider(self):
        self.write({'state':'valide'})
    def faire(self):
        self.write({'state':'fait'})
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})
        
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('clinic.rdv') or _('New')
        vals['name'] = sequence
        result = super(ClinicRdv, self).create(vals)
        return result
    
    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    daterdv = fields.Datetime(string="Date RDV", required=True)
    medecin = fields.Many2one('clinic.medecin', string='Médecin')
    patient = fields.Many2one('clinic.patient', string='Patient')
    motif = fields.Char(string='Motif')
    name = fields.Char(string='Code RDV')
    commentaire = fields.Char(string='Commentaire')
    state = fields.Selection([('brouillon','Brouillon'),('valide','Validé'),('fait','Fait'),('annule','Annulé'),], 
        string='Etat', default='brouillon' ,track_visibility='onchange', readonly=True)


class ClinicEvaluation(models.Model):
    _name = "clinic.evaluation"
    _description = "Evaluation = Examens et Consultations"
    TYPE_PAYEMENT = [('espece', 'Espèce'), ('orange-money', 'Orange Money'), ('cheque', 'Chèque'), ('autre', 'Autre')]
    TYPE_EVALUATION = [('consultation', 'Consultation'), ('examen', 'Examen'), ('hospitalisation', 'Hospitalisation'), ('intervention', 'Intervention')]

    def valider(self):
        self.write({'state':'valide'})
    def faire(self):
        self.write({'state':'fait'})
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})
        
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('clinic.evaluation') or _('New')
        vals['name'] = sequence
        result = super(ClinicEvaluation, self).create(vals)
        return result
    
    def preremplir(self):
        t=0

    
    @api.onchange('montantass', 'montant')  
    def get_tauxass(self):
        for rec in self:
            if rec.montant:
                if rec.montantass < 0 and rec.assurance > rec.montant:
                    raise UserError("Le Montant de l'assurance doit etre superieur a 0 et ne doit pas exceder le montant total.")
                else:
                    rec.tauxass = rec.montantass * 100 / rec.montant



    @api.depends('ligne_evaluation.article','ligne_evaluation.montant', 'ligne_evaluation.qte', 'montant', 'tauxass')            
    def get_montant(self):
        for rec in self:
            montant = montantass = 0

            for record in rec.ligne_evaluation:
                # if rec.assurance.id: 
                #     record.pu = record.article.prixass
                # else:
                #     record.pu = record.article.prix
                if record.article.name.lower() == 'acte':
                    record.qte = 1
                    record.pu = rec.ko * rec.valeur_ko * rec.coeff
                record.montant = record.pu * record.qte
                montant += record.montant
            rec.montant = montant
            
            if rec.tauxass != False:
                if rec.tauxass > 0 and rec.tauxass <= 100 :
                    rec.montantass = rec.montant * rec.tauxass / 100
                else: 
                    raise UserError("Le taux doit etre compris entre 0 et 100.")
             
            rec.montantpatient = rec.montant - rec.montantass
    
    antidate = fields.Date(string="Anti-Date", readonly=True, default=fields.Date.today)
    date = fields.Date(string="Date", required=True)
    name = fields.Char(string='Référence', readonly=True, index=True)
    montant = fields.Float(string='Montant', digits=(16,0), compute=get_montant, store=True)
    montantpatient = fields.Float('Part Patient Net', compute='get_montant', store=True,digits=(16,0))
    montantass = fields.Float('Part Assurance Net', digits=(16,0))
    tauxass = fields.Float("Part Assurance %", digits=(16,8), related='patient.tauxass', readonly=False)
    typepayement = fields.Selection(TYPE_PAYEMENT, string='Type de payement', default='espece', required=True)
    typeevaluation = fields.Selection(TYPE_EVALUATION, string='Motif', default='consultation', required=True)

    patient = fields.Many2one('clinic.patient', string='Patient', required=True)
    telephone = fields.Char(string='Téléphones', related='patient.telephone', readonly=False)
    reference = fields.Char(string='Référence', related='patient.reference')
    ndossier = fields.Char(string='N° Dossier', related='patient.ndossier')
    assurance = fields.Many2one('clinic.assurance', string='Assurance', related='patient.assurance', readonly=False)
    idassurance = fields.Integer(string='ID Assurance', related='assurance.id')
    numficheas = fields.Char('N° Fiche assurance')

    ko = fields.Float('Cas Operatoire')
    valeur_ko = fields.Float('Valeur du cas')
    coeff = fields.Float('Coeficient')
    
    stateass = fields.Selection([('brouillon','Brouillon'),('valide','Facturé'),('regler','Reglé'),('annule','Annulé')], string='Etat Facture Assurance', default='brouillon', readonly=True)
    state = fields.Selection([('brouillon','Proforma'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    ligne_evaluation = fields.One2many('clinic.ligneevaluation','idevaluation', string="Details paiements")
    ligne_carnet = fields.One2many('clinic.lignecarnet','idevaluation', string="Details consultations")
    ligne_ordonance = fields.One2many('clinic.ligneordonance','idevaluation', string="Details ordonances")
    ligne_examen = fields.One2many('clinic.ligneexamen','idevaluation', string="Details examens")
    

class ClinicLigneEvaluation(models.Model):
    _name = "clinic.ligneevaluation"
    _description = "Details sur les Examens et consultations"
   
                         
    idevaluation = fields.Many2one('clinic.evaluation', string='Evaluation')
    idpatient = fields.Many2one('clinic.patient', string='Patient', related='idevaluation.patient', store=True)
    article = fields.Many2one('product.template', string='Article', required=True)
    categoriearticle = fields.Many2one('product.category', string='categorie', related='article.categ_id', store=True)
    medecins = fields.Many2many('clinic.medecin', string='Medecins', required=True)
    qte = fields.Float('Quantité', required=True, default=1, digits=(16,0))
    pu = fields.Float('Prix unitaire', related='article.prix', readonly=False, store=True, required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)
    date = fields.Date(string="Date", related='idevaluation.date', store=True)
    state = fields.Selection([('brouillon','Proforma'), ('valide','Payé'),('annule','Annulé')], string='Etat', related='idevaluation.state', store=True )