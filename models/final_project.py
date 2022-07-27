# -*- coding: utf-8 -*-

import datetime
from email.policy import strict
from random import randint
import string
from unicodedata import name
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class FinalProject(models.Model):
    _name = 'final.project'

    name = fields.Char('Nom du projet', required=True)
    sequence = fields.Char('Sequence', readonly=True, required=True,copy=False,
                        index=True, default=lambda self: _('New'))
    department_id = fields.Many2one('department', string="spécialité", required=True)
    description = fields.Text('Description')
    tatchment = fields.Binary('Atatchment' , attachment=True)
    file_name= fields.Char()
    color = fields.Integer('Color Index')
    your_date_field = fields.Date(string='date de depot',default=lambda self: fields.Date.today() , readonly=True)

    @api.constrains('tatchment')
    def _check_file(self):
        if str(self.file_name.split(".")[1]) != 'pdf':
            raise ValidationError("Cannot upload file different from .pdf file")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'project.sequence')
        res = super(FinalProject, self).create(vals)
        return res

class ProjectProject(models.Model):
    _inherit = 'project.project'

    department_id = fields.Many2one('department', string='Department')
