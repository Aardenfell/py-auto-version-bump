import re
import subprocess
import json

def get_current_version():
    # Read current version from descriptor.mod
    descriptor_mod_path = './descriptor.mod'  # Update with your actual file path
    current_version = read_descriptor_mod_version(descriptor_mod_path)

    if not current_version:
        # If descriptor.mod does not contain version, read from package.json
        package_json_path = './package.json'  # Update with your actual file path
        current_version = read_package_json_version(package_json_path)

    return current_version

def read_descriptor_mod_version(file_path):
    try:
        # Read version from descriptor.mod
        with open(file_path, 'r') as f:
            content = f.read()
            match = re.search(r'version="([\d.]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass  # Handle file not found error

    return None

def read_package_json_version(file_path):
    try:
        # Read version from package.json
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get('version')
    except FileNotFoundError:
        pass  # Handle file not found error

    return None

def update_descriptor_mod_version(file_path, new_version):
    try:
        # Update version in descriptor.mod
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Update version in descriptor.mod
        with open(file_path, 'w') as f:
            content = re.sub(r'version="([\d.]+)"', f'version="{new_version}"', content)
            f.write(content)
    except FileNotFoundError:
        pass  # Handle file not found error

def update_package_json_version(file_path, new_version):
    try:
        # Update version in package.json
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        data['version'] = new_version
        
        # Write updated content back to package.json
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        pass  # Handle file not found error

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
    current_version = get_current_version()
    commit_message = f"chore: bump version from {current_version} to {new_version}"
    subprocess.run(['git', 'commit', '-am', commit_message])

    # Tag the commit with the new version
    subprocess.run(['git', 'tag', new_version])

    # Push the commit and tag to origin
    subprocess.run(['git', 'push', 'origin', new_version])

if __name__ == '__main__':
    current_version = get_current_version()
    new_version = input(f"Enter the new version number (current version is {current_version}): ")
    update_version(new_version)
