from odoo import models, fields 

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="estate property type"
    _order = "sequence desc"
    
    property_ids = fields.One2many('estate.property','property_type_id',string='Properties')

    
    name=fields.Char(string='Name' , required=True)
    sequence = fields.Integer(default=10)
    
    
    

    
    