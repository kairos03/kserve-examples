# sklearn iris classifier

This examele deploy sklearn iris classifier model to kubeflow dex base kserve as a inference services.

check files:
```
sklearn-iris
├ sklearn-iris.yaml       : Kserve InferenceService yaml file
├ iris-input.json         : example input file
├ predict.sh              : shell script example
├ kserve-dex-iris.py      : python example
```

## prerequisites
- set kube-config in your `~/.kube` directory
- kserve is deployed with kubeflow multi-user mode(dex)

## 1. Deploy model
```sh
kubectl apply -f sklearn-iris.yaml
```

## 2. Check model deployed
```sh
kubectl get isvc sklearn

NAMESPACE   NAME                URL                                            READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                         AGE
admin       sklearn-iris        http://sklearn-iris.admin.example.com          True           100                              sklearn-iris-predictor-default-00001        116s
```

## 3. run predict.sh
before you run this shell script, you need `authsession` data. please follow [this](https://github.com/kserve/kserve/tree/master/docs/samples/istio-dex) and replace `SESSION` variable.

set your `INGRESS_HOST` and `INGRESS_PORT`. If you using port-forwarding using port 8080 then set `localhost` and `8080` respectively.

set `NAMESPACE` that your model is deployed.

run predict.sh

```sh
./predict.sh
```

## 4. run python client
You can use python client for request prediction.
This code contain get authsession so it is more convinient.

Before run `predict.py` install `kserve-==0.7.0`.

Edit `predict.py` file. Set `HOST`, `USERNAME`, and `PASSWORD`.

Then run:
```sh
python predict.py
```
