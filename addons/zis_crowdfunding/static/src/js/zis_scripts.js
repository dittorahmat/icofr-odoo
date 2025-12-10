odoo.define('zis_crowdfunding.animation', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    var ZISCounter = publicWidget.Widget.extend({
        selector: '.zis-counter',
        start: function() {
            this.animateCounters();
            return this._super.apply(this, arguments);
        },
        animateCounters: function() {
            var self = this;
            // Gunakan Intersection Observer untuk memicu animasi saat elemen terlihat
            if ('IntersectionObserver' in window) {
                var observer = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            self.animateCounter(entry.target);
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                this.$('.zis-counter').each(function() {
                    observer.observe(this);
                });
            } else {
                // Fallback jika IntersectionObserver tidak didukung
                this.$('.zis-counter').each(function() {
                    self.animateCounter(this);
                });
            }
        },
        animateCounter: function(element) {
            var $element = $(element);
            var targetValue = parseFloat($element.data('target')) || parseFloat($element.text().replace(/,/g, ''));
            var currentValue = 0;
            var increment = targetValue / 50; // Bagi dalam 50 langkah
            var duration = 2000; // 2 detik
            var stepDuration = duration / 50;
            
            var timer = setInterval(function() {
                currentValue += increment;
                if (currentValue >= targetValue) {
                    clearInterval(timer);
                    $element.text(self.formatNumber(targetValue));
                } else {
                    $element.text(self.formatNumber(currentValue));
                }
            }, stepDuration);
        },
        formatNumber: function(num) {
            return num.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    });

    return ZISCounter;
});