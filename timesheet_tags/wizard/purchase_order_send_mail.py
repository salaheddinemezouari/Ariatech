from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from odoo.http import request


class PurchaseOrderSend(models.TransientModel):
    _name = "send.mail.order.wizard"

    bc_id = fields.Many2one('purchase.order', 'Bon de commande', required=True)
    subject = fields.Char(string="Objet")
    message = fields.Html(string="Message", required=True)

    @api.model
    def create(self, vals):
        print("im in wizard")
        print("values => ", vals)

        record = super(PurchaseOrderSend, self).create(vals)

        # record = self.env['send.mail.order.wizard'].search([('id', '=', 2)])
        print("record =>", record)

        purchase_order = self.env['purchase.order'].search([('id', '=', vals.get('bc_id'))])
        print(purchase_order)

        web_url = request.env['ir.config_parameter'].get_param('web.base.url')
        employee = self.env['hr.employee'].search(
            [('user_id', '=', purchase_order.user_id.id)])
        recipients = employee.work_email
        subject = vals.get('subject')
        message = "<p>Un nouveau message de %s </p>" % (self.env.user.name)
        message += vals.get('message')
        message += '<br/><a class="btn-primary" href="%s/web#id=%d&model=purchase.order&view_type=form")">Cliquez ici</a>' % (
            web_url, purchase_order.id)
        emailcc=""

        users = self.env.ref('aria.group_approuver1').users
        for user in users:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', user.id)])
            print(employee)
            print(employee.name)
            emailcc += employee.work_email
            emailcc += "; "

        users = self.env.ref('aria.group_approuver2').users
        for user in users:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', user.id)])
            print(employee)
            print(employee.name)
            emailcc += employee.work_email
            emailcc += "; "

        users = self.env.ref('aria.group_approuver3').users
        for user in users:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', user.id)])
            print(employee)
            print(employee.name)
            emailcc += employee.work_email
            emailcc += "; "

        self.send_email(recipients, emailcc, subject, message)
        return record

    def send_email(self, recipients, emailcc, subject, message):
        email1="smezouari3@gmail.com; salaheddinemezouari04@gmail.com"
        email2="salaheddinemezouari04@gmail.com"
        list = [email1, email2]
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
            'email_to': recipients,
            'email_cc': emailcc
        }
        template_id = template_obj.create(template_data)
        template_obj.send(template_id)
        template_id.send()

    def send(self):
        print("sent")
