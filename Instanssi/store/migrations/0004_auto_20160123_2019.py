# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-23 20:19


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20160123_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeitem',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Tuotteen hinta senttein\xe4.', max_digits=5, verbose_name='Tuotteen hinta'),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='original_price',
            field=models.DecimalField(decimal_places=2, help_text='Tuotteen hinta ostoshetkell\xe4 ilman alennuksia', max_digits=5, verbose_name='Tuotteen alkuper\xe4inen hinta'),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, help_text='Tuotteen hinta ostoshetkell\xe4', max_digits=5, verbose_name='Tuotteen hinta'),
        ),
    ]
