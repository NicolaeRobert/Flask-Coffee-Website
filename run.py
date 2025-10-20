from app import create_app

#Here we create the instance of the app using the function create_app()
app=create_app()

#Here we run the whole app
if __name__=="__main__":
    app.run(debug=True)