# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    partner_group_id2 = fields.Many2one('res.partner.group', string='Partner Group',)
    internal_group_id = fields.Many2one('res.partner.internal.group', string='Partner Group',)
    internal_hij_group_id = fields.Many2one('res.partner.hij.group', string='Partner Group',)
    internal_omra_group_id = fields.Many2one('res.partner.omra.group', string='Partner Group',)


class ResPartnerHijGroup(models.Model):
    _name = "res.partner.hij.group"

    name = fields.Char()
    active = fields.Boolean(default=True)
    image = fields.Binary()
    description = fields.Text("الوصف")
    trip_date = fields.Datetime('تاريخ الرحله')
    trip_place = fields.Char('جهه الرحله')
    partner_group_ids = fields.Many2many('res.partner', 'partner_hij_group_id', string='عملاء')
    partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_hij_id', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.partner_group_ids:
                if line.total_invoiced > 0:
                    line.partner_hij_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'العملاء',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('partner_hij_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('internal_hij_group_id', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.partner_group_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('internal_hij_group_id', '=', partner.id)])


class ResPartnerOmraGroup(models.Model):
    _name = "res.partner.omra.group"

    name = fields.Char()
    active = fields.Boolean(default=True)
    image = fields.Binary()
    description = fields.Text("الوصف")
    trip_date = fields.Datetime('تاريخ الرحله')
    trip_place = fields.Char('جهه الرحله')
    partner_group_ids = fields.Many2many('res.partner', 'partner_omra_group_id', string='عملاء')
    partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_omra_id', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.partner_group_ids:
                if line.total_invoiced > 0:
                    line.partner_omra_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'العملاء',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('partner_omra_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('internal_omra_group_id', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.partner_group_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('internal_omra_group_id', '=', partner.id)])


class ResPartnerInternalGroup(models.Model):
    _name = "res.partner.internal.group"

    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                     string='Related Partner', help='Partner-related data of the student')

    name = fields.Char()
    active = fields.Boolean(default=True)
    image = fields.Binary()
    description = fields.Text("الوصف")
    trip_date = fields.Datetime('تاريخ الرحله')
    trip_place = fields.Char('جهه الرحله')
    partner_group_ids = fields.Many2many('res.partner', 'partner_internal_group_id', string='عملاء')
    partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_id2', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.partner_group_ids:
                if line.total_invoiced > 0:
                    line.partner_internal_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'العملاء',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('partner_internal_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('internal_group_id', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.partner_group_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('internal_group_id', '=', partner.id)])


class ResPartnerGroup(models.Model):
    _name = "res.partner.group"

    name = fields.Char()
    active = fields.Boolean(default=True)
    image = fields.Binary(attachment=False)
    description = fields.Text("الوصف")
    trip_date = fields.Datetime('تاريخ الرحله')
    trip_place = fields.Char('جهه الرحله')
    partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_id')
    partner_group_ids = fields.Many2many('res.partner', 'partner_group_id', string='عملاء')
    partner_files_ids = fields.One2many('partner.attach.file', 'partner_file_id', string='ملفات')
    task_count = fields.Integer(compute='_compute_task_count', string='# Tasks')
    total_invoiced = fields.Float(compute='_compute_total_invoiced')

    def open_partner_history2(self):
        for rec in self:
            for line in rec.partner_group_ids:
                if line.total_invoiced > 0:
                    line.partner_group_id = rec.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'العملاء',
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('partner_group_id', '=', rec.id)],
                'target': 'current',
            }

    def get_related_tasks(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'tasks',
                'res_model': 'project.task',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('partner_group_id2', '=', record.id)],
                'target': 'current',
            }

    def _compute_total_invoiced(self):
        for partner in self:
            partner.total_invoiced = sum(line.total_invoiced for line in partner.partner_group_ids)

    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([('partner_group_id2', '=', partner.id)])


class PartnerAttachFile(models.Model):
    _name = "partner.attach.file"

    partner_file_id = fields.Many2one('res.partner.group', string='Partner File',)
    partner_file_id2 = fields.Many2one('res.partner.internal.group', string='Partner File',)
    partner_file_hij_id = fields.Many2one('res.partner.hig.group', string='Partner File',)
    partner_file_omra_id = fields.Many2one('res.partner.omra.group', string='Partner File',)
    attach_file2 = fields.Binary('الاسم')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_group_id = fields.Many2one('res.partner.group')
    partner_internal_group_id = fields.Many2one('res.partner.internal.group')
    partner_hij_group_id = fields.Many2one('res.partner.hij.group')
    partner_omra_group_id = fields.Many2one('res.partner.internal.group')
    place_of_birth_date = fields.Char('مكان الميلاد')
    date_of_birth = fields.Date('تاريخ الميلاد')
    nationality = fields.Char('الجنسيه')
    national_number = fields.Char('الرقم القومي')
    military_status = fields.Char('موقف التجنيد')
    phone2 = fields.Char('رقم الموبايل')
    passport_number = fields.Char('رقم الباسبور')
    passport_place = fields.Char('جهه اصدار الباسبور')
    passport_start_date = fields.Date('تاريخ اصدار الباسبور')
    passport_end_date = fields.Date('تاريخ انتهاء الباسبور')
    email_pix = fields.Char('البريد الالكتروني')
    password = fields.Char('الرقم السري')
    embassy_password = fields.Char('الرقم السرى للسفاره')
    received_file_date = fields.Date('تاريخ استلام الملف')
    required_paper = fields.Char('الاوراق المطلوبه')
    country_id = fields.Many2one('res.country', 'الجهة')
    code2 = fields.Char('الكود البريدى')
    cgi = fields.Char('CGI')
    embassy_date = fields.Datetime('ميعاد السفاره')
    previous_visa = fields.Char('التاشيره السابقه')
    visa_state = fields.Char('حاله التاشيره')
    visa_type = fields.Char('نوع التاشيره')
    translation_paper = fields.Char('الاوراق المترجمه')
    translation_type = fields.Char('نوع الترجمه')
    translation_fees = fields.Float('رسوم الترجمه')
    embassy_fess = fields.Char('رسوم السفاره')
    file_fess = fields.Char('رسوم تحضير الملف')
    payment_type = fields.Char('نوع الدفع')
    embassy_address = fields.Char('عنوان السفاره')
    embassy_email = fields.Char('البريد الالكتروني للسفاره')
    embassy_phone = fields.Char('تليفون السفاره')
    region22 = fields.Char('الجهه')
    hospital_name = fields.Char('اسم المستشفي')
    address22 = fields.Char('العنوان')
    patient_type = fields.Char('نوع المرض')
    hotel_name = fields.Char('اسم الفندق')
    confirmation_date = fields.Datetime('تاريخ الحجز')
    retrieve_date = fields.Datetime('تاريخ المغادره')
    cancel_date = fields.Datetime('تاريخ الالغاء')
    pin_code = fields.Char()
    confirmation_code = fields.Char()
    description = fields.Char('الوصف')
    att_file = fields.Binary('اضافه ملف')
    is_external = fields.Boolean()

    is_enternal = fields.Boolean()
    no_of_family_enternal = fields.Char("عدد الاسره")
    no_of_childs_enternal = fields.Char("عدد الاطفال")
    no_of_babys_enternal = fields.Char("عدد الرضع")
    no_of_free_enternal = fields.Char("عدد الاطفال المجانيه")
    no_of_boys_enternal = fields.Char("عدد المراهقين")
    no_of_days_enternal = fields.Char("عدد الليالي")
    child_no_enternal = fields.Char("عدد الاطفال عمر 6-12 سنه")
    hotel_name_enternal = fields.Char("اسم الفندق")
    hotel_address_enternal = fields.Char("عنوان الفندق")
    hotel_number_enternal = fields.Char("رقم تليفون الفندق")
    hotel_level_enternal = fields.Char("مستوى الفندق")
    reservation_employee_enternal = fields.Char("اسم موظف الحجوزات")
    is_aqua_bark_enternal = fields.Boolean("به اكوابارك ام لا")
    single_double_enternal = fields.Selection(string="للاطفال فقط ام للكبار ايضا",
                             selection=[('child', 'للاطفال فقط'), ('double', 'للاطفال والكبار'), ])
    room_type_enternal = fields.Selection(string="نوع الغرفه", selection=[('one', 'فرديه'), ('two', 'ثنائيه'),
                                                             ('three', 'ثلاثيه'), ('four', 'سويت'),
                                                             ('five', 'مزدوجه'), ('six', 'عائليه'), ])

    no_of_members_enternal = fields.Char("عدد الافراد في كل غرفه")
    iqama_system_enternal = fields.Selection(string="نظام الاقامه", selection=[('one', 'فطار + غدا'), ('two', 'فطار+غدا+ عشا'), ])
    extra_service_enternal = fields.Char("خدمات اضافيه")


    is_religion = fields.Boolean()
    is_hij = fields.Boolean()
    is_omra = fields.Boolean()
    is_commercial = fields.Boolean()
    is_free = fields.Boolean()
    mobile_religion = fields.Char("رقم الموبايل2")
    service_type_religion = fields.Char("نوع الخدمه")
    passport_no_religion = fields.Char("رقم الجواز")
    region_start_religion = fields.Char("جهه الاصدار")
    start_date_religion = fields.Date("تاريخ الاصدار")
    finish_date_religion = fields.Date("تاريخ الانتهاء")
    finger_print_religion = fields.Date("تاريخ البصمه")
    traveling_date_religion = fields.Datetime("تاريخ السفر")
    medical_religion = fields.Char("الكشوفات الطبيه")
    gift_religion = fields.Char("الهدايا")
    agency_religion = fields.Char("الوكيل/المطوف")
    shipment_company2_religion = fields.Char("شركه النقل داخل الحرم")
    shipment_company_religion = fields.Char("شركه النقل للمطار")
    company_religion = fields.Char("الشركه الضامنه")
    director_religion = fields.Char("المدير المسئول للشركه الضامنه")
    hotel_name_maka_religion = fields.Char("اسم فندق مكه")
    hotel_madina_level_religion = fields.Char("مستوى الفندق")
    iqama_maka_religion = fields.Char("نوع الاقامه")
    hotel_madina_name_religion = fields.Char("اسم فندق المدينه")
    hotel_maka_level_religion = fields.Char("مستوى الفندق")
    iqama_madina_religion = fields.Char("نوع الاقامه")
    time_religion = fields.Datetime("التوقيت")
    job_religion = fields.Char("الوظيفه")

