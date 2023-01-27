from odoo import api, fields, models, _, exceptions

class TimeSheet(models.Model):
    _inherit = "account.analytic.line"

    category_id = fields.Many2many('timesheet.tags', string='Tags')





