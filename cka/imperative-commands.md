# Imperative and Declarative Approach

**Imperative Approach Kubernetes Commands for Exam Prepartions:**

**Deployments**
```bash
kubectl run --image=nginx nginx
kubectl run nginx --image=nginx --dry-run=client -o yaml   ##Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)
kubectl create deployment --image=nginx nginx --namespace=<namespace-name>
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml  # Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)
kubectl expose deployment nginx --port 80
kubectl edit deployment nginx  # Edit command modifies the current state of the kubernetes resources, not the definition yaml files.
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml  #Generate Deployment YAML file (-o yaml). Don't create it(--dry-run) with 4 Replicas (--replicas=4)
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


**ReplicaSets**
```bash
kubectl scale --replicas=6 -f replicaset-definition.yml
kubectl scale --replicas=6 replicaset myapp-replicaset
kubectl create -f replicaset-definition.yml
kubectl get replicaset
kubectl delete replicaset myapp-replicaset
kubectl replace -f replicaset-definition.yml
kubectl scale -replicas=6 -f replicaset-definition.yml
```

**Namespace**

```bash
kubectl create namespace <namespace-name>
kubectl config set-context $(kubectl config current-context) --namespace=dev   #set the default namespace as dev
```


Reference: [https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)



**Declarative Approach**

* For creating objects everytime, use this command `kubectl apply -f nginx.yml`
* For updating objects everytime, use this command `kubectl apply -f nginx.yml`
