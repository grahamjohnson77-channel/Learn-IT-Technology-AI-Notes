Series 2.7 Mock Exam 2 - KodeKloud.md
*************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

## Introduction

    To join KodeKloud for CKA for the Course, Labs and Mock Exams:
    https://kodekloud.com/courses/certified-kubernetes-administrator-cka/
    
    Use the following lab by KodeKloud:
    https://kodekloud.com/topic/mock-exam-2-4/
    
    Part of the 'Certified Kubernetes Administrator (CKA) with Practice Tests' course:
    https://www.udemy.com/share/101Xtg3@xUHP8uVHKj8-v6hPn2j_h9jWI8F7ASIr-UmWxrYnolWuwnZAfQZrPAQf2BXYvQbF/
    
## Useful Exam Cmds

    # Aliases
    alias k=kubectl

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage
    cat pod.yaml                                                                # output file

## Mock Exam 2

    # Search Keyword: etcd
    # REF: https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

    ETCDCTL_API=3 etcdctl version 																    # show current etcd version
    cd /etc/kubernetes/manifests/ 																    # show the current version
    cat etcd.yaml 	 																			            # get the cacert and cert locations

    ETCDCTL_API=3 etcdctl ....																	      # get the entire command string from the etcd.yaml file!
    ETCDCTL_API=3 etcdctl .... member list 														# get the entire command string from the etcd.yaml file! But check it works!
    ETCDCTL_API=3 etcdctl .... snapshot save /tmp/etcd-backup.db			# get the entire command string from the etcd.yaml file! Save the snapshot
    ETCDCTL_API=3 etcdctl .... snapshot status /tmp/etcd-backup.db -w table						# get the entire command string from the etcd.yaml file! Verify the snapshot

    Final answer:
    cat /etc/kubernetes/manifests/etcd.yaml | grep file            # show the current files listed

    ETCDCTL_API=3 etcdctl --endpoints 127.0.0.1:2379 snapshot save /opt/etcd-backup.db \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key

    ls -lhr /opt
    
    ..
    
    # Search Keyword: PersistentVolume
    # REF: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolume

    kubectl run redis-storage --image=redis:alpine --dry-run=client -o yaml > redis-storage.yaml
    vi redis-storage.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: redis-storage
      name: redis-storage
    spec:
      containers:
      - image: redis:alpine
        name: redis-storage
        resources: {}
        volumeMounts:
        - name: cache-volume
          mountPath: /data/redis
      volumes:
        - name: cache-volume
          emptyDir: {}

    kubectl create -f redis-storage.yaml
    kubectl describe pod redis-storage
    
    ..
    
    REF: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
    
    kubectl run super-user-pod --image=busybox:1.28 --dry-run=client -o yaml > super-user-pod.yaml

    vi super-user-pod.yaml

    Add the following under 'resources field' in the container:
    securityContext:
      capabilities:
        add: ["SYS_TIME"]

    Because is a busybox image, it needs also this line under name:
      command: ["sleep","4800"]

    kubectl create -f super-user-pod.yaml
    kubectl get pods
    kubectl describe pod super-user-pod
    
    ..
    
    # Search Keyword: pvc
    # REF: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims

    cat /root/CKA/use-pv.yaml
    kubectl get pv
    kubectl get pvc

    vi pvc.yaml                                                       # create the pvc first

    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: my-pvc
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 10Mi

    kubectl create -f pvc.yaml
    kubectl get pvc

    NOTE: The PVC should be in a bound status now!

    # Search Keyword: claims as volumes
    # REF: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#claims-as-volumes

    vi /root/CKA/use-pv.yaml

    Remove everything after name tag!

    Then add:

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: use-pv
      name: use-pv
    spec:
      containers:
      - image: nginx
        name: use-pv
        volumeMounts:
          - mountPath: "/data"
            name: mypd
      volumes:
        - name: mypd
          persistentVolumeClaim:
            claimName: my-pvc

    kubectl create -f /root/CKA/use-pv.yaml
    kubectl describe pod use-pv
    
    ..
    
    kubectl create deploy nginx-deploy --image=nginx:1.16                           # create a new deployment (notice the record option!)
    kubectl scale deployment.apps/nginx-deploy --replicas=1
    kubectl get deploy
    kubectl describe pod nginx-deploy
    kubectl rollout history deployment nginx-deploy 											          # get the rollout history
    kubectl set image deployment.apps/nginx-deploy nginx=nginx:1.17 --record        # upgrade the deployment to new version (nginx=nginx:1.17 is for container!)
    kubectl describe deployments nginx-deploy | grep -i image 									    # show the image version now
    
    ..
    
    # Search Keyword: signing request
    # REF: https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/

    ls /root/CKA/                                                                   # list files
    cd /root/CKA
    cat john.csr                                                                    # look at existing csr (signing request)

    ls -lhr | tail -2 																# check to see if the john.key and john.csr are available
    kubectl api-versions | grep certificates

    cat john.csr | base64 | tr -d "\n"                                              # get the csr in base64 encoding for the new CSR below!

    # Part 1. First, create a signing request and get it approved
    vi john_csr.yaml

    apiVersion: certificates.k8s.io/v1
    kind: CertificateSigningRequest
    metadata:
      name: john-developer
    spec:
      request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZEQ0NBVHdDQVFBd0R6RU5NQXNHQTFVRUF3d0VhbTlvYmpDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRApnZ0VQQURDQ0FRb0NnZ0VCQU5CQ1VqVUNTUnR4NWNWVVZScndCc2RaUUJXbGhETHR0SWxqVnlVTGNYSnR4cEQ5CkhDNSthVW5Cd2lRSkM0TnZ4eWZDczE1b3ZNUEg4a2xOelIwRWZlTTcxUm9SMzlnUzZCcDhLYktmckZNcnBXM2MKUWdLOVF6U3dGbXBOazMyYWZheDlxRFBuY3hsczFPUk5uZUozSXc2N1ovVDhRYzJxcDFOUEMyeVdnenRWSkZSRApTamNrQWZzYU5MQUFUTXFZWE9XWTVKdU40RW1EdmRsNnovSzJINHBtK3RWaTVYVGo3Y0RYdENIemd3d0VsR0FNCkFVNS9HZjNnbUp1VDNZOXZhdHRkaUpXdkRsbG1zSWhrQnFQaHR6WThoRndxbW5MY0YyQXF3YmljVTBYY1lnWUgKeFlwQzFCbUxJV0pkbnUzSGVoZjRxNEtOcEJVQ0Yyb3lPTldWNThNQ0F3RUFBYUFBTUEwR0NTcUdTSWIzRFFFQgpDd1VBQTRJQkFRQmFwSFNsdVQ4ZVUwbGoyMDIxQXhtS0UvblhqaCtqTWtvNnRXa1RtcWQvaFpYZWp6dXN5S2kyCmJiV28yRFF3Z2RDcjIvN2o4NDFXT0FPN1V0M01qckp0SEhxTmdLeXV4QzF2NlNSTlRxMzFvdDZrejI1aDRvMEoKenNFVDg3K3NOUEZGYnlCYm1PU1JjSmhsVHRsNFl6TXRZQVA5QUpCR2hmZWhwVWN5Wk1ZUXcrRHBMblNzOXl3SgovNGtTV1lkT1NIdk1kUHg3dnFpS3dUMHVyT05NUG9ucndFcCtDNFVKaGVtb2hJRENma21FTVdnZldGTzZQeUN5CnByUEIrQklSbmNneHQ4YXJWMmxNKzF3dDIveUVDWWZlUGZhZ1h4b2pLay9XTmE0K2tnS3RsdmJMVmpLTFdtZXYKZEJwTmhDM3dDY1NpdThqSkRNcDMzRWdpQXgvclZBSnYKLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tCg==
      signerName: kubernetes.io/kube-apiserver-client
      usages:
      - client auth

    kubectl create -f john_csr.yaml

    controlplane ~/CKA ➜  kubectl create -f john_csr.yaml
    certificatesigningrequest.certificates.k8s.io/john-developer created

    kubectl get csr 														# should now show the john-developer csr at pending state
    kubectl certificate approve john-developer								# need to approve it! to change the status

    certificatesigningrequest.certificates.k8s.io/john-developer approved

    # Part 2. Create the new developer role
    kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development
    kubectl get role -n development
    kubectl describe role developer --namespace=development
    kubectl get clusterroles.rbac.authorization.k8s.io --namespace=development
    kubectl get roles.rbac.authorization.k8s.io --namespace=development

    # Part 3. Add john to that role
    kubectl create rolebinding developer-role-binding --role=developer --user=john --namespace=development
    kubectl -n development describe rolebindings.rbac.authorization.k8s.io developer-role-binding 	# describe the role to see if John is a user now!
    kubectl auth can-i update pods --as=john --namespace=development 								# check if john can now run a simple 'update pods' command (yes!)
    kubectl auth can-i delete pods --as=john --namespace=development 								# check if john can now run a simple 'delete pods' command (yes!)
    kubectl auth can-i list pods --as=john --namespace=development 									# check if john can now run a simple 'list pods' command (yes!)
    kubectl auth can-i watch pods --as=john --namespace=development 								# check if john can now run a simple 'watch pods' command (no!)
    
    ..
    
    # Search Keyword: dns
    # REF: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
    
    kubectl run nginx-resolver --image=nginx                                        # create the pod
    kubectl get pods                                                                # list the pod
    kubectl expose pod nginx-resolver --name=nginx-resolver-service --port=80 		  # expose the pod on the service with a name!
    kubectl describe svc nginx-resolver-service                                     # check if service has an endpoint and selectors ?
    kubectl run busybox --image=busybox:1.28 -- sleep 4000                         # create a pod but use sleep trick to keep it running

    kubectl exec busybox -- nslookup nginx-resolver-service                         # check if we can resolve the service
    kubectl exec busybox -- nslookup nginx-resolver-service > /root/CKA/nginx.svc   # save results to svc file
    cat /root/CKA/nginx.svc

    kubectl get pods -o wide                                                        # get ip of resolver pod for the next command to work
    
    # save results to pod file (IP address uses dash not dots here!)
    kubectl exec busybox -- nslookup 10-244-192-4.default.pod.cluster.local > /root/CKA/nginx.pod  # your IP will probably be different!
    cat /root/CKA/nginx.pod
    
    NOTE: For running in detached mode, the nslookup command should use IP with -, and not .
 
    ..
    
    # Search Keyword: static pod
    # REF: https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/
    # REF: https://unofficial-kubernetes.readthedocs.io/en/latest/concepts/cluster-administration/static-pod/
    
    k get pods -n kube-system
    
    cat /var/lib/kubelet/config.yaml | grep staticPodPath                           # check static pod location on 'control-plane'
    
    e.g. staticPodPath: /etc/kubernetes/manifests
    
    kubectl get nodes -o wide                                                       # create a static pod on node01
    ssh node01                                                                      # ssh into node1
    
    # Now, lets update the static pod path FIRST on the kubelet now, otherwise the statcic file gets deleted then the kubelet is restarted!
    
    # Then, add the location for the static pod to the kubelet 
    vi /var/lib/kubelet/config.yaml                                                 # add static pod location on 'node01'
    
    # Update the staticPodPath line if does not exist!
    # NOTE: Both shutdownGracePeriod lines will probably exist so do not re-add!
    shutdownGracePeriod: 0s
    shutdownGracePeriodCriticalPods: 0s
    staticPodPath: /etc/kubernetes/manifests
    
    sudo systemctl restart kubelet
    sudo systemctl enable kubelet
    sudo systemctl status kubelet

    ls /etc/kubernetes/manifests                                                    # check for any static pods (none right now)
    
    #kubectl run -h
    #kubectl run nginx-critical --image=nginx --dry-run=client -o yaml > nginx-critical.yaml 			# copy the contents
    
    vi /etc/kubernetes/manifests/nginx-critical.yaml                               # make sure the syntax is correct!
    
    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: nginx-critical
      name: nginx-critical
    spec:
      containers:
      - image: nginx
        name: nginx-critical
        
    kubectl get pods
    
    controlplane ~ ✖ kubectl get pods
    NAME                    READY   STATUS    RESTARTS   AGE
    nginx-critical-node01   1/1     Running   0          23s
