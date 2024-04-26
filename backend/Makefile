# 定数
GCP_PROJECT=geekcamp2024-vol4-topaz
GCP_REGION=asia-northeast1
GCP_SERVICE=app

deploy:
	gcloud run deploy ${GCP_SERVICE} \
		--project ${GCP_PROJECT} \
		--region ${GCP_REGION} \
		--allow-unauthenticated \
		--source .