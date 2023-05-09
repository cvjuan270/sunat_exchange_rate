import json
from datetime import timedelta

import requests

from odoo import models, fields, api


class CurrencyRateWizard(models.TransientModel):
    _name = 'currency.rate.wizard'
    _description = 'SUNAT Currency rate wizard'
    _check_company_auto = True

    date_from = fields.Date('Fecha desde', required=True)
    date_to = fields.Date('Fecha hasta', required=True)

    @api.model
    def _get_sunat_currency_rate(self, date):
        if date:
            try:
                url = 'https://api.apis.net.pe/v1/tipo-cambio-sunat?fecha={}'.format(date.strftime('%Y-%m-%d'))
                response = requests.request("GET", url)
                if response.status_code == 200:
                    return json.loads(response.text)
                else:
                    print(f'Error: {response.status_code}', response.text)
                    return False
            except Exception as e:
                print(f'Error: ', e)
        return False

    def set_currency_rate(self):
        for rec in self:
            # Currency
            _currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            _currency_rates = self.env['res.currency.rate'].search([('currency_id', '=', _currency.id)])
            lst_dates = []
            lst_dates.append(rec.date_from)
            num_days = (rec.date_to - rec.date_from).days
            if num_days > 1:
                for i in range(1, num_days + 1):
                    lst_dates.append(rec.date_from + timedelta(days=i))
            for date in lst_dates:
                if _currency_rates.filtered(lambda r: r.name != date):
                    sunat_currency_rate = self._get_sunat_currency_rate(date)
                    if sunat_currency_rate:
                        currency_rate = self.env['res.currency.rate']
                        currency_rate.create(
                            {'currency_id': _currency.id,
                             'inverse_company_rate': sunat_currency_rate['venta'],
                             'name': date, })

    def set_currency_rate_cron(self):
        date = fields.Date.context_today(self)
        _currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        sunat_currency_rate = self._get_sunat_currency_rate(date)
        if sunat_currency_rate:
            self.env['res.currency.rate'].create(
                {'currency_id': _currency.id,
                 'name': date,
                 'inverse_company_rate': sunat_currency_rate['venta']
                 })
