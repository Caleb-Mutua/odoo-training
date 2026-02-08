from odoo import models, fields
from dateutil.relativedelta import relativedelta


class Estateproperty(models.Model):
  _name = "estate.property"
  _description = "Real estate property"

  
  
  name = fields.Char(required=True )
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(copy=False,default=lambda self: fields.Date.today() + relativedelta(months=3))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly= True)
  bedrooms = fields.Integer(default= 2,copy=False)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
  active= fields.Boolean(default=True )
  state= fields.Selection([
    ('new', 'New'),
    ('offer_recieved', 'Offer Accepted'),
    ('offer_accepted','Offer Accepted'),
    ('sold','Sold'),
    ('canceled','Canceled')
  ],required=True,copy=False,default='new')
  
  property_type_id = fields.Many2one("estate.property.type",string="Property Type")
  buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
  salesperson_id = fields.Many2one("res.users",string="Salesperson",default=lambda self: self.env.user)
  offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")
  tag_ids = fields.Many2many("estate.property.tag",string="Tags")
  
