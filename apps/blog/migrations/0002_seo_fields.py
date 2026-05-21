from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Meta description (max 160 chars). Puste = auto z excerpt.', max_length=160),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='Słowa kluczowe oddzielone przecinkami.', max_length=255),
        ),
        migrations.AddField(
            model_name='post',
            name='cover_image_alt',
            field=models.CharField(blank=True, help_text='Alt text dla cover image (SEO + dostępność).', max_length=125),
        ),
        migrations.AddField(
            model_name='post',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Kanoniczny URL (puste = auto z get_absolute_url).'),
        ),
    ]
