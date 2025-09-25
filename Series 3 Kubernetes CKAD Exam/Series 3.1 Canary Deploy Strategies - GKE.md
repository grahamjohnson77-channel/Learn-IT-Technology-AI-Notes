Series 3.1 Canary Deploy Strategies - GKE.md
************************************************

# *** SUBSCRIBE BANNER ***
# Please feel free to use the notes as a basis for your own study ... But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@cloudsolutionarchitects-dot

    3.1 Deployments Exercises:        https://github.com/ContainerSolutions/k8s-deployment-strategies
                                      https://blog.container-solutions.com/kubernetes-deployment-strategies
    Creates Flask versions of v1/v2   https://www.urbancode.com/resource/kubernetes-blue-green-deployments-working-example/
    Long Tutorial on GCP (In-depth)   https://blog.dockbit.com/kubernetes-canary-deployments-for-mere-mortals-6696910a52b2
    Shows nice automation             https://www.ianlewis.org/en/bluegreen-deployments-kubernetes
                                      https://github.com/IanLewis/kubernetes-bluegreen-deployment-tutorial
    Nice example using Helm           https://angegar.github.io/Kubernetes/bluegreen/
    Shows working example with ISTIO  https://thenewstack.io/tutorial-blue-green-deployments-with-kubernetes-and-istio/
    Shows HaProxy example             https://haproxy-ingress.github.io/docs/examples/blue-green/

# Study Notes

    # Expections: Zero down time, Quick to Market, Quick Customer Feedback, Easy to Rollback
    
    Rolling - Update first set of servers, then second set of servers until all complete (K8s updates pods on %)
    Canary - Focus on set of customers...based on country, client base or demographic (LB Traffic to both parallel)
    Blue Green - LB sends traffic to new version (blue) and completely away from old version (green) (or revert back)
    A-B Deployment (Testing) - Normally used to test a new specific feature

    # Canary Updates (Weighted % Routing):
    Deploy the new version and route only a 'small' % of traffic to it
    If all good, we upgrade the original deployment to use the new viewer (using Rolling Upgrade strategy for example)
    First, add deployment1 deploy with Service. Add a label (version: v1) to pods to route traffic there. Use the same label as selector (on svc)
    We then deploy 2nd deployment, called deployment2.
    With Canary, we want traffic to go to both versions at the same time. However, only route a small amount of traffic!
    
    So first, create a common label, e.g. app: front-end
    We update the selector label in the service, to match this 'common' label (this routes traffic to both then!)
    But right now, its routing it equally, 50% to each deployment...not want we want :(
    To enable canary, reduce the 1 deployment to the smallest of 1 pod
      - if 6 pods, then 83%/17% split
      OR for example:
      - if 4 pods, then 75%/25% split
      OR for example:
      - if 8 pods, then 50%/50% split
    Once testing is complete, we then increase deployment2 and decrease deployment1 pods!
    
    Using the Kubes way, we can only split by amount of pods (100% is 100 pods)...which is why ISTIO can allow only 1% !!!

    When you add the canary deployment to a Kubernetes cluster, it is managed by a service through selectors and labels.
    The service routes traffic to the pods that have the specified label. This allows you to add or remove deployments easily.
    The amount of traffic that the canary gets corresponds to the number of pods it spins up.
    In most cases, you start by routing a smaller percentage of traffic to the canary and increase the number over time.

    # NOTE: Remember, the Canary deployment requires a common label to route traffic to both deployments at the same time...

# Practice Questions

    # Export Cmd
    export dr="--dry-run=client -o yaml" && echo $dr                            # show the command
    k run nginx --image=nginx $dr > pod.yaml                                    # sample usage

    # Tmp pod
    k run temppod --image=nginx --restart=Never --port=80                       # temp pod to verify deployment % weighting
    k exec -it temppod -- sh                                                    # log into temp pod

    # NOTE: Deployment Strategies are all based around Labels! We are concerned only about 
    labels on deploy/pods & service selector!

## Q1. Canary Deployment * (Percentage Weighting Example)

    There are 2 deployments, deployment1 and deployment2. Send 25% of the traffic to deployment2, so 75% of the traffic goes to deployment1.

    OR

    The frontend-v2 deployment currently has 2 replicas.
    The frontend service now routes traffic to to 7 pods in total (5 replicas on the frontend deployment and 2 replicas from frontend-v2 deployment).
    Since the service distributes traffic to all pods equally, in this case, approximately 29% of the traffic will go to frontend-v2 deployment.

    To reduce this below 20%, scale down the pods on the v2 version to the minimum possible replicas = 1.
    k scale deployment --replicas=1 frontend-v2. Once this is done, only ~17% of traffic should go to the v2 version.

    vi myapp-deployment1-canary.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-deployment1
      labels:
        app: myapp
        type: front-end
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end                    # <- THIS LABEL IS 'COMMON' FOR BOTH DEPLOYMENTS % ROUTING!
        spec:
          containers:
          - name: app-container
            image: nginx:1.20.1
      replicas: 2
      selector:
        matchLabels:
          type: front-end

    # Create the deploy:
    k create -f myapp-deployment1-canary.yaml

    vi myapp-deployment2-canary.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-deployment2
      labels:
        app: myapp
        type: front-end
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end                    # <- THIS LABEL IS 'COMMON' FOR BOTH DEPLOYMENTS % ROUTING!
        spec:
          containers:
          - name: app-container
            image: nginx:1.21.1
      replicas: 2
      selector:
        matchLabels:
          type: front-end

    # Create the deploy:
    k create -f myapp-deployment2-canary.yaml

    vi myservice-definition-canary.yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: myapp-service
    spec:
      selector:
        type: front-end
      ports:
        - protocol: TCP
          port: 80

    # Create the canary service:
    k create -f myservice-definition-canary.yaml

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
    
    # Exit out of temp pod!

    # At this point, the svc would be sending traffic to BOTH deployments, 50-50. Now check canary is working!!!
    
    Question asked to send 25% of traffic to the deployment2! (4 pods = 3 deployment1 for 75% and 1 deployment2 for 25%)
    
    k scale deployments.apps myapp-deployment1 --replicas=3                         # scale down deployment to 0%
    k scale deployments.apps myapp-deployment2 --replicas=1                         # scale up this new deployment to 100%

    # See the pods status now (wait for all to come back up):
    k get pods

    # Log back into temp pod:
    k exec -it temppod -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s -I myapp-service | grep Server:

    # Continous loop:
    while sleep 0.5; do curl -s -I myapp-service | grep Server:; done

    # Retry the Loop 100 times so that 25% is going to deployment2:
    for i in `seq 1 100`; do curl -s -I myapp-service | grep Server: | awk -F Server:  {'print $2'}; done | sort | uniq -c

    # Finally, clean up:
    k delete deployments.apps myapp-deployment1
    k delete deployments.apps myapp-deployment2
    k delete svc myapp-service

    ## Final Solution

    Remember the Question:
    
    There are 2 deployments, deployment1 and deployment2. Send 25% of the traffic to deployment2, so 75% of the traffic goes to deployment1.
    
    # Show labels for currently running deployments:
    k get deploy --show-labels
    k get pod --show-labels

    # What we want is to have the common label for both deployments:
    type: front-end                    # <- THIS LABEL IS 'COMMON' FOR BOTH DEPLOYMENTS % ROUTING!

    vim deployment1.yaml                                                                # change deploy labels to front-end

    NOT FOR EXAM! BUT NICE TO HAVE:
    # Add a NEW POD labels in the yaml updates so we can use 'k get pods -l pod=deployment1' for example!
    template:
        metadata:
          creationTimestamp: null
          labels:
            type: front-end
            pod: deployment1
          name: myapp-pod

    # Copy the existing deployment1 to be deployment2 too (if both running):
    cp deployment1.yaml deployment2.yaml

    vim deployment2.yaml                                                               # make changes for deployment2!

    If 4 pods were the orignal deployment1, then we want 3 in deployment1 and 1 in deployment2! (for 25%)...so change replicas too now!

    k delete deploy myapp-deployment1
    k delete deploy myapp-deployment2

    k create -f deployment1.yaml
    k create -f deployment2.yaml

    # Get information about the existing service:
    k get svc myapp-service
    k describe svc myapp-service                                       # get service selector                              

    # Patch the service to ensure it is pointed now to the 'common' deployment label:
    k patch service myapp-service -p '{"spec":{"selector":{"type": "front-end"}}}'
    service/myapp-service patched

    # Log into temp pod:
    k exec -it temppod -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s -I myapp-service | grep Server:

    # Continous loop:
    while sleep 0.5; do curl -s -I myapp-service | grep Server:; done

    # Retry the Loop 100 times so that 25% is going to deployment2:
    for i in `seq 1 100`; do curl -s -I myapp-service | grep Server: | awk -F Server:  {'print $2'}; done | sort | uniq -c

## Q2. Canary Deployment - ConfigMap HTML Example

    # Ref: https://phoenixnap.com/kb/kubernetes-canary-deployments
    Create the index.html file:
    vi index.html

    <html>
    <h1>Hello World!</h1>
    <p>This is version 1</p>
    </html>

    # Create the configmap:
    k create configmap nginx-index-html-configmap-v1 --from-file=index.html
    k get cm
    k describe cm nginx-index-html-configmap-v1

    vi myapp-primary-configmap.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-primary
      labels:
        app: myapp
        type: front-end
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end                      # <- THIS IN THE IMPORTANT ADDITIONAL LINE FOR CANARY!
        spec:
          containers:
          - name: app-container
            image: nginx:1.20.1
            resources:
              limits:
                memory: "128Mi"
                cpu: "50m"
            volumeMounts:
            - mountPath: /usr/share/nginx/html/index.html
              name: nginx-conf
              subPath: index.html
          volumes:
            - name: nginx-conf
              configMap:
                name: nginx-index-html-configmap-v1
      replicas: 5
      selector:
        matchLabels:
          type: front-end

    # Create the primary deploy:
    k create -f myapp-primary-configmap.yaml

    # Modify the index.html file to say v2:
    vi index.html

    <html>
    <h1>Hello World!</h1>
    <p>This is version 1</p>
    </html>

    # Create the v2 configmap:
    k create configmap nginx-index-html-configmap-v2 --from-file=index.html
    k get cm
    k describe cm nginx-index-html-configmap-v2

    vi myapp-canary-configmap.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-canary
      labels:
        app: myapp
        type: front-end
    spec:
      template:
        metadata:
          name: myapp-pod
          labels:
            type: front-end                      # <- THIS IN THE IMPORTANT ADDITIONAL LINE FOR CANARY!
        spec:
          containers:
          - name: app-container
            image: nginx:1.21.1
            resources:
              limits:
                memory: "128Mi"
                cpu: "50m"
            volumeMounts:
            - mountPath: /usr/share/nginx/html/index.html
              name: nginx-conf
              subPath: index.html
          volumes:
            - name: nginx-conf
              configMap:
                name: nginx-index-html-configmap-v2
      replicas: 1
      selector:
        matchLabels:
          type: front-end

    # Create the canary deploy:
    k create -f myapp-canary-configmap.yaml

    vi myservice-definition-service-configmap.yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: myapp-service
    spec:
      selector:
        type: front-end
      ports:
        - protocol: TCP
          port: 80

    # Create the canary service:
    k create -f myservice-definition-configmap.yaml

    # Get the service:
    k get service

    # Log into temp pod:
    k exec -it temp -- sh

    # So here, we can get the nginx version our nginx-service is using:
    curl -s myapp-service | grep '<p>'

    # Continous loop:
    while sleep 0.5; do curl -s myapp-service | grep '<p>'; done

    # Loop 100 times:
    for i in `seq 1 100`; do curl -s myapp-service | grep '<p>' | awk -F '<p>'  {'print $2'}; done | sort | uniq -c

    # Clean up:
    k delete deploy myapp-primary
    k delete deploy myapp-canary
    k delete svc myapp-service
    k delete cm nginx-index-html-configmap-v1
    k delete cm nginx-index-html-configmap-v2
