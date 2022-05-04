## deploy custom model 

```
kubectl apply -f pvc.yaml
```

```
kubectl apply -f copy-pod.yaml

kubectl exec -it model-store-pod -- bash
```

```
kubectl cp cifar model-store-pod:/models -c model-store
```

```
ls /model
```

