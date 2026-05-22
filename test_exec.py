from app.services.safe_executor import execute_safe
code = """
import os
path = os.path.join(os.environ.get('USERPROFILE'), 'Desktop', 'TestFolder2')
os.makedirs(path, exist_ok=True)
print(f"Created {path}")
"""
print(execute_safe(code))
