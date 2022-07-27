# -*- coding: utf-8 -*-
import re
import string
from odoo import models, fields, api,_
from datetime import datetime

from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    graduation_dep_id = fields.Many2one('department')


class StudentStudent(models.Model):
    _name = 'student.student'


    name = fields.Char(String='Full Name', compute='_compute_full_name')
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    date_of_birth = fields.Date(string="Date of Birth", requird=True)
    image = fields.Binary('Image')
    father_name = fields.Char(string="Father")
    mother_name = fields.Char(string="Mother")
    department_id = fields.Many2one('department', string="Department", required=True)
    teacher_id1 = fields.Many2one('teacher', string="Supervisor", required=True)
    ad_no = fields.Char(string="Identity Number", required=True)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ],
                              string='Gender', required=True, default='male',
                              track_visibility='onchange')
    per_street = fields.Char(string='Street1')
    per_street2 = fields.Char(string='Street2')
    per_zip = fields.Char(change_default=True)
    per_city = fields.Char(string='City')
    per_state_id = fields.Many2one("res.country.state", string='State',
                                   ondelete='restrict')
    per_country_id = fields.Many2one('res.country', string='Country',
                                     ondelete='restrict')
    nationality = fields.Many2one('res.country', string='Nationality',
                                  ondelete='restrict')
    phone_number = fields.Char(string='Phone Number')
    email = fields.Char(string='Email', required=True)
    age = fields.Integer(string='Age', compute='_compute_age')
    is_projects_selected = fields.Boolean(string='IS selected')
    is_projects_validated = fields.Boolean(string='Is Validated')
    project_ids = fields.Many2many('final.project', string='Projects Selected',readonly=True)
    related_user_id = fields.Many2one('res.users')
    accepted_project = fields.Many2one('final.project', string='Accepted Project', readonly=True)
    state = fields.Selection([
        ("à l'attend de validation","à l'attend de validation"),
        ('En cours', 'En cours'),
        ('Projet Valide', 'Projet Valide')],
        string='State',
        default="à l'attend de validation",
        compute="_change_state",
        readonly="1"
    )
    login_date = fields.Datetime(related='log_ids.create_date', string='Latest authentication', readonly=False)
    log_ids = fields.One2many('res.users.log', 'create_uid', string='User log entries')

    _sql_constraints = [
        ('ad_no', 'unique(ad_no)',
         "Another Student already exists with this Identity number!")
    ]

    def validate_email(email):
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@usms\.ac\.ma$', email)
        if match == None:
            return False
        return True

    @api.depends('is_projects_selected')
    def _change_state(self):
        for record in self:
            if record.is_projects_validated:
                record.state="Projet Valide"
            elif record.is_projects_selected:
                record.state="à l'attend de validation"
            else:
                record.state="En cours"

    def action_view_menu(self):
        action = self.env.ref('graduation_project.final_project_action')
        result = action.read()[0]
        return result

    @api.depends('first_name','last_name')
    def _compute_full_name(self):
        for rec in self:
            name = ' '
            if rec.first_name and rec.last_name:
                name += rec.first_name + ' ' + rec.last_name

            rec.name = name

    @api.onchange('per_country_id')
    def _restrict_state(self):
        for student in self:
            if student.per_country_id:
                return {'domain': {'per_state_id': [('country_id', '=', student.per_country_id.id)]}}

    @api.depends('date_of_birth')
    def _compute_age(self):
        for student in self:
            if student.date_of_birth:
                student.age = ((datetime.today().date() - student.date_of_birth).days) / 365
            else:
                student.age = 0

    def create_related_user(self):
        # user_group = self.env.ref("graduation_project.group_student") or False
        tab = []
        tab.append(self.env.ref('graduation_project.group_student').id)
        tab.append(self.env.ref('base.group_user').id)
        user_group = self.env['res.groups'].search([('id', 'in', tab)])
        users_res = self.env['res.users']
        for record in self:
            if not record.related_user_id:
                user_id = users_res.create({
                    'name': record.first_name,
                    'login': record.email,
                    'student_id': record.id,
                    'groups_id': user_group,
                    'email': record.email,
                    'graduatio_department_id': record.department_id.id,
                    'password': str(record.first_name) + 'odoo',
                    'tz': self._context.get('tz'),
                })
                record.related_user_id = user_id.id
    @api.onchange('department_id')
    def _restrict_state(self):
        for student in self:
            if student.department_id:
                return {'domain': {'project_ids': [('department_id', '=', student.department_id.id)]}}
class ResUsers(models.Model):
    _inherit = 'res.users'

    graduatio_department_id = fields.Many2one('department', string='Department')
    student_id = fields.Many2one('student.student', string='Student')


