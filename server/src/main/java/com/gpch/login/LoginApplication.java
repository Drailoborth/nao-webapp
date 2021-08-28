package com.gpch.login;

import com.gpch.naocontrol.Server;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.logging.Logger;

@SpringBootApplication
public class LoginApplication {

    private static final Logger LOGGER = Logger.getLogger("");

    @Bean
    public Server startServer() {
        Server s = new Server(65432);
        s.startServer();
        return s;
    }

    public static void main(String[] args) {
        SpringApplication.run(LoginApplication.class, args);
    }
}
