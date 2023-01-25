from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from odoo.http import request


class PurchaseOrderRefuses(models.TransientModel):
    _name = "refuse.order.wizard"

    bc_id = fields.Many2one('purchase.order', 'Bon de commande', required=True)
    reason_refusal = fields.Text(string="Motif de refus")
    state = fields.Char(string="Etat")

    @api.model
    def create(self, vals):
        print("im in wizard")
        print("values => ", vals)

        record = super(PurchaseOrderRefuses, self).create(vals)

        # record = self.env['refuse.order.wizard'].search([('id', '=', 1)])

        print(record)

        bc_validation_list = self.env['bc.validation'].search([('bc_id', '=', vals.get('bc_id'))])
        if len(bc_validation_list) == 0:
            print("length of bc validation list")
            print(len(bc_validation_list))
            raise ValidationError(
                _("Vous ne pouvez pas refuser une demande de prix qui n'a pas de fiche de validation "))
        bc_validation_list[0].state = "cancel3"

        purchase_order = self.env['purchase.order'].search([('id', '=', vals.get('bc_id'))])
        print(purchase_order)
        print(purchase_order.reason_refusal)
        vals = {"reason_refusal": vals.get('reason_refusal'),"state": 'refuse'}
        # vals = {"reason_refusal": vals.get('reason_refusal')}
        res = self.env['purchase.order'].refuse_update(purchase_order, vals)

        web_url = request.env['ir.config_parameter'].get_param('web.base.url')
        employee = self.env['hr.employee'].search(
            [('user_id', '=', purchase_order.user_id.id)])
        recipients = employee.work_email
        subject = "Approbation de la demande de prix : %s" % (purchase_order.name)
        message = "<p>Bonjour %s </p><p>Votre demande de prix %s est refusée par <b>%s</b></p><p>Cordialement.</p>" % (
            purchase_order.user_id.name, purchase_order.name, self.env.user.name)
        message += '<a class="btn-primary" href="%s/web#id=%d&model=purchase.order&view_type=form")">Cliquez ici</a>' % (
            web_url, purchase_order.id)
        self.send_email(recipients, subject, message)

        super(PurchaseOrderRefuses, record).write(vals)

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
