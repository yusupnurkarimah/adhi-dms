# -*- coding: utf-8 -*-
from odoo import http
import simplejson

class VitDmsWeb(http.Controller):

    @http.route('/vit_dms_web/index', auth='public',website=True)
    def index(self, **kw):
        return http.request.render('vit_dms_web.index', {
        })


    @http.route('/vit_dms_web/files', auth='public')
    def files(self, **kw):
        files = http.request.env['muk_dms.file'].search_read([])
        return simplejson.dumps(files)

    @http.route('/vit_dms_web/directories', auth='public')
    def directories(self, **kw):
        # print kw

        ######### get directories
        if 'id' in kw:
            directory_id = int(kw['id']) - 1000
            print directory_id
            domain=[('parent_directory','=', directory_id)]
            files = http.request.env['muk_dms.file'].search_read([('directory', '=', directory_id)])
        else:
            domain = [('is_root_directory','=', True)]
            files = []
            directory_id=False
        directories = http.request.env['muk_dms.directory'].search_read(domain)


        #### prepare final files combined directoris and files
        data=[]
        for dir in directories:
            data.append({
                'id': dir['id'] + 1000,
                'name': dir['name'],
                'state': 'closed',
                'parentId': str(directory_id),
                'type': 'directory'
            })
        for file in files:
            data.append({
                'id': str(file['id']),
                'name': file['name'],
                'state': 'open',
                'parentId': str(directory_id),
                'type': 'file',
            })

        return simplejson.dumps(data)

    ##### review API
    @http.route('/vit_dms_web/reviews/read/<int:file_id>', auth='public', csrf=False)
    def review_read(self, file_id, **kw):
        reviews=[]
        domain=[('file_id','=', file_id)]
        reviews = http.request.env['muk_dms.review'].search_read(domain)
        return simplejson.dumps(reviews)

    @http.route('/vit_dms_web/reviews/create/<int:file_id>', auth='public', csrf=False)
    def review_create(self, file_id, **kw):
        print kw
        isNewRecord = kw.get('isNewRecord')
        ulas = kw.get('ulas')
        name = kw.get('name')
        tanggal_jam = kw.get('tanggal_jam')
        redaksi_asal = kw.get('redaksi_asal')

        data = {
            'file_id':file_id,
            'ulas': ulas,
            'name': name,
            'tanggal_jam': tanggal_jam,
            'redaksi_asal': redaksi_asal
        }
        new_id = http.request.env['muk_dms.review'].create(data)
        data.update({'id': new_id.id})
        return simplejson.dumps(data)

    @http.route('/vit_dms_web/reviews/update/<int:file_id>', auth='public', csrf=False)
    def review_update(self, file_id, **kw):
        print kw
        isNewRecord = kw.get('isNewRecord')
        ulas = kw.get('ulas')
        name = kw.get('name')
        tanggal_jam = kw.get('tanggal_jam')
        redaksi_asal = kw.get('redaksi_asal')
        id = kw.get('id')

        data = {
            'ulas': ulas,
            'name': name,
            'tanggal_jam': tanggal_jam,
            'redaksi_asal': redaksi_asal
        }
        updated_id = http.request.env['muk_dms.review'].browse(int(id)).write(data)
        data.update({'id':updated_id})
        return simplejson.dumps(data)

    @http.route('/vit_dms_web/reviews/delete/<int:file_id>', auth='public', csrf=False)
    def review_delete(self, **kw):
        print kw
        id = kw.get('id')
        http.request.env['muk_dms.review'].browse(int(id)).unlink()
        return simplejson.dumps({'success': True})

    ##### info API ###########
    @http.route('/vit_dms_web/infos/read/<int:file_id>', auth='public', csrf=False)
    def info_read(self, file_id, **kw):
        infos=[]
        domain=[('file_id','=', file_id)]
        infos = http.request.env['muk_dms.info'].search_read(domain)
        return simplejson.dumps(infos)

    @http.route('/vit_dms_web/infos/create/<int:file_id>', auth='public', csrf=False)
    def info_create(self, file_id, **kw):
        print kw
        isNewRecord = kw.get('isNewRecord')
        name = kw.get('name')
        tanggal_naskah = kw.get('tanggal_naskah')
        partner = kw.get('partner')
        deskripsi = kw.get('deskripsi')

        data = {
            'file_id':file_id,
            'tanggal_naskah': tanggal_naskah,
            'name': name,
            'partner': partner,
            'deskripsi': deskripsi
        }
        new_id = http.request.env['muk_dms.info'].create(data)
        data.update({'id': new_id.id})
        return simplejson.dumps(data)

    @http.route('/vit_dms_web/infos/update/<int:file_id>', auth='public', csrf=False)
    def info_update(self, file_id, **kw):
        print kw
        isNewRecord = kw.get('isNewRecord')
        name = kw.get('name')
        tanggal_naskah = kw.get('tanggal_naskah')
        partner = kw.get('partner')
        deskripsi = kw.get('deskripsi')
        id = kw.get('id')

        data = {
            'tanggal_naskah': tanggal_naskah,
            'name': name,
            'partner': partner,
            'deskripsi': deskripsi
        }
        updated_id = http.request.env['muk_dms.info'].browse(int(id)).write(data)
        data.update({'id':updated_id})
        return simplejson.dumps(data)

    @http.route('/vit_dms_web/infos/delete/<int:file_id>', auth='public', csrf=False)
    def info_delete(self, **kw):
        print kw
        id = kw.get('id')
        http.request.env['muk_dms.info'].browse(int(id)).unlink()
        return simplejson.dumps({'success': True})

    @http.route('/vit_dms_web/partner', auth='public', csrf=False)
    def get_partner(self):
        partners = http.request.env['res.partner'].search_read([], fields=['id','name','display_name'])
        return simplejson.dumps(partners)

