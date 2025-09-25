Series 1.6 Kubernetes on GCP Cloud - The Kubeadm Way (Intermediate).md
**********************************************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@cloudsolutionarchitects-dot

# Everything you need to know about kubernetes networking on GCP
    https://www.tigera.io/blog/everything-you-need-to-know-about-kubernetes-networking-on-google-cloud/

    More Information here on kubeadm and other Kubernetes technologies:
    https://kubernetes.io/docs/reference/setup-tools/kubeadm/
    https://containerd.io/
    https://prometheus.io/
    https://www.envoyproxy.io/
    https://coredns.io/

    # Kubernetes Certified Exam
    https://www.cncf.io/certification/cka/

# Section 01 Prerequisites - GCP Free vs Billing

    # IMPORTANT:
    IF A NEW GCP ACCOUNT, PLEASE MAKE SURE TO ENABLE THE 300 US OR EUR CREDIT ON THE ACCOUNT SO NOT TO BE CHARGED.

    Please see here before you build anything on GCP !
    https://cloud.google.com/free

    IF EXISTING ACCOUNT, PLEFASE MAKE SURE YOU HAVE ENABLED BILLING FOR THE NEW PROJECT ! MORE INFORMATION HERE:
    https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
    SEARCH 'BILLING' AND IT SHOULD COME UP 'LINK A BILLING ACCOUNT' TO THIS PROJECT ... 
    SEARCH FOR 'ACCOUNT MANAGEMENT' TO SEE WHICH PROJECTS HAVE BILLING ENABLED !

    # TIP: Always look at the GCP free tier options to see if you can use those first !
    https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits

    gcloud auth login                                                           # gcp auth login

    gcloud projects list --sort-by=projectId --limit=5                          # list projects

    gcloud config set project <PROJECT ID>                                      # set project (using project ID for your project)

      e.g.
      cloudsolutionarchitects_eu@cloudshell:~ (cka-study-k8s-374707)$

    # To see what your default region and zone settings are, run the following gcloud command:
    gcloud compute project-info describe --project 'Your own project id here'

## Section 02a Prerequisites - GCP Setup

    gcloud compute regions list                                                 # list regions
    gcloud compute zones list                                                   # list zones

    gcloud config set compute/region europe-west1                               # set region
    gcloud config set compute/zone europe-west1-b                               # set zone

    # List of GCP regions/zones here:
    https://cloud.google.com/compute/docs/regions-zones
    
    # Create the VPC
    gcloud compute networks create cka-study-k8s --subnet-mode custom

    # Create the k8s-nodes subnet in the cka-study-k8s VPC network:
    gcloud compute networks subnets create k8s-nodes \
      --network cka-study-k8s \
      --range 10.240.0.0/24

    # Create a firewall rule that allows internal communication across TCP, UDP, ICMP and IP in IP (used for the Calico overlay):
    gcloud compute firewall-rules create cka-study-k8s-allow-internal \
      --allow tcp,udp,icmp,ipip \
      --network cka-study-k8s \
      --source-ranges 10.240.0.0/24

    # Create a firewall rule that allows external SSH, ICMP, and HTTPS:
    gcloud compute firewall-rules create cka-study-k8s-allow-external \
      --allow tcp:22,tcp:6443,icmp \
      --network cka-study-k8s \
      --source-ranges 0.0.0.0/0

    # Get List of FW rules
    gcloud compute firewall-rules list --filter "network: cka-study-k8s"
    
## Section 02b Prerequisites - VM Setup

    # Get List of GCP Images
    gcloud compute images list | grep ubuntu -A2 -B2

    # Create the controller VM:
    gcloud compute instances create controller \
      --async \
      --boot-disk-size 200GB \
      --can-ip-forward \
      --image-family ubuntu-2004-lts \
      --image-project ubuntu-os-cloud \
      --machine-type e2-standard-2 \
      --private-network-ip 10.240.0.11 \
      --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
      --subnet k8s-nodes \
      --zone europe-west1-b \
      --tags cka-study-k8s,controller

    # Check the status
    gcloud compute operations describe <URI>

    # Create three worker VMs:
    for i in 0 1 2; do
      gcloud compute instances create worker-${i} \
        --async \
        --boot-disk-size 200GB \
        --can-ip-forward \
        --image-family ubuntu-2004-lts \
        --image-project ubuntu-os-cloud \
        --machine-type e2-standard-2 \
        --private-network-ip 10.240.0.2${i} \
        --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
        --subnet k8s-nodes \
        --zone europe-west1-b \
        --tags cka-study-k8s,worker
    done

    # Get list of GCP VMs from GCP CLI !
    gcloud compute instances list

    # Some useful commands for troubleshooting
    Get Kubectl Version - kubectl version
    Get System OS version - cat /etc/os-release
    Get Kernel Information - uname -a
    Get Docker Information - docker -v
    Show Linux Packages for Kube - rpm -qa | grep kube
    
## Section 02c Prerequisites - VM Installation

# ALL Nodes

    # SSH Into the new VM in cloud console

    # On Root: Disable swap on ubuntu if cluster not starting
    sudo -i
    swapoff -a
    exit

    # On Root: Install tools like 'ifconfig' etc.
    sudo -i
    apt install net-tools
    exit

    # Section 03 Kubernetes Cluster on GCP - Cluster Kubeadm
    sudo apt update
    sudo apt upgrade
    sudo apt dist-upgrade

    # We need to add Kubernetes repository to all nodes:
    sudo apt-get install apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

    # Update repo and install kubeadm on all nodes:
    sudo apt-get update

    # Install latest version?
    # NOTE: This cmd will install kubelet, kubectl and kubeadm in 1
    sudo apt-get install kubeadm

    # NOTE: This will install the following components:
    Get:6 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubelet amd64 1.26.0-00 [20.5 MB]
    Get:7 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubectl amd64 1.26.0-00 [10.1 MB]
    Get:8 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubeadm amd64 1.26.0-00 [9730 kB]

    OR

    # Install specific version?
    https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

    # You can use the apt-cache command to see what Kubernetes versions are supported for various versions:
    apt-cache madison kubectl | grep 1.23
    apt-cache madison kubectl | grep 1.24
    apt-cache madison kubectl | grep 1.25
    apt-cache madison kubectl | grep 1.26

    # sample installations of various versions (good for practice of upgrading between versions)
    sudo apt install -y kubeadm=1.23.14-00 kubelet=1.23.14-00 kubectl=1.23.14-00              - version 23
    sudo apt install -y kubeadm=1.24.6-00 kubelet=1.24.6-00 kubectl=1.24.6-00                 - version 24
    sudo apt install -y kubeadm=1.25.6-00 kubelet=1.25.6-00 kubectl=1.25.6-00                 - version 25
    sudo apt install -y kubeadm=1.26.0-00 kubelet=1.26.0-00 kubectl=1.26.0-00                 - version 26

    # Mark hold
    sudo apt-mark hold kubelet kubeadm kubectl

    # containerd considered more for CPU, memory, and startup times than Docker. Plus GKE and AWS use it !
    More Information here: https://containerd.io/

    # First we are going to handle prerequisites on all nodes:
    echo 'overlay
    br_netfilter' | sudo tee -a /etc/modules-load.d/containerd.conf
    sudo modprobe overlay
    sudo modprobe br_netfilter
    echo 'net.bridge.bridge-nf-call-iptables  = 1
    net.ipv4.ip_forward                 = 1
    net.bridge.bridge-nf-call-ip6tables = 1' | sudo tee -a /etc/sysctl.d/99-kubernetes-cri.conf
    sudo sysctl --system

    Now we can add the repository and install containerd to all nodes:

    # Install containerd
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Add Docker apt repository.
    sudo add-apt-repository \
       "deb https://download.docker.com/linux/ubuntu \
       focal \
       stable"

    # Install containerd
    sudo apt-get update
    sudo apt-get install containerd.io

    # Configure containerd
    sudo containerd config default | sudo tee /etc/containerd/config.toml

    # Restart containerd
    sudo systemctl restart containerd
    sudo systemctl status containerd

    The core configuration file is /etc/systemd/system/kubelet.service.d/10-kubeadm.conf and its contents are shown below.

    # Now we would need to configure kubelet agent to use containerd, so let’s edit:
    sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

    and add the line below under other Environment settings:
    Environment="KUBELET_EXTRA_ARGS=--cgroup-driver=systemd --container-runtime=remote --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock"

    # Reloading and restarting deamon is what we are going to do next:
    sudo systemctl daemon-reload
    sudo systemctl enable kubelet.service
    sudo systemctl restart kubelet.service

    # NOTE: kubelet service will not be running until we install kubernetes using kubeadm !

    # We will configure endpoint for crictl, which is basically what can be use for interaction with containers instead of docker:
    sudo vi /etc/crictl.yaml

    # Add this line:
    runtime-endpoint: unix:///run/containerd/containerd.sock
    
    # Exit line mode and save /etc/crictl.yaml file
    ESC then wq!

# Master Node Only

    # Next, we will prefetch kubernetes system images and initialize our master node with LATEST VERSION:

    # Install latest version?
    sudo kubeadm config images pull
    sudo kubeadm init --pod-network-cidr 10.240.0.0/24 --cri-socket /run/containerd/containerd.sock

    OR

    # Install specific version?
    Use kubeadm to install the SPECIFIC VERSION of Kubernetes:

    # Install v26 but really could be v23, v24, v25, v26 etc for testing
    sudo kubeadm config images pull --kubernetes-version v1.26.0
    sudo kubeadm init --cri-socket /run/containerd/containerd.sock \
        --pod-network-cidr=10.240.0.0/24 \
        --kubernetes-version v1.26.0
    
    # You should get successful installation on screen
    Your Kubernetes control-plane has initialized successfully!

    # NOTE: DO NOT RUN! Just showing more advanced options are available for kubadm, so worth exploring other options too
    sudo kubeadm init   --pod-network-cidr=10.244.0.0/16   --upload-certs --kubernetes-version=v1.24.0  --control-plane-endpoint=$(hostname) --ignore-  preflight-errors=all  --cri-socket /var/run/cri-dockerd.sock

    # NOTE:
    Copy the kubeadm join command out to run it later on the worker nodes!

    # Let’s configure kubectl for our user:
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    Please note that the printout of the init command will contain keys you need in order to join nodes to the cluster.

    # Here, I rebooted:
    sudo reboot
    
    # After reboot is complete ... log back onto master controller to verify ...

    # This will take a minute or two, so we can monitor the progress with (on master node):
    kubectl get pods --all-namespaces

    # We can now check on our cluster from master node:
    kubectl get nodes

    NAME         STATUS     ROLES           AGE    VERSION
    controller   NotReady   control-plane   107s   v1.26.0
    
    NOTE: The NotReady status is expected here ...

# Worker Nodes Only

    # NOTE: First, I had to reboot all to make sure the master was available to join!

    Remember to Skip this if you only have 1 controller node and no workder nodes !

    # You should ran that command on all worker nodes. e.g.
    
    # Log in as root
    sudo -i

    # DO NOT COPY THIS COMMAND. USE ONE YOU GOT AS RESULT IN INIT for Worker Nodes:
    sudo kubeadm join 10.240.0.11:6443 --token 8unvaj.p2jj59kpdm7uw0vp \
      --discovery-token-ca-cert-hash sha256:fdb9b03cfe5c5fc9845cda1524769a3788b5c6e4077d6429aa8aaf4b3d18769

    # NOTE: Find the join cmd if lost:
    kubeadm token create --print-join-command

    # Output:
    This node has joined the cluster:
    * Certificate signing request was sent to apiserver and a response was received.
    * The Kubelet was informed of the new secure connection details.

    We can now check on our cluster from master node:
    kubectl get nodes
    
    That’s it for now. Note that nodes are marked as not running, because there is no networking between them yet.

# Section 04 Kubernetes Cluster on GCP - Networking

# Master Node Only

    Project Calico — Installation on MASTER NODE ONLY!
    
    # Remove any existing taints now for the controller
    kubectl taint node controller node.kubernetes.io/not-ready:NoSchedule-

    # NOTE: On installation of Worker, it can take a while for master and worker to come back as STATUS Ready.
    
    # New Calico installation (use this!)
    kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml

    # I just ran this too!
    kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/tigera-operator.yaml
    kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/custom-resources.yaml
    kubectl taint node controller node-role.kubernetes.io/control-plane:NoSchedule-
    
    # More Notes here on the new method!
    https://docs.tigera.io/calico/3.25/getting-started/kubernetes/quickstart

    # Older Calico installation
    # First, we need to download calico configuration file on master node:
    #curl https://docs.projectcalico.org/manifests/calico.yaml -O

    # CIDR IP block will automatically be detected so we can just apply yaml to our cluster
    #kubectl apply -f calico.yaml

    # On GCP, it took about 10-12 minutes for pods to be running state, so we can monitor the progress with:
    kubectl get pods --all-namespaces

    pi@master:~$ kubectl get pods --all-namespaces
    NAMESPACE     NAME                                      READY   STATUS             RESTARTS        AGE
    kube-system   calico-kube-controllers-7bdbfc669-82cjx   1/1     Running            2 (56s ago)     2m54s
    kube-system   calico-node-cmkjp                         1/1     Running            3 (32s ago)     2m54s
    kube-system   coredns-787d4945fb-5829t                  1/1     Running            2 (2m6s ago)    10m
    kube-system   coredns-787d4945fb-phdww                  1/1     Running            2 (2m2s ago)    10m
    kube-system   etcd-controller                           1/1     Running            3 (98s ago)     11m
    kube-system   kube-apiserver-controller                 1/1     Running            3 (5m18s ago)   11m
    kube-system   kube-controller-manager-controller        1/1     Running            8 (2m6s ago)    11m
    kube-system   kube-proxy-pxb5s                          0/1     CrashLoopBackOff   7 (33s ago)     10m
    kube-system   kube-scheduler-controller                 1/1     Running            3 (107s ago)    11m

    # Once all pods are running we can confirm that all our nodes now are now in a ready state by running:
    kubectl get nodes

    NAME         STATUS   ROLES           AGE     VERSION
    controller   Ready    control-plane   9m27s   v1.26.0

    Congratulations your Kubernetes cluster is now running on GCP!

    # Before I could start to use the cluster, check existing taints:
    kubectl describe node controller | grep Taints
    Taints:             node-role.kubernetes.io/control-plane:NoSchedule

    # I had to remove the existing taint:
    kubectl taint node controller node-role.kubernetes.io/control-plane:NoSchedule-
    node/controller untainted

    # Alternative to Calico is Flannel:
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Section 05 Kubernetes Cluster on GCP - LoadBalancing

    # MetalLB Load Balancer Installation on MASTER NODE
    As we don’t have an external load balancer, we are going to need a software solution, and metalLB looks like a good choice.

    There are some compatibility issues with Calico and metaLB and you can read about them more here.

    However, they are not important for what we are trying to do.

    # On our master node let’s install our load balancer.

    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/namespace.yaml
    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/metallb.yaml

    # On first install only
    kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"

    Now we need to configure our IP pool. Make sure it is out of address range for your local DHCP, but that is in range for your router’s local network.

    # Let’s save config map below as: 

    vi metalLB-config.yaml

    apiVersion: v1
    kind: ConfigMap
    metadata:
      namespace: metallb-system
      name: config
    data:
      config: |
        address-pools:
        - name: default
          protocol: layer2
          addresses:
          - 10.240.0.200-10.240.254.254

    Run:
    kubectl apply -f metalLB-config.yaml

# Section 06 Kubernetes Cluster on GCP - Validations

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

    NAME                                READY   STATUS    RESTARTS   AGE   IP             NODE         NOMINATED NODE   READINESS GATES
    nginx-deployment-6b7f675859-2dcfm   1/1     Running   0          12s   10.240.0.133   controller   <none>           <none>
    nginx-deployment-6b7f675859-7pb66   1/1     Running   0          12s   10.240.0.136   controller   <none>           <none>
    nginx-deployment-6b7f675859-bnjwg   1/1     Running   0          12s   10.240.0.135   controller   <none>           <none>
    nginx-deployment-6b7f675859-bvbb2   1/1     Running   0          12s   10.240.0.134   controller   <none>           <none>
    
    # IMPORTANT NOTE: IF you see pods are not starting, yet the kubectl service is started (active state) ...
    
    cloudsolutionarchitects_eu@controller:~$ kubectl get pods -o wide
    NAME                                READY   STATUS    RESTARTS   AGE    IP       NODE     NOMINATED NODE   READINESS GATES
    nginx-deployment-6b7f675859-2bfqb   0/1     Pending   0          3m3s   <none>   <none>   <none>           <none>
    nginx-deployment-6b7f675859-2pdch   0/1     Pending   0          3m3s   <none>   <none>   <none>           <none>
    nginx-deployment-6b7f675859-6cc82   0/1     Pending   0          3m3s   <none>   <none>   <none>           <none>
    nginx-deployment-6b7f675859-rqkf8   0/1     Pending   0          3m3s   <none>   <none>   <none>           <none>
    
    # Then describe a pod and see if there is some message like the following for taints:
    kubectl describe pod nginx-deployment-6b7f675859-2bfqb
    
        Events:
      Type     Reason            Age    From               Message
      ----     ------            ----   ----               -------
      Warning  FailedScheduling  2m15s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
    
    # NOTE: Before I could start to use the cluster, I had to remove the existing taint:
    pi@master:~$ kubectl describe node master | grep Taints
    Taints:             node-role.kubernetes.io/control-plane:NoSchedule

    kubectl taint node controller node-role.kubernetes.io/control-plane:NoSchedule-

    # Now we need to retrieve an external IP address from the service:
    kubectl get svc nginx-service

    e.g.
    NAME            TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)        AGE
    nginx-service   LoadBalancer   10.100.178.187   10.240.0.200   80:30956/TCP   38s

    # We can use curl to check if everything works fine:
    #change IP address to one that you got by running previous command:
    curl 10.240.0.200

    e.g.
    cloudsolutionarchitects_eu@controller:~$ curl 10.240.0.200
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>

    Traffic should be available on multiple nodes:
    NAME                               READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
    nginx-deployment-cd55c47f5-cx5rc   1/1     Running   0          46s   172.16.196.130   node01   <none>           <none>
    nginx-deployment-cd55c47f5-mgnbv   1/1     Running   0          46s   172.16.219.100   master   <none>           <none>
    nginx-deployment-cd55c47f5-qrbqz   1/1     Running   0          46s   172.16.219.101   master   <none>           <none>
    nginx-deployment-cd55c47f5-wc8gw   1/1     Running   0          46s   172.16.196.129   node01   <none>           <none>

    Before we go let’s do some cleanup and remove our nginx test deployment.

    # Finally, please delete the resources to save credits or money!
    
    # Just make sure you don't need the new setup for more studying!
    kubectl delete -f nginx-fake-deployment.yaml

    # IMPORTANT! PLEASE REMEMBER TO DELETE THE COMPLETE PROJECT OFF GCP IF NOT NEEDED, OR YOU WILL BE CHARGED !
