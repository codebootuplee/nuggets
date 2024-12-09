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
    """Forcefully delete the specified pods in the given namespace."""
    # Load the kubeconfig file
    config.load_kube_config()

    # Create the API client
    v1 = client.CoreV1Api()

    for pod_name in pod_names:
        try:
            print(f"Forcefully deleting pod: {pod_name}")
            v1.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace,
                body=client.V1DeleteOptions(),  # Pass empty delete options
                grace_period_seconds=0,
                propagation_policy="Foreground",
            )
            print(f"Pod {pod_name} deleted.")
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

    confirm = input("\nDo you want to force delete these pods? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        delete_pods(terminating_pods, namespace_to_check)
        print("Selected pods have been forcefully deleted.")
    else:
        print("No pods were deleted.")

if __name__ == "__main__":
    main()
