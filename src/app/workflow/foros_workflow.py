# # último código funcional (con moodle)
import requests
from IPython.display import display
from IPython.core.display import HTML
import numpy as np
import time
import re
import json
import logging
from typing import Dict, List
from .utils.prompts import Prompts
from .utils.moodle_flow import MoodleWorkflow
from langchain.base_language import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class ForosWorkflow:


    def __init__(self, llm:BaseLanguageModel, url_becat:str, token:str):
        """
        Esta función se conecta a la api de OpenAI y también recibe el token de Moodle 
        """
        self.__moodle_flow = MoodleWorkflow(url_becat, token)
        self.llm = llm


    def __run_model(self, contexto, preguntas, lista_respuestas) -> Dict[str, List[str]]:

        # General task
        _task = "Genera un feedback por cada respuesta de un alumno en un foro academico."

        

        if type(lista_respuestas) is dict:
            # invoke chain 
            respuesta_usuario = f"{lista_respuestas['author']['fullname']}: {lista_respuestas['message']}"
            
            system_prompt = Prompts.prompt_foros(contexto, preguntas, respuesta_usuario)
            # prompt
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        system_prompt
                    ),
                    MessagesPlaceholder(variable_name="message"),
                ]
            )
    
            # create chain
            chain = prompt | self.llm | JsonOutputParser()

            chain_response = chain.invoke({'message':[HumanMessage(content=_task)]})
            # print(chain_response)
            # print(type(chain_response))
            # process response 
            # response = json.loads(chain_response.content)
            return chain_response
        
        elif type(lista_respuestas) is list:
            post = []
            for respuesta in lista_respuestas:
                post.append(f"{respuesta['author']['fullname']}: {respuesta['message']}")

            if len(post) == 2: 
                system_prompt = Prompts.prompt_foros(contexto, preguntas, post[0])
            elif len(post) == 3: 
                system_prompt = Prompts.prompt_foros(contexto, preguntas, post[0])
            elif len(post) == 4: 
                system_prompt = Prompts.prompt_foros(contexto, preguntas, post[0])

            # prompt
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        system_prompt
                    ),
                    MessagesPlaceholder(variable_name="message"),
                ]
            )
    
            # create chain
            chain = prompt | self.llm | JsonOutputParser()

            # chain response
            chain_response = chain.invoke({'message':[HumanMessage(content=_task)]})
            # print(chain_response)
            # print(type(chain_response))
            # # process response 
            # response = json.loads(chain_response)

            return chain_response
        

    # Función para extraer contenido de la lista de diccionarios que contiene "Contexto", "Caso"
    def extract_content(self, intro, section_name):
        pattern = rf'<strong>{section_name}</strong></h3>\s*<p>(.*?)</p>'
        match = re.search(pattern, intro, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    # Función para extraer las preguntas de la sección TAREA
    def extract_tarea_questions(self, intro):
        pattern = r'<h3><strong>TAREA:</strong></h3>\s*<p>.*?</p>\s*<ul>(.*?)</ul>'
        match = re.search(pattern, intro, re.DOTALL)
        if match:
            ul_content = match.group(1).strip()
            # Extraer las preguntas dentro de <li>
            questions = re.findall(r'<li><em>(.*?)</em></li>', ul_content, re.DOTALL)
            return questions
        return None


    def execute(self) -> dict:
            """
            Función que ejecuta el proceso de obtención de los cursos, foros, discusiones y posts, luego ejecuta el modelo para generar la
            retroalimentación por posts de cada estudiante. Lo anterior se hace usando las funciones anteriores.
            """
            courses = self.__moodle_flow.get_courses()
            # display(courses)
            current_time = int(time.time())
            available_courses = [course for course in courses if course['enddate'] == 0 or course['enddate'] > current_time]

            # este diccionario almacena las retroalimentaciones por curso y por discusión
            feedback_by_course_discussion = {}

            for course in available_courses:
                forums = self.__moodle_flow.get_forums_by_course(course['id'])
                
                # obtener la fecha actual
                current_time = int(time.time())
                
                # filtrar los foros disponibles
                available_forums = [forum for forum in forums if forum['cutoffdate'] == 0 or forum['cutoffdate'] > current_time]
                foro_1 = available_forums[0]
                id_modulo_foro = foro_1['id']
                # display(foro_1)


                if 'intro' in foro_1:
                    intro = foro_1['intro']
                    contexto_foro = self.extract_content(intro, "CONTEXTO")
                    caso = self.extract_content(intro, "CASO")
                    lista_preguntas_tarea = self.extract_tarea_questions(intro)
                    preguntas_unificadas_tarea = " ".join(lista_preguntas_tarea)

                # display(contexto_foro)
                # display(caso)
                # display(preguntas_unificadas_tarea)
                
                ## Creando una lista de un solo elemento (foro_1)
                lista_foro_1 = []
                lista_foro_1.append(foro_1)

                for forum in lista_foro_1:
                    discussions = self.__moodle_flow.get_discussions_by_forum(forum['id'])
                    # organizar discusiones por fecha de creación
                    sorted_discussions = sorted(discussions, key=lambda x: x['created'], reverse=True)
                    # display(sorted_discussions)
                    # Si se quiere tomar solo la última discusión (último post)
                    # primera_discusion = []
                    # primera_discusion.append(sorted_discussions[0])
                
                    for discussion in sorted_discussions:
                        posts = self.__moodle_flow.get_posts_by_discussion(discussion['discussion'])
                        
                        # display(posts)

                        if posts[0]["subject"] == "Re: Retroalimentaciones":
                            print('El post ya cuenta con la Retroalimentacion') 
                            continue
                        else:
                            contador = 0
                            for post in posts:
                                if post["subject"] != "Re: Retroalimentaciones":
                                    contador += 1
                                # else:
                                #     break

            
                            if contador == 1:
                                # print( f'primer post : {posts[0]}')
                                feedback_message = self.__run_model(caso, preguntas_unificadas_tarea, posts[0]) 
                            elif contador == 2:
                                # print(f'respuesta del post : {posts[:2]}')
                                feedback_message = self.__run_model(caso, preguntas_unificadas_tarea, posts[:2])
                            else:
                                # print(posts[:contador])
                                feedback_message = self.__run_model(caso, preguntas_unificadas_tarea, posts[:contador])
                            
                            # display(feedback_message)
                            # display(type(feedback_message))
                            usuario_list = list(feedback_message.keys())
                            html_list = list(feedback_message.values())

                            if course['fullname'] not in feedback_by_course_discussion:
                                feedback_by_course_discussion[course['fullname']] = {}

                            if discussion['id'] not in feedback_by_course_discussion[course['fullname']]:
                                feedback_by_course_discussion[course['fullname']][discussion['id']] = []

                            for i in range(len(feedback_message)):    
                                feedback_by_course_discussion[course['fullname']][discussion['id']].append({
                                    'discussionid': discussion['id'],
                                    'usuario': usuario_list[i].split('_')[0],
                                    'html': html_list[i][0],
                                    'calificacion': html_list[i][1]
                                })

                                # contextid = int(posts[0]['html']['rating'].split('name="contextid" value="')[1].split('"')[0])
                                # display(contextid)
                                # itemid = int(posts[0]['html']['rating'].split('name="itemid" value="')[1].split('"')[0])
                                # display(itemid)
                                # rateduserid = int(posts[0]['html']['rating'].split('name="rateduserid" value="')[1].split('"')[0])
                                # display(rateduserid)
                                # rating = int(html_list[i][1][-1])
                                # display(rating)

                                # display(id_modulo_foro)
                                # # función para calificar el post
                                # self.__moodle_flow.calificar_post(id_modulo_foro, itemid, rateduserid, rating)
                            
            # se ordenan las retroalimentaciones de los usuarios
            for course in feedback_by_course_discussion:
                for discussion in feedback_by_course_discussion[course]:
                    feedback_by_course_discussion[course][discussion] = feedback_by_course_discussion[course][discussion][::-1]
            # display(feedback_by_course_discussion)
            self.__moodle_flow.subir_feedback(feedback_by_course_discussion)
            return True
