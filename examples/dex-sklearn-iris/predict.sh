# get authsession cookie. check this https://github.com/kserve/kserve/tree/master/docs/samples/istio-dex
SESSION=<YOUR DATA>

# ingress host and port
INGRESS_HOST=localhost
INGRESS_PORT=8080
NAMESPACE=<YOUR NAMESPACE>

# inference service hostname
SERVICE_HOSTNAME=$(kubectl get isvc sklearn-iris -n ${NAMESPACE} -o jsonpath='{.status.url}' | cut -d "/" -f 3)

# request prediction
curl -v -H "Cookie: authservice_session=${SESSION}" -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/sklearn-iris:predict -d @./iris-input.json
