# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Teacher(models.Model):
    _name = 'teacher'
    _description = 'Teacher Information'


    _inherit = 'person'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee ID',
        ondelete='cascade',
        #   required=True,
        help="Enter related employee")
    dept_id = fields.Many2one('hr.department',
                              string="Department ID",
                              help="Select the related Department")
    department_id = fields.Many2one('department', string="Department", required=True)
    # job = fields.Many2one(comodel_name='hr.job',string='Job',related='employee_id.job_id',readonly=True)
    job_id = fields.Many2one('hr.job',
                             'Job position',
                             ondelete='cascade',
                             help="Select your job")
    # job_title = fields.Char(string='Job Title')
    student_id = fields.Many2one('res.users')
    certificate_level = fields.Selection(string='Certificate Level',
                                         selection=[('lisence', 'Lisence'),
                                                    ('master', 'Master'),
                                                    ('doctorat', 'Doctorat')],
                                         required=True)
    # student_ids = fields.One2many('student', 'teacher_id', string="Student_id")
    hr_icon_display = fields.Selection(string='Hr Icon Display',
                                       selection=[
                                                ('presence_present','Present'),
                                                ('presence_absent_active','Present but not active'),
                                                ('presence_absent','Absent'),
                                                ('presence_to_define','To define'),
                                                ('presence_undetermined','Undetermined')
                                           ],
                                       related='employee_id.hr_icon_display',
                                       readonly=True)

    @api.model_create_multi
    def create(self, vals):
        vals[0]['name'] = '{} {}'.format(vals[0].get('nom'),
                                         vals[0].get('prenom'))
        vals[0]['display_name'] = '{} {}'.format(vals[0].get('nom'),
                                                 vals[0].get('prenom'))
        ts = super(Teacher, self).create(vals)
        return ts

    def write(self, vals):
        vals['name'] = '{} {}'.format(self.nom, self.prenom)
        vals['display_name'] = '{} {}'.format(self.nom, self.prenom)
        res = super().write(vals)
        self.employee_id.name = '{} {}'.format(self.nom, self.prenom)
        if self.image_1920:
            self.employee_id.image_1920 = self.image_1920
        self.user_id.name = '{} {}'.format(self.nom, self.prenom)
        if self.email:
            self.user_id.login = self.email
        return res

    def create_teacher_user(self):
        tab = []
        tab.append(self.env.ref('graduation_project.group_professor').id)
        tab.append(self.env.ref('base.group_user').id)
        user_group = self.env['res.groups'].search([('id', 'in', tab)])
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'graduatio_department_id': record.department_id.id,
                    'password': 'estbmprofessor',
                    'tz': self._context.get('tz'),
                    'teacher_id':record.id, 
                })
                record.user_id = user_id

    def create_employee(self):
        self.ensure_one()
        emp_id = self.env['hr.employee'].create(dict(
            name=self.name,
            company_id=self.env.company.id,
            **self.env['hr.employee']._sync_user(self.user_id)
        ))
        self.write({'employee_id': emp_id.id})
        self.partner_id.write({'partner_share': True, 'employee': True})

class ResUsers(models.Model):
    _inherit = 'res.users'

    graduatio_department_id = fields.Many2one('department', string='Department')
    teacher_id1 = fields.Many2one('teacher')