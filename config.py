# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wmtechmakers18:wmtechmakers18@wmtechmakers18.cqf2qq23tddm.us-east-1.rds.amazonaws.com:3306/wmtechmakers18'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'ertELkS0jRXGH7uQ0vOvyJqD9tE6o9vRJ6tK/ic1'