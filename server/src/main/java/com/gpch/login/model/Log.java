package com.gpch.login.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "log")
public class Log {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "log_id")
    private int id;
    @Column(name = "date_and_time")
    private String dateAndTime;
    @Column(name = "type")
    private String type;
    @Column(name = "message")
    private String message;
    @Column(name = "status")
    private String status;
    @Column(name = "ip_and_port")
    private String ipAndPort;
}
