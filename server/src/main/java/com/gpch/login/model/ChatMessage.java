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
@Table(name = "message")
public class ChatMessage {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "message_id")
    private int id;
    @Column(name = "content")
    private String content;
    @Column(name = "sender")
    private String sender;
    @Column(name = "type")
    private MessageType type;

    public enum MessageType {CHAT, LEAVE, JOIN}

}