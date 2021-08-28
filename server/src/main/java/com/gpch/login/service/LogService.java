package com.gpch.login.service;

import com.gpch.login.model.Log;
import com.gpch.login.repository.LogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service("logService")
public class LogService {

    private LogRepository logRepository;

    @Autowired
    public  LogService(LogRepository logRepository){
        this.logRepository=logRepository;
    }

    public Log saveLog(Log log) {return logRepository.save(log);}

    public List<Log> getAllLogs(){ return logRepository.findAll();}
}
