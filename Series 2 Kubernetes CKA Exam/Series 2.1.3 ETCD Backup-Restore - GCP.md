Series 2.1.3 ETCD Backup-Restore - GCP.md
*****************************************

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
  
# Series 2.1.3 - Backup-Restore ETCD Keystore DB

    # NOTE: Check these for good information too before you start!
    https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
    https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster
    https://github.com/mmumshad/kubernetes-cka-practice-test-solution-etcd-backup-and-restore
    https://docs.vmware.com/en/VMware-Application-Catalog/services/tutorials/GUID-backup-restore-data-etcd-kubernetes-index.html

## Q3. Practice Backup and Restore ETCD

    # Using Option 2: GCP Cluster
    
    sudo apt install etcd-client                                                # I had to install etcd using this on GCP cluster
    
    etcdctl version                                                            # GCP Cluster get version e.g. 3.3.13
    etcdctl -version                                                             # RaspberryPi get version e.g. 3.3.13
    
    kubectl -n kube-system get pods                                             # get etcd-master is running
    
    kubectl get deployments.apps                                                # get deployments
    kubectl -n kube-system get pods                                             # get running etcd-master is running there
    kubectl -n kube-system describe pod etcd-controller                         # insect version of the etcd pod on the system

    kubectl -n kube-system logs etcd-controller | grep -i 'etcd-version'        # find out exact version of the etcd running e.g. 3.5.6

    # At what address can you reach the ETCD cluster from the controlplane node?
    kubectl -n kube-system describe pod etcd-controller | grep '\--listen-client-urls'

    # Where is the ETCD server certificate file located?
    kubectl describe pod etcd-controller -n kube-system                          # find out the exact version of the etcd running on the cluster
    OR
    kubectl describe pod etcd-controller -n kube-system | grep .crt              # even better command!

    # NOTE: This line shows the endpoint of etcd: --listen-client-urls=https://127.0.0.1:2379,https://172.17.0.44:2379
    # NOTE: This line shows the path of the server certificate: --cert-file=/etc/kubernetes/pki/etcd/server.crt
    # NOTE: This line shows the path of the trusted ca certificate: --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

    ETCDCTL_API=3 etcdctl snapshot save -h                                        # show the options for taking snapshots

    # Lets start the snapshot backup!
    sudo -i                                                                       # log in as root
    
    # List the current members that use the database store
    ETCDCTL_API=3 etcdctl member list --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://127.0.0.1:2379
    
    e.g.
    3334fe02fedea274, started, controller, https://10.240.0.11:2380, https://10.240.0.11:2379
    
    # Maintenance tonight so lets make a ETCD backup! 
    Store the backup at /backup20230204/snapshot-etcd.db
    
    mkdir /backup20230204                                                          # just a dummy folder for holding snapshot for now
    ls -lhr /backup20230204                                                        # list contents of the folder
    
    ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key \
    snapshot save /backup20230204/snapshot-etcd.db
    
    Snapshot saved at /backup20230204/snapshot-etcd.db                             # snapshot saved
    
    exit                                                                           # come back out of root
    
    # IMAGINE MAINTENANCE IS ONGOING NOW ... OOPS, WE HAVE AN ISSUE !

    # Something is wrong with applications, none are working :(
    
    kubectl get pods,deployments,svc                                                # show the current status (but nothing is shown!)
    kubectl -n kube-system get pods                                                 # get etcd-master is running there
    
    # Lets start the snapshot restore!
    sudo -i                                                                         # log in as root

    # Check data dir of existing setup
    cat /etc/kubernetes/manifests/etcd.yaml | grep etcd                             # find occurences of etcd in the etcd file
    
    # Restore the original state of the cluster using the backup file.
    ETCDCTL_API=3 etcdctl snapshot restore -h                                        # show the options for snapshots restore!
    
    ls -lhr /var/lib/etcd-from-backup                                                # nothing in our data working directory as yet

    # Restore the snapshot backup!
    ETCDCTL_API=3 etcdctl --data-dir=/var/lib/etcd-from-backup \
    snapshot restore /backup20230204/snapshot-etcd.db
    
    OR
    
    ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --name=controller \
     --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key \
     --data-dir /var/lib/etcd-from-backup \
     --initial-cluster=controller=https://127.0.0.1:2380 \
     --initial-cluster-token etcd-cluster-1 \
     --initial-advertise-peer-urls=https://127.0.0.1:2380 \
     snapshot restore /backup20230204/snapshot-etcd.db
    
    ls -lhr /var/lib/etcd-from-backup                                                # whats there now ? yes, a new member folder!

    # You should see something like
    2022-08-22 09:08:36.419427 I | mvcc: restore compact to 956
    2022-08-22 09:08:36.426445 I | etcdserver/membership: added member 8e9e05c52164694d [http://localhost:2380] to cluster cdf818194e3a8c32
    
    # Note: In this case, we are restoring the snapshot to a different directory but in the same server where we took the backup (the controlplane node) 
    As a result, the only required option for the restore command is the --data-dir.

    # Edit the data dir location to the new backup
    cp /etc/kubernetes/manifests/etcd.yaml /etc/kubernetes/manifests/etcd.yaml.bk   # backup the file incase of issue later
    
    vi /etc/kubernetes/manifests/etcd.yaml                                           # go here so we can update location
    
    --data-dir=/var/lib/etcd                                                         # original
    e.g.
    --data-dir=/var/lib/etcd-from-backup                                             # new!

    # We have now restored the etcd snapshot to a new path
    On the controlplane - /var/lib/etcd-from-backup, so, the only change to be made in the YAML file, is to change the hostPath for the volume called etcd-data from old directory (/var/lib/etcd) to the new directory (/var/lib/etcd-from-backup).

    # Update the volumeMount and hostPath sections for etcd-data entry! e.g.
    
        volumeMounts:
        - mountPath: /var/lib/etcd-from-backup
          name: etcd-data
      volumes:
      - hostPath:
          path: /var/lib/etcd-from-backup
          type: DirectoryOrCreate
        name: etcd-data

    # With this change, /var/lib/etcd on the container points to /var/lib/etcd-from-backup on the controlplane
    
    # When this file is updated, the ETCD pod is automatically re-created as this is a static pod placed under the /etc/kubernetes/manifests directory.

    # Note 1: If the etcd pod is not getting Ready 1/1, then
    restart it by 'kubectl delete pod -n kube-system etcd-master2' and wait 1 minute.
    
    kubectl -n kube-system delete pod etcd-controller

    # Note 2: This is the simplest way to make sure that ETCD uses the restored data after the ETCD pod is recreated.
    You don't have to change anything else.

    kubectl -n kube-system get pods                                                             # get etcd-master is running there
    kubectl -n kube-system describe pod etcd-controller                                         # insect version of etcd-master pod on the system

    # Show the new etcd member list
    ETCDCTL_API=3 etcdctl member list --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://127.0.0.1:2379

    # Recheck the pods, deployments and svcs are now working as before!
    kubectl get pods,deployments.apps,svc 											             # get pods,deployments,svc
    
    # Only use if you want to revert back to original state
    backup20230204
    rm -rf /var/lib/etcd-from-backup
    rm -rf /backup20230204
    
    # Before we go let’s do some cleanup and remove our nginx test deployment.

    # Finally, please delete the resources to save credits or money!
    kubectl delete -f nginx-fake-deployment.yaml
