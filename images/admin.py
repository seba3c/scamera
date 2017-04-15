from django.contrib import admin

from images.models import PeopleDetectorTest


class PeopleDetectorTestAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'state',
                    # 'creation_timestamp',
                    'running_timestamp',
                    'time_took_f',
                    'accuracy_f',
                    'avg_time_per_sample',
                    'positive_samples_count',
                    'negative_samples_count',
                    'total_samples_count',
                    'true_positives',
                    'false_positives',
                    'true_negatives',
                    'false_negatives',
                    )
    list_display_links = ('id',)

    ordering = ('-_accuracy', 'time_took', '_total_samples_count')

    search_fields = ['id', 'state']

    readonly_fields = ('id',
                       'creation_timestamp',
                       'P',
                       'N',
                       'sensitivity',
                       'specificity',
                       'precision',
                       'negative_predictive_value',
                       'fall_out',
                       'false_discovery_rate',
                       'miss_rate',
                       'accuracy',
                       'balanced_accuracy',
                       'avg_time_per_sample',
                       'total_samples_count')

    fieldsets = (
        (None, {
            'fields': ('id',
                       'title',
                       'state',
                       'settings',
                       'creation_timestamp',
                       'running_timestamp',
                       ('time_took',
                        'avg_time_per_sample'),
                       ('positive_samples_dir',
                        'negative_samples_dir'),
                       'save_enhaced_images',
                       ('positive_samples_count',
                        'negative_samples_count',
                        'total_samples_count')
                       )
        }),
        ('TEST Metrics', {
            'classes': ('extrapretty',),
            'fields': (('true_positives',
                       'false_positives',),
                       ('true_negatives',
                       'false_negatives',),
                       ('P',
                       'N',),
                       ('sensitivity',
                        'specificity',
                        'precision',),
                       ('negative_predictive_value',
                        'fall_out',
                        'false_discovery_rate',
                        'miss_rate',),
                       ('accuracy',
                       'balanced_accuracy')),
        }),
        )

    def time_took_f(self, obj):
        return "%.2f secs" % obj.time_took
    time_took_f.short_description = 'Time Took'
    time_took_f.admin_order_field = 'time_took'

    def sensitivity(self, obj):
        return "%.2f" % obj.sensitivity
    sensitivity.short_description = 'sensitivity TPR = TP/P = TP/(TP+FN)'

    def specificity(self, obj):
        return "%.2f" % obj.specificity
    specificity.short_description = 'specificity SPC = TN/N = TN/(FP+TN)'

    def precision(self, obj):
        return "%.2f" % obj.precision
    precision.short_description = 'precision PPV = TP/(TP+FP)'

    def negative_predictive_value(self, obj):
        return "%.2f" % obj.negative_predictive_value
    negative_predictive_value.short_description = 'negative predictive value NPV = TN/(TN+FN)'

    def fall_out(self, obj):
        return "%.2f" % obj.fall_out
    fall_out.short_description = 'fall out FPR = FP/N = FP/(FP+TN)'

    def false_discovery_rate(self, obj):
        return "%.2f" % obj.false_discovery_rate
    false_discovery_rate.short_description = 'false discovery rate FDR = FP/(FP+TP) = 1 - PPV'

    def miss_rate(self, obj):
        return "%.2f" % obj.miss_rate
    miss_rate.short_description = 'miss rate FNR = FN/(FN+TP)'

    def accuracy(self, obj):
        return "%.2f" % obj.accuracy
    accuracy.short_description = 'accuracy ACC = (TP+TN)/(P+N)'

    def accuracy_f(self, obj):
        return self.accuracy(obj)
    accuracy_f.short_description = 'accuracy'
    accuracy_f.admin_order_field = '_accuracy'

    def balanced_accuracy(self, obj):
        return "%.2f" % obj.balanced_accuracy
    balanced_accuracy.short_description = 'balanced accuracy BACC = (TP/P + TN/N)/2'

    def avg_time_per_sample(self, obj):
        if obj.avg_time_per_sample > 0:
            return "%.2f secs (%.2f samples/s)" % (obj.avg_time_per_sample, 1 / obj.avg_time_per_sample)
        return "-"
    avg_time_per_sample.short_description = 'avg time'

    def total_samples_count(self, obj):
        return obj.total_samples_count
    total_samples_count.short_description = 'Total Samples'
    total_samples_count.admin_order_field = '_total_samples_count'


admin.site.register(PeopleDetectorTest, PeopleDetectorTestAdmin)
