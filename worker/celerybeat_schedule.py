"""
Celery Beat Schedule - Agendamento de Missões
Define quando cada missão deve ser executada
"""

from celery.schedules import crontab

# Configuração de Periodicidade das Missões
CELERYBEAT_SCHEDULE = {
    # Missão Social: A cada 2 horas (Instagram muda rápido)
    'social-mission-every-2h': {
        'task': 'execute_social_mission',
        'schedule': crontab(minute=0, hour='*/2'),  # 00:00, 02:00, 04:00...
    },
    
    # Missão Técnica: A cada 6 horas (Google Search é mais estável)
    'technical-mission-every-6h': {
        'task': 'execute_technical_mission',
        'schedule': crontab(minute=0, hour='*/6'),  # 00:00, 06:00, 12:00, 18:00
    },
    
    # Missão Luxo: 1x por dia (Artigos mudam devagar)
    'luxury-mission-daily': {
        'task': 'execute_luxury_mission',
        'schedule': crontab(minute=0, hour=9),  # 09:00 todos os dias
    },
}

# Timezone
CELERY_TIMEZONE = 'America/Sao_Paulo'
