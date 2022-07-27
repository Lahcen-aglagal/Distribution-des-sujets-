import datetime
from msilib.schema import Complus
import re
import string
from odoo import models, fields, api, exceptions
from odoo.addons.website import tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from odoo.fields import Image
from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta


class Stage(models.Model):
    _name = 'stage.stage'
    _description = 'stage.stage'
    # _rec_name = 'Stagiaires'

    nom = fields.Char("Nom de Stagiaire",required=True)
    entrepris_name = fields.Char(string="emplacement de stages")
    prenom = fields.Char("prenom de Stagiaire",required=True)
    ar_nom = fields.Char(string=':الاسم')
    ar_prenom = fields.Char(string=':النسب')
    email = fields.Char(string="E-mail" , required=True)
    filiere = fields.Selection([('Informatique', 'informatique'), ('Megatronique', 'megatronique'), ], string="spécialité",tracking=True)
    contact = fields.Char("Contact", tracking=True)
    gender = fields.Selection([('Homme', 'homme'), ('Femme', 'femme'), ], 'Sexe', required=True , default="Homme")
    date = fields.Date(string="Date de naissance" ,required=True)
    image = fields.Binary(string="Picture", required=True, attachment=True)
    phone_urgent = fields.Char("urgent numero tele")
    cin= fields.Char(string="CIN", size=15)
    CNE= fields.Char(string="CNE", String="CNE", size=30)
    age = fields.Integer(string='Age', compute='_compute_age')
    adresse_stage = fields.Char("Adresse")
    # email_id= fields.Char()
    desc_stage = fields.Text(string="description de stage")
    active = fields.Boolean("Active", default=True)
    ville=fields.Char(string="Ville")
    rue= fields.Char(String="Rue")
    date_debut = fields.Date(string="Date de debut")
    date_fin = fields.Date(string="Date de fin")

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    @api.constrains('date')
    def _check_date_birth(self):
        for record in self:
            if record.date and record.date > fields.date.today(
            ):
                raise ValidationError('the date must be less then today !!!!')


    def get_two_date_comp(self):
        date_debut = self.StartDate.strftime('%Y-%m-%d')
        date_fin = self.EndDate.strftime('%Y-%m-%d')
        if date_debut > date_fin:
            raise ValidationError("Date invalide")

    @api.depends('date')
    def _compute_age(self):
        for student in self:
            if student.date:
                student.age = ((datetime.today().date() - student.date).days) / 365
            else:
                student.age = 0

class ResUsers(models.Model):
    _inherit = 'res.users'

    student_id = fields.Many2one('student',string='Your Informations')

