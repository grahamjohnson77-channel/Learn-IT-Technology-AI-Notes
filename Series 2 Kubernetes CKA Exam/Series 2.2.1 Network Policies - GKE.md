Series 2.2.1 Network Policies - GKE.md
**************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

    # 2.2 Network Policy Exercises: https://github.com/ahmetb/kubernetes-network-policy-recipes
    #                               https://github.com/GoogleCloudPlatform/gke-network-policy-demo
    # Notes on Calico:              https://docs.projectcalico.org/security/tutorials/kubernetes-policy-basic
    # Notes on Labels:              https://www.golinuxcloud.com/kubernetes-add-label-to-running-pod/
    
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

## Q1. Basic Network Policy Example

    Create an nginx deployment of 2 replicas, expose it via a ClusterIP service on port 80

    # For practice!
    k create ns q1testns

    # Create NetworkPolicy so only pods with labels 'access: granted' can access deployment and apply it
    k create deployment nginx --image=nginx --replicas=2 -n q1testns
    k expose deployment nginx --port=80 -n q1testns
    k get pods -n q1testns

    k describe svc nginx -n q1testns                                       # see 'app=nginx' selector for pods
    or
    k get svc nginx -o yaml -n q1testns

    vi q1.yaml

    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: access-nginx                                                    # pick a name
      namespace: q1testns
    spec:
      podSelector:
        matchLabels:
          app: nginx                                                        # selector for the pods
      ingress:                                                              # allow ingress traffic
      - from:
        - podSelector:                                                      # from pods
            matchLabels:                                                    # with this label
              access: granted

    k create --validate -f q1.yaml

    k get netpol -n q1testns                                                # get and describe netpol

    cloudsolutionarchitects_eu@cloudshell:~ (cka-study-k8s-376910)$ k get netpol -n q1testns
    NAME           POD-SELECTOR   AGE
    access-nginx   app=nginx      26s

    # describe the network policy
    k describe netpol -n q1testns

    cloudsolutionarchitects_eu@cloudshell:~ (cka-study-k8s-376910)$ k describe netpol -n q1testns
    Name:         access-nginx
    Namespace:    q1testns
    Created on:   2023-02-05 10:43:38 +0000 UTC
    Labels:       <none>
    Annotations:  <none>
    Spec:
      PodSelector:     app=nginx
      Allowing ingress traffic:
        To Port: <any> (traffic allowed to all ports)
        From:
          PodSelector: access=granted
      Not affecting egress traffic
      Policy Types: Ingress

    # Get the pods for the question
    k get pods -n q1testns -l app=nginx

    # This should not work :)
    k run busybox1 --image=busybox --rm -it --restart=Never -n q1testns -- wget -O- http://nginx:80 --timeout 2

    # This should be work!
    k run busybox2 --image=busybox --rm -it --restart=Never -n q1testns --labels="access=granted" -- wget -O- http://nginx:80 --timeout 2

    # IF you were to delete the NetPol, it would allow all traffic again!
    k delete netpol access-nginx -n q1testns

    # Finally, clean up:
    k delete ns q1testns

## Q2. Network Policy * (But Do Not Create - Labels Based Fix)

    You have rolled out a new pod (pod1) to your infrastructure and now you need to allow it to communicate with
    the pod2 and pod3 but nothing else. Given the running pod1 in the q2testns ns, edit it to use a
    network policy that will allow it to send and receive traffic only to and from the pod2 and pod3.
    
    Therefore, a new pod4 that was also created should not be allowed access to the pod1.

    NOTE: All required NetworkPolicy resources are already created and ready for use as appropriate.
    You should not create, modify or delete any network policies whilst completing this item.

    HINT: Can we use multiple labels to solve this problem ? e.g. "front-end=web", "back-end=db"
    I.e Is the network policy checking for specific labels for the pod2 and pod3 ?

    For practice!
    k create ns q2testns
    
    # Part 1. Create the required pods
    
    k run pod1 --image=gcr.io/google-samples/hello-app@sha256:2b0febe1b9bd01739999853380b1a939e8102fd0dc5e2ff1fc6892c4557d52b9 --port 8080 --expose -n q2testns
    k run pod2 --image=gcr.io/google-samples/hello-app@sha256:2b0febe1b9bd01739999853380b1a939e8102fd0dc5e2ff1fc6892c4557d52b9 --port 8080 --expose -n q2testns
    k run pod3 --image=gcr.io/google-samples/hello-app@sha256:2b0febe1b9bd01739999853380b1a939e8102fd0dc5e2ff1fc6892c4557d52b9 --port 8080 --expose -n q2testns
    k run pod4 --image=gcr.io/google-samples/hello-app@sha256:2b0febe1b9bd01739999853380b1a939e8102fd0dc5e2ff1fc6892c4557d52b9 --port 8080 --expose -n q2testns
    
    # Please see here on why I could not attach a shell to the version 1.0
    https://askubuntu.com/questions/1448795/why-can-i-not-attach-a-shell-to-googles-hello-appv1-container
    
    # deployment version here
    https://cloud.google.com/kubernetes-engine/docs/samples/container-helloapp-deployment?hl=it

    k describe pod pod1 -n q2testns                                         # label, port 80/TCP etc.

    k get pods -n q2testns -o wide --show-labels                            # show pods and labels
    
    k get all,netpol -n q2testns                                            # show all running components!
    
    # Part 2. Check connections FROM pod1...
    
    k -n q2testns exec --stdin --tty pod1 -- /bin/sh
    
    wget -qO- --timeout=2 <pod2>:8080                                         # pod2 should work!
    wget -qO- --timeout=2 <pod3>:8080                                         # pod3 should work!
    wget -qO- --timeout=2 <pod4>:8080                                         # pod4 should work! (at the start until netpol is applied)

    # Could also try netcat just for testing!
    nc -z -v 10.32.1.8 8080	                                                  # netcat to <pod2 IP> should show open!
    nc -z -v -w 1 10.32.1.8 8080                                              # netcat with timeout

    # Connection using pod1 works at the moment ... thats ok, as no Network Policies have been applied yet.
    Hello, world!
    Version: 2.0.0

    # Test pod access OUT to others if using nginx:
    k -n q2testns exec --stdin --tty pod1 -- /bin/sh
    
    curl -s -I <pod2-ip> | grep HTTP
    curl -s -I <pod3-ip> | grep HTTP
    curl -s -I <pod4-ip> | grep HTTP

    e.g.
    cat /etc/*-release                                                      # show which version of linux is being used
    apk add curl
    curl -s -I 10.68.1.14:8080 | grep HTTP                                  # ok from pod1 OUT to pod2 IP (using headers -I)
    curl -s 10.68.1.14:8080                                                 # ok from pod1 OUT to pod3 IP (using -s output only)
    HTTP/1.1 200 OK

    # Part 3. Check connections TO pod1...
    
    k -n q2testns exec --stdin --tty pod2 -- /bin/sh
    wget -qO- --timeout=2 <pod1 IP>:8080                                     # <pod1 IP> should work!

    k -n q2testns exec --stdin --tty pod3 -- /bin/sh
    wget -qO- --timeout=2 <pod1 IP>:8080                                     # <pod1 IP> should work!

    k -n q2testns exec --stdin --tty pod4 -- /bin/sh
    wget -qO- --timeout=2 <pod1 IP>:8080                                     # <pod1 IP> should work!

    # Connection using pods work at the moment!
    Hello, world!
    Version: 2.0.0
    Hostname: pod1

    NOTE: All communications in and out are working so far :) As expected ...

    # Part 4. Now, create the netpol to block anything but from/to 'app=special'
    
    # INGRESS
    vi hello-only-from-chosen.yaml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: hello-only-from-chosen
      namespace: q2testns
    spec:
      policyTypes:
      - Ingress
      podSelector:
        matchLabels:
          app: special                           # pod applied too is labelled as special
      ingress:
      - from:
        - podSelector:
            matchLabels:
              app: chosen                        # connection allowed from

    k apply --validate -f hello-only-from-chosen.yaml

    # EGRESS
    vi hello-only-to-chosen.yaml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: hello-only-to-chosen
      namespace: q2testns
    spec:
      policyTypes:
      - Egress
      podSelector:
        matchLabels:
          app: special                          # pod applied too is labelled as special
      egress:
      - to:
        - podSelector:
            matchLabels:
              app: chosen                       # connection allowed too

    k apply --validate -f hello-only-to-chosen.yaml

    k get pods -n q2testns -o wide --show-labels                              # show pods and labels
    
    NAME   READY   STATUS    RESTARTS   AGE   IP           NODE                                             NOMINATED NODE   READINESS GATES   LABELS
    pod1   1/1     Running   0          71m   10.32.1.7    gke-cka-gke-cluster-default-pool-122c800b-n8dr   <none>           <none>            run=pod1
    pod2   1/1     Running   0          71m   10.32.1.8    gke-cka-gke-cluster-default-pool-122c800b-n8dr   <none>           <none>            run=pod2
    pod3   1/1     Running   0          71m   10.32.1.9    gke-cka-gke-cluster-default-pool-122c800b-n8dr   <none>           <none>            run=pod3
    pod4   1/1     Running   0          71m   10.32.1.10   gke-cka-gke-cluster-default-pool-122c800b-n8dr   <none>           <none>            run=pod4

    #### Final Solution ####

    # Remember the Question:
    
    You have rolled out a new pod (pod1) to your infrastructure and now you need to allow it to communicate with
    the pod2 and pod3 but nothing else. Given the running pod1 in the q2testns ns, edit it to use a
    network policy that will allow it to send and receive traffic only to and from the pod2 and pod3.
    
    Therefore, a new pod4 that was also created should be be allowed access to the pod1.

    # NOTE: All required NetworkPolicy resources are already created and ready for use as appropriate.
    You should not create, modify or delete any network policies whilst completing this item.

    # FIRST! See EVERYTHING THAT IS RUNNING IN THE NAMESPACE!
    k get -n q2testns all,netpol -o wide --show-labels                        # show all running components!
    
    # --- NOTE: In the exam, there were 4 Network Policies so these might exist too be default
    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: default-deny-ingress
      namespace: q2testns
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
    ---
    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: default-deny-egress
      namespace: q2testns
    spec:
      podSelector: {}
      policyTypes:
      - Egress

    # Describe the existing Network Policies in place:                        # describe netpols for flows
    k describe netpol hello-only-from-chosen -n q2testns
    k describe netpol hello-only-to-chosen -n q2testns

    # Question states to only allow connections from pod1 to others! (would be 'PodSelector' field!):
    k label pod pod1 {run=pod1,app=special} -n q2testns --overwrite            # add multiple labels at once!

    # Question states to only allow connections to pod2 and pod3! (would be 'To/From PodSelector' field!):
    k label pod pod2 {run=pod2,app=chosen} -n q2testns --overwrite             # add multiple labels at once!
    k label pod pod3 {run=pod3,app=chosen} -n q2testns --overwrite             # add multiple labels at once!

    k get pods -o wide -n q2testns --show-labels                               # show pods and labels again now!

    # Check connections FROM pod1...(AGAIN!) IP: 10.68.1.23
    k -n q2testns exec --stdin --tty pod1 -- /bin/sh

    wget -qO- --timeout=2 10.32.1.8:8080                                        # <pod2 IP> should work!
    wget -qO- --timeout=2 10.32.1.9:8080                                        # <pod3 IP> should work!
    wget -qO- --timeout=2 10.32.1.10:8080                                       # <pod4 IP> should fail! (no label)
                                                                                # e.g. wget: download timed out
                                                                            
    # Could also try netcat just for testing!
    nc -z -v -w 1 10.68.1.24 8080	                                            # netcat to <pod2 IP> should be open!
    nc -z -v -w 1 10.68.1.25 8080	                                            # netcat to <pod3 IP> should be open!
    nc -z -v -w 1 10.68.1.26 8080	                                            # netcat to <pod4 IP> should be closed!
    nc -z -v -w 1 10.68.1.14 8080                                               # netcat with timeout

    # Check connections TO pod1...(AGAIN!)
    k -n q2testns exec --stdin --tty pod2 -- /bin/sh
    wget -qO- --timeout=2 10.68.1.7:8080                                        # <pod1 IP> should work!

    k -n q2testns exec --stdin --tty pod3 -- /bin/sh
    wget -qO- --timeout=2 10.68.1.23:8080                                       # <pod1 IP> should work!

    k -n q2testns exec --stdin --tty pod4 -- /bin/sh
    wget -qO- --timeout=2 10.68.1.23:8080                                       # <pod1 IP> should fail!
                                                                                # e.g. wget: download timed out
    # Finally, clean up:
    k delete ns q2testns

## Q3. Network Policies Example on GKE

    Configure a NetworkPolicy to allow traffic to the hello-web Pods from only the app=foo Pods. 
    Other incoming traffic from Pods that do not have this label, external traffic, and traffic from Pods in other namespaces are blocked.
    
    # For practice!
    k create ns q3testns
    
    # First, run a web server application with label app=hello and expose it internally in the cluster:
    kubectl run hello-web --labels app=hello \
      --image=us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0 --port 8080 --expose -n q3testns

    The following manifest selects Pods with label app=hello and specifies an Ingress policy to allow traffic only from Pods with the label app=foo:

    vi hello-allow-from-foo.yaml

    kind: NetworkPolicy
    apiVersion: networking.k8s.io/v1
    metadata:
      name: hello-allow-from-foo
      namespace: q3testns
    spec:
      policyTypes:
      - Ingress
      podSelector:
        matchLabels:
          app: hello
      ingress:
      - from:
        - podSelector:
            matchLabels:
              app: foo

    k apply --validate -f hello-allow-from-foo.yaml

    # Validate the Ingress policy
    First, run a temporary Pod with the label app=foo and get a shell in the Pod:
    kubectl run -l app=foo --image=alpine --restart=Never --rm -i -t test-1 -n q3testns

    # Make a request to the hello-web:8080 endpoint to verify that the incoming traffic is allowed:
    wget -qO- --timeout=2 http://hello-web:8080
    
    exit

    # Next, run a temporary Pod with a different label (app=other) and get a shell inside the Pod:
    kubectl run -l app=other --image=alpine --restart=Never --rm -i -t test-1 -n q3testns

    wget -qO- --timeout=2 http://hello-web:8080

    wget: download timed out
    
    # delete the namespace
    k delete namespace q3testns

    # Restricting outgoing traffic from the Pods
    https://cloud.google.com/kubernetes-engine/docs/tutorials/network-policy#restricting_outgoing_traffic_from_the_pods
