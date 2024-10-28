# noinspection PyUnresolvedReferences
from odoo import models, fields, api, _
import datetime
from odoo.odoo.exceptions import ValidationError


class PatientsManagement(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    # _log_access = False
    name = fields.Char(required=1, default="New", size=7)
    height = fields.Float(digits=(0, 1))
    phone_number = fields.Char()
    weight = fields.Float(digits=(0, 1))
    date_of_birth = fields.Date()
    country = fields.Char(default="Egypt", readonly=1)
    age = fields.Integer(compute='calc_age', store=1)
    temperature = fields.Float(digits=(0, 1))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])
    image = fields.Binary()
    status = fields.Selection(
        [
            ('well', 'Well'),
            ('sick', 'Sick'),
        ], default='well',compute='compute_temperature')
    doctor_id = fields.Many2one('hospital.doctors')
    name_sequence = fields.Char(string='Patient Sequence', required=True, copy=False, readonly=1,
                                index=True, default=lambda self: _('New'))

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This Name Already Exist')
    ]

    @api.depends('date_of_birth')
    def calc_age(self):
        for record in self:
            print("in calc_age")
            if record.date_of_birth:
                date_obj = fields.Date.from_string(record.date_of_birth)
                record.age = datetime.datetime.now().year - date_obj.year

    @api.constrains('height', 'weight')
    def _check_height_weight_validation(self):
        for rec in self:
            if rec.height == 0 or rec.weight == 0:
                raise ValidationError('Please Add valid Number')

    @api.onchange('height')
    def _on_change(self):
        # I use this for validation or to make anything if change happens
        for rec in self:
            if rec.height < 0:
                return {
                    'warning': {'title': 'warning', 'message': 'only positive numbers', 'type': 'notification '}
                }

    @api.depends('temperature')
    def compute_temperature(self):
        for rec in self:
            if rec.temperature < 34:
                rec.status = 'well'
            else :
                rec.status = 'sick'

    @api.model
    def create(self, vals):  #Vals is the dict
        if vals.get('name_sequence', _('New')) == _('New'):
            vals['name_sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        # this line create the record
        result = super(PatientsManagement, self).create(vals)
        return result

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        res = super(PatientsManagement, self).search(domain, offset=0, limit=None, order=None)
        print("Read")
        return res

    def write(self, vals):
        res = super(PatientsManagement, self).write(vals)
        print("Write")
        return res

    def unlink(self):
        res = super(PatientsManagement, self).unlink()
        print("Delete")
        return res

    def action_well(self):
        for rec in self:
            rec.write(
                {'status': 'well'}
            )

    def action_sick(self):
        for rec in self:
            rec.write(
                {'status': 'sick'}
            )

