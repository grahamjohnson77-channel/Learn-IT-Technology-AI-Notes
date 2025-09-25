Series 2.1.2 Node Cluster Upgrades - GCP.md
*******************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

# Introduction

With multiple scenarios to verify and learn, we have multiple learning options we can use:

    # Option 1: GKE (Kubernetes Engine on GCP)
    
    SETUP README AVAILABLE HERE:
    https://github.com/cloudsolutionarchitects-dot-eu/youtube-series/blob/main/Series%201%20Introduction/Series%201.7%20Kubernetes%20on%20GCP%20Cloud%20-%20The%20GKE%20Way%20(Intermediate).md
    
    # Option 2: GCP Cluster (Single/Multi Node Cluster)
    
    SETUP README AVAILABLE HERE:
    https://github.com/cloudsolutionarchitects-dot-eu/youtube-series/blob/main/Series%201%20Introduction/Series%201.6%20Kubernetes%20on%20GCP%20Cloud%20-%20The%20Kubeadm%20Way%20(Intermediate).md
    
    # Option 3: RaspberryPi (Single/Multi Node Cluster)
    
    SETUP README AVAILABLE HERE:
    https://github.com/cloudsolutionarchitects-dot-eu/youtube-series/blob/main/Series%201%20Introduction/Series%201.5%20Kubernetes%20on%20Raspberry%20Pi%20(Intermediate).md
    
    # Option 4: Some other cloud provide like AWS, Azure or Linode
    
    # Option 5: Udemy Course, CloudGuru or another provider

Personally I will use (as already available to me):

    # For Scenario 1: Testing 'Node Unavailable' - Option 1: GKE (Kubernetes Engine on GCP)
    # For Scenario 2: Testing 'Node Upgrades' - Option 2: GCP Cluster
    (GKE will not work for this as no kubeadm command available!)
    # For Scenario 3: Practice 'Backup and Restore ETCD' - Option 2: GCP Cluster
    (GKE will not work for this as no etcdctl command available!)

Setup Test Fake Running Deployment for Verifications on GKE, GCP or RaspberryPi

    vi nginx-fake-deployment.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx-fake-deployment
    spec:
      selector:
        matchLabels:
          app: nginx
      replicas: 4
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:latest
            ports:
            - containerPort: 80
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: nginx-service
    spec:
      selector:
        app: nginx
      ports:
        - protocol: TCP
          port: 80
          targetPort: 80
      externalTrafficPolicy: Local
      type: LoadBalancer

    # Let’s apply it with:
    kubectl apply -f nginx-fake-deployment.yaml
    
    cloudsolutionarchitects_eu@cloudshell:~ (cka-gke-study-project)$ kubectl apply -f nginx-fake-deployment.yaml
    deployment.apps/nginx-deployment created
    service/nginx-service created

    # We can confirm that our pods are created by running
    kubectl get pods
    OR
    kubectl get pods -o wide
    
    # We can now check on our cluster from master node
    kubectl get nodes

    # Right now on either on GKE, GCP cluster or Pi, we can see we have at least 1 pod on each of the 1 nodes, because all allow traffic
    
    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage

    # Create Tmp Pod
    k run temppod --image=nginx --restart=Never --port=80                       # temp pod to verify deployment % weighting
    k exec -it temppod -- sh                                                    # log into temp pod

# Series 2.1.2 - Node Upgrades

## Q2. Node Upgrades
    # Using Option 2: GCP Cluster

    Upgrade the node to be the next version ...

    A.
    # You can use the apt-cache command to see what Kubernetes versions are supported for various versions:
    apt-cache madison kubeadm | grep 1.26
    
    apt-cache madison kubectl | grep 1.23
    apt-cache madison kubectl | grep 1.24
    apt-cache madison kubectl | grep 1.25
    apt-cache madison kubectl | grep 1.26
    
    etc.
    
    kubectl get nodes -o wide                                                                   # get the current version
    
    # prepare the node for maintenance by marking it unschedulable and evicting the workloads:
    kubectl drain controller --delete-local-data --ignore-daemonsets --force                    # drain controller on GCP cluster
    
    # log in as root to start you system upgrade
    
    # then ...

    # sample installations of various versions (good for practice of upgrading between versions)
    sudo apt install -y kubeadm=1.23.14-00 kubelet=1.23.14-00 kubectl=1.23.14-00              - version 23
    sudo apt install -y kubeadm=1.24.6-00 kubelet=1.24.6-00 kubectl=1.24.6-00                 - version 24
    sudo apt install -y kubeadm=1.25.6-00 kubelet=1.25.6-00 kubectl=1.25.6-00                 - version 25
    sudo apt install -y kubeadm=1.26.0-00 kubelet=1.26.0-00 kubectl=1.26.0-00                 - version 26
    sudo apt install -y kubeadm=1.26.1-00 kubelet=1.26.1-00 kubectl=1.26.1-00                 - version 26.1
    
    # OR from Kubernetes documentation

    # upgrade kubeadm
    apt-mark unhold kubeadm && \
    apt-get update && apt-get install -y kubeadm=1.26.x-00 && \
    apt-mark hold kubeadm
    
    # Verify that the download works and has the expected version
    kubeadm version
    
    # Verify the upgrade plan
    kubeadm upgrade plan
    
    # finally, upgrade to the new version!
    kubeadm upgrade apply 1.26.1 --etcd-upgrade=false
    
    # Upgrade the kubelet and kubectl
    apt-mark unhold kubelet kubectl && \
    apt-get update && apt-get install -y kubelet=1.26.x-00 kubectl=1.26.x-00 && \
    apt-mark hold kubelet kubectl
    
    # restart services & uncordon
    systemctl daemon-reload
    systemctl restart kubelet
    systemctl status kubelet
    
    kubectl uncordon controller
    
    # More info: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

    # NOTE: "apt-get install kubeadm=1.20.0-00 --disableexcludes=kubernetes" you are saying that you want to 
          install kubeadm and if it’s included in an excluded package called “kubernetes”, the system must include it.
          https://kodekloud.com/community/t/there-is-a-question-which-is-a-bit-confusing-set-the-node-named-node-1-as-unav/23693/2
