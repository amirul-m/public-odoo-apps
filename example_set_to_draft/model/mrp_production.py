from odoo import fields, models, api


class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'base.set.to.draft']

