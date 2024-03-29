Пожары Карелии
==============

Интерактивное веб-приложение, позволяющее оценить количество пожаров, их влияние на экономику региона, а также количество местных жителей, готовых добровольно помогать тушить пожары.

![example](example.gif)

Запуск
------

Чтобы запустить приложение, создайте новую виртуальную среду и установите зависимости:

`pip install -r requirements.txt`

или 

`conda install --file requirements.txt -c conda-forge`,

если используете `conda`.

Далее выполните 

```bash
git clone https://github.com/pepperke/karelia_fires.git 
cd karelia_fires
python3 app.py
```

и перейдите по адресу `localhost:8050`

---

Данные пожаров были предоставлены Карельским республиканским
отделением Общероссийской общественной организации Всероссийское
добровольное пожарное общество (http://vdpo.karelia.info/)

Данные о районах Карелии были получены с помощью <a href="http://overpass-turbo.eu">
Overpass API</a> на базе <a href="https://www.openstreetmap.org">OpenStreetMap</a>.