package com.gpch.login.repository;

import com.gpch.login.model.Log;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LogRepository extends JpaRepository<Log, Integer> {
    Log findByMessage(String message);
}
