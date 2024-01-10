# Generated by Django 4.2.6 on 2024-01-01 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='account_type',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='bank',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='currency',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(max_length=200),
        ),
    ]