# Nomes das filas utilizadas
INPUT_QUEUES = ['00_syrin_notification_critical', '00_syrin_notification_warning']
OUTPUT_QUEUES = [
    '01_syrin_notification_audio_process',
    '01_syrin_notification_message_process'
]
CREATED_QUEUES = [
    '02_syrin_notification_audio_process_categories,02_syrin_notification_audio_reprocess_categories', # Esse processo gerar o texto para ser transformando em TTS
    '03_syrin_notification_audio_process_tts,03_syrin_notification_audio_reprocess_tts', # Esse processso irar transformando o texto em TTS
    '04_syrin_notification_audio_process_play,03_syrin_notification_audio_reprocess_play', # Esse processso irar tocando o som

    '02_syrin_notification_message_process_categories,02_syrin_notification_message_reprocess_categories', # Esse processo gerar o texto para ser enviado ao telegram
    '03_syrin_notification_message_process_send,03_syrin_notification_message_reprocess_send' # Esse processo irar enviando o texto ao telegram
]