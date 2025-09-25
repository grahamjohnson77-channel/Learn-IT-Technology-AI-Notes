Series 2.4 JsonPath & Custom Columns - GKE.md
*********************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

    REF: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
         https://linuxhint.com/kubernetes-jsonpath/
         https://gist.github.com/noseka1/231105ca1e39b304c7e737323378825a
         https://stackoverflow.com/questions/57418535/kubectl-use-custom-columns-output-with-maps
         https://stackoverflow.com/questions/43225591/selecting-array-elements-with-the-custom-columns-kubernetes-cli-output
         
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
    
    # Delete the cluster
    gcloud container clusters delete cka-gke-cluster --zone europe-west1-b

# Q1. List the pods in Different Ways
    k get pods
    k get po --all-namespaces
    k get pods --sort-by=.metadata.creationTimestamp
    k get pods --no-headers --sort-by=.metadata.name                            # sort asc
    k get pods --no-headers --sort-by=.metadata.name | sort --reverse           # sort desc
    k get po -l name=dev -n q1testns -o name                                    # get by label
    
    k get po nginx --v=6
    k get po nginx --v=7
    k get po nginx --v=8
    k get po nginx --v=9

# Q2. Create Temp Pods with different outputs
    k run busybox --image=busybox -it --rm --restart=Never -- /bin/sh -c 'echo temp pod'
    k run busybox --image=busybox --restart=Never -- /bin/sh -c "sleep 4500"

# Q3. Use JSONPath to Get Cluster Information
    k get po -o json
    k get po -o jsonpath='{@}'
    k get po -o jsonpath='{range .items[0].metadata.name}{"\n"}'
    k get po -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.namespace}{"\n"}{end}'
    k get po -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
    k get po -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}' > testfile.txt
    k get po -A -o jsonpath='{range .items[*]}{.status.podIP}{"\n"}{end}'
    k get po -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"/"}{.metadata.name}{","}{.status.podIP}{"\n"}{end}'
    k get nodes -o jsonpath='{range .items[*]}{.metadata.name} {.status.addresses[?(@.type=="ExternalIP")].address}{"\n"}'

    ip-10-10-40-13.xxxxx.internal xx.xx.xx.175
    ip-10-10-40-15.xxxxx.internal xx.xx.xx.236
    ip-10-10-40-18.xxxxx.internal xx.xx.xx.207
    
    NOTE:
    To quote plain text inside Jsonpath expressions, insert double quotes.
    Iterate lists utilizing the range and end operators.
    Negative slice catalogues are used to go backward through a list.
    @ is the current object
    [ ] or . is the child operator
    . . recursive descent
    * is used to get all objects
    [,]is the union operator
    ” is used to quote interpreted string
    
    Function	        Description                 Example	                                        Result
    text	            the plain text	            kind is {.kind}	                                kind is List
    @	                the current object          {@}	                                            the same as input
    . or []	            child operator	            {.kind} or {['kind']}	                        List
    ..	                recursive descent           {..name}	                                    127.0.0.1 127.0.0.2 myself e2e
    *	                wildcard. Get all objects   {.items[*].metadata.name}	                    [127.0.0.1 127.0.0.2]
    [start:end :step]	subscript operator          {.users[0].name}	                            myself
    [,]	                union operator              {.items[*]['metadata.name', 'status.capacity']}	127.0.0.1 127.0.0.2 map[cpu:4] map[cpu:8]
    ?()	                filter                      {.users[?(@.name=="e2e")].user.password}	    secret
    range, end	        iterate list	            {range .items[*]}[{.metadata.name}, {.status.capacity}] {end}	[127.0.0.1, map[cpu:4]] [127.0.0.2, map[cpu:8]]
    ""	                quote interpreted string	{range .items[*]}{.metadata.name}{"\t"}{end}	127.0.0.1 127.0.0.2

# Q4. Use Custom Columns to Get Cluster Information
    k get po -o=custom-columns="POD_NAME:.metadata.name,POD_STATUS:.status.containerStatuses[].state"
    
    k get svc -o=custom-columns='NAME:.metadata.name,IP:.spec.clusterIP,PORT:.spec.ports[*].targetPort'

    k get pvc -o custom-columns=NAME:.metadata.name,"ANNOTATIONS":".metadata.annotations.pv\.kubernetes\.io/bind-completed" -n monitoring
    
    NAME                                 ANNOTATIONS
    prometheus-k8s-db-prometheus-k8s-0   yes
    prometheus-k8s-db-prometheus-k8s-1   yes

    k get service -n kube-system -o=custom-columns='NAME:.metadata.name,IP:.spec.clusterIP,PORT:.spec.ports[*].targetPort'
    OR
    k get service -n kube-system  -o=custom-columns="NAME:.metadata.name,IP:.spec.clusterIP,PORT:.spec.ports[*].targetPort"
    
    NAME                   IP           PORT
    kube-dns               10.0.0.10    53,53
    kubernetes-dashboard   10.0.0.250   9090

    k get svc -o custom-columns='SVC:.metadata.name,IP:.metadata.annotations.domainName,PORT:.spec.ports[*].targetPort'
    
    SVC      IP          PORT
    event    site1.com   9000 
    gdpr     site2.com   3333,8080
    svcInt   none        80
    ui       site6.com   80,6123,6124,6125,8081
    
    kubectl get nodes -o=custom-columns='NAME:.metadata.name,ROLE:TOBEDEFINED,CPU:.status.capacity.cpu,MEM:.status.capacity.memory,IP:.status.addresses[?(@.type=="InternalIP")].address'
    
    NAME        CPU   MEM   IP
    name-node   8     8     10.10.10.10
    
    kubectl get no -o=custom-columns=NAME:.metadata.name,"MY CUSTOM LABEL":".metadata.labels.me/my-custom-label","AWS NODE SIZE":".metadata.labels.beta\.kubernetes\.io/instance-type"

    Ref: https://duffn.dev/get-kubernetes-nodes-with-custom-columns/
    A couple of notes here:
    This example assumes EKS for the metadata.labels.beta.kubernetes.io/instance-type label, so adjust accordingly for whatever columns you’d like to retrieve.
    Be sure to escape the periods in any of the fields that you’d like to retrieve, like .metadata.labels.beta\.kubernetes\.io/instance-type.
    Also try the custom-columns option with pods!
    
## Reminder to delete the cluster when finished
    gcloud container clusters delete cka-gke-cluster --zone europe-west1-b
