Series 1.5 Kubernetes on Raspberry Pi (Intermediate).md
*******************************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@grahamjohnson77

## Taints on Nodes

    kubectl get node -o custom-columns=NAME:.metadata.name,TAINT:.spec.taints[*].effect
    
    # remove taint from all nodes
    kubectl taint nodes --all node-role.kubernetes.io/control-plane-
    kubectl taint nodes --all node-role.kubernetes.io/master-
    OR
    # remove taint from specific nodes
    kubectl taint nodes master node-role.kubernetes.io/control-plane-

## Section 01 Raspberry Pi Setup

    NOTE: I ordered a new Pi with 4GB RAM!
    Otherwise, you will get a message later when doing the 'sudo kubeadm init' cmd saying:
    [ERROR Mem]: the system RAM (905 MB) is less than the minimum 1700 MB

    # Download Raspberry Pi Imager
    https://www.raspberrypi.com/software/

    # Raspberry Pi and Flash MicroSD Card Steps
    https://www.raspberrypi.com/documentation/computers/getting-started.html
    https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2

    # Flash the MicroSD Card and install the Ubuntu Server
    Used Ubuntu Server 20.4.5 LTS (64-bit) for the new Raspberry Pi 4

    NOTE 1: Use the pi installer to set the ssh option (using the gear icon), and 'pi' user and 'raspberry' password (only for quick demo purposes!)
    NOTE 2: I also called this new instance 'Master2' so not to interfere with the existing instance of 'Master', using the same NOTE 1 step!

    # Get the IP of the new Pi when you plug it into the Raspberry Pi system
    I use a tool called IP Scanner (Version 5.01 (1344)) to get the IP, which is available here:
    https://10base-t.com/ipscanner/

    # SSH into your Raspberry Pi !!
    (IP Scanner should have shown you the Raspberry PI. Another way to get it is directly from your Router Web Interface)

    # Assign Static IP to the Pi
    For Ubuntu LTS 20.04 Server Installed from Pi Installer
    ## NOTE: Replace the <Choose New IP on your network for the Pi> and <Gateway IP on your network> with your real IPs
    sudo vi /etc/netplan/00-installer-config.yaml

    network:
      ethernets:
        eth0:
          addresses: [<Choose New IP on your network for the Pi>/24]
          gateway4: <Router Gateway IP on your network>
          nameservers:
            addresses: [4.2.2.2, 8.8.8.8]
      version: 2

    sudo netplan apply

    ip add show
    ip route show

    sudo reboot

    # Pi User Access
    Create a new user on each pi:
    sudo adduser master

    # See existing groups
    groups

    # Add the user to all default user groups except ‘ubuntu’ (as we will remove it after):
    sudo usermod -a -G adm,dialout,cdrom,floppy,sudo,audio,dip,video,plugdev,netdev,lxd master

    # Log in and verify the new user works!
    ssh master@<YOUR PIs IP ADDRESS HERE>

    # If it was working, we can now safely delete default user with
    sudo deluser --remove-home ubuntu

    # Enable SSL Key-Based Authentication on our Pi
    The next thing in the queue would be to enable SSH Key-Based Authentication.
    The following steps should be done on the machine that we will be using to control our cluster.

    # Generate Key on your MAC
    ssh-keygen

    Specify the name of the file where key will be saved as ~/.ssh/id_master.

    # Copy the SSH key to master node
    ssh-copy-id -i ~/.ssh/id_master master@<YOUR PIs HOSTNAME>
    e.g. ssh-copy-id -i ~/.ssh/id_master master@master2

    # Disable login for the root user and login via password (always best practices!):
    sudo nano /etc/ssh/sshd_config

    ## We are going to change the following lines
    From:
    #PermitRootLogin prohibit-password
    #PasswordAuthentication yes
    #PubkeyAuthentication yes
    To:
    PermitRootLogin no
    PasswordAuthentication no
    PubkeyAuthentication yes

    # Validate no errors and restart SSH daemon
    # NOTE: A daemon in Linux is the same as a service in Windows!
    sudo /usr/sbin/sshd -t
    sudo systemctl restart sshd.service

    # Back on our MAC, we can configure ssh config file, so we don’t need to specify key file every time we are connecting to the node:
    sudo vi ~/.ssh/config

    # You can copy lines below, which will bind your nodes to appropriate host name, user and RSA key:
    Host k8-master
    HostName k8-master
    User master
    IdentityFile ~/.ssh/id_master

    Finally, we should be able to login into your master node just by typing 'ssh k8-master'

## Section 02 Upgrade our System for Kubernetes Installation

    We are going to update our installation, so we have latest and greatest packages by running
    NOTE: This can take a few minutes!

    sudo apt update
    sudo apt upgrade
    sudo apt dist-upgrade

    # After this we are going to reboot our server with
    sudo reboot

    # We need to setup Linux Control Groups that are used for resource monitoring and isolation that are needed by Kubernetes:
    sudo vi /boot/firmware/cmdline.txt

    # And add the following line to the end of the line
    cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
    NOTE: Read more about cgroups here: https://en.wikipedia.org/wiki/Cgroups

    My full line was as follows:
    elevator=deadline net.ifnames=0 console=serial0,115200 dwc_otg.lpm_enable=0 console=tty1 root=LABEL=writable rootfstype=ext4 rootwait fixrtc quiet splash cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory

    # Install tools like 'ifconfig' etc.
    sudo -i
    apt install net-tools

    # Now we can reboot our nodes:
    sudo reboot

## Section 03 Start Our Kubernetes Installation

## All Nodes

    # Add Kubernetes repository to all nodes
    sudo apt-get install apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

    # Update repo and install kubeadm on all nodes
    sudo apt-get update

    # Install latest version?
    sudo apt-get install kubeadm

    OR

    # Install specific version?
    https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

    You can use the apt-cache command to see what Kubernetes versions are supported for various versions:
    apt-cache madison kubectl | grep 1.23
    apt-cache madison kubectl | grep 1.24

    sudo apt install -y kubeadm=1.23.14-00 kubelet=1.23.14-00 kubectl=1.23.14-00              - version 23
    sudo apt install -y kubeadm=1.24.6-00 kubelet=1.24.6-00 kubectl=1.24.6-00                 - version 24

    sudo apt-mark hold kubelet kubeadm kubectl

    For container runtime, we are going to use containerd.
    More Information here: https://containerd.io/

    First we are going to handle prerequisites on all nodes:

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
    # Set up the repository
    # Install packages to allow apt to use a repository over HTTPS
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

    Now we would need to configure kubelet agent to use containerd, so edit
    sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

    and add the line below under other Environment settings
    Environment="KUBELET_EXTRA_ARGS=--cgroup-driver=systemd --container-runtime=remote --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock"

    # Reloading and restarting deamon is what we are going to do next
    sudo systemctl daemon-reload
    sudo systemctl enable kubelet.service
    sudo systemctl restart kubelet.service

    # We will configure endpoint for crictl, which is basically what can be use for interaction with containers instead of docker:
    sudo vi /etc/crictl.yaml

    and add this line:
    runtime-endpoint: unix:///run/containerd/containerd.sock

## Master Node Only

    Next, we will prefetch kubernetes system images and initialize our master node with LATEST VERSION

    # Install latest version?
    sudo kubeadm config images pull
    sudo kubeadm init --cri-socket /run/containerd/containerd.sock
    
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

    Copy the kubeadm join command out to run it later on the worker nodes!

    # Let’s configure kubectl for our user:

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    Please note that the printout of the init command will contain keys you need in order to join nodes to the cluster.

    # This will take a minute or two, so we can monitor the progress with (on master node):
    kubectl get pods --all-namespaces

    # We can now check on our cluster from master node:
    kubectl get nodes

    pi@master2:~$ kubectl get nodes
    NAME       STATUS     ROLES           AGE    VERSION
    master2    NotReady   control-plane   10m    v1.26.0

## Worker Nodes Only

    NOTE: First, i had to reboot all to make sure the master was available to join!
    
    Tip: Copy the command below into Notepad first to remove any extra spaces!

    You should ran that command on all worker nodes. e.g.

    # DO NOT COPY THIS COMMAND. USE ONE YOU GOT AS RESULT IN INIT for Worker Nodes
    sudo kubeadm join <master IP>:6443 --token wpc1pz.6lqqbx8vio7jaxoa --discovery-token-ca-cert-hash sha256:d243258fb6f7654a2cb8cfbe683c1c7e3e82a2f82dfba1bd287759cf0b00a315

    NOTE: Find the join cmd if lost:
    kubeadm token create --print-join-command

    Output:
    This node has joined the cluster:
    * Certificate signing request was sent to apiserver and a response was received.
    * The Kubelet was informed of the new secure connection details.

    We can now check on our cluster from master node:
    sudo kubectl get nodes

    pi@master2:~$ kubectl get nodes
    NAME       STATUS     ROLES           AGE    VERSION
    master2    NotReady   control-plane   10m    v1.26.0
    worker1    NotReady   control-plane   10m    v1.26.0

    NOTE: Nodes are not currently running as there is no networking setup, so lets do that!

    # ----------------------------------------------------------
    # Section 03 Kubernetes Cluster on Raspberry Pi - Networking
    # https://levelup.gitconnected.com/step-by-step-slow-guide-kubernetes-cluster-on-raspberry-pi-4b-part-3-899fc270600e

## Master Node Only

    Project Calico — Installation on MASTER NODE ONLY!

    NOTE: On installation of Worker, it can take a while for master and worker to come back as STATUS Ready.
    
    NOTE: From Feb 2023, the simply download of Calico stopped working so I had to use version 3.11 !
    
    # Describe the node to see if issues
    kubectl describe node master2
    
    # New Calico installation (use this!)
    kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml

    # Older Calico installation
    # First, we need to download calico configuration file on master node:
    #curl https://docs.projectcalico.org/manifests/calico.yaml -O
    # CIDR IP block will automatically be detected so we can just apply yaml to our cluster
    #kubectl apply -f calico.yaml

    This will take a minute or two, so we can monitor the progress

    kubectl get pods --all-namespaces

    pi@master:~$ kubectl get pods --all-namespaces
    NAMESPACE     NAME                                       READY   STATUS     RESTARTS   AGE
    kube-system   calico-kube-controllers-798cc86c47-lp7md   0/1     Pending    0          13s
    kube-system   calico-node-cmqgx                          0/1     Init:0/3   0          13s
    kube-system   coredns-565d847f94-4gwlt                   0/1     Pending    0          2m5s
    kube-system   coredns-565d847f94-j6ll5                   0/1     Pending    0          2m5s
    kube-system   etcd-master                                1/1     Running    0          2m8s
    kube-system   kube-apiserver-master                      1/1     Running    0          2m8s
    kube-system   kube-controller-manager-master             1/1     Running    0          2m8s
    kube-system   kube-proxy-vwc4h                           1/1     Running    0          2m6s
    kube-system   kube-scheduler-master                      1/1     Running    0          2m8s

    Once all pods are running we can confirm that all our nodes now are now in a ready state by running:

    kubectl get nodes

    pi@master2:~$ kubectl get nodes
    NAME       STATUS     ROLES           AGE    VERSION
    master2    Ready      control-plane   10m    v1.26.0

    Congratulations your Kubernetes cluster is now running!

    # NOTE: Before I could start to use the cluster, I had to remove the existing taint:
    pi@master:~$ kubectl describe node master | grep Taints
    Taints:             node-role.kubernetes.io/control-plane:NoSchedule

    kubectl taint node master node-role.kubernetes.io/control-plane:NoSchedule-
    kubectl taint node master2 node-role.kubernetes.io/control-plane:NoSchedule-

## Section 04 Kubernetes Cluster on GCP - LoadBalancing

    # MetalLB Load Balancer Installation on MASTER NODE
    As we don’t have an external load balancer, we are going to need a software solution, and metalLB looks like a good choice.

    There are some compatibility issues with Calico and metaLB and you can read about them more here.

    However, they are not important for what we are trying to do.

    On our master node let’s install our load balancer.

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
          - <Router IP subnet>.200-<Router IP subnet>.254.254

    Run:
    kubectl apply -f metalLB-config.yaml

## Section 05 Kubernetes Cluster on GCP - Validations

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

    # Now we need to retrieve an 'external IP address' from the service
    kubectl get svc nginx-service

    # Change IP address to one that you got by running previous command
    curl  The IP of the service!

    Nginx Response from our Kubernetes cluster !

    # Open Browser and see if this IP loads!
    http://The IP of the service!

    Traffic should be available on multiple nodes (sample below using multiple nodes etc.):
    NAME                               READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
    nginx-deployment-cd55c47f5-cx5rc   1/1     Running   0          46s   172.16.196.130   node01   <none>           <none>
    nginx-deployment-cd55c47f5-mgnbv   1/1     Running   0          46s   172.16.219.100   master   <none>           <none>
    nginx-deployment-cd55c47f5-qrbqz   1/1     Running   0          46s   172.16.219.101   master   <none>           <none>
    nginx-deployment-cd55c47f5-wc8gw   1/1     Running   0          46s   172.16.196.129   node01   <none>           <none>

    # Before we go, let’s do some cleanup and remove our nginx test deployment.
    kubectl delete -f nginx-fake-deployment.yaml
    
## Section 06 To Delete Node from Raspberry Pi Kubernetes Cluster

    kubectl get nodes
    kubectl drain <node-name> --ignore-daemonsets --delete-local-data
    kubectl delete node <node-name>
