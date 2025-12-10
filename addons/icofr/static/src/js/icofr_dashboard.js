/* JavaScript untuk Dashboard ICORF */
odoo.define('icofr.dashboard', function(require) {
    'use strict';

    const { Component, useState, onMounted } = owl;
    const Registries = require('web.core').Registries;
    const Widget = require('web.Widget');

    // Fungsi untuk mendapatkan data dashboard dari server
    async function fetchDashboardData() {
        try {
            const data = await $.ajax({
                url: '/icofr/dashboard/data',
                type: 'GET',
                dataType: 'json',
                async: true
            });
            return data;
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            return null;
        }
    }

    // Komponen untuk menampilkan grafik batang
    class IcofrBarChart extends Component {
        setup() {
            this.state = useState({
                data: [],
                labels: []
            });
        }

        async willStart() {
            // Load data saat komponen dimulai
            this.loadChartData();
        }

        async loadChartData() {
            const dashboardData = await fetchDashboardData();
            if (dashboardData) {
                // Siapkan data untuk grafik batang kontrol
                const controls = dashboardData.control_summary;
                const labels = controls.map(control => control.name);
                const effectivenessData = controls.map(control => {
                    if (control.effectiveness === 'high') return 100;
                    if (control.effectiveness === 'medium') return 60;
                    if (control.effectiveness === 'low') return 30;
                    return 0;
                });

                this.state.labels = labels;
                this.state.data = effectivenessData;
                this.render();
            }
        }

        renderChart() {
            // Implementasi rendering grafik batang
            const canvasId = this.props.canvasId || 'barChart';
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Contoh rendering grafik batang sederhana (dalam implementasi nyata akan lebih kompleks)
            const barWidth = canvas.width / (this.state.data.length + 1);
            const maxValue = Math.max(...this.state.data, 100);

            this.state.data.forEach((value, index) => {
                const x = barWidth * (index + 0.5);
                const barHeight = (value / maxValue) * (canvas.height - 40);
                const y = canvas.height - barHeight - 20;

                // Warna berdasarkan efektivitas
                if (value >= 80) {
                    ctx.fillStyle = '#2ecc71'; // Hijau untuk efektif
                } else if (value >= 50) {
                    ctx.fillStyle = '#f39c12'; // Kuning untuk sedang
                } else {
                    ctx.fillStyle = '#e74c3c'; // Merah untuk rendah
                }

                ctx.fillRect(x - barWidth/3, y, barWidth * 0.66, barHeight);

                // Label di bawah
                ctx.fillStyle = '#2c3e50';
                ctx.font = '10px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.state.labels[index] || `Ctrl ${index+1}`, x, canvas.height - 5);
            });
        }

        mounted() {
            this.renderChart();
        }

        patched() {
            this.renderChart();
        }
    }

    // Komponen untuk menampilkan grafik lingkaran
    class IcofrPieChart extends Component {
        setup() {
            this.state = useState({
                data: [70, 20, 10], // Contoh: 70% efektif, 20% sedang, 10% rendah
                labels: ['Efektif', 'Sedang', 'Rendah']
            });
        }

        renderChart() {
            const canvasId = this.props.canvasId || 'pieChart';
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const radius = Math.min(centerX, centerY) - 10;

            let currentAngle = 0;
            const total = this.state.data.reduce((a, b) => a + b, 0);

            this.state.data.forEach((value, index) => {
                const sliceAngle = (value / total) * 2 * Math.PI;
                const startAngle = currentAngle;
                const endAngle = currentAngle + sliceAngle;

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();

                // Warna berbeda untuk setiap slice
                const colors = ['#2ecc71', '#f39c12', '#e74c3c'];
                ctx.fillStyle = colors[index % colors.length];
                ctx.fill();

                ctx.strokeStyle = '#fff';
                ctx.stroke();

                currentAngle = endAngle;
            });
        }

        mounted() {
            this.renderChart();
        }

        patched() {
            this.renderChart();
        }
    }

    // Widget utama dashboard
    class IcofrDashboardWidget extends Widget {
        constructor(parent) {
            super(parent);
            this.data = {};
            this.fetchData();
        }

        async fetchData() {
            this.data = await fetchDashboardData();
            if (this.data) {
                this.render();
            }
        }

        async start() {
            await this._super();
            // Perbarui data setiap 5 menit
            setInterval(() => {
                this.fetchData();
            }, 300000);
        }

        events: {
            'click .refresh-btn': '_onRefreshClick',
            'click .export-btn': '_onExportClick'
        }

        _onRefreshClick() {
            this.fetchData();
        }

        _onExportClick() {
            // Redirect ke endpoint export
            window.location.href = '/icofr/export/control_data';
        }
    }

    // Registrasi widget
    Registries.Widget.add('IcofrDashboardWidget', IcofrDashboardWidget);

    return {
        IcofrBarChart,
        IcofrPieChart,
        IcofrDashboardWidget
    };
});