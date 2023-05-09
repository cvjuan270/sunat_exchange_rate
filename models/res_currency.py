# -*- coding: utf-8 -*-
from odoo import models


class Currency(models.Model):
    _inherit = 'res.currency'

    def open_related_window(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sunat_exchage_rate.action_currency_rate_wizard")
        return action
