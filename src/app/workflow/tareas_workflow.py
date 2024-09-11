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
from bs4 import BeautifulSoup


class TareasWorkflow:


    def __init__(self, llm:BaseLanguageModel, url_becat:str, token:str):
        """
        Esta función se conecta a la api de OpenAI y también recibe el token de Moodle 
        """
        self.__moodle_flow = MoodleWorkflow(url_becat, token)
        self.llm = llm

    def __run_model(self, preguntas, id_usuario, respuesta_usuario):

        # General taks
        _task = "Genera un feedback y calificación por cada respuesta de un alumno en una tarea."

        system_prompt = Prompts.prompt_tasks(preguntas, id_usuario, respuesta_usuario)
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
        
        return chain_response


    # Función para extraer el texto de cada entrega y devolverlo en una lista de diccionarios
    def extract_text_from_submissions(self, data):
        submissions_list = []
        for assignment in data['assignments']:
            for submission in assignment['submissions']:
                userid = submission['userid']
                # Accede a `editorfields` dentro de `plugins`
                for plugin in submission['plugins']:
                    if plugin['type'] == 'onlinetext':
                        for editorfield in plugin['editorfields']:
                            if editorfield['name'] == 'onlinetext' and editorfield['text'] != '':
                                # Crea un diccionario con `id_usuario` y `texto`
                                submissions_list.append({'id_usuario': userid, 'texto': editorfield['text']})
        return submissions_list
    

    def html_to_text(self, html_content):
        """
        Convierte el contenido HTML a un formato de texto legible.
        Preserva la numeración de las listas ordenadas.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        text_content = []

        # Extraer el texto de los párrafos
        for p in soup.find_all('p'):
            text_content.append(p.get_text(strip=True))

        # Extraer el texto de las listas ordenadas
        for ol in soup.find_all('ol'):
            for index, li in enumerate(ol.find_all('li'), start=1):
                text_content.append(f"{index}. {li.get_text(strip=True)}")

        # Convertir a una cadena de texto con saltos de línea
        return '\n'.join(text_content)


    def execute(self) -> dict:
            """
            Función que ejecuta el proceso de obtención de las tareas de los estudiantes en el modulo de tareas.
            Se ejecuta el modelo para generar una retroalimentación y calificación a cada tarea de los estudiantes.
            Esta retroalimentación y calificación se suben al moodle. 
            """
            courses = self.__moodle_flow.get_courses()
            current_time = int(time.time())
            available_courses = [course for course in courses if course['enddate'] == 0 or course['enddate'] > current_time]

            for course in available_courses:
                assignments = self.__moodle_flow.get_assignments_by_course(course['id'])
                preguntas = assignments[0]['assignments'][0]['intro']
                formatted_preguntas = self.html_to_text(preguntas)

                for assignment in assignments:
                    envios_tareas = self.__moodle_flow.get_submissions_by_assignment(assignment['assignments'][0]['id'])
                    # print(f"TAREAS ENVIADAS:{envios_tareas}")
                    lista_usuarios_con_textos = self.extract_text_from_submissions(envios_tareas)
                    
                    lista_id_usuarios_con_texto = [i['id_usuario'] for i in lista_usuarios_con_textos]
                    

                    # print('-'*20)
                    lista_usuarios_calificaciones = self.__moodle_flow.get_grades_by_assignment(assignment['assignments'][0]['id'])

                    lista_id_usuarios_assignments = []
                    for i in lista_usuarios_calificaciones['assignments']:
                        for j in i['grades']:
                            lista_id_usuarios_assignments.append(j['userid'])

                    # lista con los id comunes tanto para la lista de usuarios con texto y la lista de usuarios que trae 'get_grades_by_assignment'
                    lista_id_comunes = []
                    for i in lista_id_usuarios_assignments:
                        if i in lista_id_usuarios_con_texto:
                            lista_id_comunes.append(i)
                           
                    # lista_nueva = []
                    # for i in lista_id_usuarios_con_texto:
                    #     if i in lista_id_comunes:
                    #         lista_nueva.append(i)

                    lista_usuarios_calificaciones_filtrada = lista_usuarios_calificaciones['assignments'][0]['grades']
                    for i in lista_usuarios_calificaciones_filtrada:
                        print(i)

                    lista_nueva_filtrada_con_id = []
                    for i in lista_usuarios_calificaciones_filtrada:
                        if i['userid'] in lista_id_comunes:
                            lista_nueva_filtrada_con_id.append(i)

                    lista_diccionarios_sin_calificacion = []
                    for i in lista_nueva_filtrada_con_id:
                        if i['grade'] == '-1.00000':
                            lista_diccionarios_sin_calificacion.append(i)

                    if len(lista_diccionarios_sin_calificacion) == 0:
                        print("No hay nuevas tareas, las retroalimentaciones y calificaciones están actualizadas.")

                    elif len(lista_diccionarios_sin_calificacion) != 0:
                        
                        lista_id_sin_calificacion = []
                        for i in lista_diccionarios_sin_calificacion:
                            lista_id_sin_calificacion.append(i['userid'])

                        lista_id_texto = []
                        for i in lista_usuarios_con_textos:
                            if i['id_usuario'] in lista_id_sin_calificacion:
                                lista_id_texto.append(i)

                        for usuario in lista_id_texto: 
                            respuesta = self.__run_model(formatted_preguntas, int(usuario['id_usuario']), usuario['texto'])
                            self.__moodle_flow.save_feedback_and_grade(assignment['assignments'][0]['id'], respuesta)
                            

                        



                    