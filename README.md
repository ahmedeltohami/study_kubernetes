إحنا الأساس كان عندنا الـ Flask app (Bee Quotes) شغال عادي على Docker، لكن الخطوة الجديدة كانت إننا ننقله من بيئة Docker محلية لبيئة Kubernetes.

الزيادة اللي حصلت كانت:

عملنا Deployment علشان Kubernetes يدير الـ Pods ويضمن تكرار وتشغيل التطبيق أوتوماتيك.

عملنا Service علشان نوفر طريقة ثابتة للوصول للتطبيق داخل الكلاستر أو من بره.

جربنا طرق الوصول المختلفة (NodePort، minikube service، و kubectl port-forward).

تعاملنا مع مشاكل واقعية بتحصل في Kubernetes (زي NodePort unreachable أو مشاكل سحب الصورة من Docker Hub).

يعني الدرس هنا كان مش كتابة الكود، لكن إزاي نشرحه ونديره على Kubernetes بدل ما يفضل شغال في Container واحد بس.

1) هيكل المشروع
css
Copy
Edit
bee-quotes-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── deployment.yaml
└── service.yaml
2) محتوى الملفات (انسخهم كما هم)
app.py
python
Copy
Edit
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
    })

if __name__ == '__main__':
    # التطبيق يستمع داخل الحاوية على 5050
    app.run(host='0.0.0.0', port=5050)
شرح:

host='0.0.0.0' مهم عشان الحاوية تسمع على كل الواجهات داخل الـ container.

port=5050 هو البورت الداخلي (نستخدمه لاحقًا كـ containerPort).

requirements.txt
nginx
Copy
Edit
flask
شرح: ملف التبعية لبناء الصورة.

Dockerfile (محسّن وخفيف)
Dockerfile
Copy
Edit
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تثبيت gcc إن احتاجت مكتبات تبني extensions (لو مش محتاج ممكن ترفعه)
RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
شرح أسطر مهمة:

--allow-releaseinfo-change حل لمشاكل apt-release إذا كان توقيت النظام غير متزامن.

--no-cache-dir يقلل حجم الصورة أثناء pip install.

docker-compose.yml (لتشغيل محلي سريع)
yaml
Copy
Edit
services:
  web:
    build: .
    ports:
      - "5055:5050"   # 5055 على الجهاز -> 5050 داخل الحاوية
    container_name: bee-quotes-app-web
شرح: تشغل service محلياً، ركبنا الـ host port 5055 لتفادي تعارضات سابقة.

deployment.yaml (K8s Deployment)
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
شرح:

replicas: عدد الـ pods.

image: صورة Docker على Docker Hub.

containerPort: يجب أن يطابق app.py (5050).

service.yaml (K8s Service — NodePort)
yaml
Copy
Edit
apiVersion: v1
kind: Service
metadata:
  name: bee-quotes-service
spec:
  selector:
    app: bee-quotes
  ports:
    - protocol: TCP
      port: 80         # البورت اللي داخل الكلاستر (Service)
      targetPort: 5050 # البورت داخل الـ Pod
  type: NodePort
شرح:

port: 80 هو بورت الـ Service داخل الكلاستر.

targetPort: 5050 يوجه للـ container.

type: NodePort يجعل الخدمة متاحة من نود الكلاستر عبر رقم NodePort (مثلاً 30095).

3) أوامر التشغيل خطوة بخطوة
محلي (Docker Compose)
bash
Copy
Edit
# بناء وتشغيل (يعرض اللوقات)
docker compose up --build

# أو تشغيل في الخلفية
docker compose up -d
افتح المتصفح على: http://<VM_or_local_IP>:5055

بناء الصورة ورفعها على Docker Hub
bash
Copy
Edit
# 1. بناء محلي
docker build -t bee-quotes-app .

# 2. تاغ باسم حسابك على Hub
docker tag bee-quotes-app eltohami/bee-quotes-app:v1

# 3. تسجيل دخول
docker login

# 4. رفع الصورة
docker push eltohami/bee-quotes-app:v1
لو رفع من VM بطيء/يفصل — بديل (save → نقل → load → push)
على الـ VM:

bash
Copy
Edit
docker save -o bee-quotes-app.tar eltohami/bee-quotes-app:v1
# انسخ bee-quotes-app.tar إلى جهاز Windows عبر MobaXterm (drag & drop)
على Windows:

powershell
Copy
Edit
docker load -i C:\path\to\bee-quotes-app.tar
docker login
docker push eltohami/bee-quotes-app:v1
نشر على Kubernetes (Minikube)
bash
Copy
Edit
minikube start          # لو مش شغال
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
الوصول إلى الخدمة (طرق)
minikube service (سريع لو تستخدم minikube):

bash
Copy
Edit
minikube service bee-quotes-service --url
# يطبع رابط مثل http://192.168.49.2:30095
port-forward (آمن وسريع محلياً):

bash
Copy
Edit
# على الجهاز الذي يعمل kubectl (الـ VM في حالتنا):
kubectl port-forward service/bee-quotes-service 9090:80 --address=0.0.0.0
# افتح من متصفح Windows:
http://192.168.2.110:9090   # IP الماكينة التي تعمل Minikube/VM
LoadBalancer + minikube tunnel (لـ IP خارجي ثابت):

غيّر Service إلى type: LoadBalancer ثم شغّل:

bash
Copy
Edit
minikube tunnel
kubectl apply -f service-loadbalancer.yaml
4) أوامر فحص مهمة ومشاكل شائعة وحلولها
حالة البود / لوقاته
bash
Copy
Edit
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
ErrImagePull / ImagePullBackOff
تأكد أن الصورة موجودة على Docker Hub بالاسم الصحيح.

إذا الصورة private: أنشئ secret واربطة في الـ Deployment:

bash
Copy
Edit
kubectl create secret docker-registry regcred \
  --docker-username=eltohami --docker-password=<TOKEN_OR_PASSWORD> --docker-email=you@example.com

# ثم في deployment.spec.template.spec:
imagePullSecrets:
  - name: regcred
unauthorized: authentication required عند push
شغّل docker login واستخدم الباسورد أو Access Token من Docker Hub.

Release file ... invalid yet أثناء apt-get update
ضبط التاريخ/الـ NTP:

bash
Copy
Edit
sudo timedatectl set-ntp true
# أو اضبط التاريخ يدويا:
sudo date -s "2025-07-30 12:00:00"
أو استخدم --allow-releaseinfo-change كما في Dockerfile.

Port conflicts / Bind failed
شغل docker ps وsudo lsof -i :<port> أو ss -tulnp | grep <port> لمعرفة من يستخدم البورت.

إما توقف الـ container أو غيّر ربط الـ ports في docker-compose.yml.

الشبكة وMinikube الوصول من Windows
Minikube غالبًا يقيم شبكة داخلية (مثل 192.168.49.x) — قد لا تكون قابلة للوصول مباشرة من جهازك host.

أسرع حل: kubectl port-forward ... --address=0.0.0.0 (ثم افتح IP الماكينة + البورت الذي اخترته).

أو إعداد الشبكة (Bridged) أو استخدام minikube tunnel.

5) README جاهز للـ GitHub (مقتطف تضعه في repo)
markdown
Copy
Edit
# Bee Quotes App (Flask + Docker + Kubernetes)

Simple Flask API returning a motivational quote, containerized with Docker, deployable to Kubernetes (Minikube).

## Files
- `app.py`      : Flask app
- `Dockerfile`  : Build image
- `docker-compose.yml` : Local dev
- `deployment.yaml` : Kubernetes Deployment
- `service.yaml`    : Kubernetes Service (NodePort)

## Run locally with Docker Compose
```bash
docker compose up --build
# open http://localhost:5055
Build & push image
bash
Copy
Edit
docker build -t bee-quotes-app .
docker tag bee-quotes-app eltohami/bee-quotes-app:v1
docker login
docker push eltohami/bee-quotes-app:v1
Deploy to Kubernetes (Minikube)
bash
Copy
Edit
minikube start
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
# access:
minikube service bee-quotes-service --url
# or
kubectl port-forward service/bee-quotes-service 9090:80 --address=0.0.0.0
