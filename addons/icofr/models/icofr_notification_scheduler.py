# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class IcofrNotificationScheduler(models.Model):
    """
    Model untuk mengelola penjadwalan notifikasi otomatis
    untuk CSA assignments dan testing deadlines
    """
    _name = 'icofr.notification.scheduler'
    _description = 'Penjadwal Notifikasi Otomatis ICORF'
    _order = 'next_run_date asc'

    name = fields.Char(
        string='Nama Penjadwal',
        required=True,
        help='Nama deskriptif dari penjadwal notifikasi'
    )

    notification_type = fields.Selection([
        ('csa_assignment', 'Penugasan CSA'),
        ('testing_reminder', 'Pengingat Pengujian'),
        ('certification_deadline', 'Batas Waktu Sertifikasi'),
        ('reporting_deadline', 'Batas Waktu Pelaporan'),
        ('control_review', 'Review Kontrol')
    ], string='Jenis Notifikasi', required=True,
       help='Jenis dari notifikasi yang akan dijadwalkan')

    model_ref = fields.Reference(
        selection=[
            ('icofr.csa', 'CSA'),
            ('icofr.testing.schedule', 'Jadwal Pengujian'),
            ('icofr.certification', 'Sertifikasi'),
            ('icofr.pojk.report', 'Laporan POJK')
        ],
        string='Referensi Model',
        help='Objek yang menjadi sumber notifikasi'
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help='Status penjadwal notifikasi'
    )

    interval_number = fields.Integer(
        string='Jumlah Interval',
        default=1,
        help='Jumlah satuan interval (misalnya: 1, 2, 3, dst)'
    )

    interval_type = fields.Selection([
        ('hours', 'Jam'),
        ('days', 'Hari'),
        ('weeks', 'Minggu'),
        ('months', 'Bulan')
    ], string='Tipe Interval', default='days',
       help='Tipe interval untuk penjadwalan')

    next_run_date = fields.Datetime(
        string='Tanggal Eksekusi Berikutnya',
        required=True,
        default=fields.Datetime.now,
        help='Tanggal dan waktu berikutnya untuk menjalankan notifikasi'
    )

    last_run_date = fields.Datetime(
        string='Tanggal Eksekusi Terakhir',
        readonly=True,
        help='Tanggal dan waktu terakhir notifikasi dijalankan'
    )

    notification_message = fields.Text(
        string='Pesan Notifikasi',
        help='Pesan yang akan dikirimkan dalam notifikasi'
    )

    recipient_ids = fields.Many2many(
        'res.users',
        string='Penerima Notifikasi',
        help='Pengguna yang akan menerima notifikasi ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang terkait dengan penjadwal ini'
    )

    def _generate_notification_content(self):
        """Generate konten notifikasi berdasarkan jenis dan objek referensi"""
        for scheduler in self:
            if scheduler.model_ref and scheduler.notification_type:
                if scheduler.notification_type == 'csa_assignment':
                    if scheduler.model_ref._name == 'icofr.csa':
                        scheduler.notification_message = (
                            f"Anda memiliki penugasan CSA baru: {scheduler.model_ref.name}\n"
                            f"Kontrol: {scheduler.model_ref.control_id.name}\n"
                            f"Pemilik Kontrol: {scheduler.model_ref.control_owner_id.name if scheduler.model_ref.control_owner_id else 'Tidak Ditentukan'}\n"
                            f"Periode: {scheduler.model_ref.assessment_period}\n"
                            f"Silakan segera menyelesaikan penilaian CSA ini."
                        )
                elif scheduler.notification_type == 'testing_reminder':
                    if scheduler.model_ref._name == 'icofr.testing.schedule':
                        scheduler.notification_message = (
                            f"Pengingat: Jadwal pengujian kontrol akan segera tiba\n"
                            f"Jadwal: {scheduler.model_ref.name}\n"
                            f"Kontrol: {scheduler.model_ref.control_id.name}\n"
                            f"Tester: {scheduler.model_ref.tester_id.name}\n"
                            f"Jadwal berikutnya: {scheduler.model_ref.next_scheduled_date}\n"
                            f"Harap siapkan pengujian kontrol sesuai jadwal."
                        )

    def action_manual_execute(self):
        """Eksekusi manual penjadwal notifikasi"""
        for scheduler in self:
            scheduler._execute_notification()
            scheduler.last_run_date = fields.Datetime.now()
            # Hitung tanggal eksekusi berikutnya
            scheduler.next_run_date = scheduler._calculate_next_run_date()
    
    def _calculate_next_run_date(self):
        """Hitung tanggal eksekusi berikutnya berdasarkan interval"""
        self.ensure_one()
        current_date = self.next_run_date or fields.Datetime.now()
        
        if self.interval_type == 'hours':
            return current_date + timedelta(hours=self.interval_number)
        elif self.interval_type == 'days':
            return current_date + timedelta(days=self.interval_number)
        elif self.interval_type == 'weeks':
            return current_date + timedelta(weeks=self.interval_number)
        elif self.interval_type == 'months':
            # For months, we'll add the month manually to handle month-end dates properly
            from dateutil.relativedelta import relativedelta
            return current_date + relativedelta(months=self.interval_number)
        
        return current_date

    def _execute_notification(self):
        """Eksekusi notifikasi berdasarkan konfigurasi"""
        for scheduler in self:
            if not scheduler.active:
                continue

            # Generate content if not already set
            if not scheduler.notification_message:
                scheduler._generate_notification_content()

            # Create notification record
            if scheduler.notification_message:
                recipients = scheduler.recipient_ids or scheduler._get_default_recipients()
                
                for recipient in recipients:
                    notification_vals = {
                        'name': f"Notifikasi: {scheduler.name}",
                        'notification_type': scheduler.notification_type.replace('_', '.'),
                        'model_ref': f"{scheduler.model_ref._name},{scheduler.model_ref.id}" if scheduler.model_ref else False,
                        'recipient_ids': [(4, recipient.id)],
                        'subject': f"Notifikasi {scheduler.name}",
                        'message': scheduler.notification_message,
                        'related_date': scheduler.next_run_date.date() if scheduler.next_run_date else False,
                    }
                    
                    # Create the notification
                    self.env['icofr.notification'].create(notification_vals)

    def _get_default_recipients(self):
        """Dapatkan penerima default berdasarkan jenis notifikasi"""
        self.ensure_one()
        if self.model_ref:
            if self.notification_type == 'csa_assignment' and self.model_ref._name == 'icofr.csa':
                # For CSA assignments, notify the control owner
                return self.model_ref.control_owner_id or self.env.user
            elif self.notification_type == 'testing_reminder' and self.model_ref._name == 'icofr.testing.schedule':
                # For testing reminders, notify the tester
                return self.model_ref.tester_id or self.env.user
        return self.env.user

    @api.model
    def cron_execute_scheduled_notifications(self):
        """Cron job untuk eksekusi notifikasi terjadwal"""
        current_time = fields.Datetime.now()
        
        # Dapatkan semua penjadwal yang aktif dan waktunya telah tiba
        schedulers = self.search([
            ('active', '=', True),
            ('next_run_date', '<=', current_time)
        ])
        
        # Eksekusi notifikasi untuk masing-masing penjadwal
        for scheduler in schedulers:
            try:
                scheduler._execute_notification()
                scheduler.last_run_date = current_time
                scheduler.next_run_date = scheduler._calculate_next_run_date()
            except Exception as e:
                _logger.error(f"Error executing notification scheduler {scheduler.id}: {str(e)}")
                # Tidak menghentikan eksekusi scheduler lainnya
                continue

    @api.constrains('interval_number')
    def _check_interval_number(self):
        for record in self:
            if record.interval_number <= 0:
                raise ValidationError(_("Interval number must be greater than 0"))