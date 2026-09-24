# Elasticsearch on Docker (Single-Node Cluster)

Quick setup for running a single-node Elasticsearch cluster in Docker, suitable for local development and testing.

## Prerequisites

- Docker installed and running
- At least 2GB of free RAM available to Docker


## Python Client Setup (Conda Environment)

If you want to query Elasticsearch from Python, create a dedicated conda environment:

​```bash
conda create -n elasticsearch python=3.11 -y 
conda activate elasticsearch
pip install elasticsearch
​```

Quick connection test:

​```python
    
    from elasticsearch import Elasticsearch

    es = Elasticsearch("http://localhost:9200")
    print(es.info())
​```

To remove the environment later:

​```bash
conda deactivate
conda env remove -n elasticsearch
​```

## Elastisearch Setup

```bash
# Pull the image
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.15.0

# Network + volume for persistence
docker network create es-net
docker volume create es-data

# Run single-node Elasticsearch
docker run -d \
  --name elasticsearch \
  --net es-net \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  -v es-data:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.0

# Watch it boot
docker logs -f elasticsearch
```

Wait for a "started" message in the logs, then `Ctrl+C` to stop tailing.

## Verify It's Running

```bash
curl http://localhost:9200
curl http://localhost:9200/_cluster/health?pretty
```

A `"status": "yellow"` in the health check is normal for a single-node cluster — it just means there's no second node to hold replica shards. `"status": "green"` would require additional nodes.

## Stopping / Starting

```bash
# Stop the container (data is preserved in the es-data volume)
docker stop elasticsearch

# Start it again later
docker start elasticsearch

# Stop AND remove the container (still keeps the volume/data)
docker stop elasticsearch && docker rm elasticsearch

# If you also want to wipe the data itself
docker volume rm es-data
```

A normal shutdown is just `docker stop elasticsearch` — the container and its data stay intact until you run `docker start elasticsearch` again.

## Troubleshooting

**Container exits immediately with `vm.max_map_count [65530] is too low`:**

Run this on the Docker host, then restart the container:

```bash
sudo sysctl -w vm.max_map_count=262144
```

**Security is enabled and you're locked out:**

This setup disables security (`xpack.security.enabled=false`) for local testing convenience. If you remove that flag, Elasticsearch enables TLS and password auth by default. The auto-generated `elastic` user password is printed in the startup logs, or you can reset it with:

```bash
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

With security enabled, all `curl` commands need `-u elastic:<password>`.

## Notes

- Check [elastic.co](https://www.elastic.co/downloads/elasticsearch) for the latest version tag if you want a newer release than `8.15.0`.
- `xpack.security.enabled=false` is fine for local/dev use. Enable security for anything shared or production-facing.