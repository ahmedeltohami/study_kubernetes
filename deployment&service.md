🎯 تاسك 3: إنشاء Deployment يحتوي على 3 Pods من nginx + عمل Service للوصول إليهم
✅ المطلوب منك تنفيذه:

1-أنشئ Deployment اسمه nginx-deploy فيه:

3 replicas (يعني 3 نسخ من نفس
الـ Pod).

كل Pod فيه container واحد اسمه nginx 
يستخدم الصورة nginx:latest.

يكون عند كل Pod label app: nginx.

2-أنشئ Service من النوع ClusterIP (الافتراضي) اسمه nginx-service:

يربط الـ Pods اللي عندها label app: nginx.

يفتح البورت 80.

3-تأكد إن الـ Pods فعلاً شغالة، وإن الـ Serviceشايفهم.
__________________________



حلّ التاسك 3 — Deployment (3 replicas) + Service (ClusterIP) بالتفصيل خطوة-بخطوة

انسخ الـ YAML ده في ملف واحد (مثلاً اسمه nginx-deploy-svc.yaml) ثم أطبّقه على الكلاستر. بعده هشرح كل سطر، وهديك أوامر التحقق وطُرُق الوصول والتعديلات الشائعة.

    # nginx-deploy-svc.yaml
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
     name: nginx-deploy
     labels:
      app: nginx
    spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx
      template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
          - name: nginx
            image: nginx:latest
            ports:
              - containerPort: 80
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: nginx-service
    spec:
      selector:
        app: nginx
    ports:
      - protocol: TCP
        port: 80         # بورت داخل الـ Service (ClusterIP)
        targetPort: 80   # البورت داخل الـ Pod (containerPort)
    type: ClusterIP


    
  شرح الـ YAML سطر بسطر (مهم جداً)
القسم الأول — Deployment

apiVersion: apps/v1
نستخدم apps/v1 لأن Deployment هو جزء من مجموعة الـ apps في API.

kind: Deployment
نوع المورد: Deployment يدير ReplicaSets و Pods.

metadata.name: nginx-deploy
اسم الـ Deployment.

labels: app: nginx
وسم عام نستخدمه للبحث والتنظيم.

spec.replicas: 3
نطلب تشغيل 3 نسخ من الـ Pod.

spec.selector.matchLabels
يحدد كيف الـ Deployment يختار الـ Pods التي يديرها — يجب أن يطابق template.metadata.labels.

template:
قالب الـ Pod الذي سيُنشأ: فيه metadata.labels وspec.containers.

containers:
نعرّف الحاوية nginx، الصورة nginx:latest، ونعّرف containerPort: 80.

القسم الثاني — Service

kind: Service و apiVersion: v1
Service يوفّر عنوان ثابت للوصول لمجموعة من الـ Pods.

metadata.name: nginx-service
اسم الـ Service.

spec.selector: app: nginx
يربط الـ Service بكل الـ Pods التي تحمل label: app=nginx.

ports:

port: 80 → البورت الذي يقدمه Service داخل الكلستر (ClusterIP).

targetPort: 80 → البورت داخل الـ Pod الذي سيرسل له الترافيك.

type: ClusterIP
الافتراضي؛ Service داخل الكلاستر فقط. (للوصول من outside ستستخدم port-forward أو NodePort/LoadBalancer

أوامر التطبيق والتحقّق (نفّذهم خطوة خطوة)

 1-طبّق الملف:

    kubectl apply -f nginx-deploy-svc.yaml

2-تأكّد من وجود الـ Deployment:

    kubectl get deployments
    # expected: nginx-deploy   3/3   ...

3-اعرض الـ ReplicaSet و Pods:

    kubectl get rs
    kubectl get pods -l app=nginx -o wide

4-تأكّد من حالة الـ Pods (يجب تكون Ready):

    kubectl get pods

5-اعرض الـ Service:

    kubectl get svc nginx-service
# يعرض ClusterIP و port

6-تفصيل (describe) لمزيد من المعلومات:


    kubectl describe deployment nginx-deploy
    kubectl describe svc nginx-service
    kubectl describe pod <pod-name>

7-تفحص الـ endpoints اللي يربطهم الـ Service:

    kubectl get endpoints nginx-service
___________________
الوصول إلى التطبيق (ClusterIP) — طريقتان عمليتان
أ) أسهل طريقة أثناء التعلم: port-forward من الـ Service إلى الماكين/لوكالهوست
  
    kubectl port-forward service/nginx-service 8080:80
# الآن افتح: http://localhost:8080
# أو: curl http://localhost:8080
هذا يعيد توجيه بورت 8080 على جهازك إلى بورت 80 داخل الـ Service داخل الكلاستر.
__
ب) بديل: استخدم NodePort (إذا أردت أن يكون متاح من كل Nodes دون port-forward)
غير النوع إلى NodePort أو أنشئ Service جديد من نوع NodePort.
مثال سريع:

    kubectl expose deployment nginx-deploy --type=NodePort --name=nginx-nodeport --port=80
    kubectl get svc nginx-nodeport
# شاهد قيمة nodePort (مثلاً 30080) ثم افتح http://<node-ip>:30080
