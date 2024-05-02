build-image:
    docker build -t youtube-api-job .

build-container:
    docker run -it -p 8080:8080 youtube-api-job

docker-clean:

    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)


test-service:
    curl -X GET http://0.0.0.0:8080/trigger-youtube-api-job

tag_image:
    docker buildx build --platform linux/amd64 -t youtube-api-job .

    docker tag 0c8efe59de48 europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos

    docker push europe-west9-docker.pkg.dev/maximal-ship-421811/epita-tp1-muchachos

    gcloud auth configure-docker europe-west9-docker.pkg.dev --quiet