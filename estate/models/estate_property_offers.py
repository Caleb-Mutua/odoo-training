from odoo import models, fields , api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name= "estate.property.offer"
    _description="Estate Property Offer"
    _order ="price desc"
    
    validity =fields.Integer(default=7)
    
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    @api.depends("validity","create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days
                
    def action_accept(self):
        for offer in  self:
            property_rec = offer.property_id 
             
            existing = property_rec.offer_ids.filtered(lambda o: o.state == 'accepted')
            if existing:
                raise UserError("Only one offer can be accepted per property.")
            
            offer.state ='accepted'
            
            other_offers = property_rec.offer_ids.filtered(lambda o: o.id != offer.id)
            other_offers.write({'state':'refused'})
            
            property_rec.write({
                'state': 'sold',
                'selling_price': offer.price,
                'buyer_id':offer.partner_id.id,
            })
            
    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id'))

            highest_offer= max(property_id.offer_ids.mapped('price'),default=0)
            if vals.get('price') <= highest_offer:
               raise UserError("The offer must be higher than the existing highest offer.")

        offers = super().create(vals_list)
        
        for offer in offers:
            offer.property_id.state = 'offer_recieved'
        return offers
    @api.constrains('state')
    def _check_single_accepted(self):
        for offer in self:
            if offer.state == 'accepted':
               accepted = offer.property_id.offer_ids.filtered(lambda o: o.state == 'accepted')
               if len(accepted) > 1:
                  raise ValidationError("Only one accepted offer is allowed per property.")
            
    price =fields.Float(string="Offer Price")
    state =fields.Selection(
        [
            ('pending','Pending'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",copy=False,default='pending'
    )
    partner_id=fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
    )
    property_id= fields.Many2one(
        'estate.property',
        string="property",
        required=True,
        ondelete="cascade",
        
    )
    property_type_id= fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
        readonly=True,
    )
    
    