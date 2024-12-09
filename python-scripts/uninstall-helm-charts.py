import subprocess
import json

def list_helm_releases(namespace="default"):
    """List all Helm releases in the specified namespace."""
    try:
        # Run `helm list` and parse the output as JSON
        cmd = ["helm", "list", "--namespace", namespace, "-o", "json"]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        releases = json.loads(result.stdout)
        return [release["name"] for release in releases]
    except subprocess.CalledProcessError as e:
        print(f"Error listing Helm releases: {e.stderr}")
        return []

def uninstall_helm_release(release_name, namespace="default"):
    """Uninstall a Helm release."""
    try:
        # Run `helm uninstall`
        cmd = ["helm", "uninstall", release_name, "--namespace", namespace]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Uninstalled release: {release_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error uninstalling release {release_name}: {e.stderr}")

def main():
    namespace = input("Enter the namespace to check for Helm releases (default: 'default'): ") or "default"

    # List all Helm releases in the namespace
    releases = list_helm_releases(namespace)

    if not releases:
        print("No Helm releases found.")
        return

    print("\nThe following Helm releases will be uninstalled:")
    for release in releases:
        print(f"- {release}")

    confirm = input("\nDo you want to uninstall these releases? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        for release in releases:
            uninstall_helm_release(release, namespace)
        print("All selected releases have been uninstalled.")
    else:
        print("No releases were uninstalled.")

if __name__ == "__main__":
    main()
