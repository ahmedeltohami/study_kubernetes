# Bee Quotes App on Kubernetes

## 📌 Overview
هذا المشروع يوضح كيفية تشغيل تطبيق Flask بسيط (Bee Quotes App) على Kubernetes باستخدام Minikube.  
الغرض من المشروع هو التعلم العملي على:

- بناء تطبيق Python + Flask  
- تحويله لـ Docker Image  
- رفع الصورة على DockerHub  
- تشغيله على Kubernetes (Minikube)  

---

## 📂 Project Structure
.
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
└── README.md



---

## 🐍 1. Application File (app.py)
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
شرح الملف:

الكود الرئيسي للتطبيق.

بيستخدم Flask لعمل Web Server بسيط.

Route / بيرجع رسالة JSON فيها Quote عن النحل.

التطبيق بيشتغل على البورت 5050 داخل الكونتينر.
____________________________________________________________________________________
📦 2. Requirements File (requirements.txt)
flask
شرح الملف:

بيحتوي على المكتبات المطلوبة لتشغيل البرنامج.

Docker بيقرأ الملف ويعمل pip install لكل المكتبات المذكورة.
______________________________________________________________________________________
📄 3. Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
شرح الملف:

FROM python:3.9-slim → نسخة Python خفيفة.

WORKDIR /app → تحديد فولدر العمل داخل الكونتينر.

COPY requirements.txt . → نسخ ملف المتطلبات.

RUN pip install → تثبيت المكتبات.

COPY . . → نسخ باقي ملفات المشروع.

CMD ["python", "app.py"] → تشغيل التطبيق.

🛠️ 4. Build & Push Docker Image
bash
Copy
Edit
docker build -t eltohami/bee-quotes-app:v1 .
docker login
docker push eltohami/bee-quotes-app:v1
شرح الخطوات:

docker build → بناء صورة Docker من الـDockerfile.

docker login → تسجيل الدخول في DockerHub.

docker push → رفع الصورة إلى DockerHub.
__________________________________________________________________________-
📄 5. Kubernetes Deployment File (deployment.yaml)

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
شرح الملف:

Deployment → لتشغيل وإدارة البودز.

replicas: 1 → نسخة واحدة من التطبيق.

image → صورة Docker المرفوعة على DockerHub.

containerPort: 5050 → البورت داخل الكونتينر.
___________________________________________________________________________
📄 6. Kubernetes Service File (service.yaml)

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
شرح الملف:

Service → وسيط للوصول للتطبيق.

type: NodePort → يجعل التطبيق متاح على IP النود وبورت خارجي.

port: 80 → البورت داخل الكلاستر.

targetPort: 5050 → البورت داخل الكونتينر.

nodePort: 30095 → البورت الخارجي للوصول للتطبيق.
__________________________________________________________________
🚀 7. Apply Kubernetes Files

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
شرح الخطوات:

إنشاء Deployment و Service في Kubernetes.

التأكد أن البودز والخدمات اشتغلت.
__________________________________________________________
📡 8. Access the App
عن طريق Minikube:

minikube service bee-quotes-service --url
أو عن طريق Port Forward:


kubectl port-forward service/bee-quotes-service 5080:80 --address=0.0.0.0
🐝 Expected Output
{
  "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
}
________________________________
📝 Notes
يجب تشغيل Minikube قبل تنفيذ الأوامر.

يجب رفع صورة Docker على DockerHub.

يمكن استخدام Port-Forward إذا كان NodePort لا يعمل.
