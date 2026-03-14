from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Tags of Estate property"
    
    name=fields.Char(string="Tag Name",required=True)
    color = fields.Integer(string="color")
    