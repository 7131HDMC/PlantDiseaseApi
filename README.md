## PlantDiseaseHD API
This is an application that employs a custom machine learning model, utilizing a simple Convolutional Neural Network (CNN), to identify plant diseases through images. 
The model has been trained with a public dataset from Kaggle.

### Prerequisites
You need to have the following tools installed globally on you machine:
* Python
* Docker

### Installation

Because there is limit of 100MB from github, we need to install the model from this [link](https://drive.google.com/file/d/1iqv0P2JLC9I1X6UJFwCeDKf1DU8kEAZv/view?usp=drive_link) and move it within `app` dir.
You can use the `drive_download.py` to download it 

### Run localy

Build image
`docker build -t plant_disease .`

Run container
`sudo docker run --name container_plant_disease -p 8000:8000 plant_disease`

### Deploy on Google Cloud 

* [Install Google Cloud CLI](https://cloud.google.com/sdk/docs/install?hl=pt-br#rpm)
* Configure the gcloud  with the docker
    * You’ll need to determine in which location you want to have your container stored. You can find a full list [here](https://cloud.google.com/artifact-registry/docs/repositories/repo-locations).
        * `sudo gcloud auth configure-docker LOCATION-docker.pkg.dev`
* The next two steps can be done in you GCP UI. 
    * Go to the Artifact Registry in the navigation menu and click the button to enable the API. Then, go to the repositories and click Create Repository button. In the pop-up menu, specify that this is a Docker repository and set its location equal to the previously selected one.
* The next step is tag the image with appropriate name and to push it. The commands will take some time to execute but once it’s done, you’ll be able see your Docker image in your Artifact Registry UI. the commands are:
    * `docker tag IMAGE-NAME LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE-NAME`
    * `docker push LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE-NAME`
* The last step is to deploy the image on cloud run. The actual deployment step is relatively easy with GCP. The only thing you need to take care of is to enable the Cloud Run API in your GCP project by going to the Cloud Run section in navigation menu and clicking on the button to enable the API. This command will create a default-service (a.k.a our API) from the previously uploaded image in the Artifact Registry. In addition, it also specifies the region (the same as our Docker image), the port to expose, and the RAM available to the service.  

      gcloud run deploy default-service \ 
      --image LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE-NAME \
      --region LOCATION \
      --port 8000 \
      --memory 3Gi``
