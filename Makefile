# Build the image
build-image:
	docker-compose build

# Build and run the container locally
build-container:
	docker-compose up -d

# Stop all running containers
docker-stop:
	docker stop $$(docker ps -a -q)

# Remove all containers
docker-clean:
	docker rm $$(docker ps -a -q)

docker-run-api:
	docker-compose run youtube-data-retrieval python main.py

docker-run-processing:
	docker-compose run youtube-data-processing python main.py

# Tag and push the Docker image to the Google Cloud Registry
tag_image_retrevial:
	# Assuming youtube-data-retrieval service is the main service to be pushed
	docker tag iaas-cloud-youtube-data-retrieval:latest europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos/youtube-api-job
	gcloud auth configure-docker europe-west9-docker.pkg.dev --quiet
	docker push europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos/youtube-api-job

tag_image_processing:
	# Assuming youtube-data-processing service is the main service to be pushed
	docker tag iaas-cloud-youtube-data-processing:latest europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos/youtube-api-job
	gcloud auth configure-docker europe-west9-docker.pkg.dev --quiet
	docker push europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos/youtube-api-job

connection_database:
	docker-compose exec db psql -U postgres -d youtube_data


# Clean up local files
clean:
	rm -rf __pycache__ local_storage celerybeat-schedule
