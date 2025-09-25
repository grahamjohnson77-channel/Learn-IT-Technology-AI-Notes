Series 2.2.2 Network Policies (More Discussion) - GKE.md
********************************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

    # 2.2 Network Policy Exercises: https://github.com/ahmetb/kubernetes-network-policy-recipes
    #                               https://github.com/GoogleCloudPlatform/gke-network-policy-demo
    # Notes on Calico:              https://docs.projectcalico.org/security/tutorials/kubernetes-policy-basic
    # Notes on Labels:              https://www.golinuxcloud.com/kubernetes-add-label-to-running-pod/
    
    # Great Network Policies:       https://github.com/ahmetb/kubernetes-network-policy-recipes
    
    # Please read these a few times!
    https://kubernetes.io/docs/concepts/services-networking/network-policies/
    https://github.com/GoogleCloudPlatform/gke-network-policy-demo/blob/master/README.md
    
    # Enable network policy enforcement on new or existing cluster
    https://cloud.google.com/kubernetes-engine/docs/how-to/network-policy
    
    # Warning
    By default, pods accept traffic from any source.
    A network policy helps to specify how a group of pods can communicate with each other and other network endpoints.
    Network Policy uses 'labels' to select pods and define rules to specify what traffic is allowed to the selected pods.
    Once there is a NetworkPolicy applied on a particular pod, that pod will reject connections that are not allowed 
    the NetworkPolicy. The pods that are not selected by any NetworkPolicy will continue to accept all traffic.

    If the exercises says that you need to find the broken service, and only the affected k8s object, describe the service,
    search for the selector and find the pod with that one, and that is the failing one even though there may be other 
    kubernetes objects.

    # IMPORTANT - PLEASE READ ARTICLE ON NETPOLs:
    https://cloudogu.com/en/blog/k8s-app-ops-part-1
    https://cloudogu.com/en/blog/k8s-app-ops-part-2

    # Troubleshooting
    If you are missing endpoints for your service, try listing pods using the labels that Service uses e.g.
    spec:
      - selector:
          name: nginx
          type: frontend

    k get pods --selector=name=nginx,type=frontend

    # Test connectivity with timeout (5 seconds)
    k run curl --image=radial/busyboxplus -it --rm --restart=Never - curl -m 5 my-service:8080          # curl
    k run wget --image=busybox -it --rm --restart=Never -- wget --timeout 5 -O- my-service:8080         # wget
    k run wget --image=busybox -it --rm --restart=Never -- nc -w 5 -zv my-service 8080                  # netcat TCP
    k run wget --image=busybox -it --rm --restart=Never -- nc -w 5 -zuv my-service 8181                 # netcat UDP

# Introduction

With multiple scenarios to verify and learn, we have multiple learning options we can use. But for studying Network Policies, we will use:

    # Option 1: GKE (Kubernetes Engine on GCP)
    
    SETUP README AVAILABLE HERE:
    https://github.com/cloudsolutionarchitects-dot-eu/youtube-series/blob/main/Series%201%20Introduction/Series%201.7%20Kubernetes%20on%20GCP%20Cloud%20-%20The%20GKE%20Way%20(Intermediate).md
    
    # IMPORTANT:
    # KIND and RaspberryPi were not working for testing Network Policies, so use GCP, AWS or Azure
    
    # create a cluster with network polices (with network policy enabled!!!)
    gcloud container clusters create cka-gke-cluster --zone europe-west1-b --enable-network-policy
    
    # try listing GKE clusters
    gcloud container clusters list

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
    
    # Let’s delete again it with:
    kubectl delete -f nginx-fake-deployment.yaml
    
    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage

    # Create Tmp Pod
    k run temppod --image=nginx --restart=Never --port=80                       # temp pod to verify deployment % weighting
    k exec -it temppod -- sh                                                    # log into temp pod

    # NOTE: Network Policies are all based around Labels!
    We are concerned only about labels on deploy/pods & service selector!
    
    # Sample: Add the following section to allow TCP connections on port 80:
    
      policyTypes:
      - Ingress
      ingress:
      - from:
        - podSelector:
            matchLabels:
              name: <pod name>
        ports:
        - protocol: TCP
          port: 80

## Q4. Try 3 Different Scenarios for Pod to Pod Communications

    # Ref: https://faun.pub/kubernetes-ckad-weekly-challenge-6-networkpolicy-6cc1d390f289

    # Today we will work with a given scenario:
    wget https://raw.githubusercontent.com/wuestkamp/k8s-challenges/master/6/scenario.yaml
    
    # Before running, modify the scenario file to use nginx!
    vi scenario.yaml
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      creationTimestamp: null
      labels:
        app: api-deployment
      name: api-deployment
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: api
      template:
        metadata:
          labels:
            app: api
        spec:
          containers:
          - image: alpine/socat
            name: api
            command: ["/bin/sh"]
            args: ["-c", "socat - TCP-LISTEN:3333,fork,reuseaddr"]
    ---
    apiVersion: v1
    kind: Service
    metadata:
      creationTimestamp: null
      labels:
        app: api-service
      name: api-service
    spec:
      ports:
      - name: "3333"
        port: 3333
        protocol: TCP
        targetPort: 3333
      selector:
        app: api
      type: ClusterIP
    status:
      loadBalancer: {}

    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: nginx-deployment
      name: nginx-deployment
    spec:
      replicas: 5
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - image: nginx
            name: nginx
            command: ["/bin/sh"]
            args: ["-c", "apt-get -y update && apt-get -y install netcat iputils-ping net-tools && nginx -g 'daemon off;'"]

    ---
    apiVersion: v1
    kind: Service
    metadata:
      labels:
        app: nginx-service
      name: nginx-service
    spec:
      ports:
      - name: 80-80
        port: 80
        protocol: TCP
        targetPort: 80
        nodePort: 31111
      selector:
        app: nginx
      type: NodePort
    
    k create -f scenario.yaml
    
    # Keep cluster information running in a terminal
    watch "kubectl config current-context; echo ''; kubectl config view | grep namespace; echo ''; kubectl get namespace,pod,svc,deployment,networkpolicy -o wide"

    kubectl get namespace,pod,svc,deployment,networkpolicy -o wide

    # The objects:
    deployment nginx-deployment with 5 replicas, nginx on port 80
    deployment api-deployment with 2 replicas, simple service running port 3333
    NodePort service nginx-service which exposes port 31111 on each node and forwards to port 80 on the nginx pods
    ClusterIP service api-service to handle simple internal load balancing from nginx instances to api instances on port 3333

    # Connection from nginx deployment pod to outer world:
    alias k=kubectl
    
    # Connection from nginx to outer world:
    k exec nginx-deployment-54c84d865-cv724 -- nc -zv www.google.de 80
    Connection to www.google.de (142.251.5.94) 80 port [tcp/*] succeeded!
    
    # Connection from nginx to api:
    k exec nginx-deployment-54c84d865-cv724 -- nc -zv api-service 3333
    Connection to api-service (10.36.14.52) 3333 port [tcp/*] succeeded!

    # Connection from api to outer world:
    k exec api-deployment-645668c65c-6vnr7 -- nc -zv www.google.de 80
    www.google.de (142.251.5.94:80) open

    # Connection from api to api:
    k exec api-deployment-645668c65c-6vnr7 -- nc -zv api-service 3333
    api-service (10.36.14.52:3333) open

    # Todays Task: NetworkPolicy:
    Make sure all your NetworkPolicies still allow DNS resolution.
    Implement a NetworkPolicy for nginx pods to only allow egress to the internal api pods on port 3333. No access to the outer world (but DNS).
    Implement a NetworkPolicy for api pods to only allow ingress on port 3333 from the internal nginx pods. To test negative: check from api to api.
    Implement a NetworkPolicy for api pods to only allow egress to (IP of google.com) port 443.

    # Part #1 NetworkPolicy for nginx pods to only allow egress to the internal api pods on port 3333
    Create a new file nginx-networkpolicy.yaml:

    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: nginx-network-policy
    spec:
      podSelector:
        matchLabels:
          app: nginx
      policyTypes:
      - Egress
      egress:
      - to:
        - podSelector:
            matchLabels:
              app: api
        ports:
          - port: 3333
            protocol: TCP
      - to:
        ports:
          - port: 53
            protocol: TCP
          - port: 53
            protocol: UDP

    # Followed by:
    alias k=kubectl
    k -f nginx-networkpolicy.yaml create
    k exec nginx-deployment-57d6c8d759-knnsq -- nc -zv www.google.de 80 # FAILS
    k exec nginx-deployment-57d6c8d759-knnsq -- nc -zv nginx-service 80 # FAILS
    k exec nginx-deployment-57d6c8d759-knnsq -- nc -zv api-service 3333 # WORKS

    # Part #2 NetworkPolicy for api pods to only allow ingress on port 3333 from the internal nginx pods
    cp nginx-networkpolicy.yaml api-networkpolicy.yaml and then edit the copy to:
    
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: api-network-policy
    spec:
      podSelector:
        matchLabels:
          app: api
      policyTypes:
      - Ingress
      ingress:
        - from:
          - podSelector:
              matchLabels:
                app: nginx
          ports:
            - port: 3333
              protocol: TCP

    # Then test with by trying to connect from api to api:
    k -f api-networkpolicy.yaml create

    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv api-service 3333 # FAILS
    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv www.google.de 80 # WORKS

    # Part #3 NetworkPolicy for api pods to only allow egress to (IP of google.com) port 443
    We limit here to an IP (ping www.google.com) because as of now there are no DNS selectors available for NetworkPolicies.

    # Let’s adjust the api-networkpolicy.yaml to include egress limitation:
    
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: api-network-policy
    spec:
      podSelector:
        matchLabels:
          app: api
      policyTypes:
      - Egress
      - Ingress
      ingress:
        - from:
          - podSelector:
              matchLabels:
                app: nginx
          ports:
            - port: 3333
              protocol: TCP
      egress:
      - to:
        - ipBlock:
            cidr: 216.58.208.35/32
        ports:
          - port: 443
            protocol: TCP
      - to:
        ports:
          - port: 53
            protocol: TCP
          - port: 53
            protocol: UDP

    # Then we run:
    k -f api-networkpolicy.yaml apply
    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv nginx-service 80 # FAILS
    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv api-service 3333 # FAILS
    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv 216.58.208.35 80 # FAILS
    k exec api-deployment-7ff954cdcf-cfbl6 -- nc -zv 216.58.208.35 443 # WORKS
    
## Q5. Samples of Ingress and Egress To Complete

    # Ref: https://www.howtoforge.com/kubernetes_network_policy/

    # Ingress Network Policy:
    Create a hello-web pod with a label "app-destination-pod" and service on which we will allow incoming traffic on port 8080.

    # NOTE: sleep add here to keep the pod alive!
    kubectl run hello-web --labels app=destination-pod --image=nginx --port 8080 --
    kubectl get pod | grep hello-web

    kubectl get service | grep hello-web

    # Create an ingress definition file using the following content which allows traffic on the 
    "hello-web" pod with label "app=destination-pod" on port 8080 from the pod matching the label "app=source-pod".

    vim ingress.yml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: destination-pod-allow-from-source-pod
    spec:
      policyTypes:
      - Ingress
      podSelector:
        matchLabels:
          app: destination-pod
      ingress:
      - from:
        - podSelector:
            matchLabels:
              app: source-pod

    # Before we create an ingress policy create a pod with label "app=unknown" not matching the rule of the policy.

    kubectl run -l app=unknown --image=alpine --restart=Never --rm -i -t test-1
    
    # Now when we try to access our "hello-web" pod on port 8080 from this pod, the pod will be accessible!

    wget -qO- --timeout=2 http://hello-web:8080

    # Now create a policy that allows connection on the pod with label "app=destination-pod" from the pod with label "app=source-pod" and get details of it.

    kubectl apply -f ingress.yml
    kubectl get networkpolicy destination-pod-allow-from-source-pod

    # Now, again create a pod with a label not matching the rule defined in the policy.

    kubectl run -l app=unknown --image=alpine --restart=Never --rm -i -t test-1
    
    # If we again try to access the "hello-web" pod from this pod, the "hello-web" pod will not be reachable.

    wget -qO- --timeout=2 http://hello-web:8080

    # This time, let's create a pod matching the network policy rule i.e. pod with label "app=source-app" 

    kubectl run -l app=source-pod --image=alpine --restart=Never --rm -i -t test-1
    
    # Now, if we try to access the "hello-web" pod  from the pod with label "app=source-pod", the "hello-web" can be accessed.

    wget -qO- --timeout=2 http://hello-web:8080

    # In the above screenshot, you can see that the "hello-web" pod was accessible from the pod with label "app=source-pod". This means that we restricted connections on our "hello-web" and only pods with label "app=source-pod"  can connect to it.

    # Egress Network Policy:
    Create a new file for Egress Network Policy with the following content.

    vim egress.yml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: source-pod-allow-to-destination-pod
    spec:
      policyTypes:
      - Egress
      podSelector:
        matchLabels:
          app: source-pod
      egress:
      - to:
        - podSelector:
            matchLabels:
              app: destination-pod
      - ports:
        - port: 53
          protocol: TCP
        - port: 53
          protocol: UDP

    # The above policy will allow outgoing connections from the pod with label "app=source-pod" to the pod with label "app=destination-pod" and also on port 53 for DNS resolution.

    # Before we apply Egress Policy in the cluster, create a pod "hello-web-2" and service which does not match our policy.

    kubectl run hello-web-2 --labels app=hello-2 --image=nginx --port 8080 --expose
    kubectl get pod | grep hello-web-2
    kubectl get service | grep hello-web-2

    # Now create a pod with label "app=source-pod".

    kubectl run -l app=source-pod --image=alpine --restart=Never --rm -i -t test-2

    # Before we apply the Egress policy, both the apps "hello-web" and "hello-web-2" can be accessed from the pod with label "app=source-pod"

    wget -qO- --timeout=2 http://hello-web:8080
    wget -qO- --timeout=2 http://hello-web-2:8080

    # Now, create a Network policy with egress rule.

    kubectl create -f egress.yml
    kubectl get networkpolicy | grep source-pod-allow-to-destination-pod

    # Let's create a pod with label "app=source-pod" and try to access both the pod "app=source-pod"

    kubectl run -l app=source-pod --image=alpine --restart=Never --rm -i -t test-3

    wget -qO- --timeout=2 http://hello-web-2:8080

    # You can observe that this time the pod "hello-web-2" was not reachable as it does not match the egress policy which allows connection from a pod with label "app=source-pod" to the pod with label "app=destination-pod".

## Q6. Create Policies for Weave and Calico (they both use slightly diff configuration)

    # Ref: https://banzaicloud.com/docs/pipeline/security/network-policy/examples/

    kubectl run --generator=run-pod/v1 busybox1 --image=busybox -- sleep 3600
    kubectl run --generator=run-pod/v1 busybox2 --image=busybox -- sleep 3600

    kubectl get pod -o wide

    # Weave

    Create a deny-all policy:
    cat << EOF | kubectl apply -f -
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: deny-all
      namespace: default
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
      - Egress
    EOF
    kubectl exec -ti busybox2 -- ping -c3 10.20.160.6

    PING 10.20.160.6 (10.20.160.6): 56 data bytes

    --- 10.20.160.6 ping statistics ---
    3 packets transmitted, 0 packets received, 100% packet loss

    Create an allow-out-to-in policy, and add labels to pods:
    cat << EOF | kubectl apply -f -
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-out-to-in
      namespace: default
    spec:
      podSelector: {}
      ingress:
      - from:
        - podSelector:
            matchLabels:
              test: out
      egress:
      - to:
        - podSelector:
            matchLabels:
              test: in
      policyTypes:
      - Ingress
      - Egress
    EOF

    # Set labels of busybox pods
    kubectl label pod busybox1 test=in
    kubectl label pod busybox2 test=out

    kubectl exec -ti busybox2 -- ping -c3 10.20.160.6 

    PING 10.20.160.6 (10.20.160.6): 56 data bytes
    64 bytes from 10.20.160.6: seq=0 ttl=64 time=0.710 ms
    64 bytes from 10.20.160.6: seq=1 ttl=64 time=0.596 ms
    64 bytes from 10.20.160.6: seq=2 ttl=64 time=0.637 ms

    --- 10.20.160.6 ping statistics ---
    3 packets transmitted, 3 packets received, 0% packet loss
    round-trip min/avg/max = 0.596/0.647/0.710 ms
    
    OR

    # Calico

    Create a standard deny-all policy:
    With Calico you can define standard NetworkPolicy.

    cat << EOF | kubectl apply -f -
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: deny-all
      namespace: default
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
      - Egress
    EOF
    kubectl exec -ti busybox2 -- ping -c3 192.168.67.136

    PING 192.168.67.136 (192.168.67.136): 56 data bytes

    --- 192.168.67.136 ping statistics ---
    3 packets transmitted, 0 packets received, 100% packet loss

    # Create an allow-ingress-from-out policy in a namespace:
    Now we can use Project Calico NetworkPolicy to allow some traffic overriding standard deny-all NetworkPolicy.

    cat << EOF | kubectl apply -f -
    apiVersion: crd.projectcalico.org/v1
    kind: NetworkPolicy
    metadata:
      name: allow-ingress-from-out
    spec:
        ingress:
        - action: allow
          source:
            selector: test == 'out'
    EOF

    # Create an allow-egress-to-in policy globally:
    Due to egress isn’t enabled in step 3 the ping doesn’t work yet. Now create GlobalNetworkPolicy enbling egress to specified labelled pods clusterwide.

    cat << EOF | kubectl apply -f -
    apiVersion: crd.projectcalico.org/v1
    kind: GlobalNetworkPolicy
    metadata:
      name: allow-egress-to-in
    spec:
        egress:
        - action: allow
          destination:
            selector: test == 'in'
    EOF
    kubectl exec -ti busybox2 -- ping -c3 192.168.67.136

    PING 192.168.67.136 (192.168.67.136): 56 data bytes
    64 bytes from 192.168.67.136: seq=0 ttl=254 time=0.068 ms
    64 bytes from 192.168.67.136: seq=1 ttl=254 time=0.072 ms
    64 bytes from 192.168.67.136: seq=2 ttl=254 time=0.075 ms

    --- 192.168.67.136 ping statistics ---
    2 packets transmitted, 2 packets received, 0% packet loss
    round-trip min/avg/max = 0.068/0.070/0.072 ms

# EXTRA INFORMATION ON NETWORK POLICIES

    # Service Communication Explained
    The normal way to communicate within a cluster is through Service resources.
    A Service also has an IP address and additionally a DNS name. A Service is backed by a set of pods.
    The Service forwards requests to itself to one of the backing pods.
    The fully qualified DNS name of a Service is:

    <service-name>.<service-namespace>.svc.cluster.local
    This can be resolved to the IP address of the Service from anywhere in the cluster (regardless of namespace).

    # For example, if you have:
    Namespace ns-a: Service svc-a → set of pods A
    Namespace ns-b: Service svc-b → set of pods B

    # Then a pod of set A can reach a pod of set B by making a request to:
    svc-b.ns-b.svc.cluster.local

    k create ns ns-a
    k create ns ns-b

    k create deployment nginx-a --image=nginx --replicas=1 --namespace ns-a
    k expose deployment nginx-a --port=80 --namespace ns-a                    # NOTE: Creates svc called nginx-a

    k create deployment nginx-b --image=nginx --replicas=1 --namespace ns-b
    k expose deployment nginx-b --port=80 --namespace ns-b                    # NOTE: Creates svc called nginx-b

    # Log into pod and curl the 2nd namespace:
    k exec -it nginx-a-76865cf8c8-tz7w5 --namespace ns-a -- curl nginx-b.ns-b.svc.cluster.local

    # Microsoft Azure - Network Policies Example
    # Ref: https://docs.microsoft.com/en-us/azure/aks/use-network-policies
    First, follow the documentation to create a Microsoft Azure cluster...

    # For the sample application environment and traffic rules, let's first create a namespace called development to run the example pods:
    k create namespace development
    k label namespace/development purpose=development

    # Create an example back-end pod that runs NGINX. This back-end pod can be used to simulate a sample back-end web-based application. Create this pod in the development namespace, and open port 80 to serve web traffic. Label the pod with app=webapp,role=backend so that we can target it with a network policy in the next section:
    k run backend --image=mcr.microsoft.com/oss/nginx/nginx:1.15.5-alpine --labels app=webapp,role=backend --namespace development --expose --port 80

    # Create another pod and attach a terminal session to test that you can successfully reach the default NGINX webpage:
    k run --rm -it --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11 network-policy --namespace development

    # At the shell prompt, use wget to confirm that you can access the default NGINX webpage:
    wget -qO- http://backend

    The following sample output shows that the default NGINX webpage returned:
    <title>Welcome to nginx!</title>

    # Then exit out of the temp pod.

    # Now that you've confirmed you can use the basic NGINX webpage on the sample back-end pod, create a network policy to deny all traffic.

    vi backend-policy.yaml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: backend-policy
      namespace: development
    spec:
      podSelector:
        matchLabels:
          app: webapp
          role: backend
      ingress: []

    k apply -f backend-policy.yaml

    # Let's see if you can use the NGINX webpage on the back-end pod again. Create another test pod and attach a terminal session:
    k run --rm -it --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11 network-policy --namespace development

    # At the shell prompt, use wget to see if you can access the default NGINX webpage.
    This time, set a timeout value to 2 seconds. The network policy now blocks all inbound traffic, 
    so the page can't be loaded, as shown in the following example:
    
    wget -O- --timeout=2 --tries=1 http://backend

    # Then exit out of the temp pod.

    # Allow inbound traffic based on a pod label:

    # In the previous section, a back-end NGINX pod was scheduled, and a network policy was created to deny all traffic. 
    Let's create a front-end pod and update the network policy to allow traffic from front-end pods.

    # Update the network policy to allow traffic from pods with the labels app:webapp,role:frontend and in any namespace. 
    Edit the previous backend-policy.yaml file, and add matchLabels ingress rules so that your manifest looks like the following example:

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: backend-policy
      namespace: development
    spec:
      podSelector:
        matchLabels:
          app: webapp
          role: backend
      ingress:
      - from:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              app: webapp
              role: frontend

    # NOTE: This network policy uses a namespaceSelector and a podSelector element for the ingress rule. 
    The YAML syntax is important for the ingress rules to be additive. In this example, both elements must match 
    for the ingress rule to be applied. Kubernetes versions prior to 1.12 might not interpret these elements correctly 
    and restrict the network traffic as you expect. For more about this behavior, see Behavior of to and from selectors.

    k apply -f backend-policy.yaml

    # Schedule a pod that is labeled as app=webapp,role=frontend and attach a terminal session:
    k run --rm -it frontend --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11 --labels app=webapp,role=frontend --namespace development

    # At the shell prompt, use wget to see if you can access the default NGINX webpage:
    wget -qO- http://backend

    <title>Welcome to nginx!</title>

    # Test a pod without a matching label:
    The network policy allows traffic from pods labeled app: webapp,role: frontend, but should deny all other traffic. 
    Let's test to see whether another pod without those labels can access the back-end NGINX pod.
    
    # Create another test pod and attach a terminal session:

    k run --rm -it --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11 network-policy --namespace development

    # At the shell prompt, use wget to see if you can access the default NGINX webpage. 
  
    # The network policy blocks the inbound traffic, so the page can't be loaded, as shown in the following example:
    
    wget -O- --timeout=2 --tries=1 http://backend

    wget: download timed out

    exit
