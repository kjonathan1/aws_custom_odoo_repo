# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict
from datetime import timedelta
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.tools.sql import create_index

from odoo.addons.payment import utils as payment_utils

INVOICE_STATUS = [
    ('upselling', 'Upselling Opportunity'),
    ('invoiced', 'Fully Invoiced'),
    ('to invoice', 'To Invoice'),
    ('no', 'Nothing to Invoice')
]

SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('sent', "Quotation Sent"),
    ('sale', "Sales Order"),
    ('cancel', "Cancelled"),
]



class NafaJob(models.Model):
    _name = "nafa.job"
    _description = "Job and Internship"

    def make_draft(self):
        self.write({'state':'draft'})
    def make_open(self):
        self.write({'state':'open'})
    def make_close(self):
        self.write({'state':'close'})
        

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('nafa.job') or _('New')
        vals['name'] = sequence
        result = super(NafaJob, self).create(vals)
        return result

    start_date = fields.Date(string="Openning date", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Closing date", required=True,)
    name = fields.Char(string="Reference" , readonly=True)
    position = fields.Char(string="Position")
    salary_range = fields.Char(string="Salary")
    experience = fields.Char(string="Experience")
    link = fields.Char(string="Link")
    # apply_phone_number = fields.Char(string="Apply phone number")
    user_id = fields.Char(string='User',)
    description = fields.Char(string="Description")
    category = fields.Selection([('job','Job'), ('internship','Internship'),('trainig','Trainig')], string='Category', readonly=True, default='job')
    state = fields.Selection([('draft','Draft'), ('open','Open'),('close','Close')], string='Etat', readonly=True, default='draft')
       
# use a form for user to apply instead of giving them possibility to send via whatsapp
#
class NafaEvent(models.Model):
    _name = "nafa.event"
    _description = "Event and Training"

    def make_draft(self):
        self.write({'state':'draft'})
    def make_open(self):
        self.write({'state':'open'})
    def make_close(self):
        self.write({'state':'close'})
        

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('nafa.event') or _('New')
        vals['name'] = sequence
        result = super(NafaEvent, self).create(vals)
        return result

    start_date = fields.Date(string="Openning date", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Closing date", required=True,)
    name = fields.Char(string="Reference" , readonly=True)
    link = fields.Char(string="Link")
    location = fields.Char(string="Location")
    price = fields.Float(string="Price", default=0)
    image = fields.Binary(string="Image", attachment=True)
    description = fields.Char(string="Description")
    category = fields.Selection([('event','Event'),('trainig','Trainig')], string='Category', readonly=True, default='event')
    state = fields.Selection([('draft','Draft'), ('open','Open'),('close','Close')], string='Etat', readonly=True, default='draft')



class NafaContract(models.Model):
    _name = "nafa.contract"
    _description = "Public / Private contracts"

    def make_draft(self):
        self.write({'state':'draft'})
    def make_open(self):
        self.write({'state':'open'})
    def make_close(self):
        self.write({'state':'close'})
        

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('nafa.contract') or _('New')
        vals['name'] = sequence
        result = super(NafaContract, self).create(vals)
        return result

    start_date = fields.Date(string="Openning date", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Closing date", required=True,)
    name = fields.Char(string="Reference" , readonly=True)
    link = fields.Char(string="Link")
    description = fields.Char(string="Description")
    pdf_document = fields.Binary(string="PDF Document", attachment=True)  # New PDF field
    pdf_document_filename = fields.Char(string="PDF Filename")  # New field to store the filename
    category = fields.Selection([('public','Public'),('private','Private')], string='Category', readonly=True, default='public')
    state = fields.Selection([('draft','Draft'), ('open','Open'),('close','Close')], string='Etat', readonly=True, default='draft')


class NafaJobFavorite(models.Model):
    _name = 'nafa.jobfavorite'
    _description = 'Job Favorites'

    user_id = fields.Char(string='User',)
    job_id = fields.Many2one('nafa.job', string='Job', required=True)
    active = fields.Boolean(default=True)


class NafaJobApplication(models.Model):
    _name = 'nafa.jobapplication'
    _description = 'Job Application'

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('nafa.jobapplication') or _('New')
        vals['name'] = sequence
        result = super(NafaJobApplication, self).create(vals)
        return result

    name = fields.Char(string="Reference" , readonly=True)
    user_id = fields.Char(string='User',)
    job_id = fields.Many2one('nafa.job', string='Job', required=True)
    active = fields.Boolean(default=True)
    application_date = fields.Date(string="Application date", )
    applicant_phone_number = fields.Char(string="Applicant phone number")
    applicant_email = fields.Char(string="Applicant email")
    applicant_message = fields.Char(string='Applicant Resume',)
    pdf_document = fields.Binary(string="PDF Document", attachment=True)  # New PDF field
    pdf_document_filename = fields.Char(string="PDF Filename")  # New field to store the filename