import os

class Config:
    SECRET_KEY = 'rinkorea!@#$%'  # 비밀 키는 앱의 보안을 위해 필요해요
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://twoimo:~!!1qw23e@twoimo.mysql.pythonanywhere-services.com:3306/twoimo$bbs_db'  # 데이터베이스 연결 정보
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:test1234@localhost/memo_db'  # 데이터베이스 연결 정보
    SQLALCHEMY_TRACK_MODIFICATIONS = False