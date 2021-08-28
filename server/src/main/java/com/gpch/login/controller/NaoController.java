package com.gpch.login.controller;

import com.gpch.login.model.Log;
import com.gpch.login.model.Session;
import com.gpch.login.model.User;
import com.gpch.login.service.LogHandler;
import com.gpch.login.service.LogService;
import com.gpch.login.service.UserService;
import com.gpch.naocontrol.Command;
import com.gpch.naocontrol.Controlable;
import com.gpch.naocontrol.Server;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.servlet.ModelAndView;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Controller
@Scope(WebApplicationContext.SCOPE_SESSION)
public class NaoController {

    @Autowired
    private UserService userService;

    @Autowired
    private LogService logService;

    @Autowired
    private Server server;

    private Controlable activeInst;

    @ModelAttribute("allCommands")
    public List<String>populateCommands(){
        return Stream.of(Command.values())
                .map(Command::name)
                .collect(Collectors.toList());
    }

    @ModelAttribute("CommandSAY")
    public Command say(){return Command.SAY;}

    @ModelAttribute("CommandFORWARD")
    public Command move(){return Command.FORWARD;}

    @ModelAttribute("CommandBACKWARD")
    public Command moveBack(){return Command.BACK;}

    @ModelAttribute("CommandSTOP")
    public Command stop(){return Command.STOP;}

    @ModelAttribute("CommandRIGHT")
    public Command moveRight(){return Command.RIGHT;}

    @ModelAttribute("CommandLEFT")
    public Command moveLeft(){return Command.LEFT;}

    @ModelAttribute("CommandTURNLEFT")
    public Command turnLeft(){return Command.TURNLEFT;}

    @ModelAttribute("CommandTURNRIGHT")
    public Command turnRight(){return Command.TURNRIGHT;}

    @ModelAttribute("CommandWAKEUP")
    public Command wakeUp(){return Command.WAKEUP;}

    @ModelAttribute("CommandLARMUP")
    public Command leftArmUp(){return Command.LARMUP;}

    @ModelAttribute("CommandRARMUP")
    public Command rightArmUp(){return Command.RARMUP;}

    @ModelAttribute("CommandLARMDOWN")
    public Command leftArmDown(){return Command.LARMDOWN;}

    @ModelAttribute("CommandRARMDOWN")
    public Command rightArmDown(){return Command.RARMDOWN;}

    @ModelAttribute("CommandLARMCLOSE")
    public Command leftArmClose(){return Command.LARMCLOSE;}

    @ModelAttribute("CommandLARMOPEN")
    public Command leftArmOpen(){return Command.LARMOPEN;}

    @ModelAttribute("CommandRARMCLOSE")
    public Command rightArmClose(){return Command.RARMCLOSE;}

    @ModelAttribute("CommandRARMOPEN")
    public Command rightArmOpen(){return Command.RARMOPEN;}

    @ModelAttribute("CommandREST")
    public Command rest(){return Command.REST;}

    @ModelAttribute("CommandARMREST")
    public Command armRest(){return Command.ARMREST;} //dodatok

    @ModelAttribute("CommandSTAND")
    public Command stand(){return Command.POSTURE_STAND;} //dodatok

    @ModelAttribute("CommandSIT")
    public Command sit(){return Command.POSTURE_SIT;} //dodatok

    @ModelAttribute("CommandSITRELAX")
    public Command sitRelax(){return Command.POSTURE_SITRELAX;} //dodatok

    @ModelAttribute("CommandCROUCH")
    public Command crouch(){return Command.POSTURE_CROUCH;} //dodatok

    @ModelAttribute("CommandSTANDZERO")
    public Command standZero(){return Command.POSTURE_STANDZERO;} //dodatok

    @ModelAttribute("CommandLYINGBELLY")
    public Command lyingBelly(){return Command.POSTURE_LYINGBELLY;} //dodatok

    @ModelAttribute("CommandLYINGBACK")
    public Command lyingBack(){return Command.POSTURE_LYINGBACK;} //dodatok

    @ModelAttribute("allLogs")
    public List<Log> populateLog() {
        return logService.getAllLogs();
    }

    @ModelAttribute("allInstances") //Strings w IP
    public List<String> populateInstances(){
        //TODO: Remove instance from list after it dies
        List<String> l = new ArrayList<>();
        server.getInstances().forEach(requestHandler -> {
            if (requestHandler.isConnected()) l.add(requestHandler.getIP() +":" +requestHandler.getPort());
        });

        return l;
    }

    public void depopulateInstances(){
        server.removeInstances();
    }

    @RequestMapping("/admin/home/clear")
    public ModelAndView clear() {
        depopulateInstances();
        return home();
    }

    @RequestMapping(value = "/admin/home", method = RequestMethod.GET)
    public ModelAndView home() {
        ModelAndView modelAndView = new ModelAndView();
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        User user = userService.findUserByEmail(auth.getName());
        modelAndView.addObject("userName",
                "Welcome " + user.getName() + " " + user.getLastName() + " (" + user.getEmail() + ")");
        modelAndView.addObject("adminMessage", "Content Available Only for Users with Admin Role");

        Session s = new Session();
        s.setUsername(user.getName());
        modelAndView.addObject("session", s);
        populateLog();
        modelAndView.setViewName("admin/home");
        return modelAndView;
    }

    @RequestMapping(value = "/chat", method = RequestMethod.GET)
    public ModelAndView chat(@ModelAttribute("session") Session session, Map<String, Object> model){
        ModelAndView modelAndView = new ModelAndView();
        model.put("username", session.getUsername());
        modelAndView.setViewName("admin/chat");
        return modelAndView;
    }

    @RequestMapping(value = "/about", method = RequestMethod.GET)
    public ModelAndView about(@ModelAttribute("session") Session session, Map<String, Object> model){
        ModelAndView modelAndView = new ModelAndView();
        model.put("username", session.getUsername());
        modelAndView.setViewName("admin/about");
        return modelAndView;
    }


    @RequestMapping(value="/admin/home/selectInstance",method = RequestMethod.POST)
    public ModelAndView info(@ModelAttribute("session") Session session, Model model){

        if (server.getInstanceByIP(session.getActiveIP())==null) {
            model.addAttribute("err", "Error occurred while selecting instance");
        }
        else {
            this.activeInst = server.getInstanceByIP(session.getActiveIP());
            model.addAttribute("selected", activeInst);
        }
        return home();
    }

    @RequestMapping(value = "/admin/home/executeCommand", method={RequestMethod.POST, RequestMethod.GET})
    public ModelAndView executeCommand(@ModelAttribute(value="session") Session session, Model model) {

        if (activeInst==null) {
            model.addAttribute("err", "Can't execute command. No instance was selected!");
            return home();
        }

        model.addAttribute("selected", activeInst);
        ModelAndView maw = new ModelAndView();
        activeInst.execute(Command.valueOf(session.getCommand()),session.getArg());
        SimpleDateFormat ft =
                new SimpleDateFormat ("E yyyy.dd.MM '-' hh:mm:ss a zzz");
        Log l = new Log(0,ft.format(new Date()),"COMMAND",session.getCommand(),"OK",session.getActiveIP());
        logService.saveLog(l);
        // Log activity
        maw.setViewName("admin/home");
        return maw;
    }






    @RequestMapping("/admin/home/video/{videoId}")
    public ResponseEntity<byte[]> getvideo(@PathVariable String videoId) throws IOException {
        InputStream in = new FileInputStream(new File(""));
        final HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        return new ResponseEntity<>(StreamUtils.copyToByteArray(in),headers, HttpStatus.CREATED);
    }

}
