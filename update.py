import re
import subprocess
import json

def update_version(new_version):
    # Update descriptor.mod file
    descriptor_mod_path = './descriptor.mod'  # Update with your actual file path
    update_descriptor_mod_version(descriptor_mod_path, new_version)

    # Update package.json file
    package_json_path = './package.json'  # Update with your actual file path
    update_package_json_version(package_json_path, new_version)

    # Run auto-changelog command
    subprocess.run(['auto-changelog.cmd', '-p'])

    # Add CHANGELOG.md to staging area
    subprocess.run(['git', 'add', 'CHANGELOG.md'])

    # Commit the changes with Angular Conventional message
    commit_message = f"chore: bump version to {new_version}"
    subprocess.run(['git', 'commit', '-am', commit_message])

def update_descriptor_mod_version(file_path, new_version):
    # Read current content from descriptor.mod
    with open(file_path, 'r') as f:
        content = f.read()

    # Update version attribute
    content = re.sub(r'version="[\d.]+"', f'version="{new_version}"', content)

    # Write updated content back to descriptor.mod
    with open(file_path, 'w') as f:
        f.write(content)

def update_package_json_version(file_path, new_version):
    # Read package.json
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Update version attribute
    data['version'] = new_version

    # Write updated content back to package.json
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    new_version = input("Enter the new version number: ")
    update_version(new_version)
