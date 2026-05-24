from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Garante que o código de inicialização só rode no processo principal do Django
        if os.environ.get('RUN_MAIN') == 'true' or os.environ.get('RENDER'):
            try:
                from core.models import UsuarioNexus
                email_fixo = "engenharia@nexus.com"
                
                # Verifica se o administrador já existe no PostgreSQL de produção
                if not UsuarioNexus.objects.filter(email=email_fixo).exists():
                    UsuarioNexus.objects.create_superuser(
                        username=email_fixo,
                        email=email_fixo,
                        password="senha_nexus_2026",
                        first_name="Talita Costa",
                        is_active=True
                    )
                    print("\n==================================================")
                    print("🚀 INFRA: SUPERUSUÁRIO ADMINISTRATIVO INJETADO!")
                    print("==================================================\n")
            except Exception as e:
                # Evita o travamento do servidor se as tabelas ainda estiverem indexando
                print(f"\nAviso na inicialização do usuário de infraestrutura: {str(e)}\n")