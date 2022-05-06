# deploy custom model 

## Prerequisites
- Kserve and Kubeflow with istio
- PV or Storeage Class with Dynamic PV provisoner

## Create PVC
create pvc for store model
```
kubectl apply -f pvc.yaml
```

create copy pod to copy model into pvc and enter created pod.
```
kubectl apply -f copy-pod.yaml

kubectl exec -it model-store-pod -- bash
```

In other terminal, copy model
```
kubectl cp cifar model-store-pod:/cifar -c model-store
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

