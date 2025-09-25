Series 2.6 Mock Exam 1 - KodeKloud.md
*************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

## Introduction

    To join KodeKloud for CKA for the Course, Labs and Mock Exams:
    https://kodekloud.com/courses/certified-kubernetes-administrator-cka/

    Use the following lab by KodeKloud:
    https://kodekloud.com/topic/mock-exam-1-4/

    Part of the 'Certified Kubernetes Administrator (CKA) with Practice Tests' course:
    https://www.udemy.com/share/101Xtg3@xUHP8uVHKj8-v6hPn2j_h9jWI8F7ASIr-UmWxrYnolWuwnZAfQZrPAQf2BXYvQbF/
    
## Useful Exam Cmds

    # Aliases
    alias k=kubectl

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage
    cat pod.yaml                                                                # output file

## Mock Exam 1
    kubectl run nginx-pod --image=nginx:alpine                          # create pod using image
    kubectl get pods
    
    ..
    
    kubectl run messaging --image=redis:alpine -l tier=msg              # create pod (with label) using image
    kubectl get pods -l tier=msg
    
    ..
    
    kubectl create ns apx-x9984574                                      # create ns namespace
    
    ..
    
    kubectl get nodes -o json                                           # get all nodes in json
    kubectl get nodes -o json > /opt/outputs/nodes-z3444kd9.json        # get all nodes in json (in output file)
    cat /opt/outputs/nodes-z3444kd9.json
    
    ..
    
    kubectl expose --help
    kubectl expose pod messaging --name messaging-service --port 6379 --target-port 6379
    kubectl describe svc messaging-service                              # get service info
    kubectl get pods -o wide
    
    ..
    
    kubectl create deployment hr-web-app --image=kodekloud/webapp-color # create deployment
    kubectl scale deployment hr-web-app --replicas=2                    # scale it to 2
    kubectl get deployments.apps                                        # validate it!
    
    ..
    
    cd /var/lib/kubelet/                                                # to verify location of static pods!
    grep -i staticPod config.yaml

    cd /etc/kubernetes/manifests/                                       # static pods location
    kubectl run static-busybox --image busybox --dry-run=client -o yaml --command -- sleep 1000 > static-busybox.yaml 
                                                                        (check the sleep cmd here!)
    vi static-busybox.yaml                                              # have a look at the static pod
    ls -l                                                               # check location of static pods
    kubectl get pods
    kubectl describe pod static-busybox-controlplane                    # static pods get the node name attached!

    ..
    
    kubectl get ns                                                      # check if the ns exists
    kubectl run temp-bus --image=redis:alpine --namespace finance --dry-run=client -o yaml > q8.yaml
    vi q8.yaml
    kubectl apply -f q8.yaml
    kubectl -n finance get pods                                         # check pod has been created in the finance namespace
    
    ..
    
    kubectl get deployments.apps                                        # check if orange app exists!
    kubectl get pods                                                    # check if orange app exists! here too...if you see init: 
                                                                        (it means there is an issue with init container)
    kubectl describe pod orange                                         # there is a typo here for 'sleeeep'
    kubectl logs orange init-myservice                                  # get logs for init container
    kubectl get pod orange -o yaml > q9.yaml                            # save off pod config
    kubectl delete pod orange                                           # delete original (broken) pod
    vi q9.yaml                                                          # to fix the typo in 'sleeeep'!
    kubectl apply -f q9.yaml                                            # recreate it!
    kubectl get pods                                                    # check if orange app now works!

    k edit pod orange                                                   # NOTE: Also possible to do it like this
    k replace --force -f /tmp/kubectl-edit-9wg48.yaml
    
    ..
    
    kubectl get deployments.apps
    kubectl expose deployment hr-web-app --name hr-web-app-service --type=NodePort --port 8080 --target-port 8080 --dry-run=client -o yaml > q10.yaml
    vi q10.yaml
    Add nodePort: 30082 under targetPort tag!
    kubectl apply -f q10.yaml
    
    ..

    Open Kubernetes documentation and search for jsonpath
    https://kubernetes.io/docs/reference/kubectl/cheatsheet/
    https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources 			# use this for this question!

    kubectl get nodes -o jsonpath='{.items[*]}'                                                 # list all items in node configuration
    kubectl get nodes -o jsonpath='{.items[*].status}'                                          # list all items in node configuration in status section
    kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo}'                                 # list all items in node configuration in status.nodeInfo section
    kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}'                         # list all items in node configuration in status.nodeInfo.osImage section
    kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}' > /opt/outputs/nodes_os_x43kj56.txt 		# output to file!
    cat /opt/outputs/nodes_os_x43kj56.txt                                                       # verify the work!
    NOTE: Use kubectl get nodes -o json | less 													# if you need to verify the location of the element you search for
    
    ..
    
    REF: https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume
    
    Reopen the documenation and go to Storage -> Persistent Volumes
    Search for hostpath example but none exists, so use a template
    Copy the Persistent Volumes template...
    Create vi pv.yaml and add the template:
    
    vi q12.yaml

    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: pv-analytics
    spec:
      capacity:
        storage: 100Mi
      accessModes:
        - ReadWriteMany
      hostPath:
        path: /pv/data-analytics
    
    kubectl create -f q12.yaml                                                      # create the persistent volume
    kubectl get pv                                                                  # inspect it!
    kubectl describe pv pv-analytics                                                # describe it to show the host path 
                                                                                    (i.e. Source -> Path: /pv/data/analytics
   
    kubectl explain pv --recursive                                                  # get more details on the command
    Search for /hostPath
