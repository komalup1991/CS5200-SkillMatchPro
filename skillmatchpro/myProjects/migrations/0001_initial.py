# Generated by Django 3.1.7 on 2023-11-13 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryid', models.IntegerField(db_column='categoryID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'db_table': 'Category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectid', models.AutoField(db_column='projectID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('projectstatus', models.CharField(blank=True, db_column='projectStatus', max_length=15, null=True)),
                ('startdate', models.DateTimeField(blank=True, db_column='startDate', null=True)),
            ],
            options={
                'db_table': 'Project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('userid', models.AutoField(db_column='userID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=15, null=True)),
                ('registrationdate', models.DateTimeField(blank=True, db_column='registrationDate', null=True)),
                ('lastlogin', models.DateTimeField(blank=True, db_column='lastLogin', null=True)),
                ('specialization', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'UserInfo',
                'managed': False,
            },
        ),
    ]
