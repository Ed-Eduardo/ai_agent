from functions.get_files_info import get_files_info

print("""
=================================================
Running: get_files_info("calculator", ".")
Expected:
Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True
Actual:""")
print(get_files_info("calculator", "."))

print("""
=================================================
Running: get_files_info("calculator", "pkg")
Expected:
Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False
Actual: """)
print(get_files_info("calculator", "pkg"))

print("""
=================================================
Running: get_files_info("calculator", "/bin")
Expected:
Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory
Actual:""")
print(get_files_info("calculator", "/bin"))

print("""
=================================================
Running: get_files_info("calculator", "../"):
Expected: 
Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory
Actual:""")
print(
get_files_info("calculator", "../"))