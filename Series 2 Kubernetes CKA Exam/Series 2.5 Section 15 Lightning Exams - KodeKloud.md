Series 2.5 Lightning Labs - KodeKloud.md
****************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

## Introduction

    To join KodeKloud for CKA for the Course, Labs and Mock Exams:
    https://kodekloud.com/courses/certified-kubernetes-administrator-cka/

    Use the following lab by KodeKloud:
    https://kodekloud.com/lessons/lightning-labs-3/

    Part of the 'Certified Kubernetes Administrator (CKA) with Practice Tests' course:
    https://www.udemy.com/share/101Xtg3@xUHP8uVHKj8-v6hPn2j_h9jWI8F7ASIr-UmWxrYnolWuwnZAfQZrPAQf2BXYvQbF/
    
## Useful Exam Cmds

    # Aliases
    alias k=kubectl

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage
    cat pod.yaml                                                                # output file

## Q1. Upgrade Cluster

    Upgrade the current version of kubernetes from 1.25.0 to 1.26.0 exactly using the kubeadm utility.
    Make sure that the upgrade is carried out one node at a time starting with the controlplane node.
    To minimize downtime, the deployment gold-nginx should be rescheduled on an alternate node before upgrading each node.

    Upgrade controlplane node first and drain node node01 before upgrading it.
    Pods for gold-nginx should run on the controlplane node subsequently.

    # Search Keyword: kubeadm upgrade (in Tasks!)
    # REF: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

    kubectl get nodes                                   # explore the environment (shows roles, age & versions!)
    #OR
    kubeadm version                                     # show version of cluster
    kubectl version --short                             # show the short version!
    kubectl get pods -o wide                            # show many nodes can host workloads in this cluster
    kubectl get deployments.apps -o wide                # show many applications are hosted on the cluster

    kubectl get pods -o wide | grep gold                # see where the deployment is currently scheduled
    kubectl describe node controlplane | grep -i taint  # check for any existing taints at the start

    # Work on ControlPlane
    kubectl drain controlplane --ignore-daemonsets      # upgrading the master node first (marks it UnSchedulable)
    sudo -i                                             # run whoami command to see if already root! otherwise login as root
    apt update                                          # upgrade the system first

    apt install kubeadm=1.26.0-00                       # upgrade kubeadm tool first
    apt install kubelet=1.26.0-00                       # update the kubelet version (updates the master)
    apt install kubectl=1.26.0-00                       # update the kubectl version (updates the master)
    OR
    apt install kubeadm=1.26.0-00 kubelet=1.26.0-00 kubectl=1.26.0-00
    
    apt-mark hold kubeadm                               # make sure its not upgraded automatically
    apt-mark hold kubelet                               # make sure its not upgraded automatically
    apt-mark hold kubectl                               # make sure its not upgraded automatically
    OR
    apt-mark hold kubeadm kubelet kubectl
    
    kubeadm upgrade plan v1.26.0                        # shows latest versions available for upgrade plan
    kubeadm upgrade apply v1.26.0                       # upgrade the cluster - apply your upgrade plan
    systemctl daemon-reload                             # restart the daemon reload
    systemctl restart kubelet.service                   # recheck kubelet service
    systemctl status kubelet.service                    # status kubelet service
    
    kubectl get nodes                                   # explore the environment (shows roles, age & versions!)
    kubectl uncordon controlplane                       # mark the master to be scheduleable again!
    kubeadm version                                     # show version of cluster (again)

    # Before draining node01, we need to remove the taint from the controlplane node.
    # Remove the taint with help of "kubectl taint" command.
    # NOTE: When we run the drain command, it will move the deployment over to another available node
    kubectl describe node controlplane | grep -i taint
    kubectl taint node controlplane node-role.kubernetes.io/control-plane:NoSchedule-
    kubectl describe node controlplane | grep -i taint
    
    kubectl get pods -o wide | grep gold                # see where the deployment is currently scheduled

    # Work on node01
    kubectl drain node01 --ignore-daemonsets            # upgrading the node01 (marks it UnSchedulable)
    ssh node01
    apt-get update                                      # upgrade system - will this take long ?
    
    apt install kubeadm=1.26.0-00                       # upgrade kubeadm tool first
    apt install kubelet=1.26.0-00                       # update the kubelet version
    apt install kubectl=1.26.0-00                       # update the kubectl version
    OR
    apt install kubeadm=1.26.0-00 kubelet=1.26.0-00 kubectl=1.26.0-00
    
    apt-mark hold kubeadm                               # make sure its not upgraded automatically
    apt-mark hold kubelet                               # make sure its not upgraded automatically
    apt-mark hold kubectl                               # make sure its not upgraded automatically
    OR
    apt-mark hold kubeadm kubelet kubectl
    
    kubeadm upgrade node                                # upgrade node configuration (using kubeadm!)
    
    systemctl daemon-reload                             # restart the daemon reload
    systemctl restart kubelet.service                   # recheck kubelet service
    systemctl status kubelet.service                    # status kubelet service
    
    Ctrl+d to log out of node01 or type exit
    kubectl uncordon node01                             # make node01 schedulable again!
    kubectl get nodes                                   # explore the environment (shows roles, age & versions!)

    kubectl get pods -o wide | grep gold                # make sure this is scheduled on node
    
    At the end, are is the Cluster Upgraded? and pods 'gold-nginx' running on controlplane?

## Q2. Printing

    Print the names of all deployments in the admin2406 namespace in the following format:
    DEPLOYMENT CONTAINER_IMAGE READY_REPLICAS NAMESPACE
    <deployment name> <container image used> <ready replica count> <Namespace>
    The data should be sorted by the increasing order of the deployment name.

    Write the result to the file /opt/admin2406_data.
    Hint: Make use of -o custom-columns and --sort-by to print the data in the required format.

    # Search Keyword: custom-columns
    # REF: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

    # Note, there are 2 ways to complete this question, either with custom-columns or 'vi visual block'
    # Option 1:
    kubectl -n admin2406 get deployment -o json
    kubectl -n admin2406 get deployment -o custom-columns=DEPLOYMENT:.metadata.name,CONTAINER_IMAGE:.spec.template.spec.containers[].image,READY_REPLICAS:.status.readyReplicas,NAMESPACE:.metadata.namespace --sort-by=.metadata.name > /opt/admin2406_data
    cat /opt/admin2406_data

    # Option 2:
    k get deployments.apps -A | grep admin2406
    k get deployments.apps -A -o wide | grep admin2406
    k get deployments.apps -A -o wide | grep admin2406 > /opt/admin2406_data
    vi /opt/admin2406_data
    Highlight and remove the 7m6s and nginx fields from the file using 'Vi Visual Block'
    Highlight and remove the first admin2406 field using 'Vi Visual Block'

    Resulting file should look like (with deploy1 to 5 listed):

    DEPLOYMENT   CONTAINER_IMAGE   READY_REPLICAS   NAMESPACE
    deploy1      nginx             1                admin2406
    deploy2      nginx:alpine      1                admin2406
    deploy3      nginx:1.16        1                admin2406
    deploy4      nginx:1.17        1                admin2406
    deploy5      nginx:latest      1                admin2406


## Q3. Troubleshooting

    A kubeconfig file called admin.kubeconfig has been created in /root/CKA. There is something wrong with the configuration. Troubleshoot and fix it.
    
    kubectl cluster-info                                        # get cluster info

    # Search Keyword:
    vi /root/CKA/admin.kubeconfig
    server: https://controlplane:6443                            # update this line to match (port was incorrect)

    kubectl cluster-info --kubeconfig /root/CKA/admin.kubeconfig # to know cluster information

## Q4. Upgrade Deployment

    Create a new deployment called nginx-deploy, with image nginx:1.16 and 1 replica.
    Next upgrade the deployment to version 1.17 using rolling update.
    Make sure that the version upgrade is recorded in the resource annotation.
    
    # Search Keyword: Deployment (Updating)
    # REF: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment

    kubectl create deployment nginx-deploy --image=nginx:1.16 --replicas=1
    kubectl set image deployment/nginx-deploy nginx=nginx:1.17 --record

## Q5. Persistent Volumes

    A new deployment called alpha-mysql has been deployed in the alpha namespace. However, the pods are not running. Troubleshoot and fix the issue.
    The deployment should make use of the persistent volume alpha-pv to be mounted at /var/lib/mysql and should use the environment 
    variable MYSQL_ALLOW_EMPTY_PASSWORD=1 to make use of an empty root password.
    Important: Do not alter the persistent volume.

    # Search Keyword: PersistentVolumeClaims
    # REF: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims

    kubectl get pods
    kubectl -n alpha get pods
    kubectl -n alpha describe po alpha-mysql-6d945ffc78-cfhjg
    It will show that the mysql-alpha-pvc not found!
    
    kubectl -n alpha get pv
    kubectl -n alpha get pvc

    NOTE: The claim shold have the exact same access Modes as the PV so that it can bind to it!

    vi pvc.yaml

    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: mysql-alpha-pvc
      namespace: alpha
    spec:
      accessModes:
        - ReadWriteOnce
      volumeMode: Filesystem
      resources:
        requests:
          storage: 1Gi
      storageClassName: slow

    kubectl create -f pvc.yaml                  # create the claim
    kubectl -n alpha get pvc
    history                                     # show history
    !30                                         # re-run the command to describe the pod that was failing (might be a different index number?)

## Q6. Backup ETCD

    Take the backup of ETCD at the location /opt/etcd-backup.db on the controlplane node

    # Search Keyword: etcd
    # REF: https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

    # At what address can you reach the ETCD cluster from the controlplane node?
    kubectl -n kube-system describe pod etcd-controlplane

    # Check if current command is working first!
    ETCDCTL_API=3 etcdctl member list --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://127.0.0.1:2379

    # Take a snapshot backup of the current etcdctl
    ETCDCTL_API=3 etcdctl snapshot save --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://127.0.0.1:2379 /opt/etcd-backup.db

    NOTE: This line shows the endpoint of etcd: --listen-client-urls=https://127.0.0.1:2379,https://172.17.0.44:2379
    NOTE: This line shows the path of the trusted ca certificate: --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    NOTE: This line shows the path of the server certificate: --cert-file=/etc/kubernetes/pki/etcd/server.crt
    NOTE: This line shows the path of the key-file: --key-file=/etc/kubernetes/pki/etcd/server.key

    ETCDCTL_API=3 etcdctl snapshot save -h                     # show the options for taking snapshots

## Q7. Secrets

    Create a pod called secret-1401 in the admin1401 namespace using the busybox image.
    The container within the pod should be called secret-admin and should sleep for 4800 seconds.

    The container should mount a read-only secret volume called secret-volume at the path /etc/secret-volume.
    The secret being mounted has already been created for you and is called dotfile-secret.

    # Search Keyword: secrets
    # REF: https://kubernetes.io/docs/concepts/configuration/secret/

    kubectl get secrets                                        # list the current secrets
    kubectl get pods,svc                                       # list out those components

    k -n admin1401 run secret-1401 --image=busybox --dry-run=client -o yaml > q7.yaml
    vi q7.yaml

    First, Update the 'container' name: field to be secret-admin ... 

    apiVersion: v1
    kind: Pod
    metadata:
      labels:
        run: secret-1401
      name: secret-1401
      namespace: admin1401
    spec:
      containers:
        - name: secret-admin
          image: busybox
          command: ["sleep","4800"]
          volumeMounts:
          - name: secret-volume
            mountPath: /etc/secret-volume
            readOnly: true
      volumes:
      - name: secret-volume
        secret:
          secretName: dotfile-secret

    kubectl apply -f q7.yaml
    kubectl get pods -n admin1401
    kubectl describe pod secret-1401 -n admin1401
