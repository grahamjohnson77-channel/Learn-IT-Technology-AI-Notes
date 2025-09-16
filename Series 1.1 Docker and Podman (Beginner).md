Series 1.3 Docker and Podman (Beginner).md
******************************************

## 🌟 Subscribe Banner 🌟
## Please feel free to use the notes as a basis for your own study ... <br>But we ask in return to subscribe to the channel, so we can continue to invest time and effort in helping others. Thank you! 
https://www.youtube.com/@grahamjohnson77

## Installation

	NOTE: I have migrated completely to Podman as Kubernetes has deprecated Docker ... 
	https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/

	# Install docker on MAC
	brew install docker

	OR

	# Install podman on MAC
	brew install podman

	# More Information:
	https://docs.docker.com/desktop/
	https://podman.io/getting-started/
	https://podman.io/getting-started/installation

	# Downloads new VM image
	podman machine init

	# Then run
	podman machine start

	# Output
	Starting machine "podman-machine-default"
	Waiting for VM ...
	Mounting volume... /Users/<username>:/Users/<username>

	This machine is currently configured in rootless mode. If your containers
	require root permissions (e.g. ports < 1024), or if you run into compatibility
	issues with non-podman clients, you can switch using the following command:

		podman machine set --rootful

	API forwarding listening on: /Users/<username>/.local/share/containers/podman/machine/podman-machine-default/podman.sock

	The system helper service is not installed; the default Docker API socket
	address can't be used by podman. If you would like to install it run the
	following commands:

		sudo /opt/homebrew/Cellar/podman/4.3.1/bin/podman-mac-helper install
		podman machine stop; podman machine start

	You can still connect Docker API clients by setting DOCKER_HOST using the
	following command in your terminal session:

		export DOCKER_HOST='unix:///Users/<username>/.local/share/containers/podman/machine/podman-machine-default/podman.sock'

	Machine "podman-machine-default" started successfully

	# If you see the following error for Podman:
	Cannot connect to Podman. 
	Please verify your connection to the Linux system using `podman system connection list`, or try `podman machine init` and `podman machine start` to manage a new Linux VM
	Error: unable to connect to Podman socket: Get "http://d/v4.3.1/libpod/_ping": dial unix ///var/folders/lx/_0wwpj2n3yv7t1qlkq0z_cjr0000gn/T/podman-run--1/podman/podman.sock: connect: no such file or directory

	I had to run: 'podman machine init' to download the VM image for Podman!
	e.g. Downloading VM image: fedora-coreos-37.20221225.2.2-qemu.aarch64.qcow2.xz [===============================================>------] 517.2MiB / 576.0MiB

## Project Setup

	# Now, we can use the following commands in Podman:
	podman image ls								                # list docker images currently available!
	podman container ls 						              # list docker containers currently available
	podman stop <container name>				          # stop container name
	podman rm $(podman ps -a -q)				          # Remove all stopped containers
	podman image rm -f <image name>				        # To remove an image (forcefully)
	podman rmi $(podman images -a -q)			        # delete ALL images in one command!

	# To create a network for running locally
	podman network create test_network						# create a new network bridge
	podman network ls
	podman network inspect test_network						# recheck the network bridge!

	# Create a new dockerfile
	vi Dockerfile_test_podman

	# Add the following contents to the file:
	FROM nginx
	COPY static-html-directory /usr/share/nginx/html

	# Make the new static folder
	mkdir static-html-directory

	NOTE: Please see here for more details: https://hub.docker.com/_/nginx

	# Build the specific container image
	podman build -t my_test_image:latest . -f Dockerfile_test_podman
	OR
	podman build -t my_test_image:1.0 . -f Dockerfile_test_podman

	# Run the container
	podman run -d -p 80:80 --net test_network --name testing_podman my_test_image:1.0

	# Running this gives an error!
	podman run -d -p 80:80 --net test_network --name testing_podman my_test_image:1.0
	Error: rootlessport cannot expose privileged port 80, you can add 'net.ipv4.ip_unprivileged_port_start=80' to /etc/sysctl.conf (currently 1024), or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied

	## More info here on exposing ports IF you really wanted too...not recommended.
	https://blog.while-true-do.io/podman-networking-3/

	## So will use a good port for testing by stoping the old container and starting a new! (Browser port:Internal Port)
	podman stop testing_podman
	podman rm $(podman ps -a -q)
	podman run -d -p 8080:80 --net test_network --name testing_podman my_test_image:1.0

	podman run -d -p 8080:80 --net test_network --name testing_podman my_test_image:1.0
	76baa6dd550baf84bcfd77ac205242cb84011c56e0f15ee6629517d68e9e699e

	podman container ls
	CONTAINER ID  IMAGE                        COMMAND               CREATED        STATUS            PORTS                 NAMES
	76baa6dd550b  localhost/my_test_image:1.0  nginx -g daemon o...  7 seconds ago  Up 7 seconds ago  0.0.0.0:8080->80/tcp  testing_podman

	# Go to the browser you should be able to use this to see the nginx front page!
	http://127.0.0.1:8080/

	# Quick cleanup
	podman container ls
	podman stop <container id>
	podman rmi $(podman images -a -q)

	# Mount Working Folder (Advanced)
	cd to working directory!
	podman build --target dev . -t python
	podman run -it --rm -v ${PWD}:/work python sh

	# Troubleshooting
	https://podman-desktop.io/docs/troubleshooting
