# Nomes das filas utilizadas
INPUT_QUEUES = ['00_syrin_notification_critical', '00_syrin_notification_warning']
OUTPUT_QUEUES = [
    '01_syrin_notification_audio_process',
    '01_syrin_notification_message_process'
]
CREATED_QUEUES = [
    '02_syrin_notification_audio_process_categories,02_syrin_notification_audio_reprocess_categories', # Esse processo gerar o texto para ser transformando em TTS
    '03_syrin_notification_audio_process_categories,03_syrin_notification_audio_reprocess_categories', # Esse processso irar transformando o texto em TTS

    '02_syrin_notification_message_process_categories,02_syrin_notification_message_reprocess_categories', # Esse processo gerar o texto para ser enviado ao telegram
    '03_syrin_notification_message_process_categories,03_syrin_notification_message_reprocess_categories', # Esse processo irar enviando o texto ao telegram

    '05_syrin_notification_message_process_humanized,05_syrin_notification_message_reprocess_humanized',
]