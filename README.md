# run
```bash
apt-get update
apt-get install git podman

git clone https://github.com/start-from-scratch/pixelbot

podman build -t pixelbot pixelbot
podman run --name pixelbot -d pixelbot
```
