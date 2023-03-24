import hashlib
import subprocess

# Compute the SHA-256 hash of a file
def hash_file(file_path):
    with open(file_path, 'rb') as f:
        hasher = hashlib.sha256()
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
        return hasher.hexdigest()

# Compute the SHA-256 hash of the source code
source_hash = hash_file('main.py')
print('Source hash:', source_hash)

# Compile the code using PyInstaller
subprocess.call(['pyinstaller', '--onefile', 'main.py'])

# Compute the SHA-256 hash of the compiled binary
binary_hash = hash_file('dist/main')
print('Binary hash:', binary_hash)

# Compare the hashes
if source_hash == binary_hash:
    print('Verification successful: the compiled binary matches the source code')
else:
    print('Verification failed: the compiled binary does not match the source code')
