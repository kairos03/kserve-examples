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

```
kubectl apply -f inferenceservice.yaml
```

```
kubectl get isvc

NAME           URL                                       READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                    AGE
onnx-cifar10   http://onnx-cifar10.omnious.example.com   True           100                              onnx-cifar10-predictor-default-00001   1m
```

