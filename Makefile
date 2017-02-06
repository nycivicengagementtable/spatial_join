IMAGE=spatial_join
PORT=8000

all: run

build:
	docker build -t $(IMAGE) .

run: build
	docker run -it -p $(PORT):$(PORT) -e PORT=$(PORT) $(IMAGE)

test: build
	docker run -it $(IMAGE) pytest -v
