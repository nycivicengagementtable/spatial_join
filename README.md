# Spatial Join

## Running locally

1. Install Docker.
1. Run the application.

    ```sh
    docker build -t spatial_join . && docker run -it -p 8000:8000 spatial_join
    ```

1. Open http://localhost:8000.

## Running tests

```sh
docker build -t spatial_join . && docker run -it spatial_join pytest -v
```
