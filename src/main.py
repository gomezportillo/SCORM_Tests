#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, os, sys
from string import Template, ascii_lowercase


class InvalidScormTestFormatException(Exception): pass

class Question:
    def __init__(self, statement):
        self.statement = statement
        self.answers = []
        self.correct = None


class Test:
    def __init__(self, title):
        self.title = title
        self.questions = []
        self.alphabet = list(ascii_lowercase) #letters from a to z

    def __repr__(self):
        test_repr = self.title

        for question in self.questions:     #on each question
            test_rep += question.statement

            for answer in question.answers: #on each answer
                test_repr += answer

        return test_repr

    def toHtml(self):

        separator='\n'

        test_txt = '{}{}{}'.format('<p>', self.title, '</p>')
        test_txt += '<blockquote>'
        for index_q, question in enumerate(self.questions):
            test_txt += '{}. {}{}'.format(index_q+1, question.statement, separator)
            test_txt += '\n<blockquote>'

            for index_a, answer in enumerate(question.answers):
                tmp_answer = '{}({}) {}{}'.format('<p>', self.alphabet[index_a], answer[1:], '</p>')
                test_txt += tmp_answer
            test_txt += '\n</blockquote>'

        test_txt += '</blockquote>'
        return test_txt + separator

    def toLatex(self):

        separator = '\\\\'
        tabulator = '\\hspace*{10mm}'

        test_txt = '{}{}{}'.format(self.title, self.getCorrectAnswers(), separator)

        for index_q, question in enumerate(self.questions):
            test_txt += '{}. {}{}'.format(index_q+1, question.statement, separator)

            for index_a, answer in enumerate(question.answers):
                tmp_answer = '{}({}) {}{}'.format(tabulator, self.alphabet[index_a], answer[1:], separator)
                test_txt += tmp_answer

        return test_txt

    def getCorrectAnswers(self):
        test_results = 'Los resultados del test del capítulo {} son '.format(self.chapter)

        for index_q, question in enumerate(self.questions):
            test_results += '{}({}), '.format(index_q+1, self.alphabet[question.correct])

        return '\\footnote{{{}.}}'.format(test_results[:-2])

def generate_test():
    #Reading markdown test file, generating and writting down html scorm test file
    templateDir = os.path.join('data', 'templates', 'scorm', 'test')

    with codecs.open('in/test3.md', 'r', encoding='utf8') as f:
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
                mytest.questions.append(Question(line[2:]))

            elif char == '=' or char == '~':
                resp_actual += 1
                mytest.questions[preg_actual].answers.append(line)
                if char == '=':
                    mytest.questions[preg_actual].correct = resp_actual

            elif char == '[':
                break

            else:
                #raise InvalidScormTestFormatException
                pass

    #print mytest.toLatex()
    output_file_name = 'out/output_test_.html'
    output_file_txt = ''
    with codecs.open(output_file_name, 'w+', encoding='utf8') as f:

        #HEADER
        num_questions = len(mytest.questions)
        main_header_file = codecs.open(os.path.join(templateDir, 'scorm_test_main_header.hit'), encoding='utf-8')
        main_header_templ = Template(main_header_file.read())
        tmp_header = main_header_templ.substitute(TestName=mytest.title,
                                                  exe_i18n='$exe_i18n', #elsewhere its detected as a variable
                                                  num_questions=num_questions)

        for i in range(num_questions):
            tmp_header += "var question{0};\n".format(i)
            tmp_header += "var key{0} = {1};\n".format(i, (mytest.questions[i].correct)+1 )
        f.write(tmp_header)
        output_file_txt += tmp_header

        #GETANSWER
        tmp_getAnswer = codecs.open(os.path.join(templateDir, 'scorm_test_getAnswer.hit'), encoding='utf-8').read()

        answer_getAnswer_file = codecs.open(os.path.join(templateDir, 'scorm_test_answer_getAnswer.hit'), encoding='utf-8')
        answer_getAnswer_templ = Template(answer_getAnswer_file.read())

        for i in range(num_questions):
            tmp_answer_getAnswer = answer_getAnswer_templ.substitute(num_iteration=i,
                                                                     num_iterationb0=str(i)+'b0',
                                                                     num_answers=len(mytest.questions[i].answers),
                                                                     correct_answer=(mytest.questions[i].correct + 1))
            tmp_getAnswer += tmp_answer_getAnswer

        f.write(tmp_getAnswer + '}\n')
        output_file_txt += tmp_getAnswer + '}\n'

        #CALCRAWSCORE
        tmp_calcRawScore = codecs.open(os.path.join(templateDir, 'scorm_test_calcRawScore.hit'), encoding='utf-8').read()

        answer_calcRawScore_file = codecs.open(os.path.join(templateDir, 'scorm_test_answer_calcRawScore.hit'), encoding='utf-8')
        answer_calcRawScore_templ = Template(answer_calcRawScore_file.read())

        for i in range(num_questions):
            tmp_calcRawScore +=  answer_calcRawScore_templ.substitute(num_iteration=i)

        f.write(tmp_calcRawScore + '}\n')
        output_file_txt += tmp_calcRawScore + '}\n'

        #CALCSCORE
        calcScore = codecs.open(os.path.join(templateDir, 'scorm_test_calcScore.hit'), encoding='utf-8')
        calcScore_file = calcScore.read()
        f.write(calcScore_file)
        output_file_txt += calcScore_file

        #TEST HEADER
        test_header_file = codecs.open(os.path.join(templateDir, 'scorm_test_test_header.hit'), encoding='utf-8')
        test_header_templ = Template(test_header_file.read())
        test_header = test_header_templ.substitute(Title=mytest.title)
        f.write(test_header)
        output_file_txt += test_header

        #PREGUNTAS Y RESPUESTAS
        tmp_pregyresp = ''
        question_file = codecs.open(os.path.join(templateDir, 'scorm_test_question.hit'), encoding='utf-8')
        question_templ = Template(question_file.read())

        answer_file = codecs.open(os.path.join(templateDir, 'scorm_test_answer.hit'), encoding='utf-8')
        answer_templ = Template(answer_file.read())

        for num_question, q in enumerate(mytest.questions):
            tmp_pregunta = question_templ.substitute(Statement=q.statement[:-1],
                                                     num_question=num_question,
                                                     num_questionb0=(str(num_question)+'{}').format('b0'))
            tmp_pregyresp += tmp_pregunta
            for num_answer, a in enumerate(q.answers):
                tmp_respuesta = answer_templ.substitute(Respuesta=a[1:-1],
                                                        num_question=num_question,
                                                        num_questionb0=str(num_question)+'b0',
                                                        num_answer=(num_answer + 1),
                                                        num_answerq=str(num_answer + 1)+'q')
                tmp_pregyresp += tmp_respuesta

            tmp_pregyresp += '</div>\n'

        tmp_pregyresp += '</div>\n'

        f.write(tmp_pregyresp)
        output_file_txt += tmp_pregyresp

        #FOOTER
        test_footer_file = codecs.open(os.path.join(templateDir, 'scorm_test_footer.hit'), encoding='utf-8')
        test_footer = test_footer_file.read()
        f.write(test_footer)
        output_file_txt += test_footer

generate_test()

print '\033[93m\033[1mTest generated correctly\033[0m'
