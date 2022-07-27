# -*- coding: utf-8 -*-

import string
from odoo import models, fields, api,_

class Avencement(models.Model):
    _name = 'avencement.projet'

    student_id = fields.Many2one('student.student', string='Etudiant', default=lambda self: self.env.get('active_id'))
    tache = fields.Char('Nom de tâche')
    avencement_file = fields.Binary('pièce jointe')
    description_avencement =fields.Html(string="description")
    accepted_project = fields.Many2one('student.student', string='Sujet', readonly=True )
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    sequence = fields.Char('Sequence', readonly=True, required=True, copy=False,
                           index=True, default=lambda self: _('New'))
    your_date_field = fields.Date(string='date de depot', default=lambda self: fields.Date.today(), readonly=True)
    kanban_state = fields.Selection([
        ('normal', 'En cours'),
        ('done', 'Prête'),
        ('blocked', 'Annulé')], string='État',
        copy=False, default='normal', required=True)
    current_user = fields.Many2one('res.users',
                              string='Assigned to',
                              default=lambda self: self.env.uid,
                              index=True, tracking=True)
    teacher_id= fields.Many2one(related='student_id.teacher_id1', string="superviseur")
    subject_affected = fields.Many2one(related='student_id.accepted_project', string='Sujet affecté')

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'project.sequence')
        res = super(Avencement, self).create(vals)
        return res



class student(models.Model):
    _inherit = 'student.student'


class Attachment(models.Model):
    _inherit = 'ir.attachment'

