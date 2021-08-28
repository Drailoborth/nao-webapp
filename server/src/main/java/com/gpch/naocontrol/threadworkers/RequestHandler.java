package com.gpch.naocontrol.threadworkers;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RequestHandler extends Thread {

    private BufferedReader in;
    private PrintWriter out;
    private Socket socket;
    private String IP;

    public int getPort() {
        return port;
    }

    private int port;
    public String getIP(){return IP;}
    private void setIP(String IP){this.IP = IP;}

    public RequestHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try {
            System.out.println("Received a connection");

            // Get input and output streams
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream());

            //Save IP of client without / at beginning
            setIP(socket.getInetAddress().toString().substring(1));

            port = socket.getPort();

            // Write out our header to the client
            out.println("Connection with NaoCloud API established!");
            out.flush();

        } catch (Exception e) {
            this.close();
            e.printStackTrace();
        }
    }

    protected void sendData(String data){
        out.println(data);
        out.flush();
    }

    protected String receiveMsg() throws Exception {
            return in.readLine();
    }

    protected void close() {
        try {
            in.close();
            out.close();
            socket.close();

        } catch (Exception e) {e.printStackTrace();}
    }
}
