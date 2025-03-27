ENV=.env
DOCKER_IMAGE=davideponzini/lensql

.PHONY: run build

run: build
	docker run --rm -p 8888:8888 $(DOCKER_IMAGE)

rund: build
	docker run -d -p 8888:8888 $(DOCKER_IMAGE)

build:
	docker build -t $(DOCKER_IMAGE) .

$(ENV):
	cp $(ENV).template $(ENV)


