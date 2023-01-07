# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.tools import html2plaintext

COMMAND_AI = '/ai'

class MailChannel(models.Model):
    _inherit = 'mail.channel'


    def execute_command_ai(self, **kwargs):
        msg = _('Oops! Something went wrong!')

        partner = self.env.user.partner_id
        body = kwargs.get('body', '').strip()

        try:
        if not body or body == COMMAND_AI or not body.startswith(COMMAND_AI):
            msg = _('Ask something to the AI by simply typing "/ai "followed by the prompt. For example "/ai What is Odoo?"')
        else:
            msg = self._execute_command_ai(
                partner=partner,
                prompt=html2plaintext(body[len(COMMAND_AI):]).strip()
            )
        except:
            msg = _('Oops! Something went wrong!')

        # Send message with SuperUser (OdooBot)
        odoobot_id = self.env['ir.model.data']._xmlid_to_res_id("base.partner_root")
        self.with_context(mail_create_nosubscribe=True).sudo().message_post(
            body=msg,
            author_id=odoobot_id,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )


    def _execute_command_ai(self, partner, prompt):
        response = self.env['odoogpt.openai.utils'].completition_create(
            prompt=_('In Odoo: {0}').format(prompt)
        )

        return _("""{0} asked <i>\"{1}\"</i> <br /> {2}""").format(
            self._ping_partners(partner),
            prompt,
            response
        )



    # UTILS

    def _ping_partners(self, partners):
        return '&nbsp;'.join("""<a href=\"{0}#model=res.partner&amp;id={1}\" class=\"o_mail_redirect\" data-oe-id=\"{1}\" data-oe-model=\"res.partner\" target=\"_blank\">@{2}</a>""".format(
            partner.get_base_url(), partner.id, partner.name
        ) for partner in partners)