package com.gpch.login.service;

import com.gpch.login.model.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Handler;
import java.util.logging.LogRecord;

public class LogHandler extends Handler {

    @Autowired
    private LogService logService;

    @Override
    public void publish(LogRecord record){

        SimpleDateFormat ft =
                new SimpleDateFormat ("E yyyy.MM.dd '-' hh:mm:ss a zzz");

        Log l = new Log();
        l.builder().dateAndTime(ft.format(new Date()))
                .type(record.getLevel().getName())
                .message(record.getMessage())
                .status("OK").build();

        //logService.saveLog(l);
    }

    @Override
    public void flush() {

    }

    @Override
    public void close() throws SecurityException {

    }


}
