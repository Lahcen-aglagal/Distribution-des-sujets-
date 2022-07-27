# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class ValidateWizard(models.TransientModel):
    _name = 'validation.wizard'

    project_id = fields.Many2one('final.project', string='Selected Project',required=True)
    validate_or_send = fields.Selection([('validate','Validate'), ('validate_and_send', 'Validate and send an email to the student')],required=True)

    def set_project(self):
        for rec in self:
            student_id = self.env['student.student'].browse(self._context.get('active_id', False))

            student_id.sudo().write({'accepted_project': rec.project_id,'is_projects_validated': True})

    @api.onchange('validate_or_send')
    def limit_projects(self):
        for rec in self:
            student_id = self.env['student.student'].browse(self._context.get('active_id', False))
            projects = student_id.project_ids
            return {'domain': {'project_id': [('id', 'in', projects.ids)]}}

