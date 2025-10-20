# Coffee website with Flask

This project is a web application developed using Flask, designed to practice Python and web development skills.

## 🧩Description of technologies

This project was created to deepen my programming knowledge and gain practical experience with web development. While learning **Python** independently, I wanted to explore building a full-stack web application, so I chose Flask as the backend framework.

The frontend is developed using **HTML** and **CSS**, keeping it simple and clean.

For data storage, I used **MySQL** to manage user information, including id, username, email, and hashed passwords, ensuring security best practices.

I also implemented **Flask Blueprints** to organize the project into modular components. This structure makes the application easier to maintain and extend, allowing separate parts of the project to be modified independently.

## 📝Description of the structure

Below you can see the project’s structure, and I’ll go over each part step by step.


```
project_root/
│
├── .vscode/
│
├── app/
│   ├── __pycache__/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── auth.py
│   ├── routes.py
│   └── utils.py
│
├── venv/
│
├── .env
├── README.md
├── requirements.txt
└── run.py
```

### 📁 Project Structure:


- **.vscode/** is the folder containing the Visual Studio Code workspace settings. I didn’t modify anything here.

- **app/** is the folder that holds the entire application.  
    - **__pycache__/** is a folder automatically created by Python. It stores compiled bytecode to make the program run faster. Whenever any file inside `app` is updated, Python will automatically regenerate this folder. You can delete it safely — Python will recreate it as needed.  
    - **__init__.py** is the file that creates the Flask app instance and applies all configurations. This is also where the blueprints are registered.  
    - **routes.py** is the file that defines the **main** blueprint, which represents the main pages of the web app.  
    - **auth.py** is the file that defines the **auth_var** blueprint, which handles routes for registration, login, logout, and registration confirmation.  
    - **utils.py** is the file that contains helper functions used throughout the project.  
    - **templates/** is the folder that contains the HTML files. Flask automatically recognizes it by name.  
    - **static/** is the folder that contains images and CSS files. Flask automatically recognizes it by name.  

- **venv/** is the virtual environment used to isolate the project dependencies.  

- **.env** is the file where sensitive information (like passwords and secret keys) is stored, and from which environment variables are loaded.  

- **README.md** is this file, which provides a description and documentation for the project.  

- **requirements.txt** is a text file listing all the Python packages and dependencies required for this project.  

- **run.py** is the file that imports the app factory from `app`, creates an instance of the Flask app, and runs the development server.

## ⚙️How to run it on your machine:

Before doing the steps below you have to install all the necessary things for MySQL to work. You also have to do some modifications so that you can connect to the SMTP server.

For this watch the following videos:

[MySQL setup for Windows](https://www.youtube.com/watch?v=50CQoMs4vRo&list=LL&index=6&t=557s "A youtube video for this")

[MySQL setup for Mac](https://www.youtube.com/watch?v=wpGnJHb2R58 "A youtube video for this")

[How to get a mail app password generated](https://www.youtube.com/watch?v=MkLX85XU5rU "A youtube video for this")



### 1️⃣ Clone the repository

For this you should use these commands in the terminal:

```
git clone https://github.com/your-username/your-project.git
cd your-project
```

### 2️⃣ Create and activate a virtual environment

```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install the dependencies

``` 
pip install -r requirements.txt 
```

### 4️⃣ Set up environment variables

Create a file named .env in the root folder and add your configuration, for example:

```
#The mail that I am using
EMAIL=your_email

#The mail app password
MAIL_PASSWORD=the mail app password generated

#The secret key of the app
APP_SECRET_KEY=a secret key

#The database password
DB_PASS=the password of yout MySQL database
```

### 5️⃣ Run the application

```
python run.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

## 🧠 Conclusion
This project helped me strengthen my understanding of Flask, backend development, and database management using MySQL.  
It was also a great opportunity to explore how different components of a web application work together.  