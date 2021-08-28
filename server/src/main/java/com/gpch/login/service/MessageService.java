package com.gpch.login.service;

import com.gpch.login.model.ChatMessage;
import com.gpch.login.repository.MessageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service("messageService")
public class MessageService {

private MessageRepository messageRepository;

    @Autowired
    public MessageService(MessageRepository messageRepository) {
        this.messageRepository= messageRepository;
    }

    public ChatMessage saveMessage(ChatMessage chatMessage) {return messageRepository.save(chatMessage);}

    public List<ChatMessage> getAllMessages(){ return messageRepository.findAll();}
}
