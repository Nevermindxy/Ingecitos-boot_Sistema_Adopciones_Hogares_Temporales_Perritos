import hashlib, secrets, getpass
from pathlib import Path
if Path(__file__).with_name('.env').exists(): raise SystemExit('Ya existe .env. Respalda y renombra ese archivo antes de reconfigurar.')
p=getpass.getpass('Nueva contraseña de administrador (mínimo 10 caracteres): ')
if len(p)<10: raise SystemExit('Contraseña demasiado corta.')
if p!=getpass.getpass('Repite la contraseña: '): raise SystemExit('No coinciden.')
sal=secrets.token_hex(16)
h=hashlib.pbkdf2_hmac('sha256',p.encode(),sal.encode(),600000).hex()
Path(__file__).with_name('.env').write_text(f'HUELLITAS_LOGIN_USER=admin\nHUELLITAS_LOGIN_SALT={sal}\nHUELLITAS_LOGIN_HASH={h}\nHUELLITAS_DB_HOST=localhost\nHUELLITAS_DB_PORT=3306\nHUELLITAS_DB_USER=root\nHUELLITAS_DB_PASSWORD=\n')
print('Configuración creada. Edita .env si tu conexión MySQL es diferente.')
