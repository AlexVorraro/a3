from website import create_app

apppplication = create_app()

if __name__=='__main__':
    apppplication.run(host='0.0.0.0', port=8080, debug=True)


