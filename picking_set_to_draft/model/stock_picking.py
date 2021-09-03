from odoo import fields, models, api


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'base.set.to.draft']

    _button_draft_exist = False
