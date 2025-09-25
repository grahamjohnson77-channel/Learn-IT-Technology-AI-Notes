Series 3.2 Blue-Green Deploy Strategies - GKE.md
****************************************************

# *** SUBSCRIBE BANNER ***
# Please feel free to use the notes as a basis for your own study ... But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@cloudsolutionarchitects-dot

    # 3.1 Deployments Exercises:        https://github.com/ContainerSolutions/k8s-deployment-strategies
    #                                   https://blog.container-solutions.com/kubernetes-deployment-strategies
    # Creates Flask versions of v1/v2   https://www.urbancode.com/resource/kubernetes-blue-green-deployments-working-example/
    # Long Tutorial on GCP (In-depth)   https://blog.dockbit.com/kubernetes-canary-deployments-for-mere-mortals-6696910a52b2
    # Shows nice automation             https://www.ianlewis.org/en/bluegreen-deployments-kubernetes
    #                                   https://github.com/IanLewis/kubernetes-bluegreen-deployment-tutorial
    # Nice example using Helm           https://angegar.github.io/Kubernetes/bluegreen/
    # Shows working example with ISTIO  https://thenewstack.io/tutorial-blue-green-deployments-with-kubernetes-and-istio/
    # Shows HaProxy example             https://haproxy-ingress.github.io/docs/examples/blue-green/

# Study Notes

    Expections: Zero down time, Quick to Market, Quick Customer Feedback, Easy to Rollback
    Rolling - Update first set of servers, then second set of servers until all complete (K8s updates pods on %)
    Canary - Focus on set of customers...based on country, client base or demographic (LB Traffic to both parallel)
    Blue Green - LB sends traffic to new version (blue) and completely away from old version (green) (or revert back)
    A-B Deployment (Testing) - Normally used to test a new specific feature

    Blue Green:
    New version (green) deployed along side old version (blue)
    Traffic is still pointed to old version. There are tests on new version, then traffic switches to new version
    e.g. First, deployment1 with Service. Add a label (version: v1) to pods to route traffic there. 
    Use the same label as selector (on svc)
    We then deploy 2nd deployment, called deployment2.
    Once all tests are passed, we route traffic to the new Green deploy by updating the service to use the new label for 
    the deployment2 pods e.g. version: v2. Goal is to route traffic to the old and new but then switch completely to it.
    
# Practice Questions

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage

    # Tmp pod
    k run temppod --image=nginx --restart=Never --port=80                       # temp pod to verify deployment % weighting
    k exec -it temppod -- sh                                                    # log into temp pod

    # NOTE: Deployment Strategies are all based around Labels!
    We are concerned only about labels on deploy/pods & service selector!

## Q1. Blue Green Deployment (Patching Service Basic Example)

    vi myapp-deployment1.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-deployment1
      labels:
        app: myapp
        type: front-end-v1
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end-v1
        spec:
          containers:
          - name: app-container
            image: nginx:1.20.1
      replicas: 2
      selector:
        matchLabels:
          type: front-end-v1

    # Create the deploy:
    k create -f myapp-deployment1.yaml

    vi myservice-definition.yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: myapp-service
    spec:
      ports:
        - protocol: TCP
          port: 80
      selector:
        type: front-end-v1

    # Create the service:
    k apply -f myservice-definition.yaml

    # See the deploy and service that is running:
    k get deploy
    k get svc myapp-service

    # Log into temp pod:
    k exec -it temppod -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s -I myapp-service | grep Server:

    # Continous loop:
    while sleep 0.5; do curl -s -I myapp-service | grep Server:; done

    # Loop 100 times:
    for i in `seq 1 100`; do curl -s -I myapp-service | grep Server: | awk -F Server:  {'print $2'}; done | sort | uniq -c

    # Create 2nd version of deployment:
    vi myapp-deployment2.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-deployment2
      labels:
        app: myapp
        type: front-end-v2
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end-v2
        spec:
          containers:
          - name: app-container
            image: nginx:1.21.1
      replicas: 2
      selector:
        matchLabels:
          type: front-end-v2

    # First, show the differences between both files (side by side):
    sdiff myapp-deployment1.yaml myapp-deployment2.yaml

    # Use -s to suppress common lines:
    sdiff -s myapp-deployment1.yaml myapp-deployment2.yaml

    # Create the green deploy:
    k create -f myapp-deployment2.yaml

    (NOTE: Another way is to create all at once using: k create -f .)

    # Get currently existing selector label e.g. v1 or v2:
    k describe svc myapp-service

    # Patch the service to update the selector:
    k patch service myapp-service -p '{"spec":{"selector":{"type": "front-end-v2"}}}'
    service/myapp-service patched

    # Log into temp pod:
    k exec -it temppod -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s -I myapp-service | grep Server:

    # Continous loop:
    while sleep 0.5; do curl -s -I myapp-service | grep Server:; done

    # Loop 100 times:
    for i in `seq 1 100`; do curl -s -I myapp-service | grep Server: | awk -F Server:  {'print $2'}; done | sort | uniq -c

    # Clean up (if not trying Canary now):
    k delete deployments.apps myapp-deployment1
    k delete deployments.apps myapp-deployment2
    k delete svc myapp-service

## Q2. Blue/green Deployment - To Release a Single Service

    # Ref: https://github.com/ContainerSolutions/k8s-deployment-strategies/tree/master/blue-green/single-servic
    
    Steps to follow:
    version 1 is serving traffic
    deploy version 2
    wait until version 2 is ready
    switch incoming traffic from version 1 to version 2
    shutdown version 1

    # Deploy the first application:
    $ kubectl apply -f app-v1.yaml

    # Test if the deployment was successful:
    $ curl $(minikube service my-app --url)
    2018-01-28T00:22:04+01:00 - Host: host-1, Version: v1.0.0

    # To see the deployment in action, open a new terminal and run the following:
    watch kubectl get po

    # Then deploy version 2 of the application:
    kubectl apply -f app-v2.yaml

    # Wait for all the version 2 pods to be running:
    kubectl rollout status deploy my-app-v2 -w
    deployment "my-app-v2" successfully rolled out

    Side by side, 3 pods are running with version 2 but the service still send traffic to the first deployment.

    If necessary, you can manually test one of the pod by port-forwarding it to your local environment.

    Once your are ready, you can switch the traffic to the new version by patching
    the service to send traffic to all pods with label version=v2.0.0:
    kubectl patch service my-app -p '{"spec":{"selector":{"version":"v2.0.0"}}}'

    # Test if the second deployment was successful:
    service=$(minikube service my-app --url)
    while sleep 0.1; do curl "$service"; done

    # In case you need to rollback to the previous version:
    kubectl patch service my-app -p '{"spec":{"selector":{"version":"v1.0.0"}}}'

    # If everything is working as expected, you can then delete the v1.0.0 deployment:
    kubectl delete deploy my-app-v1
    kubectl delete all -l app=my-app

## Q3. Blue/green Deployment - To Release Multiple Services Simultaneously using Traefik

    In this example, we release a new version of 2 services simultaneously using the blue/green deployment strategy.
    Traefik in used as Ingress controller, this example would also work with the Nginx Ingress controller.

    # Steps to follow:
    service a and b are serving traffic
    deploy new version of both services
    wait for all services to be ready
    switch incoming traffic from version 1 to version 2
    shutdown version 1

    Install the latest version of Helm, then install Traefik:

    # Deploy Traefik with Helm:
    helm install \
        --name=traefik \
        --version=1.60.0 \
        --set rbac.enabled=true \
        stable/traefik

    # Deploy version 1 of application a and b and the ingress:
    kubectl apply -f app-a-v1.yaml -f app-b-v1.yaml -f ingress-v1.yaml

    # Test if the deployment was successful:
    ingress=$(minikube service traefik --url | head -n1)
    curl $ingress -H 'Host: a.domain.com'
    Host: my-app-a-v1-66fb8d6f99-hs8jr, Version: v1.0.0

    curl $ingress -H 'Host: b.domain.com'
    Host: my-app-b-v1-5766557f99-dpghc, Version: v1.0.0

    # To see the deployment in action, open a new terminal and run the following command:
    watch kubectl get po

    # Then deploy version 2 of both applications:
    kubectl apply -f app-a-v2.yaml -f app-b-v2.yaml

    # Wait for both applications to be running:
    kubectl rollout status deploy my-app-a-v2 -w
    deployment "my-app-a-v2" successfully rolled out

    kubectl rollout status deploy my-app-b-v2 -w
    deployment "my-app-b-v2" successfully rolled out

    # Check the status of the deployment, then when all the pods are ready, you can update the ingress:
    kubectl apply -f ingress-v2.yaml

    # Test if the deployment was successful:
    curl $ingress -H 'Host: a.domain.com'
    Host: my-app-a-v2-6b58d47c5f-nmzds, Version: v2.0.0

    curl $ingress -H 'Host: b.domain.com'
    Host: my-app-b-v2-5c9dc59959-hp5kh, Version: v2.0.0

    # In case you need to rollback to the previous version:
    kubectl apply -f ingress-v1.yaml

    # If everything is working as expected, you can then delete the v1.0.0 deployment:
    kubectl delete -f ./app-a-v1.yaml -f ./app-b-v1.yaml

    # Cleanup:
    kubectl delete all -l app=my-app
    helm del --purge traefik

## Q4. Blue/green Deployment - Modify ConfigMap Example

    # Ref: https://blog.nillsf.com/index.php/2019/11/10/simple-kubernetes-blue-green-deployments/

    # Create the index.html file:
    vi index.html

    <html>
     <head>
      <title>Blue</title>
     </head>
     <body bgcolor="#11a7f7">
      <h1>V1</h1>
     </body>
    </html>

    # Create the configmap:
    k create configmap index-blue --from-file=index.html
    k get cm
    k describe cm index-blue

    vi blue-deploy-configmap.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: blue
    spec:
      replicas: 3
      template:
        metadata:
          labels:
            app: web-version
            color: blue
        spec:
          containers:
          - name: nginx
            image: nginx
            ports:
            - containerPort: 80
            volumeMounts:
            - name: config-volume
              mountPath: /usr/share/nginx/html
          volumes:
          - name: config-volume
            configMap:
              name: index-blue
      selector:
        matchLabels:
          color: blue
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: myapp-service
    spec:
      type: LoadBalancer
      ports:
      - port: 80
      selector:
        color: blue

    # Create the primary deploy:
    k create -f blue-deploy-configmap.yaml

    # And now, as production traffic is not disturbed, we can watch the deployment rollout complete: 
    k rollout status deploy blue

    # Can we verify this using a script ?
    vi show_versions.sh

    #!/bin/bash
    IP=${1?Error: no IP given}

    while :
    do
        curl -s $IP | grep h1 | sed -e 's/^[ \t]*//' -e "s/^<h1>//" -e "s/<\/h1>//"
        sleep 0.3
    done

    ./show_versions.sh <INSERT THE LOAD BALANCER IP HERE!!!>

    # Log into temp pod:
    k exec -it temp -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s myapp-service | grep '<p>'

    # Continous loop:
    while sleep 0.5; do curl -s myapp-service | grep '<p>'; done

    # Loop 100 times:
    for i in `seq 1 100`; do curl -s myapp-service | grep '<p>' | awk -F '<p>'  {'print $2'}; done | sort | uniq -c

    To test the new Green version:

    # Modify the index.html to now use v2
    vi index.html

    # Make the Green config Map:
    kubectl create configmap index-green --from-file=index.html

    # Make a copy of the deployment file:
    cp blue-deploy-configmap.yaml green-deploy-configmap.yaml

    # Modify the primary deploy to point to green labels and configMap index-green:
    vi green-deploy-configmap.yaml                                           # make volume point to v2
    k apply -f green-deploy-configmap.yaml

    # And now, as production traffic is not disturbed, we can watch the deployment rollout complete: 
    k rollout status deploy green
    OR
    We could have the service separate and edit or patch the service!
    kubectl edit svc myapp-service                                           # switch selector to green

    # Log into temp pod:
    k exec -it temp -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s myapp-service | grep '<p>'

    # Continous loop:
    while sleep 0.5; do curl -s myapp-service | grep '<p>'; done

    # Loop 100 times:
    for i in `seq 1 100`; do curl -s myapp-service | grep '<p>' | awk -F '<p>'  {'print $2'}; done | sort | uniq -c

    # Cleanup:
    k delete cm index-blue
    k delete cm index-green
    k delete daemonset svclb-blue
    k delete deploy blue
    k delete deploy green
    k delete svc myapp-service
    rm index.html
