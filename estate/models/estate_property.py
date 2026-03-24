from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError



class Estateproperty(models.Model):
  _name = "estate.property"
  _description = "Real estate property"
  _order = "id desc"
  _inherit = ['mail.thread', 'mail.activity.mixin'] 
  
  total_area = fields.Float(string="Total Area (m²)", compute="_compute_total_area",store=True,)
  best_price = fields.Float(string="Best Offer",compute="_compute_best_price",store=True,)

  
  @api.depends("living_area", "garden_area")
  
  def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area
        
  @api.depends("offer_ids.price")
  
  def _compute_best_price(self):
    for property in self:
      offers = property.offer_ids.mapped("price")
      property.best_price = max(offers) if offers else 0.0

  @api.onchange('garden')
  def _onchange_garden(self):
      for record in self:
          if record.garden:
             record.garden_area = 10
             record.garden_orientation ='north'
          else:
             record.garden_area = 0
             record.garden_orientation = False
      
  @api.onchange('date_availability')
  def _onchange_date_availability(self):
      for record in self:
          return{
              "warning":{
                  "title":("Past Availabity Date"),
                  "message":("The availability date is set before today.\n"
                            "This may indicate the property is already available."),
              }
          }
  def action_cancel(self):
      for record in self:
          if record.state == 'sold':
              raise UserError("A sold property cannot be canceled.")
          record.state = 'canceled'
          
  def action_sold(self):
      for record in self: 
          if record.state == 'canceled':
              raise UserError("A canceled property cannot be sold")
          if record.state != 'offer_accepted':
              raise UserError("A property can only be sold after accepting an offer.")
          record.state = 'sold'
  @api.ondelete(at_uninstall=False)
  def _check_property_state_before_delete(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("You can only delete properties that are New or Cancelled.")
          
  name = fields.Char(required=True , string='Property Name', tracking="1")
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(copy=False,default=lambda self: fields.Date.today() + relativedelta(months=3))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly= True)
  bedrooms = fields.Integer(default= 2,copy=False)
  living_area = fields.Integer(string='Living Area (sqm)')
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer(string='Garden Area (sqm)')
  garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
  active= fields.Boolean(default=True )
  state= fields.Selection([
    ('new', 'New'),
    ('offer_recieved', 'Offer Received'),
    ('offer_accepted','Offer Accepted'),
    ('sold','Sold'),
    ('canceled','Canceled')
  ],required=True,copy=False,default='new',tracking="1")
  
  property_type_id = fields.Many2one("estate.property.type",string="Property Type")
  buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
  salesperson_id = fields.Many2one("res.users",string="Salesperson",default=lambda self: self.env.user)
  offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")
  tag_ids = fields.Many2many("estate.property.tag",string="Tags")
  
