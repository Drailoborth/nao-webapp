
function startRecord() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var speechRecord = new webkitSpeechRecognition();
        speechRecord.continuous = false;
        speechRecord.interimResults = false;
        speechRecord.lang = "sk";
        speechRecord.start();
        var recButton = document.getElementById('recButton');
        recButton.style.border = "1px solid red";
        recButton.style.borderRadius = "20px";

        speechRecord.onresult = function(e) {
            let sentence = e.results[0][0].transcript;
            sentence = textResolveForCommands(sentence, "command", "robot", "príkaz", "prikaz", "povel", "nao", "lomitko", "lomítko");
            document.getElementById('myInput2').value = sentence;

            speechRecord.stop();

            recButton.style.border = null;
            recButton.style.borderRadius = null;
            let input = document.getElementById('myInput2').value;
            $('#myInput2').focus().trigger('click');
            if(input.charAt(0) === '.' && input.charAt(1) === '/'){
                $('#controlButton').click();
            }
        };
        speechRecord.onerror = function(e) {
            recButton.style.border = null;
            recButton.style.borderRadius = null;
            speechRecord.stop();
        }
    }
    else{
        alert("Sorry! This browser does not support Speech recognition.");
    }
}

function textResolveForCommands(str, ...args) {
    var totalWords = str;
    var firstWord = totalWords.replace(/ .*/,'');

    for (var i = 1; i < arguments.length; i++) {
        if(firstWord === arguments[i]) {
            totalWords = change(totalWords, firstWord);
            return totalWords;
        }
    }
    return str;
}

function change(totalWords, firstWord) {
    let word = firstWord + " ";
    var newString = totalWords.replace(word, "./");
    return newString;
}
