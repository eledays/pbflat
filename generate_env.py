import os
import secrets 
from config import Config

if os.path.exists(Config.BASE_DIR / '.env'):
    print('.env файл уже существует. Если вы уверены, что хотите пересоздать, сначала удалите его.')
    exit()

with open(Config.BASE_DIR / '.env', 'w') as f:
    f.write(
        f'SECRET_KEY={secrets.token_hex(32)}\n'
        f'OAUTH_CLIENT_ID={secrets.token_hex(24)}\n'
        f'OAUTH_CLIENT_SECRET={secrets.token_hex(32)}'
    )