# quizapp-using-AKS

kubectl apply -f k8s/base/secret.yaml
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/pvc-static.yaml
kubectl apply -f k8s/base/pvc-media.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/quiz-service.yaml
kubectl apply -f k8s/base/ingress.yaml
