# noinspection PyUnresolvedReferences
from odoo import models, fields, api
import datetime


class DoctorsManagement(models.Model):
    _name = 'hospital.doctors'
    _inherit = ['mail.thread', 'mail.activity.mixin', "hospital.patient"]  #_inherit is attribute and in _inherit tables
    _description = 'Doctors Record'
    name = fields.Char(string="Name")
    phone_number = fields.Char()
    date_of_birth = fields.Date()
    country = fields.Char()
    age = fields.Integer(compute='calc_age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])
    patients_ids = fields.One2many('hospital.patient', 'doctor_id', readonly=1)

    @api.depends('date_of_birth')
    def calc_age(self):
        result = super(DoctorsManagement, self).calc_age()
        return result
