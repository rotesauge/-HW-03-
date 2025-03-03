установка

  git clone https://github.com/rotesauge/-HW-03-
  
  cd ./-HW-03-
  
  sudo make

Методы
*********************************************************************************************
POST /api/submitData/  Метод submitData принимает JSON в теле запроса с информацией о перевале.

Тело запроса:

{

  "beauty_title": "string", - вид объекта(гора,перевал,тропа)
  
  "title": "string",  - имя
  
  "other_titles": "string", - дополнительное описание
  
  "connect": "string",      - дополнительное описание
  
  "add_time": "string" example "2021-09-22 13:18:13", - дата добавления
  
                       пользователь 
		       
  "user": {"email": "string", 		почта
  
           "fam": "string",       фамилия  
	   
		       "name": "string",      имя
	 
		       "otc": "string",       отчество
	 
           "phone": "string"},    телефон
	   
   "coords":{                     координаты
   
  "latitude": "float",            широта
  
  "longitude": "float",           долгота
  
  "height": "int"},               высота нан уровнем моря
  


  level:{"winter": "string",     уровень сложности зимой
  
  "summer": "string",           уровень сложности летом
  
  "autumn": "string",           уровень сложности осенью
  
  "spring": "string"},          уровень сложности весной
  
   "images": [
   
   		{"data":"bytea",   - данные изображения 
   
               title:"string"},  - описание
	       
             ]
	     
}

--------------------------------------------------------------------------------------------

Результат метода: JSON

Примеры:



{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}

{ "status": 200, "message": null, "id": 42 }



*********************************************************************************************


GET /api/submitData/<id> — получить одну запись (перевал) по её id.
Пример: http://89.169.160.83:8000/api/submitData/1

--------------------------------------------------------------------------------------------

Результат метода: JSON



{"status": 200, 

  "message": 
  
              { "date_added ":  "2024-12-05 13:16:16.890441 ",
	      
	        "beautyTitle ":  "string",
	 
	        "title ":  "string ",
	 
	        "other_titles ":  "string ",
	 
	        "connect":  "string",
	 
	        "level_winter ":  " ",
	 
	        "level_summer ":  "string",  
	 
	        "level_autumn ":  "string" 
	 
	        "level_spring ":  "string",  
	 
	        "status ":  "string"}
	 

       
}

*********************************************************************************************

PATCH /submitData/<id> — отредактировать существующую запись (замена), если она в статусе new.

Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона. 

Тело запроса:

{

  "beauty_title": "string", - вид объекта(гора,перевал,тропа)
  
  "title": "string",  - имя
  
  "other_titles": "string", - дополнительное описание
  
  "connect": "string",      - дополнительное описание
  
  "add_time": "string" example "2021-09-22 13:18:13", - дата добавления
  
                       пользователь
		       
  "user": {"email": "string", 	почта
  
           "fam": "string",       фамилия  
	   
		       "name": "string",      имя
	 
		       "otc": "string",       отчество
	 
           "phone": "string"},    телефон
	   
   "coords":{                     координаты
   
  "latitude": "float",            широта
  
  "longitude": "float",           долгота
  
  "height": "int"},               высота нан уровнем моря
  


  level:{"winter": "string",     уровень сложности зимой
  
  "summer": "string",           уровень сложности летом
  
  "autumn": "string",           уровень сложности осенью
  
  "spring": "string"},          уровень сложности весной
  

 
   "images": [{"data":"bytea",   - данные изображения 
   
               title:"string"},  - описание
	       
             ]
	     
}

--------------------------------------------------------------------------------------------

Результат метода: JSON

Примеры:

{ "state": 1 } — удалось отредактировать запись в базе данных.

{ "state": 0 } — не удалось отредактировать запись в базе данных.




*********************************************************************************************

GET /submitData/?user__email=<email> — список данных обо всех объектах,
                                       которые пользователь с почтой <email> отправил на сервер.
				       
--------------------------------------------------------------------------------------------

Результат метода: JSON

{

"status": 200, 

  "message": [
  
              { "date_added ":  "2024-12-05 13:16:16.890441 ",
	      
	        "beautyTitle ":  "string",
	 
	        "title ":  "string ",
	 
	        "other_titles ":  "string ",
	 
	        "connect":  "string",
	 
	        "level_winter ":  " ",
	 
	        "level_summer ":  "string",  
	 
	        "level_autumn ":  "string", 
	 
	        "level_spring ":  "string", 
	 
	        "status ":  "string"}
	 
	     ] 
      
}

*********************************************************************************************
