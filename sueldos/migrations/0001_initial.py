# Generated by Django 3.2.8 on 2022-02-01 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liquidacion', models.CharField(max_length=200, unique=True)),
                ('observación', models.TextField(blank=True, null=True)),
                ('abierta', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Liquidacion',
                'verbose_name_plural': 'Liquidaciones',
            },
        ),
        migrations.CreateModel(
            name='Reparticion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro', models.IntegerField(unique=True)),
                ('saf', models.IntegerField()),
                ('denominacion', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Reparticion',
                'verbose_name_plural': 'Reparticiones',
                'ordering': ['nro'],
            },
        ),
        migrations.CreateModel(
            name='TipoLiquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Tipo de liquidacion',
                'verbose_name_plural': 'Tipos de Liquidacion',
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('op', models.IntegerField(blank=True, null=True)),
                ('fechaME', models.DateField(blank=True, null=True, verbose_name='Fecha ME')),
                ('pagado', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('liquidacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sueldos.liquidacion')),
                ('reparticion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sueldos.reparticion')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
                'ordering': ['reparticion'],
            },
        ),
        migrations.AddField(
            model_name='liquidacion',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sueldos.tipoliquidacion'),
        ),
    ]