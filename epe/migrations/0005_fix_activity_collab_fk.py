# epe/migrations/0005_fix_activity_collab_fk.py
from django.db import migrations, models
import django.db.models.deletion

def copy_fk_forward(apps, schema_editor):
    # Copia os valores do FK antigo para o campo novo provisório
    with schema_editor.connection.cursor() as cur:
        # Só copia se a coluna antiga existir (em SQLite a recriação de tabela cuida disso)
        try:
            cur.execute("UPDATE epe_activity SET collaborator2_id = collaborator_id")
        except Exception:
            pass

class Migration(migrations.Migration):

    # >>> IMPORTANTE: faça 0005 depender da 0004 <<<
    dependencies = [
        ("epe", "0004_alter_workday_collaborator"),
        # Se quiser garantir ordem sobre o app common, pode adicionar a linha abaixo
        # ("common", "0001_initial"),
    ]

    operations = [
        # 1) Adiciona um novo FK provisório para common.Collaborator
        migrations.AddField(
            model_name="activity",
            name="collaborator2",
            field=models.ForeignKey(
                to="common.collaborator",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="epe_activities",
                related_query_name="epe_activity",
                verbose_name="Colaborador",
                null=True,  # temporário para permitir a cópia
            ),
        ),
        # 2) Copia os IDs do campo antigo para o novo
        migrations.RunPython(copy_fk_forward, reverse_code=migrations.RunPython.noop),

        # 3) Remove o campo antigo (que apontava para epe_collaborator)
        migrations.RemoveField(
            model_name="activity",
            name="collaborator",
        ),

        # 4) Renomeia collaborator2 -> collaborator (vira o oficial)
        migrations.RenameField(
            model_name="activity",
            old_name="collaborator2",
            new_name="collaborator",
        ),

        # 5) Torna NOT NULL para casar com o models.py atual
        migrations.AlterField(
            model_name="activity",
            name="collaborator",
            field=models.ForeignKey(
                to="common.collaborator",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="epe_activities",
                related_query_name="epe_activity",
                verbose_name="Colaborador",
                null=False,
            ),
        ),
    ]
