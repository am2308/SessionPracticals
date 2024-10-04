import subprocess

# Execute a command and wait for it to complete
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

# Print the command's output
print("STDOUT:")
print(result.stdout)

# Print any errors
print("STDERR:")
print(result.stderr)
