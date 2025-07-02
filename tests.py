# project_root/tests.py
import os
import shutil

# --- Setup for testing environment ---
current_dir = os.path.dirname(os.path.abspath(__file__))
functions_dir = os.path.join(current_dir, "functions")
calculator_dir = os.path.join(current_dir, "calculator")
calculator_pkg_dir = os.path.join(calculator_dir, "pkg")

os.makedirs(functions_dir, exist_ok=True)
os.makedirs(calculator_dir, exist_ok=True)
os.makedirs(calculator_pkg_dir, exist_ok=True)

# Create dummy files and directories for testing get_file_content
# Ensure main.py and calculator.py exist
with open(os.path.join(calculator_dir, "main.py"), "w") as f:
    f.write("def main():\n    pass\n")

# Using 'calculator.py' in pkg for the test case
with open(os.path.join(calculator_pkg_dir, "calculator.py"), "w") as f:
    f.write("class Calculator:\n    def _apply_operator(self, operators, values):\n        pass\n")

# Create lorem.txt with at least 20,000 characters
lorem_ipsum_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
(Repeat this block many times to exceed 20,000 characters)
""" * 100 # Repeat 100 times to ensure it's well over 20,000 chars

with open(os.path.join(calculator_dir, "lorem.txt"), "w") as f:
    f.write(lorem_ipsum_text)

# Import the new function
from functions.get_files_info import get_file_content

# --- Test Cases for get_file_content ---

print("--- Testing get_file_content ---")

print("\nResult for 'calculator/lorem.txt' (should be truncated):")
lorem_content = get_file_content("calculator", "lorem.txt")
print(lorem_content[:120] + "..." + lorem_content[-50:]) # Print beginning, middle indicator, and end for truncation check
assert "[...File \"lorem.txt\" truncated at 10000 characters]" in lorem_content
assert len(lorem_content) <= 10000 + len('[...File "lorem.txt" truncated at 10000 characters]')


print("\nResult for 'calculator/main.py':")
main_py_content = get_file_content("calculator", "main.py")
print(main_py_content)
assert "def main():" in main_py_content
assert "pass" in main_py_content

print("\nResult for 'calculator/pkg/calculator.py':")
pkg_calculator_content = get_file_content("calculator", "pkg/calculator.py")
print(pkg_calculator_content)
assert "def _apply_operator(self, operators, values):" in pkg_calculator_content
assert "class Calculator:" in pkg_calculator_content


print("\nResult for '/bin/cat' (should return an error for out-of-bounds):")
bin_cat_content = get_file_content("calculator", "/bin/cat")
print(bin_cat_content)
assert "Error: Cannot read \"/bin/cat\" as it is outside the permitted working directory" in bin_cat_content

# Clean up dummy files and directories after tests
# Be careful with shutil.rmtree - ensure you're deleting test data
# shutil.rmtree(calculator_dir)
# os.remove(os.path.join(functions_dir, "get_file_content.py"))
# If get_files_info.py is also in functions_dir, and you plan to reuse it, don't delete functions_dir
# os.rmdir(functions_dir) # Only if functions_dir is empty after deleting files


# --- Test Cases for write_file ---
from functions.get_files_info import write_file
print("--- Testing write_file ---")

print("\nResult for 'calculator/lorem.txt' (overwrite existing file):")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("\nResult for 'calculator/pkg/morelorem.txt' (overwrite existing file):")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("\nResult for '/tmp/temp.txt' (should return an error for out-of-bounds):")
# Note: On some systems, /tmp might be within the permitted path for the user running the test.
# However, the guardrail logic should still catch it if working_directory is "calculator"
# as /tmp is not a subpath of /calculator.
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

# Optional: Verify file contents after writing (for local testing, not part of CLI submission)
# with open(os.path.join(calculator_dir, "lorem.txt"), "r") as f:
#     print(f"\nContent of lorem.txt after write: {f.read()}")
# with open(os.path.join(calculator_pkg_dir, "morelorem.txt"), "r") as f:
#     print(f"Content of pkg/morelorem.txt after write: {f.read()}")

# Clean up dummy files and directories after tests
# shutil.rmtree(calculator_dir)
# os.remove(os.path.join(functions_dir, "file_operations.py")) # If you renamed
# os.rmdir(functions_dir) # Only if functions_dir is empty
