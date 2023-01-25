from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from odoo.http import request


class PurchaseRequisitionRefuses(models.TransientModel):
    _name = "refuse.requisition.wizard"

    ps_id = fields.Many2one('purchase.requisition', "Demande d'acaht", required=True)
    reason_refusal = fields.Text(string="Motif de refus")
    state = fields.Char(string="Etat")

    @api.model
    def create(self, vals):
        print("im in wizard")
        print("values => ", vals)

        record = super(PurchaseRequisitionRefuses, self).create(vals)

        # record = self.env['refuse.requisition.wizard'].search([('id', '=', 1)])

        print(record)

        purchase_requisition = self.env['purchase.requisition'].search([('id', '=', vals.get('ps_id'))])
        print(purchase_requisition)
        print(purchase_requisition.reason_refusal)
        vals = {"reason_refusal": vals.get('reason_refusal'),"state": 'refuse'}
        # vals = {"reason_refusal": vals.get('reason_refusal')}
        res = self.env['purchase.requisition'].refuse_update(purchase_requisition, vals)

        web_url = request.env['ir.config_parameter'].get_param('web.base.url')
        employee = self.env['hr.employee'].search(
            [('user_id', '=', purchase_requisition.user_id.id)])
        recipients = employee.work_email
        subject = "Approbation de la demande d'achat : %s" % (purchase_requisition.name)
        message = "<p>Bonjour %s</p><p>Votre demande d'achat %s est refusée par <b>%s</b></p><p>Cordialement.</p>" % (
            purchase_requisition.user_id.name, purchase_requisition.name, self.env.user.name)
        message += '<a class="btn-primary" href="%s/web#id=%d&model=purchase.order&view_type=form")">Cliquez ici</a>' % (
            web_url, purchase_requisition.id)
        self.send_email(recipients, subject, message)

        super(PurchaseRequisitionRefuses, record).write(vals)

        return record

    def send_email(self, recipients, subject, message):
        print("i'm in send mail")
        subject = subject
        recipients = recipients
        base_url = message

        message_body = base_url
        template_obj = self.env['mail.mail']
        template_data = {
            'subject': subject,
            'body_html': message_body,
            'email_from': 'p2p@ariagroup.io',
            'email_to': recipients
        }
        template_id = template_obj.create(template_data)
        template_obj.send(template_id)
        template_id.send()

    def refuse(self):
        print(self.reason_refusal)
