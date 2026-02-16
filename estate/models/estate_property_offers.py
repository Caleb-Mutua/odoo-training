from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name= "estate.property.offer"
    _description="Estate Property Offer"
    
    price= fields.Float(string="Offer Price")
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
    
    