Series 2.0.2 Kubernetes Architecture.md
***************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

# What is Kubernetes? 
    Allows Automated Hosting of Containerized Applications

    # Reminder to Review!
    https://en.wikipedia.org/wiki/Kubernetes

    # Reminder to Review Kubernetes Deployed on Raspberry PI
    https://www.youtube.com/watch?v=dQ8IGQo2QbA

    # Reminder to Review Kubernetes Deployed on GCP
    https://www.youtube.com/watch?v=T5SQuIofUu0

    # Kubernetes Components
    https://kubernetes.io/docs/concepts/overview/components/

    # Kubernetes Concepts Explained
    https://en.wikipedia.org/wiki/Kubernetes#:~:text=Kubernetes%20defines%20a%20set%20of%20building%20blocks%20%28%22primitives%22%29%2C,loosely%20coupled%20and%20extensible%20to%20meet%20different%20workloads.

    # ClickITTech Explaination
    https://www.clickittech.com/devops/kubernetes-architecture-diagram/

    # Architecture Diagram from Platform9
    https://platform9.com/blog/kubernetes-enterprise-chapter-2-kubernetes-architecture-concepts/

    # The Basics:
    Worker Nodes - Can Load Containers (Really do that work)
    Master Nodes - Manage, Plan, Schedule & Monitor Nodes (Stores Information related to these activities)
    Control Plane - Container orchestration layer that exposes the API and interfaces to define, deploy, and manage the lifecycle of containers

    # Glossary of Terms
    https://kubernetes.io/docs/reference/glossary/?all=true#term-control-plane

# Master Node

    # ETCD Cluster
    Key-Value Format Database. Stores information about the Cluster. Tracks containerized application loads in Key-value store.
    REF: https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/

    # Kube Controller Managers
    Manages ALL of the Controllers for Multiple Components. Controls Various Controllers such as Node-Controller (Watches Nodes for Changes like Unavailable), Replication-Controller (Controls Desired Number of Replicas Available).
    REF: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/
    kubectl get pods -n kube-system                             # list out the kube-controller-master pod (for kubeadm)
    cat /etc/kubernetes/manifests/kube-controller-manager.yaml      # view controller options (for kubeadm)
    cat /etc/systemd/system/kube-controller-manager.service         # view controller options (for non kubeadm)
    ps -aux | grep kube-controller-manager                          # see running processes on master node (for non kubeadm)

    # Kube API Server
    Orchestrates Operations in Cluster. Exposes Kubes API which is used for Management Operations on the Cluster.
    REF: https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver
    kubectl get pods -n kube-system                             # list out the apiserver-master pod (for kubeadm)
    cat /etc/kubernetes/manifests/kube-apiserver.yaml               # view api server options (for kubeadm)
    cat /etc/systemd/system/kube-apiserver.service                  # view api server options (for non kubeadm)
    ps -aux | grep kube-apiserver                                   # see running processes on master node (for non kubeadm)

    # Kube Scheduler
    Schedules or decides Apps or Containers on Nodes - Queries Kube API Server for Changes and Updates API Server Back. Scheduler identifies the correct node to place the container/pod/load onto, using various factors i.e. resource or policies contraints.
    REF: https://kubernetes.io/docs/concepts/overview/components/#kube-scheduler
    cat /etc/kubernetes/manifests/kube-scheduler.yaml           # view kube-scheduler options (for kubeadm)
    ps -aux | grep kube-scheduler                                   # see running processes on master node (for non kubeadm)

    # Cloud Controller Manager
    Control Plan components that embeds cloud specific control logic
    REF: https://kubernetes.io/docs/concepts/overview/components/#kube-proxy

    # Containerd, Rkt or Docker as Container Runtimes
    Controls the Different Components that are in the form of containers (DNS, Networking, Other Services etc.). Software that Runs these containers!
    REF: https://kubernetes.io/docs/setup/production-environment/container-runtimes/

# Worker Node

    # Kubelet
    Listens for Instructions from API Server and Manages Containers, Logs etc. Periodically fetches information from this as status reports.
    NOTE: Kubeadm does NOT deploy Kubelets ... it has to be always installed!
    REF: https://kubernetes.io/docs/concepts/overview/components/#kubelet
    ps -aux | grep kubelet                                      # see running processes on master node (for non kubeadm)

    # Kube Proxy
    Enables Communications and Services In the Cluster using an Internal Pod Network (uses Firewall Networking Rules).
    Example: One node with a web server and needs to communicate with another node that runs the database pod
    NOTE: Process - Its job is to look for new services, create a new FW rule to forward traffic from the backend pods to the new services that were found
    NOTE: It uses IP tables rules to forward the traffic from the IP of the service to the IP of the pod
    REF: https://kubernetes.io/docs/concepts/overview/components/#kube-proxy
    kubectl get pods -n kube-system                             # list out the kube-proxy pods (for kubeadm)
    kubectl get daemonset -n kube-system                            # kube proxy is deployed using a daemon set

    # Containerd, Rkt or Docker as Container Runtimes (Same Install as Master Node)
    Controls the Different Components that are in the form of containers (DNS, Networking, Other Services etc.). Software that Runs these containers!
    REF: https://kubernetes.io/docs/setup/production-environment/container-runtimes/
