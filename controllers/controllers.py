# -*- coding: utf-8 -*-
# from odoo import http


# class GraduationProject(http.Controller):
#     @http.route('/graduation_project/graduation_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/graduation_project/graduation_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('graduation_project.listing', {
#             'root': '/graduation_project/graduation_project',
#             'objects': http.request.env['graduation_project.graduation_project'].search([]),
#         })

#     @http.route('/graduation_project/graduation_project/objects/<model("graduation_project.graduation_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('graduation_project.object', {
#             'object': obj
#         })
