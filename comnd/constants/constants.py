equiv = {
    "Aguascalientes": 2, "Baja California": 1343, "Baja California Sur": 3675, "Campeche": 4643, "Chiapas": 5950,
    "Chihuahua": 13376, "Coahuila": 23517, "Coahuila de Zaragoza": 23517, "Colima": 27276, "Ciudad de México": 21957,
    "Durango": 28101, "Estado de México": 60991, "México": 60991, "Guanajuato": 34615, "Guerrero": 44387,
    "Hidalgo": 49185, "Jalisco": 55288, "Michoacán": 69186, "Morelos": 79437, "Nayarit": 81170, "Nuevo León": 83091, "Oaxaca": 87725,
    "Puebla": 94289, "Querétaro": 99788, "Quintana Roo": 102945, "San Luis Potosí": 104145, "Sinaloa": 110162,
    "Sonora": 114280, "Tabasco": 122904, "Tamaulipas": 125460, "Tlaxcala": 128714, "Veracruz": 130263,
    "Veracruz de Ignacio de la Llave": 130263, "Yucatán": 139245, "Zacatecas": 141001
}

query_existence = "SELECT JobID, JobRefCode FROM Jobs (nolock) WHERE RecruiterID = CAST(? AS VARCHAR(255)) AND JobRefCode IN({});"
xmx = 'xmxaigredirx'
company = 'AIG'

info_type = "info"
error_type = "error"
information_process_started_message = "Proceso de publicación de vacantes, iniciado."
information_process_finished_message = "Proceso de publicación de vacantes, concluido."
total_jobs_in_file_message = "Total de vacantes en el archivo: {}"
total_jobs_to_discard_message = "Total de vacantes que ya existen: {}"
total_jobs_to_process = "Total de vacantes nuevas a procesar: {}"
vacancy_published_message = "{} - https://www.occ.com.mx/empleo/oferta/{}"
discount_point_error_message = "Can't discount point, The account doesn't have credits."
published_vacancies_count_message = "Total de vacantes nuevas publicadas: {}"
not_published_vacancies_count_message = "Total de vacantes no publicadas: {}"
vacancies_without_points_message = "Total de vacantes no publicadas por falta de puntos: {}"
error_count_message = "Errores detectados en el momento del proceso: {}"
