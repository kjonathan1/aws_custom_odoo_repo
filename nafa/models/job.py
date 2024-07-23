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
    _description = "Job"

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
    description = fields.Char(string="Description")
    category = fields.Selection([('job','Job'), ('internship','Internship'),('trainig','Trainig')], string='Category', readonly=True, default='job')
    state = fields.Selection([('draft','Draft'), ('open','Open'),('close','Close')], string='Etat', readonly=True, default='draft')
       