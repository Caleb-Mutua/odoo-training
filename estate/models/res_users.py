from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',  # related model
        inverse_name='salesperson_id',   # field in estate.property pointing to user
        string='My Properties',
        domain=[('state', '=', 'new')]   # only available properties
    )