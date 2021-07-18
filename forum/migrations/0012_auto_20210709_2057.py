# Generated by Django 3.2.5 on 2021-07-09 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20210705_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название раздела')),
            ],
            options={
                'verbose_name_plural': 'Parent Categories',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.parentcategory', verbose_name='из раздела'),
        ),
    ]