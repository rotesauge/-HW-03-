Метод POST submitData

Метод submitData принимает JSON в теле запроса с информацией о перевале. Ниже находится пример такого JSON-а:

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
 
   "images": [{"data":"bytea",   - данные изображения 
               title:"string"},  - описание
             ]
}

Результат метода: JSON

Примеры:

{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}
{ "status": 200, "message": null, "id": 42 }
