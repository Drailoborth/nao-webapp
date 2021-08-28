package com.gpch.naocontrol;

import com.gpch.naocontrol.threadworkers.RequestHandler;

import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Random;


public class Instance extends RequestHandler implements Controlable {

    private boolean conn;

    Instance(Socket socket) {
        super(socket);
        conn=true;
        SimpleDateFormat ft =
                new SimpleDateFormat("E yyyy.MM.dd '-' hh:mm:ss");
        this.time = ft.format(new Date());
        battery = 100;
        name="testname1234";


    }

    void setInfo() {
        setBattery();
        setName();
    }

    private void setBattery(){

            sendData("SENSOR");
            // Receive response data
            try {
                String received = receiveMsg();
                System.out.println(received);

                // Regex validation and parse of data
                Pattern p = Pattern.compile("([0-9]+)");
                Matcher m = p.matcher(received);
                if (m.find())
                    this.battery = Integer.parseInt(m.group(1));
            }
            catch (Exception e) {e.printStackTrace(); disconnect();}
    }

    private void setName(){
        sendData("WHOAMI");
        try {
            String received = receiveMsg();
            this.name = received;
        } catch (Exception e) {e.printStackTrace(); disconnect();}
    }

    @Override
    public String getInstanceName() {

        final String[] proper_noun = {"Fred", "Robert", "Otis", "Eliot"};
        Random random = new Random();
        int index = random.nextInt(proper_noun.length);
        name = proper_noun[index];
        return name;
    }

    @Override
    public String getTime() {
        return time;
    }

    @Override
    public int getBattery() {
        return battery;
    }

    @Override
    public String getResponse() {
        try {
            return receiveMsg();
        } catch (Exception e) {
            e.printStackTrace();
            disconnect();
            return "FAILED";
        }
    }

    @Override
    public Boolean isConnected() {
        return conn;
    }

    @Override
    public void execute(Command command, String arg) {
        sendData(command + " " + arg);
    }
    @Override
    public void disconnect() {
        conn=false;
        close();
    }

    private String name;
    private String time;
    private int battery;

}
