import requests

class MoodleWorkflow:


    def __init__(self, url_becat:str, becat_token:str):

        self.__url_becat = url_becat
        self.__becat_token = becat_token
    

    def get_courses(self):
        """
        Esta función toma la url de Moodle y el token, también toma los cursos (en caso de que hayan otros cursos que no correspondan)
        """
        url = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'core_course_get_courses',
            'moodlewsrestformat': 'json'
        }
        response = requests.get(url, params=params)
        courses = response.json()
        # return courses
        print("Courses response:", courses)
        if isinstance(courses, list):
            # filtered_courses = [course for course in courses if course['fullname'] in ['test IA Col']]
            filtered_courses = [course for course in courses if course['fullname'] in ['Teología fundamental']]
                
        else:
            print("Unexpected courses response format")
            filtered_courses = []
        return filtered_courses

    def get_forums_by_course(self, course_id):
        """
        Esta función toma los foros por cada curso.
        """
        url = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_forum_get_forums_by_courses',
            'moodlewsrestformat': 'json',
            'courseids[0]': course_id
        }
        response = requests.get(url, params=params)
        forums = response.json()
        print(f"Foros del curso {course_id}:", forums)
        if isinstance(forums, list):
            return forums
        else:
            print(f"Unexpected forums response format for course {course_id}")
            return []

    def get_discussions_by_forum(self, forum_id):
        """
        Esta función toma las discusiones por curso.
        """
        url = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_forum_get_forum_discussions',
            'moodlewsrestformat': 'json',
            'forumid': forum_id
        }
        response = requests.get(url, params=params)
        discussions = response.json()
        print(f"Discusiones del foro {forum_id}:", discussions)
        if isinstance(discussions, dict) and 'discussions' in discussions:
            return discussions['discussions']
        else:
            print(f"Formato de respuesta de discusiones inesperadas para el foro {forum_id}")
            return []

    def get_posts_by_discussion(self, discussion_id):
        """
        Esta función toma los posts por discusión.
        """
        url = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_forum_get_discussion_posts',
            'moodlewsrestformat': 'json',
            'discussionid': discussion_id
        }
        response = requests.get(url, params=params)
        posts = response.json()
        # print(f"Posts de la discusión {discussion_id}:", posts)
        if isinstance(posts, dict) and 'posts' in posts:
            return posts['posts']
        else:
            print(f"Formato de respuesta de discusiones inesperadas para el foro {discussion_id}")
            return []

    def subir_feedback(self,feedback_by_course_discussion):
        """
        Esta función se encarga de diseñar el formato de la retroalimentación para cada usuario, y luego subirlo a Moodle.
        """
        url = self.__url_becat
        
        for course_name, discussions in feedback_by_course_discussion.items():
            for discussion_id, feedback_list in discussions.items():
                feedback_messages = ""
                puntos = ": "
                for feedback in feedback_list:
                    # feedback_messages += f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong><span style='background-color: #AEC6CF'>{feedback['html']}</span><br><br> {feedback['calificacion']}"
                    # feedback_messages += f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong><span style='background-color: #AEC6CF; display: inline;'>{feedback['html']}</span><span style='display: inline;'><strong>Calificación sugerida:</strong> {feedback['calificacion'].split(': ')[1]}</span><br><br>"
                    feedback_messages += (
                    f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong>"
                    f"<span style='background-color: #AEC6CF; display: inline;'>{feedback['html']}</span><br>"
                    f"<div style='display: inline;'><strong>Calificación:</strong> {feedback['calificacion'].split(': ')[1]}</div><br><br>")



                data = {
                    'wstoken': self.__becat_token,
                    'wsfunction': 'mod_forum_add_discussion_post',
                    'moodlewsrestformat': 'json',
                    'postid': discussion_id,
                    'subject': 'Re: Retroalimentaciones',
                    'message': feedback_messages
                }
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"Retroalimentación subida correctamente para la discusión {discussion_id} del curso {course_name}")
                else:
                    print(f"Error al subir la retroalimentación para la discusión {discussion_id} del curso {course_name}: {response.text}")



    def calificar_post(self, contextid, itemid, rateduserid, rating):
        """
        Subir una calificación a un post en Moodle.

        Args:
            base_url (str): La URL base de tu instancia de Moodle (ej. "https://aula.becat.online")
            token (str): El token de acceso a la API de Moodle.
            contextid (int): ID del contexto.
            itemid (int): ID del ítem (el post a calificar).
            rateduserid (int): ID del usuario a calificar.
            rating (int): La calificación a asignar.

        Returns:
            dict: La respuesta de la API de Moodle.
        """
        url = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'core_rating_add_rating',
            'moodlewsrestformat': 'json',
            'contextid': contextid,
            'component': 'mod_forum',
            'ratingarea': 'post',
            'itemid': itemid,
            'scaleid': 10,  # Escala
            'rating': rating,
            'rateduserid': rateduserid,
        }

        response = requests.post(url, data=params)
        response_json = response.json()
        print(f"Response JSON: {response_json}")

        if response.status_code == 200:
            print("Calificación subida correctamente")
        else:
            print(f"Error al subir la retroalimentación: {response_json}")
        return response_json
    

############################# TAREAS ################################


    def get_assignments_by_course(self, course_id):
        """
        Esta función toma las tareas por cada curso.
        """
        endpoint = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_assign_get_assignments',
            'moodlewsrestformat': 'json',
            'courseids[0]': course_id
        }
        response = requests.get(endpoint, params=params)
        assignments = response.json()
        print(f"Tareas del curso {course_id}:", assignments)
        if 'courses' in assignments:
            return assignments['courses']
        else:
            print(f"Unexpected assignments response format for course {course_id}")
            return []
        
    def get_submissions_by_assignment(self, assignment_id):
        """
        Esta función obtiene los envíos para una tarea específica.
        """
        endpoint = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_assign_get_submissions',
            'moodlewsrestformat': 'json',
            'assignmentids[0]': assignment_id
        }
        response = requests.get(endpoint, params=params)
        submissions = response.json()
        # print(f"Envíos para la tarea {assignment_id}:", submissions)
        return submissions
        # if 'assignments' in submissions:
        #     return submissions['assignments']
        # else:
        #     print(f"Unexpected submissions response format for assignment {assignment_id}")
        #     return []

    def get_grades_by_assignment(self, assignment_id):
        """
        Esta función obtiene las calificaciones para una tarea específica.
        """
        endpoint = self.__url_becat
        params = {
            'wstoken': self.__becat_token,
            'wsfunction': 'mod_assign_get_grades',
            'moodlewsrestformat': 'json',
            'assignmentids[0]': assignment_id
        }
        response = requests.get(endpoint, params=params)
        grades = response.json()

        return grades


    def save_feedback_and_grade(self, assignment_id, user_feedback, 
                                addattempt=0, workflowstate='submitted', 
                                applytoall=0, plugin_data=None):
        """
        Esta función guarda la retroalimentación y calificación para los envíos de una tarea.
        
        :param assignment_id: ID de la tarea a la que se va a guardar la retroalimentación.
        :param user_feedback: Diccionario con información de retroalimentación y calificación.
        :param addattempt: Permite otro intento si el método de reapertura del intento es manual.
        :param workflowstate: El siguiente estado del flujo de trabajo de calificación.
        :param applytoall: Si es verdadero, esta calificación se aplicará a todos los miembros del grupo (para tareas grupales).
        :param plugin_data: Datos adicionales del plugin (opcional).
        """
        endpoint = self.__url_becat
        token = self.__becat_token

        user_id = user_feedback['id_usuario']
        feedback_text = user_feedback['Feedback']
        grade = user_feedback['Calificación']
        
        # Si no se proporciona plugin_data, se establece como un diccionario vacío
        if plugin_data is None:
            plugin_data = {}

        params = {
            'wstoken': token,
            'wsfunction': 'mod_assign_save_grade',
            'moodlewsrestformat': 'json',
            'assignmentid': assignment_id,
            'userid': user_id,
            'grade': grade,
            'attemptnumber': 0,  #  el número de intentos
            'addattempt': addattempt,  # permite otro intento
            'workflowstate': workflowstate,  # estado del flujo de trabajo
            'applytoall': applytoall,  # aplicar a todos los miembros del grupo
            'plugindata[assignfeedbackcomments_editor][text]': feedback_text,
            'plugindata[assignfeedbackcomments_editor][format]': 1,  # formato HTML
            'plugindata[files_filemanager]': plugin_data.get('files_filemanager', 0)  # ID del área de borradores con archivos para esta retroalimentación
        }

        response = requests.post(endpoint, data=params)
        result = response.json()
        print(f"Resultado para el usuario {user_id}:", result)
        