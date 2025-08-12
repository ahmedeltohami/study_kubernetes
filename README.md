# Bee Quotes App on Kubernetes

## 📌 Overview
هذا المشروع يوضح كيفية تشغيل تطبيق Flask بسيط (Bee Quotes App) على Kubernetes باستخدام Minikube.  
الغرض من المشروع هو التعلم العملي على:
- **بناء تطبيق Python + Flask**
- **تحويله لـ Docker Image**
- **رفع الصورة على DockerHub**
- **تشغيله على Kubernetes (Minikube)**

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
شرح الملف:

ده هو الكود الرئيسي للتطبيق.

بيستخدم مكتبة Flask لعمل Web Server بسيط.

فيه Route / بيرجع رسالة JSON فيها Quote عن النحل.

بيشتغل على الـPort 5050 جوه الكونتينر.

📦 2. Requirements File (requirements.txt)
nginx
Copy
Edit
flask
شرح الملف:

بيحتوي على المكتبات المطلوبة لتشغيل البرنامج.

Docker بيقرأ الملف ده ويعمل pip install لكل المكتبات المذكورة فيه.

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
شرح الملف:

FROM python:3.9-slim → بيستخدم نسخة Python خفيفة.

WORKDIR /app → بيحدد فولدر العمل داخل الكونتينر.

COPY requirements.txt . → نسخ ملف المتطلبات.

RUN pip install → تثبيت المكتبات.

COPY . . → نسخ باقي ملفات المشروع.

CMD ["python", "app.py"] → تشغيل التطبيق.

🛠️ 4. Build & Push Docker Image
الأوامر:

bash
Copy
Edit
docker build -t eltohami/bee-quotes-app:v1 .
docker login
docker push eltohami/bee-quotes-app:v1
شرح الخطوات:

docker build → يبني صورة Docker من الـDockerfile.

docker login → تسجيل الدخول في DockerHub.

docker push → رفع الصورة لـDockerHub.

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
شرح الملف:

Deployment → نوع الـObject في Kubernetes لتشغيل وإدارة البودز.

replicas: 1 → يشغل نسخة واحدة من التطبيق.

image → اسم صورة Docker اللي رفعناها على DockerHub.

containerPort: 5050 → البورت اللي بيسمع عليه التطبيق داخل الكونتينر.

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
شرح الملف:

Service → بيعمل وسيط للوصول للتطبيق.

type: NodePort → بيخلي التطبيق متاح على أي IP للـNode مع بورت خارجي.

port: 80 → البورت اللي هيشتغل جوا الكلاستر.

targetPort: 5050 → البورت داخل الكونتينر.

nodePort: 30095 → البورت الخارجي اللي نقدر نستخدمه للوصول للتطبيق.

🚀 7. Apply Kubernetes Files
bash
Copy
Edit
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
شرح الخطوات:

بتنشيء Deployment وService في Kubernetes.

بيتأكد إن البودز والخدمات اشتغلت.

📡 8. Access the App
عن طريق Minikube:

bash
Copy
Edit
minikube service bee-quotes-service --url
أو عن طريق Port Forward:

bash
Copy
Edit
kubectl port-forward service/bee-quotes-service 5080:80 --address=0.0.0.0
🐝 Expected Output
json
Copy
Edit
{
  "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
}
📝 Notes
لازم Minikube يكون شغال قبل تنفيذ الأوامر.

لازم صورة Docker تكون مرفوعة على DockerHub.

ممكن تستخدم Port-Forward كحل بديل لو NodePort مش شغال.

