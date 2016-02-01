#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from SCORM_TEMPL import SCORM_test_template, InvalidScormTestFormatException

class Pregunta:
    def __init__(self, enunciado):
        self.enunciado = enunciado
        self.respuestas = []
        self.correcta = None

class Test:
    def __init__(self, title):        
        self.title = title
        self.preguntas = []               

    def __repr__(self):
        string = unicode(self.title)

        for p in self.preguntas:    #en cada pregunta
            string += unicode(p.enunciado)
            for r in p.respuestas:  #en cada respuesta
                string += unicode(r)        
                
        return string

def generate_test():
    #Reading markdown test file, generating and writting down html test file

    with codecs.open('in/test2.md', 'r', encoding='utf8') as f:
        test_file = f.readlines()

        title = test_file[0].split("=")[1][:-2]
        
        mytest = Test(title)
        
        preg_actual = -1
        resp_actual = -1
        for line in test_file[1:]:
            char = line[0]
            if char == ':':
                preg_actual += 1    
                resp_actual = -1
                mytest.preguntas.append(Pregunta(line[1:]))
                
            elif char == '=' or char == '~':
                resp_actual += 1                
                mytest.preguntas[preg_actual].respuestas.append(line)
                if char == '=':
                    mytest.preguntas[preg_actual].correcta = resp_actual

            elif char == '[':
                break
            
            else:
                #raise InvalidScormTestFormatException 
                pass           
                

    output_file_name = 'out/output_test_.html'
    with codecs.open(output_file_name, 'w+', encoding='utf8') as f:  

        #HEADER
        num_preguntas = len(mytest.preguntas)       
        tmp_header = SCORM_test_template.mega_header.decode('utf-8')
        tmp_header = tmp_header.replace('$Nombre', str(mytest.title))
        tmp_header = tmp_header.replace('$num_preguntas', str(num_preguntas))
        
        for i in range(num_preguntas):
            tmp_header += "var question"+str(i)+";\n"
            tmp_header += "var key"+str(i)+" = "+str(mytest.preguntas[i].correcta+1)+";\n"        
        f.write(tmp_header)

        #GETANSWER
        tmp_getAnswer = SCORM_test_template.getAnswer.decode('utf-8')
        for i in range(num_preguntas):
            tmp_answer_getAnswer = SCORM_test_template.answer_getAnswer.replace('$n', str(i))
            tmp_answer_getAnswer = tmp_answer_getAnswer.replace('$#respuestas', str(len(mytest.preguntas[i].respuestas)))
            tmp_answer_getAnswer = tmp_answer_getAnswer.replace('$respuesta_correcta', str(mytest.preguntas[i].correcta+1)) #pensaba que este 1 iba a ser la magia (pero no)
            tmp_getAnswer += tmp_answer_getAnswer

        f.write(tmp_getAnswer + '}\n')
        
        #CALCRAWSCORE
        tmp_calcRawScore = SCORM_test_template.calcRawScore.decode('utf-8')
        for i in range(num_preguntas):
            tmp_answer_calcRawScore = SCORM_test_template.answer_calcRawScore.replace('$n', str(i))
            tmp_calcRawScore += tmp_answer_calcRawScore

        f.write(tmp_calcRawScore + '}\n')
        
        #CALCSCORE
        f.write(SCORM_test_template.calcScore.decode('utf-8'))

        f.write('</script>')

        #TEST HEADER
        f.write(SCORM_test_template.test_header.replace('$Titulo', str(mytest.title)))
        
        #PREGUNTAS Y RESPUESTAS
        tmp_pregyresp = ''
        for num_pregunta, p in enumerate(mytest.preguntas):
            tmp_pregunta = SCORM_test_template.templ_pregunta.decode('utf-8').replace('$Enunciado', unicode(p.enunciado[:-1]))
            tmp_pregyresp += tmp_pregunta.replace('$num_pregunta', unicode(num_pregunta))
            
            for num_respuesta, r in enumerate(p.respuestas):
                tmp_respuesta = SCORM_test_template.templ_respuesta.decode('utf-8').replace('$Respuesta', unicode(r[1:-1]))
                tmp_respuesta = tmp_respuesta.replace('$num_pregunta', unicode(num_pregunta))
                tmp_respuesta = tmp_respuesta.replace('$num_respuesta', unicode(num_respuesta + 1)) 
                tmp_pregyresp += tmp_respuesta
            tmp_pregyresp += '</div>\n'

        tmp_pregyresp += '</div>\n'
        
        f.write(tmp_pregyresp)

        #FOOTER
        f.write(SCORM_test_template.templ_footer)



    #shutil.copyfile(file_name, file_name+'.html')
generate_test()

print '\033[93m\033[1mTest generated correctly\033[0m'

