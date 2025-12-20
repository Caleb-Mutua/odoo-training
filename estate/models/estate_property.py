from odoo import models, fields
 

 class Estateproperty(models.Model):
     _name= "estate_property"
     _description= "Real estate property"

     name = fields.Char(required=True )
     description = fields.Text()
     postcode = fields.Char()
     date_availability = fields.Date()
     expected_price = fields.Float()
     selling_price = fields.Float()
     bedrooms = fields.Integer()
     living_area = fields.Integer()
     facades = fields.Integer()
     garage = fields.Boolean()
     garden = fields.Boolean()
     garden_area = fields.Integer()
     garden_orientation = fields.Selection(
     [
        ('north','north'),
        ('south'. 'south'),
        ('east','east'),
        ('west','west'),
     ]
     )

