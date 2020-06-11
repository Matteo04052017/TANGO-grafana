# TANGO-grafana
An investigations on the modifiability of Prometheus and grafana in a TANGO-controls context

# run on Kubernetes 
helm install tango-grafana0 helm-chart/


---
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-provisioning-dashboards
  namespace: {{ .Release.Namespace }}
data: 
  archiver.json: |-  
{{ .Files.Get "data/dashboards/archiver.json" | indent 2  }}
  dashboard.json: |-
{{ .Files.Get "data/dashboards/dashboard.json" | indent 2  }}
  db.json: |-
{{ .Files.Get "data/dashboards/db.json" | indent 2 }}
  state.json: |- 
{{ .Files.Get "data/dashboards/state.json" | indent 2 }}