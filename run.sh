# !/bin/bash

sudo docker build -t plant_disease . && sudo docker run --name container_plant_disease -p 8000:8000 plant_disease
