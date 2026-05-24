#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala as dependências do projeto
pip install -r requirements.txt

# Coleta os arquivos estáticos de estilo
python manage.py collectstatic --noinput

# Força a criação das tabelas diretamente no PostgreSQL do Render
python manage.py migrate --run-syncdb