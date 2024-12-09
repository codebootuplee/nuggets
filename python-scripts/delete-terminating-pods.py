from kubernetes import client, config

def list_terminating_pods(namespace="default"):
    """List pods in Terminating state in the specified namespace."""
    # Load the kubeconfig file
    config.load_kube_config()

    # Create the API client
    v1 = client.CoreV1Api()

    terminating_pods = []
    try:
        # List all pods in the given namespace
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            pod_name = pod.metadata.name
            pod_status = pod.status.phase
            pod_deletion_timestamp = pod.metadata.deletion_timestamp

            # Check if the pod is in Terminating state
            if pod_status == "Running" and pod_deletion_timestamp:
                terminating_pods.append(pod_name)
    except Exception as e:
        print(f"An error occurred while listing pods: {e}")

    return terminating_pods

def delete_pods(pod_names, namespace="default"):
    """Delete the specified pods in the given namespace."""
    # Load the kubeconfig file
    config.load_kube_config()

    # Create the API client
    v1 = client.CoreV1Api()

    for pod_name in pod_names:
        try:
            print(f"Deleting pod: {pod_name}")
            v1.delete_namespaced_pod(pod_name, namespace)
        except Exception as e:
            print(f"An error occurred while deleting pod {pod_name}: {e}")

def main():
    namespace_to_check = input("Enter the namespace to check for Terminating pods (default: 'default'): ") or "default"
    terminating_pods = list_terminating_pods(namespace_to_check)

    if not terminating_pods:
        print("No pods in Terminating state found.")
        return

    print("\nThe following pods are in Terminating state:")
    for pod_name in terminating_pods:
        print(f"- {pod_name}")

    confirm = input("\nDo you want to delete these pods? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        delete_pods(terminating_pods, namespace_to_check)
        print("Selected pods have been deleted.")
    else:
        print("No pods were deleted.")

if __name__ == "__main__":
    main()
