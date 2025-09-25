Series 2.3 Ingress Controllers & Resources - GKE.md
***************************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

    REF: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/

    # 2.3 Ingress Controllers: https://kubernetes.io/docs/concepts/services-networking/ingress/
                               https://devopscube.com/kubernetes-ingress-tutorial/
                               https://devopscube.com/setup-ingress-gke-ingress-controller
                               https://devopscube.com/setup-ingress-kubernetes-nginx-controller/
                               https://acloudguru.com/hands-on-labs/configuring-the-nginx-ingress-controller-on-gke
              
    # Ports Explained:         https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-ingress-guide-nginx-example.html

    # Exercises                https://github.com/vkharge/CKA/blob/master/docs/09-Networking/22-Ingress.md

    Exposing each service as a Loadbalancer is not an ideal solution to deal with Kubernetes ingress traffic.

    You need a Kubernetes ingress controller to manage all the ingress traffic for the cluster.
    With direct DNS or a wildcard DNS mapping, you can route traffic to backend kubernetes services.
    
    Ingress allows your users access the application using 1 externally accessible URL (i.e. Layer 7 LB)
    This has has to be exposed on NodePort but 1 time configuration only. Far cleaner approach than expensive multiple LBs
    
    An ingress controller is a piece of software that provides reverse proxy, configurable traffic routing, and TLS termination for Kubernetes services
    
    Kubernetes ingress resources are used to configure the ingress rules and routes for individual Kubernetes services
    
    The rules that are deployed are referred to as the Ingress Resources!

    Also you can have multiple DNS attached to a single ingress Loadbalancer and route to different service backends using the Ingress controller
    In addition, you can have path-based routing rules in the ingress resources to different kubernetes services

    Ingress is an API object that manages external access to the services in a cluster, typically HTTP
    
    # Issues to resolve: 
    Load Balancers can only point to one single Kubernetes object (what if you need 100?)
    What if you require multiple endpoints from 1 web service endpoint ? e.g. mywebsite.com and you need mywebsite.com/support and mywebsite.com/contact to go to completely separate microservices ... the ingress controller can perform internal path resolution for your application!
    
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
    
    # delete cluster when required
    gcloud container clusters delete cka-gke-cluster --zone europe-west1-b
    
    # Vi Configure for :set paste
    Use to keep the formatting in yaml after paste
    
# Ingress Setup on GKE - Nginx Installation on GKE Notes

    # NOTE: Creating the cluster is not enough, we also need to include ingress into it

    https://kubernetes.github.io/ingress-nginx/deploy/
    https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke
    
    kubectl create clusterrolebinding cluster-admin-binding \
      --clusterrole cluster-admin \
      --user $(gcloud config get-value account)
  
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml
    
    kubectl get pods -n ingress-nginx
    kubectl get svc -n ingress-nginx

# Q1. Basic Ingress Controller

    REF: https://acloudguru.com/hands-on-labs/configuring-the-nginx-ingress-controller-on-gke
    
    Create an nginx deployment of 2 replicas, expose it via a NodePort service on port 8080

    # For practice!
    k create ns q1testns

    # Create the Hello World deployment using the container image gcr.io/google-samples/hello-app:1.0 and expose it on port 8080
    
    # Use one of the 2 images below for testing!
    k create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0 --replicas=2 -n q1testns
    OR
    k create deployment hello-world --image=gcr.io/google-samples/whereami:v1.1.1 --replicas=2 -n q1testns
    
    k expose deployment hello-world --type=NodePort --port=8080 -n q1testns
    k get pods -n q1testns
    
    # Get exposed services
    k get svc -n q1testns
    
    # Create Ingress
    vi hello-world-ingress.yaml
    
    kind: Ingress
    apiVersion: networking.k8s.io/v1
    metadata:
      name: hello-world-ingress
      namespace: q1testns
    spec:
      rules:
        - http:
            paths:
            - pathType: Prefix
              path: /
              backend:
                service:
                  name: hello-world
                  port:
                    number: 8080
                    
    kubectl apply -f hello-world-ingress.yaml
    
    # describe the ingress, will run on 80, backend runs on port 8080
    kubectl get ingress hello-world-ingress -n q1testns
    
    kubectl describe ingress hello-world-ingress -n q1testns
    
    NOTE: It took about 3-4 minutes for me to have all available:
    
    Events:
      Type    Reason     Age                  From                     Message
      ----    ------     ----                 ----                     -------
      Normal  Sync       98s                  loadbalancer-controller  UrlMap "k8s2-um-lrl0cilz-q1testns-hello-world-ingress-1fkhm5zl" created
      Normal  Sync       95s                  loadbalancer-controller  TargetProxy "k8s2-tp-lrl0cilz-q1testns-hello-world-ingress-1fkhm5zl" created
      Normal  Sync       86s                  loadbalancer-controller  ForwardingRule "k8s2-fr-lrl0cilz-q1testns-hello-world-ingress-1fkhm5zl" created
      Normal  IPChanged  85s                  loadbalancer-controller  IP is now 35.190.124.193
      Normal  Sync       14s (x6 over 2m28s)  loadbalancer-controller  Scheduled for sync

    # Then, I ran this IP '35.190.124.193' then in the browser and saw:

    Hello, world!
    Version: 1.0.0
    Hostname: hello-world-698598d84c-582nd

    AND!

    # This should work :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q1testns -- wget -O- http://hello-world:8080 --timeout 2

    cloudsolutionarchitects_eu@cloudshell:~ (cka-study-k8s-376910)$ k run busybox1 --image=busybox --rm -it --restart=Never -n q1testns -- wget -O- http://hello-world:8080/hello --timeout 2
    Connecting to hello-world:8080 (10.36.5.185:8080)
    writing to stdout
    Hello, world!
    Version: 1.0.0
    Hostname: hello-world-698598d84c-n5fm8
    -                    100% |********************************|    68  0:00:00 ETA
    written to stdout
    pod "busybox1" deleted

    # Clean up
    kubectl delete -f hello-world-ingress.yaml
    kubectl delete ns q1testns

# Q2. Single Service Ingress Controller Example (1 IP & 1 Service)

    REF: https://www.youtube.com/watch?v=LYBGBuaOH8E
         https://devops4solutions.com/setup-kubernetes-ingress-on-gke/
         https://github.com/devops4solutions/kubernetes-sample-deployment/tree/main/ingress/basic-example

    # For practice!
    k create ns q2testns
    
    # Create deployment
    vi q2_web.yaml
    
    NOTE: I just changed the ns from default to the new q2testns ns below.
    NOTE: For ingress to work, it should have the service type as NodePort OR LoadBalancer
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web
      namespace: q2testns
    spec:
      selector:
        matchLabels:
          run: web
      template:
        metadata:
          labels:
            run: web
        spec:
          containers:
          - image: gcr.io/google-samples/hello-app:1.0
            imagePullPolicy: IfNotPresent
            name: web
            ports:
            - containerPort: 8080
              protocol: TCP
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: web
      namespace: q2testns
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        run: web
      type: NodePort
    
    kubectl apply -f q2_web.yaml
    
    # Get exposed services
    k get svc -n q2testns
    
    # Create Ingress
    vi basic-ingress.yaml
        
    kind: Ingress
    apiVersion: networking.k8s.io/v1
    metadata:
      name: basic-ingress
      namespace: q2testns     
    spec:
      rules:
      - http:
          paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 8080
        
    # create the ingress controller
    kubectl apply -f basic-ingress.yaml
    
    # describe the ingress, will run on 80, backend runs on port 8080
    kubectl get ingress basic-ingress -n q2testns

    NOTE: It took about 3-4 minutes for me to have all available:
    
    kubectl describe ingress basic-ingress -n q2testns
    
    Events:
      Type    Reason     Age                    From                     Message
      ----    ------     ----                   ----                     -------
      Normal  Sync       2m25s                  loadbalancer-controller  UrlMap "k8s2-um-lrl0cilz-q2testns-basic-ingress-o93juehl" created
      Normal  Sync       2m22s                  loadbalancer-controller  TargetProxy "k8s2-tp-lrl0cilz-q2testns-basic-ingress-o93juehl" created
      Normal  Sync       2m12s                  loadbalancer-controller  ForwardingRule "k8s2-fr-lrl0cilz-q2testns-basic-ingress-o93juehl" created
      Normal  IPChanged  2m12s                  loadbalancer-controller  IP is now 34.110.238.65
      Normal  Sync       2m10s (x4 over 3m59s)  loadbalancer-controller  Scheduled for sync
      
    # Then, I ran this IP '34.110.238.65' then in the browser and saw:
    
    Hello, world!
    Version: 1.0.0
    Hostname: web-7bdf9c56b9-c5l6d
    
    AND!
    
    # This should work from cmd line :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q2testns -- wget -O- http://34.110.238.65 --timeout 2
    
    cloudsolutionarchitects_eu@cloudshell:~ (cka-study-k8s-376910)$ k run busybox1 --image=busybox --rm -it --restart=Never -n q2testns -- wget -O- http://34.110.238.65 --timeout 2
    Connecting to 34.110.238.65 (34.110.238.65:80)
    writing to stdout
    Hello, world!
    Version: 1.0.0
    Hostname: web-7bdf9c56b9-c5l6d
    -                    100% |********************************|    60  0:00:00 ETA
    written to stdout
    pod "busybox1" deleted
    
    # Clean up
    kubectl delete -f basic-ingress.yaml
    kubectl delete ns q2testns
    
# Q3. Fanout Ingress Controller Example (1 IP & 1 Service)

    NOTE: This example is continued from previous question above!
    
    REF: https://www.youtube.com/watch?v=LYBGBuaOH8E
         https://devops4solutions.com/setup-kubernetes-ingress-on-gke/
         https://github.com/devops4solutions/kubernetes-sample-deployment/tree/main/ingress/basic-example
         
         https://kubernetes.io/docs/concepts/services-networking/ingress/#simple-fanout
         
    A fanout configuration routes traffic from a single IP address to more than one Service, based on the HTTP URI being requested.
    
    # For practice!
    k create ns q3testns
    
    # Create FIRST deployment!
    
    vi q3_web1.yaml
    
    NOTE: I just changed the ns from default to the new q2testns ns below.
    NOTE: For ingress to work, it should have the service type as NodePort OR LoadBalancer
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web1
      namespace: q3testns
    spec:
      selector:
        matchLabels:
          run: web1
      template:
        metadata:
          labels:
            run: web1
        spec:
          containers:
          - image: gcr.io/google-samples/hello-app:1.0
            imagePullPolicy: IfNotPresent
            name: web1
            ports:
            - containerPort: 8080
              protocol: TCP
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: web1
      namespace: q3testns
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        run: web1
      type: NodePort
    
    kubectl apply -f q3_web1.yaml
    
    --
    
    # Create SECOND deployment!
    
    vi q3_web2.yaml
    
    NOTE: I just changed the ns from default to the new q2testns ns below.
    NOTE: For ingress to work, it should have the service type as NodePort OR LoadBalancer
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web2
      namespace: q3testns
    spec:
      selector:
        matchLabels:
          run: web2
      template:
        metadata:
          labels:
            run: web2
        spec:
          containers:
          - image: gcr.io/google-samples/hello-app:2.0
            imagePullPolicy: IfNotPresent
            name: web2
            ports:
            - containerPort: 8080
              protocol: TCP
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: web2
      namespace: q3testns
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        run: web2
      type: NodePort
    
    kubectl apply -f q3_web2.yaml
    
    # get the deployments and service endpoints
    kubectl get deploy -n q3testns
    kubectl get svc -n q3testns
    
    # Create Ingress
    vi fanout-ingress.yaml
    
    kind: Ingress
    apiVersion: networking.k8s.io/v1
    metadata:
      name: fanout-ingress
      namespace: q3testns     
    spec:
      rules:
      - http:
          paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: web1
                port:
                  number: 8080
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: web2
                port:
                  number: 8080
                  
    # create the ingress controller
    kubectl apply -f fanout-ingress.yaml
    
    # get current ingress
    kubectl get ingress -n q3testns
    
    # describe the ingress, will run on 80, backend runs on port 8080
    kubectl get ingress fanout-ingress -n q3testns

    NOTE: It took about 3-4 minutes for me to have all available:
    
    kubectl describe ingress fanout-ingress -n q3testns
    
    Events:
      Type     Reason     Age                     From                     Message
      ----     ------     ----                    ----                     -------
      Warning  Translate  3m12s (x17 over 8m19s)  loadbalancer-controller  Translation failed: invalid ingress spec: failed to validate prefix path /v1/* due to invalid wildcard; failed to validate prefix path /v2/* due to invalid wildcard
      Normal   Sync       32s                     loadbalancer-controller  UrlMap "k8s2-um-lrl0cilz-q3testns-fanout-ingress-4aeqfetk" created
      Normal   Sync       29s                     loadbalancer-controller  TargetProxy "k8s2-tp-lrl0cilz-q3testns-fanout-ingress-4aeqfetk" created
      Normal   Sync       19s (x5 over 8m19s)     loadbalancer-controller  Scheduled for sync
      Normal   Sync       19s                     loadbalancer-controller  ForwardingRule "k8s2-fr-lrl0cilz-q3testns-fanout-ingress-4aeqfetk" created
      Normal   IPChanged  19s                     loadbalancer-controller  IP is now 34.110.129.201

    # Then, to test FIRST deployment, I ran this IP '34.110.129.201/v1' then in the browser and saw:
    
    Hello, world!
    Version: 1.0.0
    Hostname: web1-557b77d76f-lz6q
    
    AND!
    
    # This should work from cmd line :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q3testns -- wget -O- http://34.110.129.201/v1 --timeout 2
    
    # Then, to test SECOND deployment, I ran this IP '34.110.129.201/v2' then in the browser and saw:
    
    Hello, world!
    Version: 2.0.0
    Hostname: web2-d464f6b7b-wtn6t
    
    AND!
    
    # This should work from cmd line :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q3testns -- wget -O- http://34.110.129.201/v2 --timeout 2
    
    # Clean up
    kubectl delete -f fanout-ingress.yaml
    kubectl delete ns q3testns
    
# Q4. Name-Based Hosting Ingress Controller Example

    NOTE: This example is continued from previous question above!
    
    REF: https://www.youtube.com/watch?v=LYBGBuaOH8E
         https://devops4solutions.com/setup-kubernetes-ingress-on-gke/
         https://github.com/devops4solutions/kubernetes-sample-deployment/tree/main/ingress/basic-example
         
         https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting
         
    For name based hosting will be providing the hostname configuration in our yaml file...
    
    # For practice!
    k create ns q4testns
    
    # Create FIRST deployment!
    
    vi q4_web1.yaml
    
    NOTE: I just changed the ns from default to the new q4testns ns below.
    NOTE: For ingress to work, it should have the service type as NodePort OR LoadBalancer
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web1
      namespace: q4testns
    spec:
      selector:
        matchLabels:
          run: web1
      template:
        metadata:
          labels:
            run: web1
        spec:
          containers:
          - image: gcr.io/google-samples/hello-app:1.0
            imagePullPolicy: IfNotPresent
            name: web1
            ports:
            - containerPort: 8080
              protocol: TCP
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: web1
      namespace: q4testns
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        run: web1
      type: NodePort
    
    kubectl apply -f q4_web1.yaml
    
    --
    
    # Create SECOND deployment!
    
    vi q4_web2.yaml
    
    NOTE: I just changed the ns from default to the new q2testns ns below.
    NOTE: For ingress to work, it should have the service type as NodePort OR LoadBalancer
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web2
      namespace: q4testns
    spec:
      selector:
        matchLabels:
          run: web2
      template:
        metadata:
          labels:
            run: web2
        spec:
          containers:
          - image: gcr.io/google-samples/hello-app:2.0
            imagePullPolicy: IfNotPresent
            name: web2
            ports:
            - containerPort: 8080
              protocol: TCP
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: web2
      namespace: q4testns
    spec:
      ports:
      - port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        run: web2
      type: NodePort
    
    kubectl apply -f q4_web2.yaml
    
    # get the deployments and service endpoints
    kubectl get deploy -n q4testns
    kubectl get svc -n q4testns
    
    # Create Ingress
    vi named-based-hosting-ingress.yaml
    
    kind: Ingress
    apiVersion: networking.k8s.io/v1
    metadata:
      name: named-based-hosting-ingress
      namespace: q4testns   
    spec:
      rules:
      - host: "test1.com"
        http:
          paths:
          - path: /test
            pathType: Prefix
            backend:
              service:
                name: web1
                port:
                  number: 8080
      - host: "test2.com"
        http:
          paths:
          - path: /test
            pathType: Prefix
            backend:
              service:
                name: web2
                port:
                  number: 8080
                  
    # create the ingress controller
    kubectl apply -f named-based-hosting-ingress.yaml
    
    # get current ingress
    kubectl get ingress -n q4testns
    
    # describe the ingress, will run on 80, backend runs on port 8080
    kubectl get ingress named-based-hosting-ingress -n q4testns

    NOTE: It took about 3-4 minutes for me to have all available:
    
    kubectl describe ingress named-based-hosting-ingress -n q4testns
    
    Events:
      Type    Reason     Age                  From                     Message
      ----    ------     ----                 ----                     -------
      Normal  Sync       50s                  loadbalancer-controller  UrlMap "k8s2-um-j6hqob5b-q4testns-named-based-hosting-ingress-nbg1x0jx" created
      Normal  Sync       46s                  loadbalancer-controller  TargetProxy "k8s2-tp-j6hqob5b-q4testns-named-based-hosting-ingress-nbg1x0jx" created
      Normal  Sync       38s                  loadbalancer-controller  ForwardingRule "k8s2-fr-j6hqob5b-q4testns-named-based-hosting-ingress-nbg1x0jx" created
      Normal  IPChanged  37s                  loadbalancer-controller  IP is now 34.110.238.65
      Normal  Sync       34s (x4 over 2m21s)  loadbalancer-controller  Scheduled for sync

    # To access this url, edit /etc/hosts file on Mac (sudo vi /etc/hosts) ... Add a line:

    IP of ingress   test1.com
    IP of ingress   test2.com

    # Then, to test FIRST deployment, I ran this http://test1.com/test then in the browser and saw:
    
    Hello, world!
    Version: 1.0.0
    Hostname: web1-557b77d76f-cqf7j
    
    AND!
    
    # This should work from cmd line :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q4testns -- wget -O- http://34.110.238.65/test --timeout 2
    
    # Then, to test SECOND deployment, I ran this http://test2.com/test then in the browser and saw:
    
    Hello, world!
    Version: 2.0.0
    Hostname: web2-d464f6b7b-568n5

    AND!
    
    # This should work from cmd line :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q4testns -- wget -O- http://34.110.238.65/test --timeout 2

    # Clean up
    kubectl delete -f named-based-hosting-ingress.yaml
    kubectl delete ns q4testns
