MAX_SYMBOLS = 16
DATA_DICT ={
    'original': 'original',
    'short': 'custom_id'
}

SHORT_ID_EXISTS = "Ссылка {custom_id} уже существует!"
SHORT_ID_INVALID = "Ссылка должна состоять только из цифр и латинских букв!"
SHORT_ID_REGEXP = r'^[A-Za-z0-9]*$'

EMPTY_REQUEST = 'В запросе необходимо ввести ссылку'