from odoo import models, fields 

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="estate property type"
    
    property_ids = fields.One2many('estate.property','property_type_id',string='Properties')

    
    name=fields.Char(string='Name' , required=True)
    
    
    
    

    
    