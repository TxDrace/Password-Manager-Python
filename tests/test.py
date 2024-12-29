from password_manager_python import db_jobs
import typer

# password = "anh tuyen rat dep chai @ 1235436"
# encrypted = crypto.encrypt(password.encode("utf-8"))
# typer.echo(f"Encrypted: {encrypted} \n Type: {type(encrypted)}")

# decrypted = crypto.decrypt(encrypted)
# typer.echo(f"Decrypted: {decrypted} \n Type: {type(decrypted)}")

# print(crypto.hash_sha256("hehehe"))


typer.echo(db_jobs.query_all_credentials()) 