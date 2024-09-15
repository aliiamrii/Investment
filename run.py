from app import create_app

app = create_app()

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)

=======
    app.run(debug=True , host = '0.0.0.0', port =3002)
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
