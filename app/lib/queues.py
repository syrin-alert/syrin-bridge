# Nomes das filas utilizadas
INPUT_QUEUES = ['00_syrin_notification_critical', '00_syrin_notification_warning']
OUTPUT_QUEUES = [
    '01_syrin_notification_audio_process',
    '01_syrin_notification_message_process'
]
CREATED_QUEUES = [
    '02_syrin_notification_audio_process_categories,02_syrin_notification_audio_reprocess_categories',
    '02_syrin_notification_message_process_categories,02_syrin_notification_message_reprocess_categories',
    '05_syrin_notification_message_process_humanized,05_syrin_notification_message_reprocess_humanized',
]