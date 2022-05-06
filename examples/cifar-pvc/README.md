# Deploy pytorch model with PVC

## Prerequisites
- Kserve and Kubeflow with istio
- PV or Storeage Class with Dynamic PV provisoner

## Download model and convert to onnx
We need to convert torch `pth` to `onnx` format.
Run `prepare_model.py`.

```sh
python prepare_model.py
```

## Create PVC and copy model
create pvc for store model
```
kubectl apply -f pvc.yaml
```

create copy pod to copy model into pvc and enter created pod.
```
kubectl apply -f copy-pod.yaml

kubectl exec -it model-store-pod -- bash
```

In other terminal, copy model into pvc via model-store-pod.
```
kubectl cp cifar model-store-pod:/cifar -c model-store
```

In model-store-pod, check model is copied.
```
ls /models

cifar
```

## Create inference service
apply inferenceserver 
```
kubectl apply -f inferenceservice.yaml
```

Check Inference server is runnning. It may takes a few minute.
```
kubectl get isvc

NAME           URL                                       READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                    AGE
onnx-cifar10   http://onnx-cifar10.omnious.example.com   True           100                              onnx-cifar10-predictor-default-00001   1m
```

## 