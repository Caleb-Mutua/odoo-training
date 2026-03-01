from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Tags of Estate property"
    
    name=fields.Char(string="Tag Name",required=True)
    
    _sql_constraints = [
        ('estate_property_tag_name_unique','UNIQUE(name)','propert tag name must be unique.')
    ]