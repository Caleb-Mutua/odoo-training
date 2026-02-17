from odoo import models, fields , api
from dateutil.relativedelta import relativedelta

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
    
    