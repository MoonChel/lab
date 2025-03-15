provider "helm" {
  kubernetes {
    config_path    = "/etc/rancher/k3s/k3s.yaml"
    config_context = "default"
  }
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.8.10"
  create_namespace = true

  values = [file("${path.module}/values/argocd.yaml")]
}
