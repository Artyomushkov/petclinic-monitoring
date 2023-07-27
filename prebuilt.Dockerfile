FROM eclipse-temurin:20-jre-alpine
EXPOSE 8080
RUN apk add dumb-init
RUN addgroup -S javauser && adduser -S javauser -G javauser
COPY ./target/spring-petclinic-3.2.1-SNAPSHOT.jar /app.jar
CMD ["dumb-init", "java", "-jar", "/app.jar"]
