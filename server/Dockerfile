# Alpine Linux with OpenJDK JRE
FROM openjdk:8-jre-alpine
# copy fat WAR
COPY target/server-component-0.5.1-SNAPSHOT.jar /app.jar
# set port mapping
EXPOSE 8081:65432
EXPOSE 80:8080
#EXPOSE 3307:3306
# runs application
CMD ["java", "-jar", "/app.jar"]