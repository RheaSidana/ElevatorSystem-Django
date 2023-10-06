<h1>Elevator System</h1>

<h5>Assumptions: <br/> 
    1. This is used by one building only right now. <br/>
    2. Each request contians the number of people onboarding and offborading on floors, 
    inorder to implement people capacity of the Elevator. <br/>
    3. Each Elevator has the request capacity = 8 from the Floors, 
    if the nearest elevator request capacity is full 
    then other elevator is searched to fulfill the request
</h5>
<br/>
<h3>Functionality:</h3>
<h3>
    1. Add/Retrieve Number of Floors  <br/>
    2. Add/Retrieve Number of Elevator  <br/>
    3. Add Requests for Calling the Elevator on Floors  <br/>
    4. Add Requests from the Elevator to Reach on a Floors  <br/>
    5. Mark Elevator as working, in maintainence or non-operational  <br/>
    6. Add Requests from the Elevator to Open or Close a door  <br/>
    7. Retrieve the next destination of a particular Elevator  <br/>
    8. Fulfill the next destination of all the Elevators  <br/>
    9. Retrieve Requests for all Callings on Floors, of the particular Elevator (certain date)  <br/>
    10. Retrieve Requests from the particular Elevator to Reach on a Floors (certain date)  <br/>
    11. Retrieve the moving direction of a particular Elevator <br/>
    <br/>
    ** Redis is implemented on Data Seeded models, ElevatorFunctionality and Floor
</h3>
<br/>
<br/>
<br/>
<h4>Functionality left for implementation: </h4>
<h5>
    1. Implementing Redis caching on all models <br/>
    2. Writing test for all the functions in the project.<br/>
</h5>
<br/>
<br/>
<br/>
<hr/>
<h1>Installation</h1>

<h3>1. Clone the repo</h3>

```
git clone https://github.com/RheaSidana/ElevatorSystem-Django.git
```

<h4>cd in the cloned project folder</h4>
<br/>
<br/>
<h3>2. Create Virtual Environment for the project</h3>
<h4>This project was built using Python 3.10.11</h4>

```
python -m venv venv
```

<br/>
<br/>
<h4>Activate the virtual environment on VS terminal</h4>

```
venv\Scripts\activate
```

<br/>
<br/>
<h3>3. Install the packages: </h3>

```
pip install -r requirements.txt
```

<br/>
<br/>
<h3>4. Postgres: </h3>
<h4>Update the DATABASES dict according to the configuration on your system</h4>

```
File: elevatorSystem/settings.py
```

<br/>
<br/>
<h3>5. Redis: </h3>
<h4>Update the CACHES dict according to the configuration on your system</h4>
<h4>Cache will remain alive for 1 hr if no change occurs</h4>

```
File: elevatorSystem/settings.py
```

<br/>
<br/>
<h3>6. Migrations: </h3>

```
python manage.py makemigrations
```

```
python manage.py migrate
```

<br/>
<br/>
<h3>7. Create Super User:</h3>
<h4>to view all the tables in the ADMIN url</h4>

```
python manage.py createsuperuser
```

<h4>add username, email and password</h4>
<br/>
<br/>
<h3>8. Data Seeding the tables</h3>

```
python manage.py seed_data
```

<br/>
<br/>
<h3>9. Run the server: </h3>

```
python manage.py runserver
```

<br/>
<br/>
<h3>10. Run the tests</h3>
<h4>a. dataSeeding app tests</h4>

```
python manage.py test dataSeeding
```

<br/>
<br/>
<h4>b. elevator app tests</h4>

```
python manage.py test elevator
```

<br/>
<br/>
<hr/>
<h1>APIs: </h1>
<h3> Port: 3033</h3>
<a href="https://documenter.getpostman.com/view/28378586/2s9XxyRDnr">
    Postman Documentation of the APIs
</a>

<br/>
<a href="[https://documenter.getpostman.com/view/28378586/2s9XxyRDnr](https://drive.google.com/drive/folders/1xRWzTSe5S97YSzpAv0qpzyVkmAP5byqa?usp=sharing)https://drive.google.com/drive/folders/1xRWzTSe5S97YSzpAv0qpzyVkmAP5byqa?usp=sharing">
    Video Description of the APIs
</a>

