FROM eclipse-temurin:20-jdk-alpine as base
WORKDIR /app
COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN ./mvnw dependency:resolve
COPY src ./src
RUN ./mvnw package

FROM base as development
CMD ["./mvnw", "spring-boot:run", "-Dspring-boot.run.profiles=mysql"]

FROM base as build
RUN ./mvnw package

FROM eclipse-temurin:20-jre-alpine as production
EXPOSE 8080
RUN apk add dumb-init
RUN addgroup -S javauser && adduser -S javauser -G javauser
COPY --from=build /app/target/spring-petclinic-*.jar /app.jar
CMD ["dumb-init", "java", "-jar", "/app.jar"]