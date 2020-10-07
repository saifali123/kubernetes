#Kubernetes Architecture.

##Master Node

* Master Node is responsible for managing, planning, scheduling and monitoring the nodes.

* Master Node contains multiple components which handles all these operations. These components are called as **Control Plane Components**.

####* Control Plane Components: 

1. etcd

Containers information are stored in a key-value distributed database which is called as etcd. ETCD is a distributed reliable key-value store that is Simple, Secure and Fast. 
It stores the kubernetes cluster information such as:

  * Nodes
  * Pods
  * Configs
  * Secrets
  * Accounts
  * Roles
  * Bindings
  * Others
  
2. kube-scheduler

Kube-scheduler is responsible for placing a right container on a node based on the container resource requirements and constraints.

3. Controllers-Manager

Controllers are responsible in Kubernetes for certain areas and sections. There are multiple controllers who does this, such as:

  * Node Controller: The Node Controller takes cares of Nodes. They are responsible for provisioning new Nodes on the cluster, handling of Nodes if not healthy or gets destroyed.
  * Replication Controller: Replication Controller are responsible for checking the desired number of replications running.

4. kube-apiserver

The kube-apiserver is responsible for handling all of these components to work all together. It orchestrates all these components in Kubernetes Cluster. 
The kube-apiserver is the external interface for a customer or a user for performing operations and managing the kubernetes cluster.

5. kubelet

A kubelet is an agent which runs on each node, it listens the instructions from the kube-apiserver and deletes or creates the nodes as instructed from the kube-apiserver.
Kube-apiserver always fetches information of all the nodes in the cluster for checking the status.

6. kube-proxy service

The kube-proxy service is responsible for helping worker nodes to communicate each other.                                                                          
                                                                                               

 


##Worker Node

Worker nodes hosts applications as containers.

![kubernetes-architecture](./videos-screenshots/kubernetes-architecture.png)

# 1. ETCD 
![ETCD](./videos-screenshots/etcd.png)

* ETCD runs on port 2379 and can be run using `./etcd` command.
* The default etcd client is `./etcdctl` and can be used to store and retrieve the key value data.
* To store the key value data use `./etcdctl set key1 value1` command. Whereas to retrieve the data use `./etcdctl get key1 ` and for more information use `./etcdctl` command only. 

##ETCD in Kubernetes
* ETCD cluster stores cluster information such as 
* To get all the keys which are stored in Kubernetes etcd use `kubectl exec etcd-master -n kube-system etcdl get / --prefix -keys-only` command.
* Kubernetes stores the data in a specific directory structure. The root directory is the registry directory and under that all directories are present such as minions, pods, replicasets,
  deployments, roles and secrets.
* In a high availability environment, we will have multiple masters node in the cluster on top of that masters node there will be etcd pods. The connection between these etcd pods are 
  configured in the etcd.service configuration. In the initial cluster flag, in the etcd.service configuration, there we have to specify the etcd pods details.   

# 2. Kube-API Server

* When we execute any `kubectl` command such as `kubectl get nodes` this request goes to kube-api server, kube-api server then authenticates the request and validates it. The kube-api server then request the get nodes data to the etcd cluster and response back with the get nodes data. 

* Kube-api server performs the below tasks
    1. Authenticate User
    2. Validate Request
    3. Retrieve Data from ETCD cluster
    4. Update Data to ETCD cluster
    5. Scheduler
    6. Kubelet

* Kube-api server is the only component that interacts directly with the etcd datastore.
* If we want to install the kube-api server from the scratch and configure it in detail then we have to install the Kubernetes in a hard-way. For example, we can also configure certificates(SSL/TLS) in the kube-api server to perform secure connections between other components. We can also specify the ETCD server connection in the kube-api serverv config file such as the ETCD pod ip and its port. The default port for the ETCD server in kubernetes is 2379
* To get the kube-api server details, it is totally depends on how we have setup the kubernetes cluster. To setup the kubernetes cluster, there are two ways, using the kubeadm tool or without using the kubeadm which is the hard-way
* To get the details of the kube-api server which is setup using the kubeadm tool, we can get the kube-api server pod by listing all pods using `kubectl get pods -n kube-system ` command.
We can see the definition yaml file for the kube-api server in the /etc/kubernetes/manifests/kube-apiserver.yml location.
* Whereas, if the kubernetes cluster is setup without the kubeadm tool, that is the hard-way, we can see the kube-api server definition yaml file in /etc/systemd/system/kube-apiserver.service. To also see the kube-apiserver process on the master node use `ps aux | grep kube-apiserver` command
     
    
    
# 3. Kube Controller Manager

A controller is a process that continously monitors the state of various components within the system and works towards bringing the whole system to the desired functioning state. 

## i. Node controller

![Node Controller](./videos-screenshots/nodecontroller.png)

* It is responsible for monitoring the status of the nodes and taking necessary actions to keep the application running it does this using the kube-api server.
* The node controller checks the status of the nodes every 5 seconds that way it monitors the status of the nodes. If node controllers stops receiving heart beats, it declares          that node as unreachable. Before officially declaring the node as unreachable, the node controller waits for more 40 seconds.
* After the node is declared or marked as unreachable, node controller gives 5 minutes to the node to come back. If it does not come, the node controller removes the created pods from that unreachable node and provisions them on the healthy one if the pods are the part of the replica set.  

## ii. Replication Controller

* It is responsible for monitoring the status of the replica sets and ensures that the desired number of pods are available at all times within the replica sets. If a pod dies it creates another one.

* There are multiple controllers present in the controller manager. To download the controller manager, download it from using the kubernetes release page and run it as a service. 

![Controller File](./videos-screenshots/controllerservice.png)

* To configure the controller manager use its service file. All the configuration details such as monitoring period, grace period, timeouts, etc can be configured in this service. By default all the controller are enable, if we want to enable specific controllers we can also do that using the `--controller flag`

* To view the kube-controller-manager server options, it totally depends on how we have setup our kubernetes cluster with or without kubeadm. If kubeadm is used we can see the kube-controller-manager pod using `kubectl get pods -n kube-system` command. To see the kube-controller-manager definition yaml file, see `/etc/kubernetes/manifests/kube-controller-manager.yaml` file

*  To view the kube-controller-manager service file for the cluster which is setup without the kubeadm tool, see `/etc/systemd/system/kube-controller-manager.service` file 

* To see the process of the kube-controller-manager on the master node use `ps aux | grep kube-controller-manager` command.



# 4. Kube Scheduler

* Kube-scheduler only decides which pods goes on which node. It does not actually place the pods on the node, thats the job of kubelet. The kubelet is responsible for creating the pods on the nodes. The scheduler only decides which pods goes on which nodes.

![Kube Scheduler](./videos-screenshots/kubescheduler.png)

* Kube-scheduler has certain criteria for placing the specific pods on the specific nodes. Criteria such as resource requirements needed, etc. We will be having multiple pods on the nodes which runs specific applications, and scheduler places these pods on that specific nodes which runs that applications. For example, if there is a pod which requires 10 CPU cores and there are 4 nodes which has various CPUs limits. First node has 4 CPU cores, Second has 4 CPU cores, Third has 12 CPU cores and Fourth has 16 CPU cores. So now the scheduler calculates the CPU cores and checks when the pod with 10 CPU cores will be placed on these Four Nodes which will be having more CPU cores left after placing the 10 CPU cores pod. So the best fit will be the Fourth Node which contains 16 CPU cores and when the 10 CPU cores pod will be placed on it then, 6 more CPU cores will be left. So the Fourth Node will get the higher rank than the other nodes. This is how the kube-scheduler places the pods on the nodes.  
 
![Kube Scheduler Service](./videos-screenshots/kubeschedulerservice.png)
 
* To download the kube-scheduler use the kubernetes official page and run it as a service. We can configure the service file of the kube-scheduler as well. If the cluster is setup using the kubeadm tool, then the kube-scheduler pod is created on the master node and to view the kube-scheduler definition yaml file see `/etc/kubernetes/manifests/kube-scheduler.yaml`

* To see the process on the master node use `ps aux | grep kube-scheduler` command

# 5. Kubelet

* Kubelet registers the nodes in the kubernetes cluster. When it receives the instructions  to load a pods on the nodes it requests the container runtime engine such as Docker to pull the required image and run the pods. The kubelet then monitors the pods and response to the kube-api server on a timely basis.

![Kubelet Service](./videos-screenshots/kubeletservice.png)

* If we use the kubeadm tool to setup the cluster it does not automatically deploys the kubelet, we have to manually install it on the kubernetes worker nodes. Download it from the kubernetes service, extract it and run it as a service.

* To view the kubelet process on the worker nodes use `ps aux | grep kubelet` command. 

# 6. Kubeproxy

* Kube-proxy is a process on each node in the kubernetes cluster. Its job is to look for new services and every time a new service is created it creates an appropriate rules on each node to forward traffic to those services to the backend pods.

![Kube Proxy](./videos-screenshots/kubeproxy.png)

* One way it does this is using the IP tables rules. It creates an IP table rules on each node in the cluster to forward traffic heading to the IP of the service(10.96.0.12) to the IP of the actual pod(10.32.0.15)

![Kube Prxoy](./videos-screenshots/kubeproxyservice.png)

* To download it use the kubernetes service and run it as a service.   

* To view the pod of the kube-proxy use the `kubectl get pods -n kube-system` command.

 
# Namespaces

* There are different namespaces for different purpose. For example, kube-system namespace is the kubernetes official namespace where it deploys all its important components. Next, the second namespace is the default namespace, where we as a user creates our own resources such as pods, deployments, services, replicasets, etc. These namespaces are isolated with each other for not interrupting each other namespaces and keep it secured. The third namespace is kube-public, in this, the resources that should be made available to all users are created. So whenever we setup a kubernetes cluster it creates three namespaces automatically, they are:
       1. kube-system (official kubernetes namespace)
       2. default (for users)
       3. kube-public (for all users to make resources public)

![Namespace Isolation](./videos-screenshots/namespaceisolation.png)
 
* However, we can create our own namespaces as well, for example, if we have multiple environments in an Organisation such as Dev, Stage and Production. We can create that as well.

* We can also ***assign policies and resource limits*** for each namespace and specify who can do what.

* We can also connect any pod to each other. For example, if there is a three tier application in first namespace that contains web-pod, db-service and web-deployment. The web-pod can connect to the db-service by just specifying the db-service name such as like this `mysql.connect("db-service")`. 

![Namespace Connectivity](./videos-screenshots/namespaceconnection.png)

* We can also connect  web-pod from first namespace to another pod(db-service) which is in second namespace by just specifying the namespace name.
For example if the second namespace name is `dev`. Then the command will go like this `mysql.connect("db-service.dev.svc.cluster.local")`

Here, 

    `cluster.local` - Default domain name of the kubernetes cluster
    
    `svc` - subdomain for the service
    
    `dev` - namespace name
    
    `db-service` - service name 

* To list the pods from the default namespace use `kubectl get pods` command. To list the pods from another namespace such as kube-system use `kubectl get pods --namespace=kube-system`

* Next, to create a pod in a default namespace use `kubectl create -f po-definition.yml` command. Whereas, to create a pod in another namespace use `kubectl create -f pod-defintion.yml --namespace=<namespace-name>`

* To create a pod in another namespace using the pod-definition.yml file, specify `namespace: <namespace-name>` under the metadata section.

* To create a namespace using the CLI command use `kubectl create namespace <namespace-name>`. Whereas to create a namespace from the definition.yml file use below script.

```hcl-terraform
apiVersion: v1
kind: Namespace
metadata:
  name: <namespace-name>
```       

* By default, we are in the default namespace. But if we need to swith to another namespace, or to set our custom namespace as a default namespace to us, then we can switch to another namespace by using this `kubectl config set-context $(kubectl config current-context) --namespace=<namespace-name>` command. However, if we need to list the pods of the kubernetes default namespaces after switching to our custom namespaces then we have to specify the `--namespace=default` option  for listing the pods of the kubernetes default namespace. To list the pods from all the namespaces use `kubectl get pods --all-namespaces` command.

* To set the resource limit for a namespace, create a resource quota such as below example:

```hcl-terraform
apiVersion: v1
kind: ResourceQuota
metadata:
  name: <resource-quota-name>
  namespace: <namespace-name>
spec: 
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi    
```

Now, to create this resource quota for specified namespace use `kubectl create -f resource-quota-definition.yml` command.


# Imperative and Declarative Approach

**Imperative Approach Kubernetes Commands for Exam Prepartions:**
```shell script
kubectl run --image=nginx nginx
kubectl create deployment --image=nginx nginx
kubectl expose deployment nginx --port 80
kubectl edit deployment nginx  # Edit command modifies the current state of the kubernetes resources, not the definition yaml files.
kubectl scale deployment nginx --replicas=5 
kubectl set image deployment nginx nginx=nginx:1.18
```

* `--dry-run`: By default as soon as the command is run, the resource will be created. If you simply want to test your command, use the `--dry-run=client` option. This will not create the resource, instead, tell you whether the resource can be created and if your command is right.

* `-o yaml`: This will output the resource definition in YAML format on the screen.

* Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run) `kubectl run nginx --image=nginx  --dry-run=client -o yaml`

* Create a deployment: `kubectl create deployment --image=nginx nginx`

* Generate Deployment YAML file (-o yaml). Don't create it(--dry-run): `kubectl create deployment --image=nginx nginx --dry-run=client -o yaml`

* `kubectl create deployment` does not have a `--replicas` option. You could first create it and then scale it using the `kubectl scale deployment <deployment-name> --replicas=<count>` command

* Save it to a file - (If you need to modify or add some other details): `kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml`. You can then update the YAML file with the replicas or any other field before creating the deployment.

* Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379: `kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml`. (This will automatically use the pod's labels as selectors) OR `kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml` (This will not use the pods labels as selectors, instead it will assume selectors as app=redis. You cannot pass in selectors as an option. So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service)

* Create a Service named nginx of type NodePort to expose pod nginx's port 80 on port 30080 on the nodes: `kubectl expose pod nginx --port=80 --name nginx-service --type=NodePort --dry-run=client -o yaml`
  (This will automatically use the pod's labels as selectors, but you cannot specify the node port. You have to generate a definition file and then add the node port in manually before creating the service with the pod.) OR `kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml` (This will not use the pods labels as selectors). Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. I would recommend going with the `kubectl expose` command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service

Reference: [https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)


**Declarative Approach**

* For creating objects everytime, use this command `kubectl apply -f nginx.yml`
* For updating objects everytime, use this command `kubectl apply -f nginx.yml`



 


 
 
# IMPORTANT COMMANDS

To modify the existing replicasets image use `kubectl edit replicaset replicaset-name` command. Modify the image name and then save the file.