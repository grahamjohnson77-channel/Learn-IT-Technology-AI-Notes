# 4.4 dgkanatsios:          https://github.com/dgkanatsios/CKAD-exercises
# 4.4 Practice Questions:   https://medium.com/bb-tutorials-and-thoughts/practice-enough-with-these-questions-for-the-ckad-exam-2f42d1228552

# 4. Export Cmd
# Bookmark: 4. Export Cmd & Interacting with Pods
export dr="--dry-run=client -o yaml" && echo $dr                        # show the command
k run nginx --image=nginx $dr > pod.yaml

# Create Cluster using Kind:
----------------------------
----------------------------
kind get clusters                                                       # get all clusters
kind create cluster --name ckad-playground 	                            # create cluster
alias k=kubectl; kubectl cluster-info --context kind-ckad-playground;   # set cluster
kind delete clusters ckad-playground                                    # delete cluster

k config view | grep namespace                                          # show current ns

# Service Communications
The normal way to communicate within a cluster is through Service resources.
A Service also has an IP address and additionally a DNS name. A Service is backed by a set of pods.
The Service forwards requests to itself to one of the backing pods.
The fully qualified DNS name of a Service is:

<service-name>.<service-namespace>.svc.cluster.local
This can be resolved to the IP address of the Service from anywhere in the cluster (regardless of namespace).

For example, if you have:
Namespace ns-a: Service svc-a → set of pods A
Namespace ns-b: Service svc-b → set of pods B

Then a pod of set A can reach a pod of set B by making a request to:
svc-b.ns-b.svc.cluster.local

k create ns ns-a
k create ns ns-b

k create deployment nginx-a --image=nginx --replicas=1 --namespace ns-a
k expose deployment nginx-a --port=80 --namespace ns-a                    # NOTE: Creates svc called nginx-a

k create deployment nginx-b --image=nginx --replicas=1 --namespace ns-b
k expose deployment nginx-b --port=80 --namespace ns-b                    # NOTE: Creates svc called nginx-b

Log into pod and curl the 2nd namespace:
k exec -it nginx-a-76865cf8c8-tz7w5 --namespace ns-a -- curl nginx-b.ns-b.svc.cluster.local

Core Concepts (13%)
-------------------
# Q: Create a namespace called 'mynamespace' and a pod with image nginx called nginx on this namespace
k create namespace mynamespace
k run nginx --image=nginx --restart=Never -n mynamespace

# Q: Create the pod that was just described using YAML
Easily generate YAML with:
kubectl run nginx --image=nginx --restart=Never --dry-run=client -n mynamespace -o yaml > pod.yaml
cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
  namespace: mynamespace
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml

Alternatively, you can run in one line:
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml | k create -n mynamespace -f -

# # Q: Create a busybox pod (using kubectl command) that runs the command "env". Run it and see the output
k run busybox --image=busybox --command --restart=Never -it -- env
k logs busybox

# # Q: Create a busybox pod (using YAML) that runs the command "env". Run it and see the output
Create a YAML template with this command:
k run busybox --image=busybox --restart=Never --dry-run=client -o yaml --command -- env > envpod.yaml

cat envpod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  containers:
  - command:
    - env
    image: busybox
    name: busybox
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k apply -f envpod.yaml
k logs busybox

# Q: Get the YAML for a new namespace called 'myns' without creating it
k create namespace myns -o yaml --dry-run=client

# Q: Get the YAML for a new ResourceQuota called 'myrq' with hard limits of 1 CPU, 1G memory and 2 pods without creating it
k create quota myrq --hard=cpu=1,memory=1G,pods=2 --dry-run=client -o yaml

# Q: Get pods on all namespaces
k get po --all-namespaces
k get po -A

# Q:  Create a pod with image nginx called nginx and expose traffic on port 80
k run nginx --image=nginx --restart=Never --port=80

# Q: Change pod's image to nginx:1.7.1. Observe that the container will be restarted as soon as the image gets pulled
k set image pod/nginx nginx=nginx:1.7.1
k describe po nginx                               # event 'Container will be killed and recreated'
k get po nginx -w
k get po nginx -o jsonpath='{.spec.containers[].image}{"\n"}'            # check pod's image

# Q: Get nginx pod's ip created in previous step, use a temp busybox image to wget its '/'
k get po -o wide                                  # get the IP, will be something like '10.244.0.7'

Create a temp busybox pod to check it:
k run busybox2 --image=busybox --rm -it --restart=Never -- wget -O- 10.244.0.7:80

Alternatively you can also try a more advanced option:
Get IP of the nginx pod:
NGINX_IP=$(kubectl get pod nginx -o jsonpath='{.status.podIP}')
Create a temp busybox pod:
k run busybox --image=busybox --env="NGINX_IP=$NGINX_IP" --rm -it --restart=Never -- sh -c 'wget -O- $NGINX_IP:80'
or
k run busybox --image=busybox --rm -it --restart=Never -- wget -O- $(kubectl get pod nginx -o jsonpath='{.status.podIP}:{.spec.containers[0].ports[0].containerPort}')

# Q: Get pod's YAML
k get po nginx -o yaml
or
k get po nginx -o yaml
or
k get po nginx --output yaml
or
k get po nginx --output=yaml

# Q: Get information about the pod, including details about potential issues (e.g. pod hasn't started)
k describe po nginx

# Q: Get pod logs
k logs nginx

# Q: If pod crashed and restarted, get logs about the previous instance
k logs nginx -p
or
k logs nginx --previous

# Q: Execute a simple shell on the nginx pod
k exec -it nginx -- /bin/sh
k exec --stdin --tty nginx -- /bin/bash

# Q: Create a busybox pod that echoes 'hello world' and then exits
k run busybox3 --image=busybox -it --restart=Never -- echo 'hello world'
or
k run busybox3 --image=busybox -it --restart=Never -- /bin/sh -c 'echo hello world'

# Q: Do the same, but have the pod deleted automatically when it's completed
k run busybox4 --image=busybox -it --rm --restart=Never -- /bin/sh -c 'echo hello world'
k get po                                                                  # -it flag used as delete

# Q: Create an nginx pod and set an env value as 'var1=val1'. Check the env value existence within the pod
k run nginx5 --image=nginx --restart=Never --env=var1=val1
then
k exec -it nginx5 -- env
or
k exec -it nginx5 -- sh -c 'echo $var1'
or
k describe po nginx5 | grep val1
or
k run nginx5 --restart=Never --image=nginx --env=var1=val1 -it --rm -- env

Multi-container Pods (10%)
--------------------------
# Q: Create a Pod with two containers, both with image busybox and command "echo hello; sleep 3600". Connect to the second container and run 'ls'

Easiest way to do it is create a pod with a single container and save its definition in a YAML file:
k run busybox --image=busybox --restart=Never -o yaml --dry-run=client -- /bin/sh -c 'echo hello;sleep 3600' > pod.yaml
vi pod.yaml

Copy/paste the container related values, so your final YAML should contain the following two containers (make sure those containers have a different name):

containers:
  - args:
    - /bin/sh
    - -c
    - echo hello;sleep 3600
    image: busybox
    imagePullPolicy: IfNotPresent
    name: busybox
    resources: {}
  - args:
    - /bin/sh
    - -c
    - echo hello;sleep 3600
    image: busybox
    name: busybox2

k create -f pod.yaml

# you can do the above with just an one-liner
k exec -it busybox -c busybox2 -- ls

# you can do some cleanup
k delete po busybox

# Q: Create a pod with nginx container exposed at port 80. Add a busybox init container which downloads a page using "wget -O /work-dir/index.html http://neverssl.com/online". Make a volume of type emptyDir and mount it in both containers. For the nginx container, mount it on "/usr/share/nginx/html" and for the initcontainer, mount it on "/work-dir". When done, get the IP of the created pod and create a busybox pod and run "wget -O- IP"
Easiest way to do it is create a pod with a single container and save its definition in a YAML file:
k run web --image=nginx --restart=Never --port=80 --dry-run=client -o yaml > pod-init.yaml
vi pod-init.yaml

Copy/paste the container related values, so your final YAML should contain the volume and the initContainer:

apiVersion: v1
kind: Pod
metadata:
  labels:
    run: box
  name: box
spec:
  initContainers:
  - args:
    - /bin/sh
    - -c
    - wget -O /work-dir/index.html http://neverssl.com/online
    image: busybox
    name: box
    volumeMounts:
    - name: vol
      mountPath: /work-dir
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    volumeMounts: 
    - name: vol 
      mountPath: /usr/share/nginx/html
  volumes: 
  - name: vol 
    emptyDir: {}

k apply -f pod-init.yaml

# Execute into Pod to run operations
k exec --stdin --tty box -- /bin/bash
or
k exec --stdin --tty box -c nginx -- /bin/bash

# Execute wget
k get po -o wide                                                          # get ip of the pod
k run box-test --image=busybox --restart=Never -it --rm -- /bin/sh -c "wget -O- IP"
k delete po box

Pod design (20%)
----------------
# Q: Create 3 pods with names nginx1,nginx2,nginx3. All of them should have the label app=v1
k run nginx1 --image=nginx --restart=Never --labels=app=v1
k run nginx2 --image=nginx --restart=Never --labels=app=v1
k run nginx3 --image=nginx --restart=Never --labels=app=v1
or
for i in `seq 1 3`; do k run nginx$i --image=nginx -l app=v1 ; done

# Q: Show all labels of the pods
k get po --show-labels

# Q: Change the labels of pod 'nginx2' to be app=v2
k label po nginx2 app=v2 --overwrite

# Q: Get the label 'app' for the pods (show a column with APP labels)
k get po -L app
or
k get po --label-columns=app

# Q: Get only the 'app=v2' pods
k get po -l app=v2
or
k get po -l 'app in (v2)'
or
k get po --selector=app=v2

# Q: Remove the 'app' label from the pods we created before
k label po nginx1 nginx2 nginx3 app-
or
k label po nginx{1..3} app-
or
k label po -l app app-

# Q: Create a pod that will be deployed to a Node that has the label 'accelerator=nvidia-tesla-p100'
Add the label to a node:
k label nodes <your-node-name> accelerator=nvidia-tesla-p100
k get nodes --show-labels

We can use the 'nodeSelector' property on the Pod YAML:

apiVersion: v1
kind: Pod
metadata:
  name: cuda-test
spec:
  containers:
    - name: cuda-test
      image: "k8s.gcr.io/cuda-vector-add:v0.1"
  nodeSelector:                                                           # add this
    accelerator: nvidia-tesla-p100                                        # the selection label

You can easily find out where in the YAML it should be placed by:
k explain po.spec
or 
Use node affinity

apiVersion: v1
kind: Pod
metadata:
  name: affinity-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: accelerator
            operator: In
            values:
            - nvidia-tesla-p100
  containers:
    ...

# Q: Annotate pods nginx1, nginx2, nginx3 with "description='my description'" value
k annotate po nginx1 nginx2 nginx3 description='my description'
or
k annotate po nginx{1..3} description='my description'

# Q: Check the annotations for pod nginx1
k annotate pod nginx1 --list
or
k describe po nginx1 | grep -i 'annotations'
or
k get po nginx1 -o custom-columns=Name:metadata.name,ANNOTATIONS:metadata.annotations.description

As an alternative to using | grep you can use jsonPath like:
k get po nginx1 -o jsonpath='{.metadata.annotations}{"\n"}'

# Q: Remove the annotations for these three pods
k annotate po nginx{1..3} description-

# Q: Remove these pods to have a clean state in your cluster
k delete po nginx{1..3}

Deployments
-----------
# Q: Create a deployment with image nginx:1.18.0, called nginx, having 2 replicas, defining port 80 as the port that this container exposes (don't create a service for this deployment)
k create deploy nginx --image=nginx:1.18.0 --replicas=2 --port=80 --dry-run=client -o yaml > deploy.yaml
k apply -f deploy.yaml

# Q: View the YAML of this deployment
k get deploy nginx -o yaml

# Q: View the YAML of the replica set that was created by this deployment
k describe deploy nginx
or you can find rs directly by:
k get rs -l run=nginx                                         # if created by 'run' command
k get rs -l app=nginx                                         # if created by 'create' command
you could also just do kubectl get rs:
k get rs nginx-7bf7478b77 -o yaml

# Q: Get the YAML for one of the pods
k get po                                                                  # get all the pods
or you can find pods directly by:
k get po -l run=nginx                                                     # if created by 'run' 
k get po -l app=nginx                                                     # if created by 'create'
k get po nginx-7bf7478b77-gjzp8 -o yaml

# Q: Check how the deployment rollout is going
k rollout status deploy nginx

# Q: Update the nginx image to nginx:1.19.8
k set image deploy nginx nginx=nginx:1.19.8
or
k edit deploy nginx                                 # change .spec.template.spec.containers[0].image

# Q: Check the rollout history and confirm that the replicas are OK
k rollout history deploy nginx
k get deploy nginx
k get rs                                            # check that a new replica set has been created
k get po

# Q: Undo the latest rollout and verify that new pods have the old image (nginx:1.18.0)
k rollout undo deploy nginx                                               # roll back nginx deployment
k get po                                                                  # select one 'Running' Pod
k describe po nginx-5ff4457d65-nslcl | grep -i image                      # should be nginx:1.18.0

# Q: Do an on purpose update of the deployment with a wrong image nginx:1.91
k set image deploy nginx nginx=nginx:1.91
# or
k edit deploy nginx
change the image to nginx:1.91
vim tip: type (without quotes) '/image' and Enter, to navigate quickly

# Q: Verify that something's wrong with the rollout
k rollout status deploy nginx
or
k get po                                                                  # gives 'ErrImagePull' or 'ImagePullBackOff'

# Q: Return the deployment to the second revision (number 2) and verify the image is nginx:1.19.8
k rollout undo deploy nginx --to-revision=2
k describe deploy nginx | grep Image:
k rollout status deploy nginx                                             # Everything should be OK

# Q: Check the details of the fourth revision (number 4)
k rollout history deploy nginx --revision=4                    # See the wrong image displayed here

# Q: Scale the deployment to 5 replicas
k scale deploy nginx --replicas=5
k get po
k describe deploy nginx

# Q: Autoscale the deployment, pods between 5 and 10, targetting CPU utilization at 80%
k autoscale deploy nginx --min=5 --max=10 --cpu-percent=80
# view the horizontalpodautoscalers.autoscaling for nginx
k get hpa nginx

# Q: Pause the rollout of the deployment
k rollout pause deploy nginx

# Q: Update the image to nginx:1.19.9 and check that there's nothing going on, since we paused the rollout
k set image deploy nginx nginx=nginx:1.19.9
or
k edit deploy nginx
# change the image to nginx:1.19.9
k rollout history deploy nginx                                           # no new revision

# Q: Resume the rollout and check that the nginx:1.19.9 image has been applied
k rollout resume deploy nginx
k rollout history deploy nginx
k rollout history deploy nginx --revision=6               # insert the number of your latest revision

# Q: Delete the deployment and the horizontal pod autoscaler you created
k delete deploy nginx
k delete hpa nginx
# or
k delete deploy/nginx hpa/nginx

Jobs
----
# Q: Create a job named pi with image perl that runs the command with arguments "perl -Mbignum=bpi -wle 'print bpi(2000)'"
k create job pi  --image=perl -- perl -Mbignum=bpi -wle 'print bpi(2000)'
k get jobs -w                   # wait till 'SUCCESSFUL' is 1 (will take time, perl image is big)
k get po                                                                  # get the pod name
k logs pi-****                                                            # get the pi numbers
k delete job pi
or
k get jobs -w                   # wait till 'SUCCESSFUL' is 1 (will take some time, perl image is big)
k logs job/pi
k delete job pi
or
k wait --for=condition=complete --timeout=300 job pi
k logs job/pi
k delete job pi

# Q: Create a job with the image busybox that executes the command 'echo hello;sleep 30;echo world'
k create job busybox --image=busybox -- /bin/sh -c 'echo hello;sleep 30;echo world'

# Q: Follow the logs for the pod
k get po                                                                  # find the job pod
k logs busybox-ptx58 -f                                                   # follow the logs

# Q: See the status of the job, describe it and see the logs
k get jobs
k describe jobs busybox
k logs job/busybox

# Q: Delete the job
k delete job busybox

# Q: Create a job but ensure that it will be automatically terminated by kubernetes if it takes more than 30 seconds to execute
k create job busybox --image=busybox --dry-run=client -o yaml -- /bin/sh -c 'while true; do echo hello; sleep 10;done' > job.yaml
vi job.yaml
Add job.spec.activeDeadlineSeconds=30

apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  activeDeadlineSeconds: 30                                              # add this line
  template:
    metadata:
      creationTimestamp: null
      labels:
        run: busybox
    spec:
      containers:
      - args:
        - /bin/sh
        - -c
        - while true; do echo hello; sleep 10;done
        image: busybox
        name: busybox
        resources: {}
      restartPolicy: OnFailure
status: {}

# Q: Create the same job, make it run 5 times, one after the other. Verify its status and delete it
k create job busybox --image=busybox --dry-run=client -o yaml -- /bin/sh -c 'echo hello;sleep 30;echo world' > job.yaml
vi job.yaml
Add job.spec.completions=5

apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  completions: 5                                                          # add this line
  template:
    metadata:
      creationTimestamp: null
      labels:
        run: busybox
    spec:
      containers:
      - args:
        - /bin/sh
        - -c
        - echo hello;sleep 30;echo world
        image: busybox
        name: busybox
        resources: {}
      restartPolicy: OnFailure
status: {}

kubectl create -f job.yaml

Verify that it has been completed:
k get job busybox -w                                                      # will take 2.5 minutes
k delete jobs busybox

# Q: Create the same job, but make it run 5 parallel times
vi job.yaml
Add job.spec.parallelism=5

apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  parallelism: 5 # add this line
  template:
    metadata:
      creationTimestamp: null
      labels:
        run: busybox
    spec:
      containers:
      - args:
        - /bin/sh
        - -c
        - echo hello;sleep 30;echo world
        image: busybox
        name: busybox
        resources: {}
      restartPolicy: OnFailure
status: {}

k create -f job.yaml
k get jobs
# NOTE: It will take some time for the parallel jobs to finish (>= 30 seconds)
k delete job busybox

Cron jobs
---------
# Q: Create a cron job with image busybox that runs on a schedule of "*/1 * * * *" and writes 'date; echo Hello from the Kubernetes cluster' to standard output
k create cronjob busybox --image=busybox --schedule="*/1 * * * *" -- /bin/sh -c 'date; echo Hello from the Kubernetes cluster'
k get cj
k get jobs --watch
k get po --show-labels               # observe pods have a label that mentions their 'parent' job!
k logs busybox-1529745840-m867r
# Bear in mind that Kubernetes will run a new job/pod for each new cron job
k delete cj busybox

# Q: Create a cron job with image busybox that runs every minute and writes 'date; echo Hello from the Kubernetes cluster' to standard output.
The cron job should be terminated if it takes more than 17 seconds to start execution after its scheduled time (i.e. the job missed its scheduled time).
k create cronjob time-limited-job --image=busybox --restart=Never --dry-run=client --schedule="* * * * *" -o yaml -- /bin/sh -c 'date; echo Hello from the Kubernetes cluster' > time-limited-job.yaml
vi time-limited-job.yaml
Add cronjob.spec.startingDeadlineSeconds=17

apiVersion: batch/v1beta1
kind: CronJob
metadata:
  creationTimestamp: null
  name: time-limited-job
spec:
  startingDeadlineSeconds: 17                                             # add this line
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: time-limited-job
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
            image: busybox
            name: time-limited-job
            resources: {}
          restartPolicy: Never
  schedule: '* * * * *'
status: {}

k create -f time-limited-job.yaml
k get jobs
k delete job time-limited-job

# Q: Create a cron job with image busybox that runs every minute and writes 'date; echo Hello from the Kubernetes cluster' to standard output.
The cron job should be terminated if it successfully starts but takes more than 12 seconds to complete execution.

k create cronjob time-limited-job --image=busybox --restart=Never --dry-run=client --schedule="* * * * *" -o yaml -- /bin/sh -c 'date; echo Hello from the Kubernetes cluster' > time-limited-job.yaml
vi time-limited-job.yaml
Add cronjob.spec.jobTemplate.spec.activeDeadlineSeconds=12

apiVersion: batch/v1beta1
kind: CronJob
metadata:
  creationTimestamp: null
  name: time-limited-job
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: time-limited-job
    spec:
      activeDeadlineSeconds: 12                                          # add this line
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
            image: busybox
            name: time-limited-job
            resources: {}
          restartPolicy: Never
  schedule: '* * * * *'
status: {}

k create -f time-limited-job.yaml
k get jobs
k delete job time-limited-job

Configuration (18%)
-------------------
# Q: Create a configmap named config with values foo=lala,foo2=lolo
k create configmap config --from-literal=foo=lala --from-literal=foo2=lolo

# Q: Display its values
k get cm config -o yaml
or
k describe cm config

# Q: Create and display a configmap from a file
echo -e "foo3=lili\nfoo4=lele" > config.txt                              # Create the file with
k create cm configmap2 --from-file=config.txt
k get cm configmap2 -o yaml

# Q: Create and display a configmap from a .env file
echo -e "var1=val1\n# this is a comment\n\nvar2=val2\n#anothercomment" > config.env
k create cm configmap3 --from-env-file=config.env
k get cm configmap3 -o yaml

# Q: Create and display a configmap from a file, giving the key 'special'
echo -e "var3=val3\nvar4=val4" > config4.txt                              # Create the file with
k create cm configmap4 --from-file=special=config4.txt
k describe cm configmap4
k get cm configmap4 -o yaml

# Q: Create a configMap called 'options' with the value var5=val5.
Create a new nginx pod that loads the value from variable 'var5' in an env variable called 'option'
k create cm options --from-literal=var5=val5
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    env:
    - name: option # name of the env variable
      valueFrom:
        configMapKeyRef:
          name: options                                                   # name of config map
          key: var5                                           # name of the entity in config map
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k exec -it nginx -- env | grep option                         # will show 'option=val5'

# Q: Create a configMap 'anotherone' with values 'var6=val6', 'var7=val7'. Load this configMap as env variables into a new nginx pod
k create configmap anotherone --from-literal=var6=val6 --from-literal=var7=val7
k run --restart=Never nginx --image=nginx -o yaml --dry-run=client > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    envFrom:                                                       # different than previous one, that was 'env'
    - configMapRef:                                             # different from the previous one, was 'configMapKeyRef'
        name: anotherone                                                 # the name of the config map
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

kubectl create -f pod.yaml
kubectl exec -it nginx -- env

# Q: Create a configMap 'cmvolume' with values 'var8=val8', 'var9=val9'.
Load this as a volume inside an nginx pod on path '/etc/lala'. Create the pod and 'ls' into the '/etc/lala' directory.
k create configmap cmvolume --from-literal=var8=val8 --from-literal=var9=val9
k run nginx --image=nginx --restart=Never -o yaml --dry-run=client > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  volumes:                                                               # add a volumes list
  - name: myvolume                                            # just a name, you'll reference this in the pods
    configMap:
      name: cmvolume                                                     # name of your configmap
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    volumeMounts:                                                         # your volume mounts are listed here
    - name: myvolume                                    # the name that you specified in pod.spec.volumes.name
      mountPath: /etc/lala                                                # path inside your container
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k exec -it nginx -- /bin/sh
cd /etc/lala
ls -lhr                                                                    # will show var8 var9
cat var8                                                                   # will show val8

SecurityContext
---------------
# Q: Create the YAML for an nginx pod that runs with the user ID 101. No need to create the pod
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  securityContext: # insert this line
    runAsUser: 101 # UID for the user
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

Set capabilities for a Container
--------------------------------
# Q: Create the YAML for an nginx pod that has the capabilities "NET_ADMIN", "SYS_TIME" added on its single container
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    securityContext:            # insert this line
      capabilities:             # and this
        add: ["NET_ADMIN", "SYS_TIME"] # this as well
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

Requests and limits
-------------------
# Q: Create an nginx pod with requests cpu=100m,memory=256Mi and limits cpu=200m,memory=512Mi
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml | kubectl set resources -f - --requests=cpu=100m,memory=256Mi --limits=cpu=200m,memory=512Mi --local -o yaml > nginx-pod.yml
kubectl create -f nginx-pod.yml

Secrets
-------
# Q: Create a secret called mysecret with the values password=mypass
k create secret generic mysecret --from-literal=password=mypass

# Q: Create a secret called mysecret2 that gets key/value from a file
Create a file called username with the value admin:
echo -n 'admin' > username
k create secret generic mysecret2 --from-file=username

# Q: Get the value of mysecret2
k get secret mysecret2 -o yaml
echo -n YWRtaW4= | base64 -d                             # on MAC it is -D, which decodes the value
Alternative using --jsonpath:
k get secret mysecret2 -o jsonpath='{.data.username}' | base64 -d         # on MAC it is -D
Alternative using --template:
k get secret mysecret2 --template '{{.data.username}}' | base64 -d        # on MAC it is -D

# Q: Create an nginx pod that mounts the secret mysecret2 in a volume on path /etc/foo
k run nginx --image=nginx --restart=Never -o yaml --dry-run=client > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  volumes:                                                                # specify volume
  - name: foo                                      # this name will be used for ref inside container
    secret:                                                               # we want a secret
      secretName: mysecret2                        # name of the secret - this must already exist
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    volumeMounts:                                                          # our volume mounts
    - name: foo                                                            # name on pod.spec.volumes
      mountPath: /etc/foo                                                  # our mount path
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k exec -it nginx /bin/bash
ls /etc/foo                                                                # shows username
cat /etc/foo/username                                                      # shows admin

# Q: Delete the pod you just created and mount the variable 'username' from secret mysecret2 onto a new nginx pod in env variable called 'USERNAME'
k delete po nginx
k run nginx --image=nginx --restart=Never -o yaml --dry-run=client > pod.yaml

vi pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    env:                                                                  # our env variables
    - name: USERNAME                                                      # asked name
      valueFrom:
        secretKeyRef:                                                     # secret reference
          name: mysecret2                                                 # our secret's name
          key: username                                                   # key of data in secret
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k exec -it nginx -- env | grep USERNAME | cut -d '=' -f 2                 # will show 'admin'

ServiceAccounts
---------------
# Q: See all the service accounts of the cluster in all namespaces
k get sa --all-namespaces

Alternatively:
k get sa -A

# Q: Create a new serviceaccount called 'myuser'
k create sa myuser

Alternatively, let's get a template easily:
k get sa default -o yaml > sa.yaml
vim sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myuser

k create -f sa.yaml

# Q: Create an nginx pod that uses 'myuser' as a service account
k run nginx --image=nginx --restart=Never --serviceaccount=myuser -o yaml --dry-run=client > pod.yaml
k apply -f pod.yaml

# or you can add manually:
k run nginx --image=nginx --restart=Never -o yaml --dry-run=client > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  serviceAccountName: myuser                              # we use pod.spec.serviceAccountName
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

or

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  serviceAccount: myuser                                   # we use pod.spec.serviceAccount
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k describe pod nginx             # see new secret called myuser-token-***** has been mounted

Observability (18%)
-------------------
# Q: Create an nginx pod with a liveness probe that runs the command 'ls'. Save its YAML in pod.yaml. 
k run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    livenessProbe:                            # our probe
      exec:                                   # add this line
        command:                              # command definition
        - ls                                  # ls command
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k describe pod nginx | grep -i liveness                       # to see that liveness probe works
k delete -f pod.yaml

# Q: Modify the pod.yaml file so that liveness probe starts kicking in after 5 seconds whereas the interval between probes would be 5 seconds.
k explain pod.spec.containers.livenessProbe                   # get the exact names

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    livenessProbe: 
      initialDelaySeconds: 5                                            # add this line
      periodSeconds: 5                                                  # add this line as well
      exec:
        command:
        - ls
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k describe po nginx | grep -i liveness
k delete -f pod.yaml

# Q: Create an nginx pod (that includes port 80) with an HTTP readinessProbe on path '/' on port 80.
k run nginx --image=nginx --dry-run=client -o yaml --restart=Never --port=80 > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    ports:
      - containerPort: 80 # Note: Readiness probes runs on the container during its whole lifecycle. Since nginx exposes 80, containerPort: 80 is not required for readiness to work.
    readinessProbe:                                                       # declare readiness probe
      httpGet:                                                            # add this line
        path: /                                                           #
        port: 80                                                          #
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

k create -f pod.yaml
k describe pod nginx | grep -i readiness                                  # pod readiness details
k delete -f pod.yaml

# Q: Lots of pods are running in qa,alan,test,production namespaces. All of these pods are configured with liveness probe. Please list all pods whose liveness probe are failed in the format of <namespace>/<pod name> per line.
k get ns                                                                  # check namespaces
k -n qa get events | grep -i "Liveness probe failed"
k -n alan get events | grep -i "Liveness probe failed"
k -n test get events | grep -i "Liveness probe failed"
k -n production get events | grep -i "Liveness probe failed"

Logging
-------
# Q: Create a busybox pod that runs 'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done' on a continous loop. Check its logs
k run busybox --image=busybox --restart=Never -- /bin/sh -c 'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done'
k logs busybox -f                                                         # follow the logs

Debugging
---------
# Q: Create a busybox pod that runs 'ls /notexist'. Determine if there's an error (of course there is), see it. In the end, delete the pod
k run busybox --restart=Never --image=busybox -- /bin/sh -c 'ls /notexist'
# show that there's an error
k logs busybox
k describe po busybox
k delete po busybox

# Q: Create a busybox pod that runs 'notexist'. Determine if there's an error (of course there is), see it.
In the end, delete the pod forcefully with a 0 grace period.
k run busybox --restart=Never --image=busybox -- notexist
k logs busybox                                        # will bring nothing! container never started
k describe po busybox                                 # in the events section, you'll see the error
also...
k get events | grep -i error                                            # you'll see error here too
k delete po busybox --force --grace-period=0

# Q: Get CPU/memory utilization for nodes (metrics-server must be running)
k top nodes

Services and Networking (13%)
-----------------------------
# Q: Create a pod with image nginx called nginx and expose its port 80
k run nginx --image=nginx --restart=Never --port=80 --expose

# Q: Confirm that ClusterIP has been created. Also check endpoints
k get svc nginx                                                          # services
k get ep                                                                 # endpoints

# Q: Get service's ClusterIP, create a temp busybox pod and 'hit' that IP with wget
k get svc nginx                                         # get the IP (something like 10.108.93.130)
k run busybox --rm --image=busybox -it --restart=Never -- sh
wget -O- IP:80
exit
or
IP=$(kubectl get svc nginx --template={{.spec.clusterIP}}) # get the IP (something like 10.108.93.130)
k run busybox --rm --image=busybox -it --restart=Never --env="IP=$IP" -- wget -O- $IP:80 --timeout 2
Tip: --timeout is optional, but it helps to get answer more quickly when connection fails (in seconds vs minutes)

# Q: Convert the ClusterIP to NodePort for the same service and find the NodePort port. Hit service using Node's IP.
Delete the service and the pod at the end.
k edit svc nginx

apiVersion: v1
kind: Service
metadata:
  creationTimestamp: 2018-06-25T07:55:16Z
  name: nginx
  namespace: default
  resourceVersion: "93442"
  selfLink: /api/v1/namespaces/default/services/nginx
  uid: 191e3dac-784d-11e8-86b1-00155d9f663c
spec:
  clusterIP: 10.97.242.220
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: nginx
  sessionAffinity: None
  type: NodePort                                             # change cluster IP to nodeport
status:
  loadBalancer: {}

or

k patch svc nginx -p '{"spec":{"type":"NodePort"}}' 
k get svc

result:
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        1d
nginx        NodePort    10.107.253.138   <none>        80:31931/TCP   3m
wget -O- NODE_IP:31931      # if you're using Kubernetes with Docker for Windows/Mac, try 127.0.0.1
if you're using minikube, try minikube ip, then get the node ip such as 192.168.99.117
k delete svc nginx                                                      # Deletes service
k delete pod nginx                                                      # Deletes pod

# Q: Create a deployment called foo using image 'dgkanatsios/simpleapp' (a simple server that returns hostname) and 3 replicas. Label it as 'app=foo'.
Declare that containers in this pod will accept traffic on port 8080 (do NOT create a service yet)
k create deploy foo --image=dgkanatsios/simpleapp --port=8080 --replicas=3
k label deployment foo --overwrite app=foo

# Q: Get the pod IPs. Create a temp busybox pod and try hitting them on port 8080
k get pods -l app=foo -o wide                                             # 'wide' will show pod IPs
kubectl run busybox --image=busybox --restart=Never -it --rm -- sh
wget -O- POD_IP:8080                                      # do not try with pod name, will not work
try hitting all IPs to confirm that hostname is different...
exit
or
k get po -o wide -l app=foo | awk '{print $6}' | grep -v IP | xargs -L1 -I '{}' k run --rm -ti tmp --restart=Never --image=busybox -- wget -O- http://\{\}:8080

# Q: Create a service that exposes the deployment on port 6262. Verify its existence, check the endpoints
k expose deploy foo --port=6262 --target-port=8080
k get service foo                                   # you will see ClusterIP as well as port 6262
k get endpoints foo                                 # IPs of the 3 replica nodes, listening on 8080

# Q: Create a temp busybox pod and connect via wget to foo service. Verify that each time there's a different hostname returned. 
Delete deployment and services to cleanup the cluster
k get svc                                                         # get the foo service ClusterIP
k run busybox --image=busybox -it --rm --restart=Never -- sh
wget -O- foo:6262            # DNS works! run it many times, you'll see different pods responding
wget -O- SERVICE_CLUSTER_IP:6262                                  # ClusterIP works as well
k delete svc foo
k delete deploy foo

# Q: NetworkPolicy - Create an nginx deployment of 2 replicas, expose it via a ClusterIP service on port 80.
Create NetworkPolicy so only pods with labels 'access: granted' can access deployment and apply it
k create deployment nginx --image=nginx --replicas=2
k expose deployment nginx --port=80

k describe svc nginx                                                    # see 'app=nginx' selector for pods
or
k get svc nginx -o yaml

vi policy.yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-nginx                                                    # pick a name
spec:
  podSelector:
    matchLabels:
      app: nginx                                                        # selector for the pods
  ingress:                                                              # allow ingress traffic
  - from:
    - podSelector:                                                      # from pods
        matchLabels:                                                    # with this label
          access: granted

Create the NetworkPolicy
k create -f policy.yaml

k run busybox --image=busybox --rm -it --restart=Never -- wget -O- http://nginx:80 --timeout 2                                                         # This should not work
k run busybox --image=busybox --rm -it --restart=Never --labels=access=granted -- wget -O- http://nginx:80 --timeout 2                                      # This should be fine

# Q: Create Ingress Controllers Rules to control traffic
Get examples from these:
https://kubernetes.io/docs/concepts/services-networking/ingress/
https://platform9.com/blog/ultimate-guide-to-kubernetes-ingress-controllers/

State Persistence (8%)
----------------------
Define volumes
--------------
# Q: Create busybox pod with two containers, each one will have the image busybox and will run the 'sleep 3600' command. Make both containers mount an emptyDir at '/etc/foo'. Connect to the second busybox, write the first column of '/etc/passwd' file to '/etc/foo/passwd'. Connect to the first busybox and write '/etc/foo/passwd' file to standard output. Delete pod.
This question is probably a better fit for the 'Multi-container-pods' section but I'm keeping it here as it will help you get acquainted with state

Easiest way to do this is to create a template pod with:
k run busybox --image=busybox --restart=Never -o yaml --dry-run=client -- /bin/sh -c 'sleep 3600' > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  dnsPolicy: ClusterFirst
  restartPolicy: Never
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    imagePullPolicy: IfNotPresent
    name: busybox
    resources: {}
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    name: busybox2 # don't forget to change the name during copy paste, must be different from the first container's name!
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  volumes: #
  - name: myvolume #
    emptyDir: {} #

Connect to the second container:
k exec -it busybox -c busybox2 -- /bin/sh
cat /etc/passwd | cut -f 1 -d ':' > /etc/foo/passwd 
cat /etc/foo/passwd                                                           # confirm info has been written
exit

Connect to the first container:
k exec -it busybox -c busybox -- /bin/sh
mount | grep foo                                                              # confirm the mounting
cat /etc/foo/passwd
exit
k delete po busybox

# Q: Create a PersistentVolume of 10Gi, called 'myvolume'. Make it have accessMode of 'ReadWriteOnce' and 'ReadWriteMany', storageClassName 'normal', mounted on hostPath '/etc/foo'. Save it on pv.yaml, add it to the cluster. Show the PersistentVolumes that exist on the cluster
vi pv.yaml

kind: PersistentVolume
apiVersion: v1
metadata:
  name: myvolume
spec:
  storageClassName: normal
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
    - ReadWriteMany
  hostPath:
    path: /etc/foo

Show the PersistentVolumes:
k create -f pv.yaml
will have status 'Available'
k get pv

# Q: Create a PersistentVolumeClaim for this storage class, called 'mypvc', a request of 4Gi and an accessMode of ReadWriteOnce, with the storageClassName of normal, and save it on pvc.yaml. Create it on the cluster. Show the PersistentVolumeClaims of the cluster. Show the PersistentVolumes of the cluster
vi pvc.yaml

kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: mypvc
spec:
  storageClassName: normal
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 4Gi

Create it on the cluster:
k create -f pvc.yaml

Show the PersistentVolumeClaims and PersistentVolumes:
k get pvc                                                                # shows 'Bound'
k get pv                                                                 # shows 'Bound' as well

# Q: Create a busybox pod with command 'sleep 3600', save it on pod.yaml. Mount the PersistentVolumeClaim to '/etc/foo'. Connect to the 'busybox' pod, and copy the '/etc/passwd' file to '/etc/foo/passwd'
Create a skeleton pod:
k run busybox --image=busybox --restart=Never -o yaml --dry-run=client -- /bin/sh -c 'sleep 3600' > pod.yaml
vi pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    imagePullPolicy: IfNotPresent
    name: busybox
    resources: {}
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  dnsPolicy: ClusterFirst
  restartPolicy: Never
  volumes: #
  - name: myvolume #
    persistentVolumeClaim: #
      claimName: mypvc #
status: {}

Create the pod:
k create -f pod.yaml
Connect to the pod and copy '/etc/passwd' to '/etc/foo/passwd':
k exec busybox -it -- cp /etc/passwd /etc/foo/passwd

# Q: Create a second pod which is identical with the one you just created (you can easily do it by changing the 'name' property on pod.yaml). Connect to it and verify that '/etc/foo' contains the 'passwd' file. Delete pods to cleanup. Note: If you can't see the file from the second pod, can you figure out why? What would you do to fix that?
Create the second pod, called busybox2:

vim pod.yaml
# change 'metadata.name: busybox' to 'metadata.name: busybox2'
k create -f pod.yaml
k exec busybox2 -- ls /etc/foo # will show 'passwd'
# cleanup
k delete po busybox busybox2

If the file doesn't show on the second pod but it shows on the first, it has most likely been scheduled on a different node.

# check which nodes the pods are on
k get po busybox -o wide
k get po busybox2 -o wide

If they are on different nodes, you won't see the file, because we used the hostPath volume type. If you need to access the same files in a multi-node cluster, you need a volume type that is independent of a specific node. There are lots of different types per cloud provider (see here), a general solution could be to use NFS.

# Q: Create a busybox pod with 'sleep 3600' as arguments. Copy '/etc/passwd' from the pod to your local folder
k run busybox --image=busybox --restart=Never -- sleep 3600
k cp busybox:etc/passwd ./passwd                                       # cp command
# previous command might report an error, feel free to ignore it since copy command works
cat passwd

----------------------------------------------------------
Practice Enough With These 150 Questions for the CKAD Exam
----------------------------------------------------------
# Create and Configure Basic Pods
---------------------------------
1. List all the namespaces in the cluster
k get namespaces
k get ns

2. List all the pods in all namespaces
k get po --all-namespaces

3. List all the pods in the particular namespace
k get po -n <namespace name>

4. List all the services in the particular namespace
k get svc -n <namespace name>

5. List all the pods showing name and namespace with a json path expression
k get pods -o=jsonpath="{.items[*]['metadata.name','metadata.namespace']}"

6. Create an nginx pod in a default namespace and verify the pod running
k run nginx --image=nginx --restart=Never
k get po

// get the yaml file with --dry-run flag
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx-pod.yaml
// cat nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
// create a pod 
k create -f nginx-pod.yaml

8. Output the yaml file of the pod you just created
k get po nginx -o yaml

9. Output the yaml file of the pod you just created without the cluster-specific information
k get po nginx -o yaml --export

10. Get the complete details of the pod you just created
k describe pod nginx

11. Delete the pod you just created
k delete po nginx
k delete -f nginx-pod.yaml

12. Delete the pod you just created without any delay (force delete)
k delete po nginx --grace-period=0 --force

13. Create the nginx pod with version 1.17.4 and expose it on port 80
k run nginx --image=nginx:1.17.4 --restart=Never --port=80

14. Change the Image version to 1.15-alpine for the pod you just created and verify
the image version is updated
k set image pod/nginx nginx=nginx:1.15-alpine
k describe po nginx
k edit po nginx
k describe po nginx

15. Change the Image version back to 1.17.1 for the pod you just updated and observe the changes
k set image pod/nginx nginx=nginx:1.17.1
k describe po nginx
k get po nginx -w # watch it

16. Check the Image version without the describe command
k get po nginx -o jsonpath='{.spec.containers[].image}{"\n"}'

17. Create the nginx pod and execute the simple shell on the pod
k run nginx --image=nginx --restart=Never
k exec -it nginx /bin/sh

18. Get the IP Address of the pod you just created
k get po nginx -o wide

19. Create a busybox pod and run command ls while creating it and check the logs
k run busybox --image=busybox --restart=Never -- ls
k logs busybox

20. If pod crashed check the previous logs of the pod
k logs busybox -p

21. Create a busybox pod with command sleep 3600
k run busybox --image=busybox --restart=Never -- /bin/sh -c "sleep 3600"

22. Check the connection of the nginx pod from the busybox pod
k get po nginx -o wide
k exec -it busybox -- wget -o- <IP Address>

23. Create a busybox pod and echo message ‘How are you’ and delete it manually
k run busybox --image=nginx --restart=Never -it -- echo "How are you"
k delete po busybox

24. Create a busybox pod and echo message ‘How are you’ and have it deleted immediately
k run busybox --image=nginx --restart=Never -it --rm -- echo "How are you"

25. Create an nginx pod and list the pod with different levels of verbosity
k run nginx --image=nginx --restart=Never --port=80
k get po nginx --v=7
k get po nginx --v=8
k get po nginx --v=9

26. List the nginx pod with custom columns POD_NAME and POD_STATUS
k get po -o=custom-columns="POD_NAME:.metadata.name, POD_STATUS:.status.containerStatuses[].state"

27. List all the pods sorted by name
k get pods --sort-by=.metadata.name

28. List all the pods sorted by created timestamp
k get pods--sort-by=.metadata.creationTimestamp

# Multi-Container Pods (10%)
----------------------------
Understand multi-container pod design patterns (eg: ambassador, adaptor, sidecar)

29. Create a Pod with three busy box containers with commands "ls; sleep 3600;",
"echo Hello World; sleep 3600;” and “echo this is the third container; sleep 3600”
respectively and check the status

// first create single container pod with dry run flag
k run busybox --image=busybox --restart=Never --dry-run -o
yaml -- bin/sh -c "sleep 3600; ls" > multi-container.yaml

k create -f multi-container.yaml
k get po busybox
multi-container pod

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  containers:
  - args:
    - bin/sh
    - -c
    - ls; sleep 3600
    image: busybox
    name: busybox1
    resources: {}
  - args:
    - bin/sh
    - -c
    - echo Hello world; sleep 3600
    image: busybox
    name: busybox2
    resources: {}
  - args:
    - bin/sh
    - -c
    - echo this is third container; sleep 3600
    image: busybox
    name: busybox3
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

30. Check the logs of each container that you just created
k logs busybox -c busybox1
k logs busybox -c busybox2
k logs busybox -c busybox3

31. Check the previous logs of the second container busybox2 if any
k logs busybox -c busybox2 --previous

32. Run command ls in the third container busybox3 of the above pod
k exec busybox -c busybox3 -- ls

33. Show metrics of the above pod containers and puts them into the file.log and verify
k top pod busybox --containers
k top pod busybox --containers > file.log
cat file.log

34. Create a Pod with main container busybox and which executes this “while true;
do echo ‘Hi I am from Main container’ >> /var/log/index.html; sleep 5; done” and
with sidecar container with nginx image which exposes on port 80.
Use emptyDir Volume and mount this volume on path /var/log for busybox and on path
/usr/share/nginx/html for nginx container. Verify both containers are running.

k run multi-cont-pod --image=busbox --restart=Never --dry-run=client -o yaml > multi-container.yaml
k create -f multi-container.yaml
k get po multi-cont-pod
vi multi-container.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: multi-cont-pod
  name: multi-cont-pod
spec:
  volumes:
  - name: var-logs
    emptyDir: {}
  containers:
  - image: busybox
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo 'Hi I am from Main container' >> /var/log/index.html; sleep 5;done"]
    name: main-container
    resources: {}
    volumeMounts:
    - name: var-logs
      mountPath: /var/log
  - image: nginx
    name: sidecar-container
    resources: {}
    ports:
      - containerPort: 80
    volumeMounts:
    - name: var-logs
      mountPath: /usr/share/nginx/html
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

35. Exec into both containers and verify that main.txt exist and query the main.txt from sidecar container with curl localhost
// exec into main container
k exec -it multi-cont-pod -c main-container -- sh
cat /var/log/index.html
// exec into sidecar container
k exec -it multi-cont-pod -c sidecar-container -- sh
cat /usr/share/nginx/html/index.html
// install curl and get default page
k exec -it multi-cont-pod -c sidecar-container -- sh
apt-get update && apt-get install -y curl
curl localhost

36. Get the pods with label information
k get pods --show-labels

37. Create 5 nginx pods in which two of them is labeled env=prod and three of them
is labeled env=dev
k run nginx-dev1 --image=nginx --restart=Never -- labels=env=dev
k run nginx-dev2 --image=nginx --restart=Never -- labels=env=dev
k run nginx-dev3 --image=nginx --restart=Never -- labels=env=dev
k run nginx-prod1 --image=nginx --restart=Never -- labels=env=prod
k run nginx-prod2 --image=nginx --restart=Never -- labels=env=prod

38. Verify all the pods are created with correct labels
k get pods --show-labels

39. Get the pods with label env=dev
k get pods -l env=dev

40. Get the pods with label env=dev and also output the labels
k get pods -l env=dev --show-labels

41. Get the pods with label env=prod
k get pods -l env=prod

42. Get the pods with label env=prod and also output the labels
k get pods -l env=prod --show-labels

43. Get the pods with label env
k get pods -L env

44. Get the pods with labels env=dev and env=prod
k get pods -l 'env in (dev,prod)'

45. Get the pods with labels env=dev and env=prod and output the labels as well
k get pods -l 'env in (dev,prod)' --show-labels

46. Change the label for one of the pod to env=uat and list all the pods to verify
k label pod/nginx-dev3 env=uat --overwrite
k get pods --show-labels

47. Remove the labels for the pods that we created now and verify all the labels are removed
k label pod nginx-dev{1..3} envkubectl
label pod nginx-prod{1..2} envkubectl
get po --show-labels

48. Let’s add the label app=nginx for all the pods and verify
k label pod nginx-dev{1..3} app=nginx
k label pod nginx-prod{1..2} app=nginx
k get po --show-labels

49. Get all the nodes with labels (if using minikube you would get only master node)
k get nodes --show-labels

50. Label the node (minikube if you are using) nodeName=nginxnode
k label node minikube nodeName=nginxnode

51. Create a Pod that will be deployed on this node with the label nodeName=nginxnode
k run nginx --image=nginx --restart=Never --dry-run -o yaml > pod.yaml
k create -f pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  nodeSelector:
    nodeName: nginxnode
  containers:
  - image: nginx
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

52. Verify the pod that it is scheduled with the node selector
k describe po nginx | grep Node-Selectors

53. Verify the pod nginx that we just created has this label
k describe po nginx | grep Labels

54. Annotate the pods with name=webapp
k annotate pod nginx-dev{1..3} name=webapp
k annotate pod nginx-prod{1..2} name=webapp

55. Verify the pods that have been annotated correctly
k describe po nginx-dev{1..3} | grep -i annotations
k describe po nginx-prod{1..2} | grep -i annotations

56. Remove the annotations on the pods and verify
k annotate pod nginx-dev{1..3} namekubectl
k annotate pod nginx-prod{1..2} namekubectl
k po nginx-dev{1..3} | grep -i annotations
k describe po nginx-prod{1..2} | grep -i annotations

57. Remove all the pods that we created so far
k delete po --all

58. Create a deployment called webapp with image nginx with 5 replicas
k create deploy webapp --image=nginx --dry-run -o yaml > webapp.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: webapp
  name: webapp
spec:
  replicas: 5
  selector:
    matchLabels:
      app: webapp
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: webapp
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}

k create -f webapp.yaml

59. Get the deployment you just created with labels
k get deploy webapp --show-labels

60. Output the yaml file of the deployment you just created
k get deploy webapp -o yaml

61. Get the pods of this deployment
k get deploy --show-labels
k get pods -l app=webapp

62. Scale the deployment from 5 replicas to 20 replicas and verify
k scale deploy webapp --replicas=20
k get po -l app=webapp

63. Get the deployment rollout status
k rollout status deploy webapp

64. Get the replicaset that created with this deployment
k get rs -l app=webapp

65. Get the yaml of the replicaset and pods of this deployment
k get rs -l app=webapp -o yaml
k get po -l app=webapp -o yaml

66. Delete the deployment you just created and watch all the pods are also being deleted
k delete deploy webapp
k get po -l app=webapp -w

67. Create a deployment of webapp with image nginx:1.17.1 with container port 80 and verify the image version
k create deploy webapp --image=nginx:1.17.1 --dry-run -o yaml > webapp.yaml
k create -f webapp.yaml
k describe deploy webapp | grep Image

apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: webapp
  name: webapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: webapp
    spec:
      containers:
      - image: nginx:1.17.1
        name: nginx
        ports:
        - containerPort: 80
        resources: {}
status: {}

68. Update the deployment with the image version 1.17.4 and verify
k set image deploy/webapp nginx=nginx:1.17.4
k describe deploy webapp | grep Image

69. Check the rollout history and make sure everything is ok after the update
k rollout history deploy webapp
k get deploy webapp --show-labels
k get rs -l app=webapp
k get po -l app=webapp

70. Undo the deployment to the previous version 1.17.1 and verify Image has the previous version
k rollout undo deploy webapp
k describe deploy webapp | grep Image

71. Update the deployment with the image version 1.16.1 and verify the image and also check the rollout history
k set image deploy/webapp nginx=nginx:1.16.1
k describe deploy webapp | grep Image
k rollout history deploy webapp

72. Update the deployment to the Image 1.17.1 and verify everything is ok
k rollout undo deploy webapp --to-revision=3
k describe deploy webapp | grep Image
k rollout status deploy webapp

73. Update the deployment with the wrong image version 1.100 and verify something is wrong with the deployment
k set image deploy/webapp nginx=nginx:1.100
k rollout status deploy webapp (still pending state)
k get pods (ImagePullErr)

74. Undo the deployment with the previous version and verify everything is Ok
k rollout undo deploy webapp
k rollout status deploy webapp
k get pods

75. Check the history of the specific revision of that deployment
k rollout history deploy webapp --revision=7

76. Pause the rollout of the deployment
k rollout pause deploy webapp

77. Update the deployment with the image version latest and check the history and
verify nothing is going on
k set image deploy/webapp nginx=nginx:latest
k rollout history deploy webapp (No new revision)

78. Resume the rollout of the deployment
k rollout resume deploy webapp

79. Check the rollout history and verify it has the new version
k rollout history deploy webapp
k rollout history deploy webapp --revision=9

80. Apply the autoscaling to this deployment with minimum 10 and maximum 20
replicas and target CPU of 85% and verify hpa is created and replicas are increased to 10 from 1
k autoscale deploy webapp --min=10 --max=20 --cpu-percent=85
k get hpa
k get pod -l app=webapp

81. Clean the cluster by deleting deployment and hpa you just created
k delete deploy webapp
k delete hpa webapp

82. Create a Job with an image node which prints node version and also verifies there is a pod created for this job
k create job nodeversion --image=node -- node -v
k get job -w
k get pod

83. Get the logs of the job just created
k logs <pod name> // created from the job

84. Output the yaml file for the Job with the image busybox which echos “Hello I am from job”
k create job hello-job --image=busybox --dry-run -o yaml -- echo "Hello I am from job"

85. Copy the above YAML file to hello-job.yaml file and create the job
k create job hello-job --image=busybox --dry-run -o yaml -- echo "Hello I am from job" > hello-job.yaml
k create -f hello-job.yaml

86. Verify the job and the associated pod is created and check the logs as well
k get job
k get po
k logs hello-job-*

87. Delete the job we just created
k delete job hello-job

88. Create the same job and make it run 10 times one after one
k create job hello-job --image=busybox --dry-run -o yaml -- echo "Hello I am from job" > hello-job.yaml
k create -f hello-job.yaml
hello-job.yaml

apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  name: hello-job
spec:
  completions: 10
  template:
    metadata:
      creationTimestamp: null
    spec:
      containers:
      - command:
        - echo
        - Hello I am from job
        image: busybox
        name: hello-job
        resources: {}
      restartPolicy: Never
status: {}

89. Watch the job that runs 10 times one by one and verify 10 pods are created and delete those after it’s completed
k get job -w
k get po
k delete job hello-job

90. Create the same job and make it run 10 times parallel
k create job hello-job --image=busybox --dry-run -o yaml -- echo "Hello I am from job" > hello-job.yaml
k create -f hello-job.yaml

apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  name: hello-job
spec:
  parallelism: 10
  template:
    metadata:
      creationTimestamp: null
    spec:
      containers:
      - command:
        - echo
        - Hello I am from job
        image: busybox
        name: hello-job
        resources: {}
      restartPolicy: Never
status: {}

91. Watch the job that runs 10 times parallelly and verify 10 pods are created and delete those after it’s completed
k get job -w
k get po
k delete job hello-job

92. Create a Cronjob with busybox image that prints date and hello from kubernetes cluster message for every minute
k create cronjob date-job --image=busybox --schedule="*/1 * *
* *" -- bin/sh -c "date; echo Hello from kubernetes cluster"

93. Output the YAML file of the above cronjob
k get cj date-job -o yaml

94. Verify that CronJob creating a separate job and pods for every minute to run and verify the logs of the pod
k get job
k get po
k logs date-job-<jobid>-<pod>

95. Delete the CronJob and verify all the associated jobs and pods are also deleted.
k delete cj date-job
k get po
k get job

96. List Persistent Volumes in the cluster
k get pv

97. Create a hostPath PersistentVolume named task-pv-volume with storage 10Gi,
access modes ReadWriteOnce, storageClassName manual, and volume at /mnt/data
and verify
k create -f task-pv-volume.yaml
k get pv

apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"

98. Create a PersistentVolumeClaim of at least 3Gi storage and access mode ReadWriteOnce and verify status is Bound
k create -f task-pv-claim.yaml
k get pvc

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi

99. Delete persistent volume and PersistentVolumeClaim we just created
k delete pvc task-pv-claim
k delete pv task-pv-volume

100. Create a Pod with an image Redis and configure a volume that lasts for the lifetime of the Pod
k create -f redis-storage.yaml

apiVersion: v1
kind: Pod
metadata:
  name: redis
spec:
  containers:
  - name: redis
    image: redis
    volumeMounts:
    - name: redis-storage
      mountPath: /data/redis
  volumes:
  - name: redis-storage
    emptyDir: {}

101. Exec into the above pod and create a file named file.txt with the text ‘This is called the file’ in the path /data/redis and open another tab and exec again with the same pod and verifies file exist in the same path.
// first terminal
k exec -it redis-storage /bin/sh
cd /data/redis
echo 'This is called the file' > file.txt
//open another tab
k exec -it redis-storage /bin/sh
cat /data/redis/file.txt

102. Delete the above pod and create again from the same yaml file and verifies there is no file.txt in the path /data/redis
k delete pod redis
k create -f redis-storage.yaml
k exec -it redis-storage /bin/sh
cat /data/redis/file.txt                                                   # file doesn't exist

103. Create PersistentVolume named task-pv-volume with storage 10Gi, access modes ReadWriteOnce, storageClassName manual, and volume at /mnt/data
Create a PersistentVolumeClaim of at least 3Gi storage and access mode ReadWriteOnce and verify status is Bound

vi task-pv-volume.yaml

apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  hostPath:
    path: "/mnt/data"

k create -f task-pv-volume.yaml

vi task-pv-claim.yaml

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
  storageClassName: manual

k create -f task-pv-claim.yaml

k get pv
k get pvc

104. Create an nginx pod with containerPort 80 and with a PersistentVolumeClaim task-pv-claim and has a mouth path "/usr/share/nginx/html"
vi task-pv-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage

k create -f task-pv-pod.yaml

# Configuration (18%)
---------------------
105. List all the configmaps in the cluster
k get cm
or
k get configmap

106. Create a configmap called myconfigmap with literal value appname=myapp
k create cm myconfigmap --from-literal=appname=myapp

107. Verify the configmap we just created has this data
k get cm -o yaml
or
k describe cm

108. Delete the configmap myconfigmap we just created
k delete cm myconfigmap

109. Create a file called config.txt with two values key1=value1 and key2=value2 and verify the file
cat >> config.txt << EOF
key1=value1
key2=value2
EOF
cat config.txt

110. Create a configmap named keyvalcfgmap and read data from the file config.txt and verify that configmap is created correctly

k create cm keyvalcfgmap --from-file=config.txt
k get cm keyvalcfgmap -o yaml

111. Create an nginx pod and load environment values from the above configmap keyvalcfgmap and exec into the pod and verify the environment variables and delete the pod
// first run this command to save the pod yml
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx-pod.yml
// edit the yml to below file and create
k create -f nginx-pod.yml
// verify
k exec -it nginx -- env
k delete po nginx

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources: {}
    envFrom:
    - configMapRef:
        name: keyvalcfgmap
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

112. Create an env file file.env with var1=val1 and create a configmap envcfgmap from this env file and verify the configmap
echo var1=val1 > file.env
cat file.env
k create cm envcfgmap --from-env-file=file.env
k get cm envcfgmap -o yaml --export

113. Create an nginx pod and load environment values from the above configmap envcfgmap and exec into the pod and verify the environment variables and delete the pod
// first run this command to save the pod yml
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx-pod.yml
// edit the yml to below file and create
k create -f nginx-pod.yml
// verify
k exec -it nginx -- env
k delete po nginx

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources: {}
    env:
    - name: ENVIRONMENT
      valueFrom:
        configMapKeyRef:
          name: envcfgmap
          key: var1
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

114. Create a configmap called cfgvolume with values var1=val1, var2=val2 and create an nginx pod with volume nginx-volume which reads data from this configmap cfgvolume and put it on the path /etc/cfg
// first create a configmap cfgvolume
k create cm cfgvolume --from-literal=var1=val1 --fromliteral=var2=val2
// verify the configmap
k describe cm cfgvolume
// create the config map
k create -f nginx-volume.yml
// exec into the pod
k exec -it nginx -- /bin/sh
// check the path
cd /etc/cfg
ls

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  volumes:
  - name: nginx-volume
    configMap:
      name: cfgvolume
  containers:
  - image: nginx
    name: nginx
    resources: {}
    volumeMounts:
    - name: nginx-volume
      mountPath: /etc/cfg
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

115. Create a pod called secbusybox with the image busybox which executes command sleep 3600 and makes sure any Containers in the Pod, all processes run with user ID 1000 and with group id 2000 and verify.
// create yml file with dry-run
k run secbusybox --image=busybox --restart=Never --dry-run -o yaml -- /bin/sh -c "sleep 3600;" > busybox.yml
// edit the pod like below and create
k create -f busybox.yml
// verify
k exec -it secbusybox -- sh
id // it will show the id and group

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secbusybox
  name: secbusybox
spec:
  securityContext: # add security context
    runAsUser: 1000
    runAsGroup: 2000
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600;
    image: busybox
    name: secbusybox
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

116. Create the same pod as above. This time set the securityContext for the container as well and verify that the securityContext of container overrides the Pod level securityContext.
// create yml file with dry-run
k run secbusybox --image=busybox --restart=Never --dry-run -o yaml -- /bin/sh -c "sleep 3600;" > busybox.yml
// edit the pod like below and create
k create -f busybox.yml
// verify
k exec -it secbusybox -- sh
id // you can see container securityContext overides the Pod level

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secbusybox
  name: secbusybox
spec:
  securityContext:
    runAsUser: 1000
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600;
    image: busybox
    securityContext:
      runAsUser: 2000
    name: secbusybox
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

117. Create pod with an nginx image and configure the pod with capabilities
NET_ADMIN and SYS_TIME verify the capabilities
// create the yaml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// edit as below and create pod
k create -f nginx.yml
// exec and verify
k exec -it nginx -- sh
cd /proc/1
cat status
// you should see these values
CapPrm: 00000000aa0435fb
CapEff: 00000000aa0435fb

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    securityContext:
      capabilities:
        add: ["SYS_TIME", "NET_ADMIN"]
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

118. Create a Pod nginx and specify a memory request and a memory limit of 100Mi and 200Mi respectively.
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add the resources section and create
k create -f nginx.yml
// verify
k top pod

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources: 
      requests:
        memory: "100Mi"
      limits:
        memory: "200Mi"
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

119. Create a Pod nginx and specify a CPU request and a CPU limit of 0.5 and 1 respectively.
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add the resources section and create
k create -f nginx.yml
// verify
k top pod

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        cpu: "0.5"
      limits:
        cpu: "1"
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

120. Create a Pod nginx and specify both CPU, memory requests and limits together and verify.
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add the resources section and create
k create -f nginx.yml
// verify
k top pod

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        memory: "100Mi"
        cpu: "0.5"
      limits:
        memory: "200Mi"
        cpu: "1"
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

121. Create a Pod nginx and specify a memory request and a memory limit of 100Gi and 200Gi respectively which is too big for the nodes and verify pod fails to start because of insufficient memory
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add the resources section and create
k create -f nginx.yml
// verify
k describe po nginx // you can see pending state

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    resources:
      requests:
        memory: "100Gi"
        cpu: "0.5"
      limits:
        memory: "200Gi"
        cpu: "1"
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

122. Create a secret mysecret with values user=myuser and password=mypassword
k create secret generic my-secret --from-literal=username=user --from-literal=password=mypassword

123. List the secrets in all namespaces
k get secret --all-namespaces

124. Output the yaml of the secret created above
k get secret my-secret -o yaml

125. Create an nginx pod which reads username as the environment variable
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add env section below and create
k create -f nginx.yml
//verify
k exec -it nginx -- env

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    env:
    - name: USER_NAME
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: username
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

126. Create an nginx pod which loads the secret as environment variables
// create a yml file
k run nginx --image=nginx --restart=Never --dry-run -o yaml > nginx.yml
// add env section below and create
k create -f nginx.yml
//verify
k exec -it nginx -- env

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    envFrom:
    - secretRef:
        name: my-secret
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

127. List all the service accounts in the default namespace
k get sa

128. List all the service accounts in all namespaces
k get sa --all-namespaces

129. Create a service account called admin
k create sa admin

130. Output the YAML file for the service account we just created
k get sa admin -o yaml

131. Create a busybox pod which executes this command sleep 3600 with the service account admin and verify
k run busybox --image=busybox --restart=Never --dry-run -o yaml -- /bin/sh -c "sleep 3600" > busybox.yml
k create -f busybox.yml
// verify
k describe po busybox

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  serviceAccountName: admin
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    name: busybox
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

# Observability (18%)
---------------------
132. Create an nginx pod with containerPort 80 and it should only receive traffic only it checks the endpoint / on port 80 and verify and delete the pod.
k run nginx --image=nginx --restart=Never --port=80 --dry-run -o yaml > nginx-pod.yaml

// add the readinessProbe section and create
k create -f nginx-pod.yaml
// verify
k describe pod nginx | grep -i readiness
k delete po nginx

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

133. Create an nginx pod with containerPort 80 and it should check the pod running 
at endpoint / healthz on port 80 and verify and delete the pod.
k run nginx --image=nginx --restart=Never --port=80 --dry-run -o yaml > nginx-pod.yaml
// add the livenessProbe section and create
k create -f nginx-pod.yaml
// verify
k describe pod nginx | grep -i readiness
k delete po nginx

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

134. Create an nginx pod with containerPort 80 and it should check the pod running at endpoint /healthz on port 80 and it should only receive traffic only it checks the endpoint / on port 80. verify the pod.
k run nginx --image=nginx --restart=Never --port=80 --dry-run -o yaml > nginx-pod.yaml
// add the livenessProbe and readiness section and create
k create -f nginx-pod.yaml
// verify
k describe pod nginx | grep -i readiness
k describe pod nginx | grep -i liveness

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

135. Check what all are the options that we can configure with readiness and liveness probes
k explain Pod.spec.containers.livenessProbe
k explain Pod.spec.containers.readinessProbe

136. Create the pod nginx with the above liveness and readiness probes so that it should wait for 20 seconds before it checks liveness and readiness probes and it should check every 25 seconds.
k create -f nginx-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    livenessProbe:
      initialDelaySeconds: 20
      periodSeconds: 25
      httpGet:
        path: /healthz
        port: 80
    readinessProbe:
      initialDelaySeconds: 20
      periodSeconds: 25
      httpGet:
        path: /
        port: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

137. Create a busybox pod with this command “echo I am from busybox pod; sleep 3600;” and verify the logs.
k run busybox --image=busybox --restart=Never -- /bin/sh -c "echo I am from busybox pod; sleep 3600;"
k logs busybox

138. Copy the logs of the above pod to the busybox-logs.txt and verify
k logs busybox > busybox-logs.txt
cat busybox-logs.txt

139. List all the events sorted by timestamp and put them into file.log and verify
k get events --sort-by=.metadata.creationTimestamp
// putting them into file.log
k get events --sort-by=.metadata.creationTimestamp > file.log
cat file.log

140. Create a pod with an image alpine which executes this command ”while true;
do echo ‘Hi I am from alpine’; sleep 5; done” and verify and follow the logs of the pod.
// create the pod
k run hello --image=alpine --restart=Never -- /bin/sh -c "while true; do echo 'Hi I am from Alpine'; sleep 5;done"
// verify and follow the logs
k logs --follow hello

141. Create the pod with this kubectl create -f
https://gist.githubusercontent.com/bbachi/212168375b39e36e2e2984c097167b0
0/raw/1fd63509c3ae3a3d3da844640fb4cca744543c1c/not-running.yml.
The pod is not in the running state. Debug it.
// create the pod
k create -f
https://gist.githubusercontent.com/bbachi/212168375b39e36e2e2984c097
167b00/raw/1fd63509c3ae3a3d3da844640fb4cca744543c1c/not-running.yml
// get the pod
k get pod not-running
k describe po not-running
// it clearly says ImagePullBackOff something wrong with image
k edit pod not-running // it will open vim editor
or
k set image pod/not-running not-running=nginx

142. This following yaml creates 4 namespaces and 4 pods. One of the pod in one of
the namespaces are not in the running state. Debug and fix it.
https://gist.githubusercontent.com/bbachi/1f001f10337234d46806929d1224539
7/raw/84b7295fb077f15de979fec5b3f7a13fc69c6d83/problem-pod.yaml
k create -f

https://gist.githubusercontent.com/bbachi/1f001f10337234d46806929d12
245397/raw/84b7295fb077f15de979fec5b3f7a13fc69c6d83/problem-pod.yaml
// get all the pods in all namespaces
k get po --all-namespaces
// find out which pod is not running
k get po -n namespace2
// update the image
k set image pod/pod2 pod2=nginx -n namespace2
// verify again
k get po -n namespace2

143. Get the memory and CPU usage of all the pods and find out top 3 pods which
have the highest usage and put them into the cpu-usage.txt file
https://medium.com/bb-tutorials-and-thoughts/practice-enough-with-these-questions-for-the-ckad-exam-2f42d1228552
// get the top 3 hungry pods
k top pod --all-namespaces | sort --reverse --key 3 --numeric | head -3
// putting into file
k top pod --all-namespaces | sort --reverse --key 3 --numeric | head -3 > cpu-usage.txt
// verify
cat cpu-usage.txt

# Services and Networking (13%)
144. Create an nginx pod with a yaml file with label my-nginx and expose the port 80
k run nginx --image=nginx --restart=Never --port=80 --dry-run -o yaml > nginx.yaml
// edit the label app: my-nginx and create the pod
k create -f nginx.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    app: my-nginx
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

145. Create the service for this nginx pod with the pod selector app: my-nginx
// create the below service
k create -f nginx-svc.yaml

apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: my-nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376

146. Find out the label of the pod and verify the service has the same label
// get the pod with labels
k get po nginx --show-labels
// get the service and check the selector column
k get svc my-service -o wide

147. Delete the service and create the service with kubectl expose command and verify the label
// delete the service
k delete svc my-service
// create the service again
k expose po nginx --port=80 --target-port=9376
// verify the label
k get svc -l app=my-nginx

148. Delete the service and create the service again with type NodePort
// delete the service
k delete svc nginx
// create service with expose command
k expose po nginx --port=80 --type=NodePort

149. Create the temporary busybox pod and hit the service. Verify the service that it
should return the nginx page index.html.
// get the clusterIP from this command
k get svc nginx -o wide
// create temporary busybox to check the nodeport
k run busybox --image=busybox --restart=Never -it --rm -- wget -o- <Cluster IP>:80

150. Create a NetworkPolicy which denies all ingress traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress

Q1: Create Secrets Using kubectl
1. To start creating a secret with kubectl, first create the files to store the sensitive information:
echo -n '[username]' > [file1]
echo -n '[password]' > [file2]

kubectl create secret generic [secret-name] \  
--from-file=[file1] \
--from-file=[file2]

Q2: Create Secrets in a Configuration File
1. To create a secret by specifying the necessary information in a configuration file, start by encoding the values you wish to store:
echo -n '[value1]' | base64
echo -n '[value2]' | base64

apiVersion: v1
kind: Secret
metadata:  
  name: newsecret
type: Opaque
data:
  username: dXNlcg==
  password: NTRmNDFkMTJlOGZh

k create -f secrets-test.yaml

Q3: Project Secrets into a Container Using Environment Variables
apiVersion: v1 
kind: Pod 
metadata: 
  name: secret-env-pod 
spec: 
  containers: 
  - name: secret-env-pod
    image: redis 
    env: 
      - name: SECRET_USERNAME 
        valueFrom: 
          secretKeyRef: 
            name: newsecret 
            key: username 
      - name: SECRET_PASSWORD 
        valueFrom: 
          secretKeyRef: 
            name: newsecret 
            key: password 
  restartPolicy: Never

# Decode Secrets
1. To decode the values in a secret, access them by typing the following command:
k get secret [secret] -o jsonpath='{.data}'
echo '[encoded-value]' | base64 --decode
or
k get secret [secret] -o jsonpath=’{.data.username}{"\n"}’ | base64 -d

Q1: Access Secrets Loaded in a Volume
vi secret-storage-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  spec:
    containers:
      - name: test-pod
        image: redis
        volumeMounts:
        - name: newsecret
          mountPath: "/etc/newsecret"
          readOnly: true
    volumes:
    - name: newsecret
      secret:
        secretName: newsecret

Open another terminal instance and use the kubectl exec command to access the pod’s bash shell:
k exec -it [pod] -- /bin/bash

cd into /etc/newsecret, and find the files contained in the secret:
cd /etc/newsecret
ls

Using cut to extract data:
cat > test.txt << EOF
user1:super_secure_password
EOF
cat test.txt | cut -f 2 -d ':' > result.txt
cat result.txt