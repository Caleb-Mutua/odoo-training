from odoo import models,api, fields 

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="estate property type"
    _order = "sequence, name"
    
    property_ids = fields.One2many('estate.property','property_type_id',string='Properties')
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string="offers" )
    property_count=fields.Integer(compute="_compute_property_count")
    
    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)
            
    def action_open_property_ids(self):
        self.ensure_one()
        return{
            "name":("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode":"list,form",
            "res_model":"estate.property",
            "target":"current",
            "domain":[("property_type_id","=",self.id)],
            "context":{"default_property_type_id":self.id}
        }
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
    name=fields.Char(string='Name' , required=True)
    sequence = fields.Integer(default=10)
    offer_count=fields.Integer(compute="_compute_offer_count")
    
    
    

    
    