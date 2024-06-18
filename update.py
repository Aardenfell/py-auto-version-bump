import re
import subprocess

def update_version(new_version):
    file_path = './descriptor.mod'  # Update with your actual file path

    # Read current content from descriptor.mod
    with open(file_path, 'r') as f:
        content = f.read()

    # Update version attribute
    content = re.sub(r'version="[\d.]+"', f'version="{new_version}"', content)

    # Write updated content back to descriptor.mod
    with open(file_path, 'w') as f:
        f.write(content)

    # Run auto-changelog command
    subprocess.run(['auto-changelog.cmd', ['-p']])

    # Add CHANGELOG.md to staging area
    subprocess.run(['git', 'add', 'CHANGELOG.md'])

    # Commit the changes with Angular Conventional message
    commit_message = f"chore: bump version to {new_version}\n\nBREAKING CHANGE: None"
    subprocess.run(['git', 'commit', '-am', commit_message])

if __name__ == '__main__':
    new_version = input("Enter the new version number: ")
    update_version(new_version)
