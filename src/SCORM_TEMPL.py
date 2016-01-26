#!/usr/bin/env python
# -*- coding: utf-8 -*-

mega_header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="es" xml:lang="es" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>$Nombre</title>
<meta name="generator" content="eXeLearning 2.0.4 - exelearning.net" />
<link rel="stylesheet" type="text/css" href="base.css" />
<link rel="stylesheet" type="text/css" href="content.css" />
<script type="text/javascript" src="exe_jquery.js"></script>
<script type="text/javascript">$exe_i18n={show:"Mostrar",hide:"Ocultar",showFeedback:"Mostrar retroalimentación",hideFeedback:"Ocultar retroalimentación",correct:"Correcto",incorrect:"Incorrecto",menu:"Menú"}</script>
<script type="text/javascript" src="common.js"></script>
<script type="text/javascript" src="SCORM_API_wrapper.js"></script>
<script type="text/javascript" src="SCOFunctions.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body class="exe-scorm" onload="loadPage()" onunload="unloadPage()"><script type="text/javascript">document.body.className+=" js"</script>
$elementos <!-- Procesar para meter los elementos del capitulo que corresponde en process.scorm -->
<div id="outer">
<div id="main">
<div id="nodeDecoration"><h1 id="nodeTitle">Inicio</h1></div>
<div class="iDevice_wrapper QuizTestIdevice em_iDevice" id="id0">
<script type="text/javascript">
<!-- //<![CDATA[
var numQuestions = $num_preguntas;
var rawScore = 0;
var actualScore = 0;
<!-- Aqui va var questionN; y var keyN = [0, respuestas(keyN)-1]; -->
"""

getAnswer = """
function getAnswer() {
"""

answer_getAnswer = """
        scorm.SetInteractionValue("cmi.interactions.$n.id", "key$nb0");
        scorm.SetInteractionValue("cmi.interactions.$n.type", "choice");
        scorm.SetInteractionValue("cmi.interactions.$n.correct_responses.0.pattern", $respuesta_correcta);
            
        for (var i=0; i < $#respuestas; i++) {
               if (document.getElementById("quizForm0").key$nb0[i].checked)
               {
                  question$n = document.getElementById("quizForm0").key$nb0[i].value;
                  scorm.SetInteractionValue("cmi.interactions.$n.student_response", question$n);
                  break;
               }
        }     
"""

calcRawScore = """
function calcRawScore(){
"""

answer_calcRawScore = """
        if (question$n == key$n) {
            scorm.SetInteractionValue("cmi.interactions.$n.result", "correct");
            rawScore++;
        }
        else {
            scorm.SetInteractionValue("cmi.interactions.$n.result", "wrong");
        }
"""

calcScore = """
function calcScore() {
        computeTime(); 
       
        document.getElementById("quizForm0").submitB.disabled = true;
       
        getAnswer();
    
        calcRawScore();
          
        actualScore = Math.round(rawScore / numQuestions * 100);
        alert("Su puntuación es " + actualScore + "%")  
          
        scorm.SetScoreRaw(actualScore+"" );
        scorm.SetScoreMax("100");
          
        var mode = scorm.GetMode();

        if ( mode != "review"  &&  mode != "browse" ) {
            if ( actualScore < 50 ) {
                scorm.SetCompletionStatus("incomplete");
                scorm.SetSuccessStatus("failed");
            }
            else {
                scorm.SetCompletionStatus("completed");
                scorm.SetSuccessStatus("passed");
            }

            scorm.SetExit("");
        }

        exitPageStatus = true;
    
        scorm.save();
    
        scorm.quit();
         
}
"""
test_header = """
<div class="iDevice emphasis1" >
    <div class="iDevice_header">
        <h2 class="iDeviceTitle">$Titulo</h2>
    </div>
    <div class="iDevice_inner">
        <div class="iDevice_content_wrapper">
            <form name="quizForm0" id="quizForm0" action="javascript:calcScore2();">
                <input type="hidden" name="passrate" id="passrate-0" value="50" />
"""

templ_pregunta = """
                    <h3 class="js-sr-av">Pregunta</h3>
                    <div id="taquestion$num_preguntab0" class="block iDevice_content">
                        <p>$Enunciado</p>
                    </div>
                    <div class="iDevice_answers">
                    <h4 class="js-sr-av">Respuestas</h4>
"""

templ_respuesta = """
                        
                        <div class="iDevice_answer">
                            <p class="iDevice_answer-field js-required">
                                <input type="radio" name="key$num_preguntab0" id="key$num_preguntab0$num_respuesta" value="$num_respuesta" /> 
                            </p>
                            <div class="iDevice_answer-content" id="answer-key0b0$n">
                                <a name="answer-key$num_preguntab0$num_respuesta"></a>
                                <div id="taoptionAnswer$num_respuestaq$num_preguntab0" class="block iDevice_content">
                                    <p>$Respuesta</p>
                                </div>
                            </div>
                        </div>
"""

templ_footer = """
<div class="block iDevice_buttons">
                    <p>
                        <input type="submit" name="submitB" value="ENVIAR RESPUESTAS" /> 
                        <span class="js-hidden js-warning">Habilitar JavaScript</span>
                    </p>
                </div>
            </form>
        </div>
    </div>
</div>
</div>
</div>
</div>
<script type="text/javascript" src="my_js.js"></script>
"""

class InvalidScormTestFormatException(Exception):
    pass
