import pytest
from unittest.mock import patch, MagicMock
from kube_secure import scanner

@patch("kube_secure.scanner.client.CoreV1Api")
def test_check_pods_running_as_root_detects_root(mock_api):
    # Create a fake pod with container running as UID 0
    pod = MagicMock()
    pod.metadata.namespace = "default"
    pod.metadata.name = "nginx"
    pod.spec.security_context = None

    container = MagicMock()
    container.security_context.run_as_user = 0
    pod.spec.containers = [container]

    mock_api.return_value.list_pod_for_all_namespaces.return_value.items = [pod]

    results = scanner.check_pods_running_as_root()
    assert isinstance(results, list)
    assert results[0]["Namespace"] == "default"
    assert results[0]["Pod name"] == "nginx"
