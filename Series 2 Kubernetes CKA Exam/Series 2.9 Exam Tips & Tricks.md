Series 2.9 Exam Tips & Tricks.md
********************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you!
https://www.youtube.com/@cloudsolutionarchitects-dot

    # Exam tip
    Set the correct context!!!
    
    # Exam tip
    Use Copy & Paste were possible! (Ctrl Shift V) - Remember, exam is in secure browser!
    More information here: https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad
    
    # Exam tip
    Use aliases all of the time
    alias k=kubectl
    e.g. k get pods
    alias kgp='k get po'
    e.g. kgp
    alias kx='kubectl explain'
    kx pods --recursive | less
    kx pods --recursive | less | grep volumes -A 5 -B 10                                    # grep for lines before/after keyword
    
    # Exam tip
    export dr="--dry-run=client -o yaml" && echo $dr                                        # show the command
    e.g. k run nginx --image=nginx $dr > pod.yaml
    --dry-run=client -o yaml is used to get the yaml output of the dry-run command.
    This is useful to see what the command will do without actually running it.

    # Exam tip
    Use -h to explain all!
    k expose -h
    k scale -h

    # Exam tip
    Use 'k run' to create pods!
    use 'k create deploy' to create deployment!
    k run foo --image=nginx

    # Exam tip
    Learn one way to create temp pod for testing!
    kubectl run busybox --image=busybox:1.28 -- sleep 1d
    Then use 'kubectl exec -it busybox -- sh' to log into the pod for interactive mode
    OR
    Then use 'kubectl exec busybox -- CMD HERE!' to just run a command
    NOTE: This type will exist after and not delete itself!
    https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
    
    # Exam tip
    Learn one way to create temp pod for testing! (This deletes itself after)
    kubectl run busybox --image=busybox -it --rm --restart=Never -- /bin/sh -c 'echo hello world'

    # Exam tip
    Use --force to delete a pod quicker!
    kubectl delete pod --force

    # Exam tip 
    Use question number e.g. q1.yaml to save time!

    # Exam tip
    Get the related pods or nodes with grep:
    kubectl get pods -o wide | grep 401

    # Exam tip
    Use the built-in notepad (Mousepad - try to find this to save time!)

    # Exam tip
    Set unavailable/reschedule means drain!

    # Exam tip
    Get Nodes
    Drain Node
    ssh Into Node
    Go as root
    apt install
    Upgrade Node
    Upgrade Apply
    Kubelet Restart
    Uncordon Node

    # Exam tip
    Looks at Secrets, DaemonSet, Ingress, Volumes, PVC & PV (Bigger questions are bigger marks of course!)

    # Exam tip
    Use JsonPath vs. Custom Columns from cheatsheet page!
    https://kubernetes.io/docs/reference/kubectl/cheatsheet/
    Use the 'get command' to see the fields in the json output!
    
    # Exam tip
    As exam is using OS Ubuntu 20.04, make sure to build a system using that OS for practice!
    cat /etc/os-release
    
    e.g.
    pi@master2:~$ cat /etc/os-release
    NAME="Ubuntu"
    VERSION="20.04.5 LTS (Focal Fossa)"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 20.04.5 LTS"
    VERSION_ID="20.04"
    HOME_URL="https://www.ubuntu.com/"
    SUPPORT_URL="https://help.ubuntu.com/"
    BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
    PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
    VERSION_CODENAME=focal
    UBUNTU_CODENAME=focal
    
    # Exam tip
    As exam was based on Ubuntu 20.04 so make sure to know how to restart services etc.
    systemctl status kubelet
    systemctl restart kubelet
    
    # Exam tip
    Learn the format of the Volumemounts and Volumes from here:
    https://kubernetes.io/docs/concepts/storage/volumes/
    
    # Exam tip
    Learn about labels REALLY REALLY well for pods, nodes, namespaces etc.
    
    # Exam tip
    Complete the Killer.sh sample questions too! They are included when you book!
    https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks#is-there-training-to-prepare-for-the-certification-exam
    Linux Foundation says "Login to My Portal and click Start/Resume to view your exam preparation checklist.
    The link to the Simulator is available on the Top Right-Hand corner of the Exam Preparation Checklist."
    
    # Final exam tip
    Try to not let nerves beat you ... prepare for a retake! (if that helps you overcome the nerves!)
