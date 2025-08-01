# Generated by Django 5.2.3 on 2025-07-07 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0004_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('is_avail', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('file', models.FileField(upload_to='files/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module1.category')),
            ],
        ),
    ]
