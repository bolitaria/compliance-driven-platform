# Infrastructure compliance for K8s manifests

package main

deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.securityContext.readOnlyRootFilesystem == true
    msg = sprintf("Container '%s' must have readOnlyRootFilesystem: true", [container.name])
}

deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.securityContext.runAsNonRoot == true
    msg = sprintf("Container '%s' must run as non-root", [container.name])
}