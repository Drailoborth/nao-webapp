package com.gpch.naocontrol;

public interface Controlable  {

    String getInstanceName();
    String getIP();
    String getTime();
    int getBattery();
    int getPort();
    String getResponse();

    Boolean isConnected();
    void execute(Command command, String arg);
    void disconnect();

}
