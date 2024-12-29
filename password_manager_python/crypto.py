import nacl.secret
import nacl.utils
import nacl.encoding
import nacl.hash
from password_manager_python import system_interact

def hash_sha256(msg:bytes) -> bytes:
    HASHER = nacl.hash.sha256
    digest = HASHER(msg, encoder=nacl.encoding.RawEncoder)
    return digest
     
def encrypt(_plain:bytes, _master_password:bytes|None = None) -> nacl.utils.EncryptedMessage: 
    key = _master_password or system_interact.get_master_password()
    box = nacl.secret.SecretBox(hash_sha256(key))
    return box.encrypt(_plain)

def decrypt(_cipher:nacl.utils.EncryptedMessage, _master_password:bytes|None = None) -> bytes: 
    key = _master_password or system_interact.get_master_password()
    box = nacl.secret.SecretBox(hash_sha256(key))
    return box.decrypt(_cipher)