import subprocess
import json

def list_terminating_pods(namespace="default"):
    """List pods in Terminating state using kubectl."""
    try:
        # Run `kubectl get pods` and parse the output as JSON
        cmd = ["kubectl", "get", "pods", "-n", namespace, "-o", "json"]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pods = json.loads(result.stdout)

        terminating_pods = []
        for pod in pods["items"]:
            pod_name = pod["metadata"]["name"]
            pod_phase = pod["status"]["phase"]
            deletion_timestamp = pod["metadata"].get("deletionTimestamp")

            # Identify Terminating pods
            if pod_phase == "Running" and deletion_timestamp:
                terminating_pods.append(pod_name)

        return terminating_pods
    except subprocess.CalledProcessError as e:
        print(f"Error listing pods: {e.stderr}")
        return []

def force_delete_pod(pod_name, namespace="default"):
    """Force delete a pod using kubectl."""
    try:
        print(f"Forcefully deleting pod: {pod_name}")
        cmd = ["kubectl", "delete", "pod", pod_name, "-n", namespace, "--grace-period=0", "--force"]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Pod {pod_name} deleted.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting pod {pod_name}: {e.stderr}")

def main():
    namespace_to_check = input("Enter the namespace to check for Terminating pods (default: 'default'): ") or "default"
    terminating_pods = list_terminating_pods(namespace_to_check)

    if not terminating_pods:
        print("No pods in Terminating state found.")
        return

    print("\nThe following pods are in Terminating state:")
    for pod_name in terminating_pods:
        print(f"- {pod_name}")

    confirm = input("\nDo you want to force delete these pods? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        for pod in terminating_pods:
            force_delete_pod(pod, namespace_to_check)
        print("Selected pods have been forcefully deleted.")
    else:
        print("No pods were deleted.")

if __name__ == "__main__":
    main()
