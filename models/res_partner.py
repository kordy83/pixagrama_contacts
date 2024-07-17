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
    partner_file_hajj_id = fields.Many2one('res.partner.hajj.group', string='Partner File',)
    attach_file2 = fields.Binary('الاسم')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_group_id = fields.Many2one('res.partner.group')
    partner_internal_group_id = fields.Many2one('res.partner.internal.group')
    partner_hij_group_id = fields.Many2one('res.partner.hij.group')
    partner_omra_group_id = fields.Many2one('res.partner.internal.group')
    partner_hajj_group_id = fields.Many2one('res.partner.hajj.group')
    partner_domestic_group_id = fields.Many2one('res.partner.domestic.group')
    partner_Investment_group_id = fields.Many2one('res.partner.Investment.group')
    partner_Trips_group_id = fields.Many2one('res.partner.Trips.group')
    
    is_external = fields.Boolean()
    is_domestic = fields.Boolean()
    is_enternal = fields.Boolean()
    is_hajj2 = fields.Boolean()
    is_religion = fields.Boolean()
    is_hij = fields.Boolean()
    is_omra = fields.Boolean()
    is_commercial = fields.Boolean()
    is_free = fields.Boolean()
    is_hajj = fields.Boolean()
    is_investment = fields.Boolean()
    is_trips = fields.Boolean()
    
    
    place_of_birth_date = fields.Char('place of birth') #
    date_of_birth = fields.Date('date of birth') 
    nationality = fields.Char('Nationality')
    national_number = fields.Char('National ID')
    military_status = fields.Char('Military Status')
    phone2 = fields.Char('Mobile Number')
    passport_number = fields.Char('Passport Number')
    passport_place = fields.Char('Passport Place')
    passport_start_date = fields.Date('Passport Release Date')
    passport_end_date = fields.Date('Passport Expiry Date')
    email_pix = fields.Char('E-mail')
    password = fields.Char('Password')
    embassy_password = fields.Char("Embassy's password")
    received_file_date = fields.Date('Received File Date')
    required_paper = fields.Char('Required Paper')
    country3_id = fields.Many2one('res.country', 'Country')
    country2_id = fields.Many2one('res.country', 'Country')
    code2 = fields.Char('Postal code')
    cgi = fields.Char('CGI')
    embassy_date = fields.Datetime('Embassy Date')
    previous_visa = fields.Char('previous visa')
    visa_state = fields.Char('Visa state')
    visa_type = fields.Char('Visa Type')
    translation_paper = fields.Char('Translated Paper')
    email2 = fields.Char('email')
    vtype = fields.Char('v')
    vstate = fields.Char('vs')
    translation_type = fields.Char('Translation Type')
    translation_fees = fields.Float('Translation Fees')
    embassy_fess = fields.Char('Embassy Fess')
    file_fess = fields.Char('File Preparation Fees')
    payment_type = fields.Char('Payment Type')
    embassy_address = fields.Char('Embassy Address')
    embassy_email = fields.Char('Embassy E-mail')
    embassy_phone = fields.Char('Embassy Phone')
    region22 = fields.Char('Region')
    hospital_name = fields.Char('Hospital name')
    address22 = fields.Char('Address')
    patient_type = fields.Char('Patient type')
    # hotel_name = fields.Char('اسم الفندق')
    confirmation_date = fields.Datetime('confirmation date')
    retrieve_date = fields.Datetime('retrieve date')
    cancel_date = fields.Datetime('cancel date')
    pin_code = fields.Char('pin_code')
    confirmation_code = fields.Char('confirmation_code')
    description = fields.Char('description')
    att_file = fields.Binary('Add File')
    att_file1 = fields.Binary('Add File')
    att_file2 = fields.Binary('Add File')
    att_file3 = fields.Binary('Add File')
    att_file4 = fields.Binary('Add File')
    att_file5 = fields.Binary('Add File')
    att_file6 = fields.Binary('Add File')
    att_file7 = fields.Binary('Add File')
    att_file8 = fields.Binary('Add File')
    att_file9 = fields.Binary('Add File')
    att_file10 = fields.Binary('Add File')
    no_of_family_enternal = fields.Char("Number Of Family Members")
    no_of_childs_enternal = fields.Char("Number Of Children")
    no_of_babys_enternal = fields.Char("Number Of Infants")
    no_of_free_enternal = fields.Char("Number Of Free Children")
    no_of_boys_enternal = fields.Char("Number Of Teenagers")
    no_of_days_enternal = fields.Char("Number Of Nights")
    child_no_enternal = fields.Char("Number Of Children Aged 6-12 years")
    hotel_name_enternal = fields.Char("Hotel Name")
    hotel_address_enternal = fields.Char("Hotel Address")
    hotel_number_enternal = fields.Char("Hotel Phone Number")
    hotel_level_enternal = fields.Char("Hotel Level")
    reservation_employee_enternal = fields.Char("Reservation Employee Name")
    is_aqua_bark_enternal = fields.Boolean("Have Aqua-Bark Or No")
    single_double_enternal = fields.Selection(string="For children only or for adults as well",
                             selection=[('child', ' children only'), ('double', 'children and adults'), ])
    room_type_enternal = fields.Selection(string="Room Type", selection=[('one', 'Single'), ('two', 'Double'),
                                                             ('three', 'Triple'), ('four', 'Sweet'),
                                                             ('five', 'couple'), ('six', 'familial'), ])

    no_of_members_enternal = fields.Char("Number of people in each room")
    iqama_system_enternal = fields.Selection(string="Residency system", selection=[('one', 'Breakfast + lunch'), ('two', 'Breakfast+lunch+ dinner'), ])
    extra_service_enternal = fields.Char("Additional services")


    
    mobile_religion = fields.Char("Mobile number2")
    service_type_religion = fields.Char("service type")
    passport_no_religion = fields.Char("Passport number")
    region_start_religion = fields.Char("Issuer")
    start_date_religion = fields.Date("Release Date")
    finish_date_religion = fields.Date("Expiry date")
    finger_print_religion = fields.Date("Fingerprint history")
    traveling_date_religion = fields.Datetime("Date Of Travel")
    medical_religion = fields.Char("Medical examinations")
    gift_religion = fields.Char("Gifts")
    agency_religion = fields.Char("Agent")
    shipment_company2_religion = fields.Char("Transportation company inside the campus of Mecca")
    shipment_company_religion = fields.Char("Airport transportation company")
    company_religion = fields.Char("Guarantor company")
    director_religion = fields.Char("The responsible director of the guarantee company")
    hotel_name_maka_religion = fields.Char("The name of the Mecca hotel")
    hotel_madina_level_religion = fields.Char("Hotel level")
    iqama_maka_religion = fields.Char("Type of residence")
    hotel_madina_name_religion = fields.Char("Name of the city hotel")
    hotel_maka_level_religion = fields.Char("Hotel level")
    iqama_madina_religion = fields.Char("Type of residence")
    time_religion = fields.Datetime("Timing")
    job_religion = fields.Char("job")
    
    #domestic
    
    hotel_name = fields.Char("Hotel name")
    address11 = fields.Char("Hotel address")
    hotel_phone = fields.Char("Hotel phone")
    gov = fields.Char("Gov")
    area = fields.Char("Area")
    supplier = fields.Char("Supplier")
    reservation_manger = fields.Char("Reservation manger")
    phone_number = fields.Char("Phone number")
    check_in_date = fields.Date("Expiry date")
    check_out_date = fields.Date("Expiry date")
    room_type = fields.Char("Room type")
    number_of_rooms = fields.Char("Number of rooms")
    meal_policy  = fields.Char("Meal policy")
    child_policy  = fields.Char("Child policy")
    canulation_policy = fields.Char("Canulation policy") 
    how_many_nights = fields.Char("How many nights") 
    facilities = fields.Char("Facilities")
    rating = fields.Char("Rating")
    level = fields.Char("Level")
    bad_review = fields.Char("Bad review")
    extra_services = fields.Char("Extra services")

