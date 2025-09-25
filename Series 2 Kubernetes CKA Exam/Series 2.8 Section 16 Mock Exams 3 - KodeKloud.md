Series 2.8 Mock Exam 3 - KodeKloud.md
*************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

## Introduction

    To join KodeKloud for CKA for the Course, Labs and Mock Exams:
    https://kodekloud.com/courses/certified-kubernetes-administrator-cka/
    
    Use the following lab by KodeKloud:
    https://kodekloud.com/topic/mock-exam-3-3/

    Part of the 'Certified Kubernetes Administrator (CKA) with Practice Tests' course:
    https://www.udemy.com/share/101Xtg3@xUHP8uVHKj8-v6hPn2j_h9jWI8F7ASIr-UmWxrYnolWuwnZAfQZrPAQf2BXYvQbF/
    
## Useful Exam Cmds

    # Aliases
    alias k=kubectl

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage
    cat pod.yaml                                                                # output file

## Mock Exam 3

    # Search Keyword: service accounts
    # REF: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/

    kubectl get nodes
    
    kubectl create serviceaccount pvviewer                                                  # creates service account in default namespace
    kubectl create clusterrole pvviewer-role --resource=persistentvolumes --verb=list       # create the clusterrole
    
    # need to include the default namespace here!
    kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer 
    
    kubectl describe clusterrole pvviewer-role                                                                          
    kubectl run pvviewer --image=redis --dry-run=client -o yaml > pod.yaml           # create pod so we can add the service account
    vi pod.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: pvviewer
      name: pvviewer
    spec:
      containers:
      - image: redis
        name: pvviewer
      serviceAccountName: pvviewer

    kubectl create -f pod.yaml
    OR
    kubectl run pvviewer --image=redis --serviceaccount=pvviewer                     # shorter version!
    kubectl describe pod pvviewer                                                    # there should have a secret name with the service account name!
    
    ..

    # Search Keyword: jsonpath
    # REF: https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources

    kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}' > /root/CKA/node_ips
    cat /root/CKA/node_ips

    # Some extra information
    kubectl get nodes -o json | jq -c 'paths'                                        # he used this ?
    kubectl get nodes -o json | grep InternalIP -B 5 -A 5                            # 5 lines before and 5 after

    k get nodes -o wide                                                              # How we got .items[*].status.addresses[?(@.type=="InternalIP")].address}
    k get nodes -o json
    k get nodes -o json | jq -c 'paths'
    k get nodes -o json | jq -c 'paths' | grep InternalIP
    k get nodes -o json | grep InternalIP
    kubectl get nodes -o json | grep InternalIP -B 5 -A 5
    k get nodes -o json | jq -c 'paths' | grep type | grep -v "metadata"
    k get nodes -o json | jq -c 'paths' | grep type | grep -v "metadata" | grep address
    
    ..
    
    # Search Keyword: pods
    # REF: https://kubernetes.io/docs/concepts/workloads/pods/

    kubectl run multi-pod --image=nginx --dry-run=client -o yaml > multi-pod.yaml   # create a template file

    vi multi-pod.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: multi-pod
      name: multi-pod
    spec:
      containers:
      - image: nginx
        name: alpha
        env:
        - name: name
          value: alpha
      - image: busybox
        name: beta
        command: ["sleep", "4800"]
        env:
        - name: name
          value: beta

    kubectl create -f multi-pod.yaml
    kubectl describe pod multi-pod
    
    ..
    
    # Search Keyword: fsGroup
    # REF: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

    kubectl run non-root-pod --image=redis:alpine --dry-run=client -o yaml > non-root-pod.yaml                       # create a template file

    vi non-root-pod.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: non-root-pod
      name: non-root-pod
    spec:
      securityContext:
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - image: redis:alpine
        name: non-root-pod
        resources: {}
      dnsPolicy: ClusterFirst
      restartPolicy: Always
    status: {}

    kubectl create -f non-root-pod.yaml
    kubectl describe pod non-root-pod

    # NOTE: Its also possible to have the securityContext at container level, but put it at pod level unless it says something like:
    "The first container should run as user ID 1000, and the second container with user ID 2000. Both containers should use file system group ID 3000.“
    e.g.
      - name: alpine-spin-b
        securityContext:
          runAsUser: 2000
        image: kubegoldenguide/alpine-spin:1.0.0
        
    ..
    
    # Search Keyword: netpol
    # REF: https://kubernetes.io/docs/concepts/services-networking/network-policies/

    kubectl get pods                                                     # explore environment
    kubectl get svc
    kubectl describe pod np-test-1
    kubectl describe svc np-test-service

    kubectl run curl --image=alpine/curl --rm -it -- sh                  # create a busybox container for testing
    curl np-test-service                                                 # but no response!
    nc -z -v -w 2 np-test-service 80                                     # test the service using netcat for 2 iteriations to see if port open?

    kubectl get netpol                                                   # get the network policy
    kubectl describe netpol default-deny                                 # describe the network policy

    kubectl get pod np-test-1 --show-labels                              # get LABELS field value!

    vi np.yaml

    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: ingress-to-nptest
      namespace: default
    spec:
      podSelector:
        matchLabels:
          run: np-test-1
      policyTypes:
      - Ingress
      ingress:
      - ports:
        - port: 80
          protocol: TCP

    kubectl create -f np.yaml                                             # create the ingress!
    kubectl get netpol                                                    # get the network policy

    kubectl run curl --image=alpine/curl --rm -it -- sh                   # create a busybox container for testing (run 2nd time!)
    curl np-test-service                                                  # this time, a response!
    nc -z -v -w 2 np-test-service 80                                      # test the service using netcat for 2 iteriations to see if port open now
    
    ..
    
    # Search Keyword: taints
    # REF: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

    kubectl get nodes
    kubectl taint node node01 env_type=production:NoSchedule              # taint the node
    kubectl describe nodes node01 | grep -i taint                         # should show the tainted details
    kubectl run dev-redis --image=redis:alpine                            # create a test node
    kubectl get pods -o wide                                              # ensure the pod is not on node1

    kubectl run prod-redis --image=redis:alpine --dry-run=client -o yaml  > prod-redis.yaml

    vi prod-redis.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: null
      labels:
        run: prod-redis
      name: prod-redis
    spec:
      containers:
      - image: redis:alpine
        name: prod-redis
      tolerations:
      - effect: NoSchedule
        key: env_type
        operator: Equal
        value: production

    kubectl create -f prod-redis.yaml                                     # create the pod
    kubectl get pods -o wide
    NOTE: The scheduler can decide to put the pod on another node!
    
    ..
    
    # Search Keyword: labels
    # REF: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

    kubectl get ns
    kubectl create ns hr
    kubectl run hr-pod --image=redis:alpine --labels=environment=production,tier=frontend --namespace=hr
    
    ..
    
    # Search Keyword: kubeconfig
    # REF: https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-kubeconfig/

    ls /root/CKA/
    kubectl get nodes

    # ask kube config to use this specific kubeconfig files
    kubectl cluster-info --kubeconfig=/root/CKA/super.kubeconfig
    You will see an error that says the connection to the server was refused!
    
    kubectl get nodes --kubeconfig /root/CKA/super.kubeconfig           # this files when we have to use the super kubeconfig                             
    cat /root/CKA/super.kubeconfig                                      # the port of 9999 looks wrong!

    cat .kube/config | grep server                                   # look at the current config file to get the correct port
    vi /root/CKA/super.kubeconfig
    kubectl get nodes --kubeconfig /root/CKA/super.kubeconfig           # this files when we have to use the super kubeconfig
    
    ..
    
    # Search Keyword: static
    # REF: https://kubernetes.io/docs/concepts/overview/working-with-objects/label

    kubectl get deployments
    kubectl scale deployment nginx-deploy --replicas=3                  # try to scale it put will not work well! :(
    kubectl get deployments
    kubectl -n kube-system get pods                                     # next logical step is check here (if scaling is not working!)
    NOTE: Static pods have all got -master OR -controlplane at the end of the pod name!

    cd /etc/kubernetes/manifests/                                       # go to the static pod default location
    ls -lhr
    vi kube-controller-manager.yaml                                     # check this file as it must have an error!

    In the file, the name kube-controller-manager name is spelt incorrectly! (Includes a '1' that should be 'l')

    grep controller kube-controller-manager.yaml                        # get all occurences
    grep contro1ler kube-controller-manager.yaml | wc -l                # count occurrences of the incorrectly spelt word!
    sed -i 's/kube-contro1ler-manager/kube-controller-manager/g' kube-controller-manager.yaml   # replace all

    kubectl get deployments                                             # this will finally work now! And show 3 available!
