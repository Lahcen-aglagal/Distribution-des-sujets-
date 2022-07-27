# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class Department(models.Model):
    _name = 'department'

    responsible_id = fields.Many2one(
        'hr.employee', string='Gestionnaire département', required=True, )
    name = fields.Char(string='Nom du département', required=True)
    sequence = fields.Char('Sequence', readonly=True, required=True, copy=False,
                           index=True, default=lambda self: _('New'))
    type = fields.Selection([('parent', 'Parent'),('child', 'Child')], default='parent')
    parent_id = fields.Many2one('department', string='Parent')

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'department.sequence')
        res = super(Department, self).create(vals)
        return res