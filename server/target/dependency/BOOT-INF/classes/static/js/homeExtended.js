
jQuery(document).ready(function(){
    printClean();
    if(document.getElementById('tblMacro').rows.length > 1) {
        var delay = parseInt(getDelay());
        delay+=50;
        setTimeout(() => {
            doCommand();
        }, delay);
    }
});

function printClean() {
    document.getElementById("myInput1").setAttribute('value', '');
    document.getElementById("myInput2").setAttribute('value', '');
}

function getDelay() {
    var value = 500;
    var macroTable = document.getElementById('tblMacro');
    var tRows = macroTable.getElementsByTagName("tr");

    var newValue = tRows[0].children[1].innerHTML;
    if(isInt(newValue)){
        if(newValue >= 0) {
            return newValue;
        }
        else return value;
    }
    else return value;
}

function doCommand(){
    var macroTable = document.getElementById('tblMacro');
    if(macroTable.rows.length <= 1) return;
    else {
        var tRows = macroTable.getElementsByTagName("tr");
        var selectedCommand = tRows[0].children[0].children[0].value;
        //selectedCommand has first command from table
        if (selectedCommand === "SAY"){
            var text = tRows[0].children[2].innerHTML;
            if(text === "<br>")text = "";
            document.getElementById("myInput2").setAttribute('value', text);
            deleteOneRow(tRows[0].children[3].children[0], 'tblMacro');
            document.getElementById("controlButton").click();
        }
        else{
            if(selectedCommand === "nothing")return; //nothing to do
            var originalSelect = document.getElementById('commandSelList');
            originalSelect.value = selectedCommand;
            deleteOneRow(tRows[0].children[3].children[0], 'tblMacro');
            document.getElementById("mainControlButton").click();
        }
    }
}

function isInt(value) {
    return !isNaN(value) &&
        parseInt(Number(value)) == value &&
        !isNaN(parseInt(value, 10));
}

function oneTimeUseOptionsFill(){
    //I think this won't work if someone makes changes that will allow to modify commands options and won't clear local storage data or reduce commands count below 21
    var originalSelect = document.getElementById('commandSelList');
    var originalOptions = originalSelect.innerHTML;

    var secondSelect = document.getElementById('MacroSelectList');
    if(secondSelect.options.length > 20) return;
    for(var i = 0; i < secondSelect.options.length - 1; i++)
        secondSelect.options.remove(i);
    var originalOptions = secondSelect.innerHTML + originalOptions;

    secondSelect.innerHTML = originalOptions;
}

document.addEventListener("DOMContentLoaded", function(event) {
    var oldConnTable = localStorage.getItem('connectionsTable');
    if(oldConnTable) document.getElementById("tblConnections").innerHTML = oldConnTable;
    var oldMacroTable = localStorage.getItem('macroTable');
    if(oldMacroTable) document.getElementById("tblMacro").innerHTML = oldMacroTable;
    var scrollPos = localStorage.getItem('scrollPos');
    if (scrollPos) window.scrollTo(0, parseInt(scrollPos));
    setBySelected("storedItems");
});

window.onbeforeunload = function(e) {
    localStorage.setItem('connectionsTable', document.getElementById("tblConnections").innerHTML);
    localStorage.setItem('macroTable', document.getElementById("tblMacro").innerHTML);
    localStorage.setItem('scrollPos', window.scrollY.toString());
    saveSelected("storedItems");
};

function getBattery() {
    document.getElementById("myInput2").setAttribute('value', './battery');
    document.getElementById("controlButton").click();
}

function sitDown() {
    document.getElementById("myInput2").setAttribute('value', './sit down');
    document.getElementById("controlButton").click();
}

function standUp() {
    document.getElementById("myInput2").setAttribute('value', './stand');
    document.getElementById("controlButton").click();
}

function executeCommand() {
    document.getElementById("myInput2").setAttribute('value', '');
    document.getElementById("controlButton").click();
}

function setLastOption() {
    var theSelect = document.getElementById('SelectList');
    var lastValue = theSelect.options[theSelect.options.length - 1].value;
    theSelect.value = lastValue;
}

// 37 - left
// 38 - up
// 39 - right
// 40 - down
// 12 - 5
// 118 - F7
// 120 - F9
// 18 - ALT
// 106 - *
$(document).keydown(function(e){
    if(!document.getElementById('myInput2').value &&
        !document.getElementById('myInput1').value) {
        if (e.which === 38) {
            $("#buttonForward").click();
            return false;
        } else if (e.which === 40) {
            $("#buttonBackward").click();
            return false;
        } else if (e.which === 37) {
            $("#buttonTurnLeft").click();
            return false;
        } else if (e.which === 39) {
            $("#buttonTurnRight").click();
            return false;
        } else if (e.which === 12) {
            $("#buttonStop").click();
            return false;
        }
    }
    if (e.which === 118) {
        localStorage.setItem('macroTableForLater', document.getElementById("tblMacro").innerHTML);
        saveSelected("storedItemsForLater");
        return e;
    }
    else if (e.which === 120) {
        var veryOldMacroTable = localStorage.getItem('macroTableForLater');
        if(veryOldMacroTable) document.getElementById("tblMacro").innerHTML = veryOldMacroTable;
        setBySelected("storedItemsForLater");
        return e;
    }
    if (e.which === 18) {
        if (e.originalEvent.location == 1) {
            if (!isElementInViewport($('.focusedLabel'))) {
                document.getElementById('myInput2').scrollIntoView();
            }
            $('#myInput2').focus().trigger('click');
            return false;
        }
    }
    if (e.which === 106) {
        $("#aRecBtn").click();
        return false;
    }
});


function isElementInViewport (el) {
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }
    var rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}


function getConnectionRecord() {
    if(!document.getElementById('IpAdd')) return;
    if(!document.getElementById('IpAdd').innerText || !document.getElementById('PortNum').innerText)
        return null;
    var ipAdd = document.getElementById('IpAdd').innerText;
    var portNum = document.getElementById('PortNum').innerText;
    var str = ipAdd + ":" + portNum;

    return str;
}

function compareAndConnect(str) {
    var theSelect = document.getElementById('SelectList');
    for(var i=0; i < theSelect.options.length; i++){
        if(theSelect.options[i].value == str){
            theSelect.value = theSelect.options[i].value;
            document.getElementById("connectButton").click();
        }
    }
}

function deleteOneRow(r, tbl) {
    var table = document.getElementById(tbl);

    if(table.rows.length == 1){
        table.rows[0].cells[0].innerHTML = "";
        table.rows[0].cells[0].abbr = "";
        return;
    }

    var i = r.parentNode.parentNode.rowIndex;
    table.deleteRow(i);
    if(tbl === "tblMacro") {
        saveSelected("storedItems");
        if(document.getElementsByClassName("macroRows").length < 2){
            document.getElementById("macro-header").style.visibility = "hidden";
        }
    }
}

function deleteAllRows(tbl) {
    var table = document.getElementById(tbl);
    var tRow = table.getElementsByTagName("tr");
    for(var i = tRow.length-2; i >= 0; i--){
        if(tbl === 'tblConnections')
            deleteOneRow(tRow[i].children[1].children[0], tbl);
        else if(tbl === 'tblMacro')
            deleteOneRow(tRow[i].children[3].children[0], tbl);
    }
}

function connectRow(r) {
    var savedIP = r.parentNode.parentNode.cells[0].abbr;
    compareAndConnect(savedIP);
}


function addNewConnection(myTable) {
    var IpAndPort = getConnectionRecord();
    if(!IpAndPort)
        return;
    var table = document.getElementById(myTable);
    var row = table.getElementsByTagName('tr');
    var row = row[row.length-1].outerHTML;

    table.innerHTML = table.innerHTML + row;
    table.rows[table.rows.length-2].cells[0].innerHTML = IpAndPort;
    table.rows[table.rows.length-2].cells[0].abbr = IpAndPort;
    table.rows[table.rows.length-2].style.display = "block";
}

function saveSelected(storage) {
    var selects = document.getElementsByClassName("macroOptions");
    var itemsToStore = [];

    for (var i = 0; i < selects.length - 1; i++) {
        var valueToStore = selects[i].options[selects[i].selectedIndex].value;

        itemsToStore.push(valueToStore);
    }
    localStorage.setItem(storage, JSON.stringify(itemsToStore));
}


function getSelects(storage) {
    var storedSelection = JSON.parse(localStorage.getItem(storage));
    if (storedSelection)
        return storedSelection;
}

function setBySelected(storage) {
    var selectMacro = document.getElementsByClassName("macroOptions");
    var storedSelection = getSelects(storage);
    if(!storedSelection)return;

    for(var i = 0; i < storedSelection.length; i++){
        selectMacro[i].value = storedSelection[i];
    }
}

function addNewCommand(myTable) {

    if(document.getElementById("macro-header").style.visibility === "hidden") {
        document.getElementById("macro-header").style.visibility = "visible";
    }

    var table = document.getElementById(myTable);

    if(table.rows.length === 1){
        oneTimeUseOptionsFill();
    }

    var row = table.getElementsByTagName('tr');
    var row = row[row.length-1].outerHTML;

    saveSelected("storedItems");

    table.innerHTML = table.innerHTML + row;
    setBySelected("storedItems");

    table.rows[table.rows.length-2].style.display = "block";

}

function copyRow(r) {

    var i = r.parentNode.parentNode;
    $(i).after($(i).clone());

}

function reloadPageAndConnect(){
    sessionStorage.setItem("refreshPage", "true");
}

window.onload = function() {
    var doConnect = sessionStorage.getItem("connectToLast");
    var refreshPage = sessionStorage.getItem("refreshPage");

    if (refreshPage) {
        sessionStorage.removeItem("refreshPage");
        sessionStorage.setItem("connectToLast", "true");
        document.getElementById('btnHome').click();
    }
    if(doConnect){
        sessionStorage.removeItem("connectToLast");
        setLastOption();
        document.getElementById("connectButton").click();
    }
}