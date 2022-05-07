#  Data prediction model for loan and customer
	
	Steps for project set up:	
	1. git clone https://github.com/hsam-2021/data_prediction.git
	2. Set up Docker for Linux following the instruction in link https://docs.docker.com/engine/install/ubuntu/
	3. Go to the folder location in your local where you clone the data_prediction repository
	4. Run command to build docker image "docker build -t  data_prediction:1 data_prediction"   (Note - please make sure you one directory above the project folder before executing the command)
	5. Run command to create docker container "docker create --restart=always -p 9000:5000 --log-opt max-size=50m --name data_prediction data_prediction:1"
	6. Run the command to start docker continer "docker start data_prediction"
