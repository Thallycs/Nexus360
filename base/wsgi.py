"""
WSGI config for base project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# ==============================================================================
# ARTIFÍCIO DE PRODUÇÃO: FORÇA O MIGRATE AGRESSIVO DIRETO NA INICIALIZAÇÃO
# ==============================================================================
if os.environ.get('RENDER'):
    import django
    django.setup()
    from django.core.management import call_command
    try:
        print("Iniciando migração forçada via WSGI...")
        call_command('migrate', '--run-syncdb', interactive=False)
        print("Migração concluída com sucesso!")
    except Exception as e:
        print(f"Aviso na migração WSGI: {str(e)}")

# Inicialização padrão do aplicativo
application = get_wsgi_application()