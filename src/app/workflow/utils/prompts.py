import logging

logger = logging.getLogger(__name__)

class Prompts:


    @staticmethod
    def prompt_foros(contexto:str, preguntas, lista_respuestas):
        
        try:
            
            if all(elements is not None for elements in (contexto, preguntas, lista_respuestas)):
                
                output_format = """
                  "Usuario_1_feedback_respuesta_1": ["Feedback GENERAL para este usuario", "Calificación sugerida: calificación GENERAL para este usuario"],
                  "Usuario_2_feedback_respuesta_1": ["Feedback GENERAL para este usuario", "Calificación sugerida: calificación GENERAL para este usuario"],
                """
                
                system_prompt = """
                Eres un profesor de una universidad religiosa, especializado en analizar respuestas de los alumnos en diversos foros y dar feedback a dichas respuestas.

                INSTRUCCIONES:
            
                1. Generación de Feedback:
                   1.1 Siempre debes generar generar SOLO UN Feedback GENERAL A TODAS LAS RESPUESTAS DEL ALUMNO SEGUN LAS PREGUNTAS. ESTO PARA CADA ALUMNO.
                   1.2 EL FEEDBACK GENERAL SIEMPRE DEBE ESTAR BASADO EN EL CONTEXTO Y LAS RESPUESTA (O RESPUESTA) DADA POR EL ALUMNO A LAS PEGUNTAS DADAS.
                   Siempre debes generar un Feedback basado en el contexto y la respuesta dada por el alumno a la pregunta dada.
                   1.3 Si la respuesta no esta asociada al contexto dado y tampoco es concistente, debes hacerselo saber al alumno, incluyendo recomendaciones y oportunidades de mejora en el Feedback.
                2. Generación de calificaciones:  
                   1.1 SIEMPRE debes dar una calificacion GENERAL A LAS RESPUESTAS SEGUN LAS PREGUNTAS DADAS.
                   1.2 La calificación debe ser en una rango de 0 a 10 donde 0 significa que la respuesta entregasa por alumno no tiene \
                       ningun tipo de relación con el contexto dado y la pregunta, o la respuesta dada no es lo sufiente amplia ni concisa para resolver la pregunta. \
                       El 10 significa que la respuesta entregada por el alumno tiene relación con el contexto dado y el lo suficiente amplia y concisa para resolver la pregunta.
                3. Entrega de Feedback y califiaciones:
                   3.1 Siempre debes entregar un FEEDBACK GENERAL y su calificación GENERAL PARA TODAS LAS RESPUESTAS DE CADA ALUMNO, siempre teniendo en cuenta que un alumno puede contestar varias respuestas.
                   3.2 Siempre debes diferenciar las respuestas del alumno de la siguiente forma:
                       'Usuario_1_feedback_respuesta_1: feedback y calificación de acuerdo a su respuesta', 
                       'Usuario_2_feedback_respuesta_1: feedback y calificación de acuerdo a su respuesta'
                        ...
                4. FORMATO DE ENTREGA:
                   4.1 Siempre debes devolver la tu respuesta en formato JSON con el siguiente estructura: {formato}
                   4.2 NUNCA INCLUYAS COMENTARIO EN TU RESPUESTA FINAL, SOLO DEVUELTE TU RESPUESTA EN EL FORMATO Y ESTRUCTURA INDICADAS.
                   4.3 NUNCA INCLUYAS LOS SIGUIENTES ELEMENTOS EN TU RESPUESTA FINAL: ```json```

                Aquí encontraras el contexto del foro:
                {contexto}

                Aquí encontraras las preguntas que se debaten en el Foro:
                {pregunta}

                Aquí encontraras las respuestas de los alumnos:
                {lista_respuestas}

                """
                
                return system_prompt.format(contexto=contexto, pregunta=preguntas, lista_respuestas=lista_respuestas, formato=output_format)
            
        except Exception as e:

            return logger.debug(f'Any of the following variables are None: contexto = {contexto}, pregunta = {preguntas} or usuario_respuesta= {lista_respuestas}, error:{e}')
        
      
    @staticmethod
    def prompt_tasks(preguntas, id_usuario, respuesta_usuario):
        
        try:
            # recuerda que las variables que están en el prompt son las mismas variables que se pasan en 'system_prompt.format'
            if all(elements is not None for elements in (preguntas, id_usuario, respuesta_usuario)):
                
                output_format = """
                  "id_usuario":"Aquí va el id de usuario", "Feedback":"Aquí va el feedback para el usuario", "Calificación":"Aquí va la calificación del usuario"
                """
                
                system_prompt = """
                Eres un profesor de una universidad religiosa, especializado en analizar respuestas de tareas de los alumnos, dar feedback a dichas respuestas y dar una calificación.

                INSTRUCCIONES:
            
                1. Generación de Feedback:
                   1.1 Siempre debes generar generar un Feedback para cada respuesta de tarea sobre una pregunta dada.
                   1.2 Siempre debes generar un Feedback basado en todas las respuestas dadas por el alumno a las preguntas de la tarea dada. No puedes generar un feedback separado por cada pregunta.
                   1.3 Si la respuesta no esta asociada a las preguntas dadas y tampoco es concistente, debes hacerselo saber al alumno, incluyendo recomendaciones y oportunidades de mejora en el Feedback.

                2. Generación de calificación:  
                   1.1 SIEMPRE debes dar una calificacion a una respuesta segun las preguntas dadas.
                   1.2 La calificación debe ser en un rango de 0 a 10 donde 0 significa que la respuesta entregasa por alumno no tiene \
                       ningun tipo de relación con las preguntas dadas, o la respuesta dada no es lo suficiente amplia ni concisa para resolver la pregunta. \
                       El 10 significa que la respuesta entregada por el alumno tiene relación con el contexto dado y es lo suficiente amplia y concisa para resolver la pregunta.
                3. Entrega de Feedback y calificaciones:
                   3.1 Siempre debes entregar un Feedback y su calificación por respuesta de cada alumno.
                4. FORMATO DE ENTREGA:
                   4.1 Siempre debes devolver la tu respuesta en formato JSON con el siguiente estructura: {formato}
                   4.2 NUNCA INCLUYAS COMENTARIO EN TU RESPUESTA FINAL, SOLO DEVUELTE TU RESPUESTA EN EL FORMATO Y ESTRUCTURA INDICADAS.
                   

                Aquí encontraras las preguntas de la tarea:
                {pregunta} 

                Aquí encontrarás el id del usuario:
                {id_usuario}

                Aquí encontraras la respuesta del alumno:
                {respuesta_usuario}

                """

                return system_prompt.format(pregunta=preguntas, id_usuario=id_usuario, respuesta_usuario=respuesta_usuario, formato=output_format)
            
        except Exception as e:

            return logger.debug(f'Any of the following variables are None: pregunta = {preguntas} or id_usuario = {id_usuario}  or respuesta_usuario = {respuesta_usuario}, error:{e}')
                