<<<<<<< HEAD
# Generated by Django 3.2.6 on 2024-07-18 12:39
=======
# Generated by Django 4.2.11 on 2024-07-19 12:02
>>>>>>> asset

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
<<<<<<< HEAD
                ('total_quantity', models.IntegerField()),
                ('available_quantity', models.IntegerField()),
                ('unique_id', models.CharField(max_length=50, unique=True)),
=======
                ('total_quantity', models.PositiveIntegerField()),
                ('available_quantity', models.PositiveIntegerField()),
                ('unique_id', models.CharField(max_length=50, unique=True)),
                ('arrival_date', models.DateField(auto_now_add=True)),
>>>>>>> asset
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('maintenance_date', models.DateField(auto_now_add=True)),
                ('is_fixed', models.BooleanField(default=False)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Lend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('lent_date', models.DateField(auto_now_add=True)),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('condition', models.CharField(default='Good', max_length=50)),
                ('quantity_good', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('quantity_bad', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
            ],
        ),
    ]
