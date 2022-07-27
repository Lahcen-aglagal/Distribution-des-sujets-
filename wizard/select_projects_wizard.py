# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class SelectWizard(models.TransientModel):
    _name = 'select.wizard'

    student_id = fields.Many2one('student.student',string='Student', required=True,default=lambda self: self.env.get('active_id'))
    project_ids = fields.Many2many('final.project', string='Selected Project',required=True)

    @api.onchange('student_id')
    def restrict_projects(self):
        for rec in self:
            if rec.student_id:
                return {'domain': {'project_ids': [('department_id', '=', rec.student_id.department_id.id)]}}

    def set_projects(self):
        for rec in self:
            student_id = self.env['student.student'].browse(self._context.get('active_id', False))
            # student_id = rec.student_id
            student_id.sudo().write({'project_ids': rec.project_ids,'is_projects_selected': True})

    @api.onchange('project_ids')
    def limit_projects(self):
        for rec in self:
            length = len(rec.project_ids)
            if length > 3:
                raise ValidationError(_('You can only choose 3 projects'))