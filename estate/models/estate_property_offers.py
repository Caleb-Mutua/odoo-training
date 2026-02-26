from odoo import models, fields , api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name= "estate.property.offer"
    _description="Estate Property Offer"
    
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
             
            # check if anotehr offer is already accepted
            accepted_offer = property_rec.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer  and accepted_offer != offer:
                raise UserError("Another offer has already been accepted fpr this property.")
            
            #Refuse all other offers
            other_offers = property_rec.offer_ids - offer
            other_offers.write({'status':'refused'})
            
            #Accept this offer
            offer.status ='accepted'
            
            #Update the property
            property_rec.write({
                'buyer_id':offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'offer_accepted',
            })
            
    def action_refuse(self):
        for offer in self:
            if offer.state == 'accepted':
                raise UserError("You cannot refuse an accepted offer.")
            offer.state = 'refused'
            
    price =fields.Float(string="Offer Price")
    status =fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",copy=False,
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
    
    