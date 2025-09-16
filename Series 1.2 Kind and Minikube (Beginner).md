Series 1.4 Kind and Minikube (Beginner).md
******************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@grahamjohnson77

## Install kubectl on MAC

      # Required for Kind and Minikube testing!
      brew install kubectl

## Kind on MAC
      brew install kind

      # More Information Here
      https://kind.sigs.k8s.io/
      https://kind.sigs.k8s.io/docs/user/quick-start/
      https://kind.sigs.k8s.io/docs/user/quick-start/#interacting-with-your-cluster

      # More Information Here on Kubernetes
      https://kubernetes.io/

      # Create Cluster using Kind:
      xcode-select --install
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      brew install kind                                                                   # run to update too!

      # Create the cluster
      kind create cluster --name kind-test

      # List your kind clusters
      kind get clusters

      # NOTE: When you run get clusters command, you see the cluster name is 'kind-test' but to kind, the real name is 'kind-kind-test' !

      # In order to interact with a specific cluster, you only need to specify the cluster name as a context in kubectl
      kubectl cluster-info --context kind-kind-test
      Kubernetes control plane is running at https://127.0.0.1:51057
      CoreDNS is running at https://127.0.0.1:51057/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

      To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

      # Create a cluster usig the config file
      #kind create cluster --config=config.yaml

      # Create a test pod
      vi pod.yaml

      # Add the following contents to the file
      apiVersion: v1
      kind: Pod
      metadata:
        name: simple-pod
      spec:
        containers:
        - name: ubuntu
          image: ubuntu
          command: ["sleep", "500000"]

      # Create pod on the nodes
      kubectl create -f pod.yaml

      # List pods on the cluster
      kubectl get pods

      # Delete cluster by name
      kind delete cluster --name kind-test

      # kind Quick Notes
      kind get clusters                                                                       # get all clusters
      kind create cluster --name ckad-playground	                                            # create cluster
      alias k=kubectl; kubectl cluster-info --context kind-ckad-playground;                   # set cluster
      kind delete clusters ckad-playground                                                    # delete cluster

      k create ns 4-10-2023                                                                   # create namespace
      k config set-context --current --namespace 4-10-2023                                    # set context ns
      k config current-context                                                                # show context name
      k config get-contexts default                                                           # show context info

      k config view --minify --output 'jsonpath={..namespace}'; echo                          # show current namespace
      k config view | grep namespace

## minikube on MAC

      # Install hyperkit (virtualbox, VMware fusion)
      brew install hyperkit
      brew install minikube
      
      minikube version
      minikube help

      # More Information Here
      https://minikube.sigs.k8s.io/docs/start/

      # Start minikube
      minikube start

      # Output seen
      Downloads $minikube start
      😄  minikube v1.28.0 on Darwin 13.1 (arm64)
      ✨  Using the docker driver based on existing profile
      👍  Starting control plane node minikube in cluster minikube
      🚜  Pulling base image ...
      🤷  docker "minikube" container is missing, will recreate.
      🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
      🐳  Preparing Kubernetes v1.25.3 on Docker 20.10.20 ...
      🔎  Verifying Kubernetes components...
          ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
      🌟  Enabled addons: storage-provisioner, default-storageclass
      🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

      # Check status
      minikube status

      # Check nodes/pods
      kubectl get nodes
      kubectl get pods

      # Create a Kubernetes Deployment using an existing image
      kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0

      # Expose the deployment as a service
      kubectl expose deployment hello-minikube --type=NodePort --port=8080

      # Check the nodes and pods
      kubectl get nodes
      kubectl get pods

      # Get URL of the service
      minikube service hello-minikube --url

      # Delete service and deployment
      kubectl delete services hello-minikube
      kubectl delete deployment hello-minikube

      # Stop minikube cluster
      minikube stop

      # Delete minikube cluster
      minikube delete

      # More Information on the Certified Kubernetes Exam here! (For the Future)
      https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/

      # More Information here on yaml syntax
      https://yaml.org/
      https://en.wikipedia.org/wiki/YAML
