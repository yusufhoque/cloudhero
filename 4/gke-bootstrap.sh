#!/bin/sh
gcloud auth login --project=$1
gcloud config set compute/zone us-central1-a
gcloud container clusters create bootcamp --num-nodes 5 --scopes "https://www.googleapis.com/auth/projecthosting,storage-rw"
gcloud container clusters get-credentials bootcamp
kubectl create secret generic tls-certs --from-file tls/
kubectl create configmap nginx-frontend-conf --from-file=nginx/frontend.conf
kubectl apply -f deployments/
kubectl apply -f services/
