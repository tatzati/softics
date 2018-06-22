# Generated by Django 2.0.6 on 2018-06-20 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_loan_saleable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedLoss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('risk', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='ProbabilityOfDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('risk', models.FloatField(default=0.0)),
            ],
        ),
        migrations.RemoveField(
            model_name='loan',
            name='expected_loss',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='probability_of_default',
        ),
        migrations.AlterField(
            model_name='loan',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='loans.Bank'),
        ),
        migrations.AddField(
            model_name='probabilityofdefault',
            name='loan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pd_loans', to='loans.Loan'),
        ),
        migrations.AddField(
            model_name='expectedloss',
            name='loan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='el_loans', to='loans.Loan'),
        ),
    ]
