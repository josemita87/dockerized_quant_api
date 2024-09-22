
build:
	docker build --progress=plain -t quant_api .

run: 
	docker run -it --network redpanda_network --rm -p 8001:8001 --name quant_api quant_api

	