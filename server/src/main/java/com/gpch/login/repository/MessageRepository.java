package com.gpch.login.repository;

import com.gpch.login.model.ChatMessage;

import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


@Repository("messageRepository")
public interface MessageRepository extends JpaRepository<ChatMessage, Long>{
    ChatMessage findBySender(String sender);

}
