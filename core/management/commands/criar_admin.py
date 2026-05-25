from django.core.management.base import BaseCommand
from core.models import UsuarioNexus

class Command(BaseCommand):
    help = 'Injeta o superusuário administrativo no banco de dados'

    def handle(self, *args, **kwargs):
        email_fixo = "engenharia@nexus.com"
        
        if not UsuarioNexus.objects.filter(email=email_fixo).exists():
            UsuarioNexus.objects.create_superuser(
                username=email_fixo,
                email=email_fixo,
                password="senha_nexus_2026",
                first_name="Talita Costa",
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS("🚀 INFRA: SUPERUSUÁRIO ADMINISTRATIVO INJETADO COM SUCESSO!"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Aviso: O superusuário já existe no banco."))