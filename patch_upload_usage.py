from pathlib import Path
p = Path('/opt/cuh-ctf/scripts/registrar_bruteforce_via_internal.sh')
text = p.read_text(encoding='utf-8')
text = text.replace("loc=upload_file(file_obj=fs, challenge_id=challenge.id)\n        db.session.add(ChallengeFiles(type='challenge',location=loc,challenge_id=challenge.id,page_id=None))", "upload_file(file=fs, type='challenge', challenge_id=challenge.id)")
p.write_text(text, encoding='utf-8')
print('patched upload_file usage')
