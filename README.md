# NaoCloud

This project is part of my Diploma thesis at KEMT TUKE. This Software is used for remote control of Nao robot via Web interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1) resolve project dependencies using Maven from public repositories 
2) set database
3) compile and run 

### Prerequisites
* JDK 1.8
* Docker Container Runtime

### Installing 

1) run build target install to create .JAR file
2) pack JAR archive (located in target dir) /w dockerfile 
3) deploy to targeted cloud platform or using docker command create image or deploy on local system
to create docker image please refer to [Docker - Create a base image](https://docs.docker.com/develop/develop-images/baseimages/) oficial guide.
  

## Built With

* [Maven](https://maven.apache.org/)
* [Docker](https://www.docker.com/)

## Notes

* set your own passwords (or ports if needed) in docker-compose.yml
* for robot connection by using Docker, reverse-proxy is missing

## Authors

* **Alexander Mudzo** - *Initial work* - [r4d1x](https://github.com/AlexanderMudzo)
* **Peter Janic** - *Previous work* - [e-mail] janicpeter1@gmail.com
* **Tomas Kacir** - *Following work* - [e-mail] tomas.kacir@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Special thanks to : **Sean Guo** for NaoRobot control script.

