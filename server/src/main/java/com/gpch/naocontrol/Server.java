package com.gpch.naocontrol;

import lombok.ToString;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;


public class Server extends Thread {

    private ServerSocket serverSocket;
    private int port;

    private boolean running = false;
    private List<Controlable> instances = new ArrayList<>();

    public Server(int port) {
        this.port = port;

    }

    public void startServer() {
        try {
            serverSocket = new ServerSocket(port);
            this.start();
        } catch (Exception e) {
            e.printStackTrace();
        }


    }

    public void stopServer() {
        running = false;
        for (Controlable r:
                getInstances()) {
            r.disconnect();
        }
        this.interrupt();
    }

    @Override
    public void run() {

        Instance instance;
        running = true;
        while (running) {
            try {
                System.out.println("Listening for a connections");

                clean();
                // Call accept() to receive the next connection
                Socket socket = serverSocket.accept();

                // Pass the socket to the RequestHandler thread for processing
                instance = new Instance(socket);
                instance.start();
                Thread.sleep(100);
                //instance.setInfo();

                instances.add(instance);

            } catch (Exception e) {
                stopServer();
                e.printStackTrace();
            }
        }
    }

    private void clean(){
        for (Controlable c : new ArrayList<>(instances)) {
            if (!c.isConnected()) {
                instances.remove(c);
            }
        }
    }

    public List<Controlable> getInstances() {
        return instances;
    }

    public List<Controlable> removeInstances() {
        while(instances.size() > 1)
            instances.remove(0);
        return instances;
    }

    public Controlable getInstanceByIP(String IP){

       String res[] = IP.split(":");

        for (Controlable r:
             getInstances()) {
            if (r.getIP().equals(res[0]) && r.getPort() == Integer.parseInt(res[1])) return r;
        }
        return null;
    }

}