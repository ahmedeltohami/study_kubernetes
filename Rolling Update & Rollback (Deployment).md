🎯 هدف التاسك:

تتعلم إزاي تعمل تحديث تدريجي (Rolling Update) للـ Deployment بدون توقف الخدمة،
وإزاي تعمل Rollback لو التحديث فشل.
_______________

🧩 التاسك العملي
📝 1. أنشئ Deployment جديد:

اكتب في ملف اسمه: 
    
    nginx-update.yaml

الكود: 

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx-update
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx-update
      template:
        metadata:
          labels:
            app: nginx-update
        spec:
          containers:
            - name: nginx
              image: nginx:1.23
              ports:
                - containerPort: 80

_________________
🚀 2. طبّق الـ Deployment: 

    kubectl apply -f nginx-update.yaml
_______________
تأكد إن البودات شغالة: 
    
    kubectl get pods -l app=nginx-update
_______________
🔁 3. اعمل Rolling Update لإصدار أحدث من nginx

هنغيّر الـ image إلى nginx:1.25 
     
     kubectl set image deployment/nginx-update nginx=nginx:1.25 --record

تابع التحديث أثناء ما بيحصل: 

     kubectl rollout status deployment/nginx-update

هتشوف حاجة زي:

     deployment "nginx-update" successfully rolled out
 __________________
 🔍 4. تأكد من التحديث 

      kubectl get pods -l app=nginx-update -o wide

وشوف أسماء البودات الجديدة (هتلاحظ إنها مختلفة عن القديمة).
كمان جرب تشوف الإصدار داخل واحدة من البودات:

      kubectl exec -it <pod-name> -- nginx -v
____________________
💥 5. جرب تحديث خاطئ (عشان نجرب Rollback)

اعمل تحديث بصورة غير موجودة مثل:
      
      kubectl set image deployment/nginx-update nginx=nginx:9.99 --record

تابع:

      kubectl rollout status deployment/nginx-update

هتلاحظ إنها فشلت أو معلّقة لأن الصورة غير موجودة.
____________________
🔄 6. نفذ Rollback 

      kubectl rollout undo deployment/nginx-update

راجع الحالة بعد الرجوع: 

      kubectl rollout history deployment/nginx-update
وهتلاقيه رجع للإصدار السابق (nginx:1.25).
____________________
🧠 ملخص سريع:
| الأمر                     | الوظيفة                                 |
| ------------------------- | --------------------------------------- |
| `kubectl set image`       | لتغيير صورة الـ container أثناء التشغيل |
| `kubectl rollout status`  | لمتابعة التحديث أثناء حصوله             |
| `kubectl rollout undo`    | للرجوع إلى الإصدار السابق               |
| `kubectl rollout history` | لعرض سجل التحديثات السابقة              |
