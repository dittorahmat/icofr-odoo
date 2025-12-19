# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class IcofrTestingSchedule(models.Model):
    _name = 'icofr.testing.schedule'
    _description = 'Jadwal Pengujian Kontrol'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Jadwal Pengujian',
        required=True,
        help='Nama unik untuk identifikasi jadwal pengujian'
    )

    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol yang Diuji',
        required=True,
        help='Kontrol internal yang menjadi subjek pengujian berkala'
    )

    schedule_type = fields.Selection([
        ('one_time', 'Satu Kali'),
        ('recurring', 'Berulang')
    ], string='Jenis Jadwal', default='recurring',
       help='Jenis dari jadwal pengujian (satu kali atau berulang)')

    frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('biweekly', 'Dua Mingguan'),
        ('monthly', 'Bulanan'),
        ('bimonthly', 'Dua Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('semiyearly', 'Semesteran'),
        ('yearly', 'Tahunan')
    ], string='Frekuensi', default='monthly',
       help='Frekuensi pelaksanaan pengujian')

    start_date = fields.Date(
        string='Tanggal Mulai',
        required=True,
        default=fields.Date.today,
        help='Tanggal mulai dari jadwal pengujian'
    )

    end_date = fields.Date(
        string='Tanggal Selesai',
        help='Tanggal selesai dari jadwal pengujian'
    )

    tester_id = fields.Many2one(
        'res.users',
        string='Pelaksana Pengujian',
        required=True,
        help='Pengguna yang akan melaksanakan pengujian berkala'
    )

    next_scheduled_date = fields.Date(
        string='Tanggal Pengujian Berikutnya',
        required=True,
        default=fields.Date.today,
        help='Tanggal berikutnya untuk pelaksanaan pengujian'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('completed', 'Selesai')
    ], string='Status', default='active',
       help='Status dari jadwal pengujian')

    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi tambahan tentang jadwal pengujian'
    )

    auto_generate_task = fields.Boolean(
        string='Otomatis Hasilkan Tugas',
        default=True,
        help='Otomatis hasilkan tugas pengujian saat jadwal tiba'
    )

    notify_before_days = fields.Integer(
        string='Hari Pemberitahuan Sebelumnya',
        default=3,
        help='Jumlah hari sebelum jadwal untuk mengirim pemberitahuan'
    )

    last_execution_date = fields.Date(
        string='Tanggal Eksekusi Terakhir',
        help='Tanggal terakhir jadwal ini dieksekusi'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait jadwal pengujian'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki jadwal pengujian ini'
    )

    testing_ids = fields.One2many(
        'icofr.testing',
        'schedule_id',
        string='Hasil Pengujian',
        help='Daftar pengujian yang dihasilkan dari jadwal ini'
    )

    @api.onchange('start_date', 'frequency')
    def _onchange_start_date_frequency(self):
        """Hitung tanggal berikutnya berdasarkan frekuensi"""
        if self.start_date and self.frequency:
            self.next_scheduled_date = self._calculate_next_date(self.start_date, self.frequency)

    def _calculate_next_date(self, start_date, frequency):
        """Menghitung tanggal berikutnya berdasarkan frekuensi"""
        if not start_date:
            return fields.Date.today()

        if frequency == 'daily':
            next_date = start_date + timedelta(days=1)
        elif frequency == 'weekly':
            next_date = start_date + timedelta(weeks=1)
        elif frequency == 'biweekly':
            next_date = start_date + timedelta(weeks=2)
        elif frequency == 'monthly':
            next_date = start_date + relativedelta(months=1) 
        elif frequency == 'bimonthly':
            next_date = start_date + relativedelta(months=2)
        elif frequency == 'quarterly':
            next_date = start_date + relativedelta(months=3)
        elif frequency == 'semiyearly':
            next_date = start_date + relativedelta(months=6)
        elif frequency == 'yearly':
            next_date = start_date + relativedelta(years=1)
        else:
            next_date = start_date

        return next_date

    def action_generate_testing(self):
        """Method untuk menghasilkan pengujian berdasarkan jadwal ini"""
        self.ensure_one()
        # Buat entri pengujian baru berdasarkan jadwal ini
        testing = self.env['icofr.testing'].create({
            'name': f'Pengujian Otomatis: {self.name}',
            'control_id': self.control_id.id,
            'tester_id': self.tester_id.id,
            'testing_date': self.next_scheduled_date,
            'schedule_id': self.id,
            'state': 'draft'
        })

        # Update tanggal pengujian berikutnya dan tanggal eksekusi terakhir
        next_date = self._calculate_next_date(self.next_scheduled_date, self.frequency)
        if self.end_date and next_date > self.end_date:
            self.write({
                'status': 'completed',
                'next_scheduled_date': False,
                'last_execution_date': fields.Date.today()
            })
        else:
            self.write({
                'next_scheduled_date': next_date,
                'last_execution_date': fields.Date.today()
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Pengujian',
            'res_model': 'icofr.testing',
            'res_id': testing.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_calendar_event(self):
        """Method untuk membuat acara kalender berdasarkan jadwal ini"""
        self.ensure_one()
        calendar_event = self.env['calendar.event'].create({
            'name': f'Pengujian Kontrol: {self.control_id.name}',
            'start': self.next_scheduled_date,
            'stop': self.next_scheduled_date,
            'allday': True,
            'user_id': self.tester_id.id,
            'description': f'Pengujian kontrol {self.control_id.name} berdasarkan jadwal: {self.name}'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Acara Kalender',
            'res_model': 'calendar.event',
            'res_id': calendar_event.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_schedule_testing_notification(self):
        """Method to create scheduled notification for testing reminders"""
        for schedule in self:
            # Calculate the notification date based on notify_before_days
            from datetime import timedelta
            notification_date = schedule.next_scheduled_date - timedelta(days=schedule.notify_before_days or 3)

            # Create a scheduler for the testing reminder notification
            scheduler = self.env['icofr.notification.scheduler'].create({
                'name': f'Pengingat Pengujian: {schedule.name}',
                'notification_type': 'testing_reminder',
                'model_ref': f'icofr.testing.schedule,{schedule.id}',
                'recipient_ids': [(4, schedule.tester_id.id)] if schedule.tester_id else [],
                'next_run_date': fields.Datetime.to_string(notification_date),
                'active': True,
                'interval_number': 1,
                'interval_type': 'days',
                'company_id': schedule.company_id.id if hasattr(schedule, 'company_id') else self.env.company.id,
            })

            # Add notification message
            scheduler._generate_notification_content()

