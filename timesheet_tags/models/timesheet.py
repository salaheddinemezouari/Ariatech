import inspect
from pprint import pprint

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import AccessError, UserError, ValidationError


from datetime import date
from odoo.http import request


class TimeSheet(models.Model):
    _inherit = "account.analytic.line"


    category_id = fields.Many2many('timesheet.tags', string='Tags')

    # analytique = fields.Many2many('analytique.affectation', string='Affectation Analytique', tracking=True, required=True)





