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

resource "kubernetes_manifest" "argocd_root_app" {
  depends_on = [helm_release.argocd]

  manifest = {
    "apiVersion" = "argoproj.io/v1alpha1"
    "kind"       = "Application"
    "metadata" = {
      "name"       = "root-app"
      "finalizers" = ["resources-finalizer.argocd.argoproj.io"]
      "namespace"  = helm_release.argocd.namespace
    }

    "spec" = {
      "project" = "default"
      "source" = {
        "repoURL"        = "https://github.com/MoonChel/lab.git"
        "path"           = "argocd/applications"
        "targetRevision" = "HEAD"
      }

      "destination" = {
        "server"    = "https://kubernetes.default.svc"
        "namespace" = helm_release.argocd.namespace
      }

      "syncPolicy" = {
        "automated" = {
          "selfHeal" = true
        }
      }
    }
  }
}
