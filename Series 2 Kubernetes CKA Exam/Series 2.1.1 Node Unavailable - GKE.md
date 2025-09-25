Series 2.1.1 Node Unavailable - GKE.md
**************************************

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

# Series 2.1.1 - Make Node Unavailable

## Q1. Node Unavailable

    # Option 1: GKE (Kubernetes Engine on GCP)
    
    Set the node named 'gke-cka-gke-cluster-default-pool-14444c0c-sjk6' as 'unavailable' 
    and reschedule all pods currently on it.
    A.
    k cordon gke-cka-gke-cluster-default-pool-14444c0c-sjk6        # this is not required I believe!
    k drain gke-cka-gke-cluster-default-pool-14444c0c-sjk6 --delete-local-data --ignore-daemonsets --force
    
    # Now we can see that that sjk6 node has no pods running anymore!
    cloudsolutionarchitects_eu@cloudshell:~ (cka-gke-study-project)$ kubectl get pods -o wide
    NAME                                READY   STATUS    RESTARTS   AGE     IP          NODE
    nginx-deployment-544dc8b7c4-cjjhs   1/1     Running   0          10m     10.32.1.6   gke-cka-gke-cluster-default-pool-14444c0c-qg0x
    nginx-deployment-544dc8b7c4-k4nvd   1/1     Running   0          5m40s   10.32.0.5   gke-cka-gke-cluster-default-pool-14444c0c-0ssh
    nginx-deployment-544dc8b7c4-s55b4   1/1     Running   0          10m     10.32.0.4   gke-cka-gke-cluster-default-pool-14444c0c-0ssh
    nginx-deployment-544dc8b7c4-wpbrf   1/1     Running   0          10m     10.32.1.7   gke-cka-gke-cluster-default-pool-14444c0c-qg0x
    
    # uncordon it to take traffic again
    kubectl uncordon gke-cka-gke-cluster-default-pool-14444c0c-sjk6
    
    # find and delete those deployment pods
    # which will cause the pods to get rescheduled
    kubectl get pods --show-labels
    kubectl get pods -l app=nginx
    kubectl delete pods -l app=nginx
    
    cloudsolutionarchitects_eu@cloudshell:~ (cka-gke-study-project)$ kubectl get pods -l app=nginx -o wide
    NAME                                READY   STATUS    RESTARTS   AGE   IP           NODE
    nginx-deployment-544dc8b7c4-6mpll   1/1     Running   0          43s   10.32.2.9    gke-cka-gke-cluster-default-pool-14444c0c-sjk6
    nginx-deployment-544dc8b7c4-87jp9   1/1     Running   0          43s   10.32.2.10   gke-cka-gke-cluster-default-pool-14444c0c-sjk6
    nginx-deployment-544dc8b7c4-schmv   1/1     Running   0          43s   10.32.1.11   gke-cka-gke-cluster-default-pool-14444c0c-qg0x
    nginx-deployment-544dc8b7c4-tl59t   1/1     Running   0          43s   10.32.0.6    gke-cka-gke-cluster-default-pool-14444c0c-0ssh
