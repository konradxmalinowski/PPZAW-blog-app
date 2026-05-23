import re

PROFANITY_LIST = [
    'chuj', 'chuja', 'chujek', 'chujnia', 'chujowy', 'chujowa',
    'cipa', 'cipka', 'cipę',
    'cwel', 'cwela',
    'debil', 'debila', 'debilizm',
    'dupa', 'dupę', 'dupka', 'dupy',
    'dziwka', 'dziwki',
    'fuck', 'fucker', 'fucking',
    'gówno', 'gówna', 'gówniarz',
    'huj', 'huja',
    'idiot', 'idiota',
    'jebać', 'jebany', 'jebana', 'jebal', 'jebać', 'jebię',
    'jeb', 'jeba',
    'kretyn', 'kretyni',
    'kurwa', 'kurwy', 'kurwę', 'kurewski', 'kurewstwo',
    'kutas', 'kutasa', 'kutasem',
    'morda', 'mordo',
    'pizda', 'pizdy', 'pizdę',
    'pierdolić', 'pierdolony', 'pierdolona', 'pierdol', 'pierdole',
    'pierdoła',
    'shit', 'bitch', 'asshole', 'bastard',
    'skurwiel', 'skurwysyn', 'skurwysynu',
    'sperma',
    'wpierdol', 'wpierdolić',
    'wypierdalać', 'wypierdal',
    'zajebać', 'zajebany',
    'zasraniec',
    'zdechlak',
    'zjeb',
]

_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(w) for w in PROFANITY_LIST) + r')\b',
    re.IGNORECASE | re.UNICODE,
)


def contains_profanity(text: str) -> bool:
    return bool(_PATTERN.search(text))


def censor(text: str, char: str = '*') -> str:
    def _replace(m):
        return char * len(m.group())
    return _PATTERN.sub(_replace, text)
