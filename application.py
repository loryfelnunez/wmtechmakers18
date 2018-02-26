from flask import Flask
application = Flask(__name__)
application.debug = True

@application.route('/', methods=['GET'])
def hello():
 return '<p>Hello World</p>'

if __name__ == '__main__':
 application.run()
 