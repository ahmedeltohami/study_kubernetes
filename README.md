# Bee Quotes App on Kubernetes

## 📌 Overview
هذا المشروع يوضح كيفية تشغيل تطبيق Flask بسيط (Bee Quotes App) على Kubernetes باستخدام Minikube.

---

## 📂 Project Structure

.
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
└── README.md

yaml
Copy
Edit

---

## 🐍 1. Application File (`app.py`)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def bee_quote():
    return jsonify({
        "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
📦 2. Requirements File (requirements.txt)
nginx
Copy
Edit
flask
📄 3. Dockerfile
dockerfile
Copy
Edit
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
🛠️ 4. Build & Push Docker Image
Build the image
bash
Copy
Edit
docker build -t eltohami/bee-quotes-app:v1 .
Login to DockerHub
bash
Copy
Edit
docker login
Push to DockerHub
bash
Copy
Edit
docker push eltohami/bee-quotes-app:v1
📄 5. Kubernetes Deployment File (deployment.yaml)
yaml
Copy
Edit
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bee-quotes-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bee-quotes
  template:
    metadata:
      labels:
        app: bee-quotes
    spec:
      containers:
      - name: bee-quotes-container
        image: eltohami/bee-quotes-app:v1
        ports:
        - containerPort: 5050
📄 6. Kubernetes Service File (service.yaml)
yaml
Copy
Edit
apiVersion: v1
kind: Service
metadata:
  name: bee-quotes-service
spec:
  type: NodePort
  selector:
    app: bee-quotes
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5050
      nodePort: 30095
🚀 7. Apply Kubernetes Files
bash
Copy
Edit
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
📡 8. Access the App
Get service URL
bash
Copy
Edit
minikube service bee-quotes-service --url
Example Output:

cpp
Copy
Edit
http://192.168.49.2:30095
OR use port-forward
bash
Copy
Edit
kubectl port-forward service/bee-quotes-service 5080:80 --address=0.0.0.0
Then access:

cpp
Copy
Edit
http://<your-ip>:5080
✅ 9. Testing from inside Minikube
If the app doesn't open from your machine, test it inside Minikube:

bash
Copy
Edit
minikube ssh
curl http://127.0.0.1:30095
🐝 Expected Output
json
Copy
Edit
{
  "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
}
