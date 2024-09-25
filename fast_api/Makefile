
build:
	docker build -t quant_api .
#In the run command, beware we change the port to internal, so we can access the cluster from docker.
run: 
	docker run \
	-it --network redpanda_network \
	--env KAFKA_BROKER_ADDRESS=redpanda-0:9092\
	--rm -p 8001:8001 \
	--name quant_api quant_api

	