import os

class Config:
    SECRET_KEY = 'rinkorea!@#$%'  # 비밀 키는 앱의 보안을 위해 필요해요
    SQLALCHEMY_DATABASE_URI = 'postgres://default:J1rmacjwKln3@ep-wild-forest-a19y89pw.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require'  # 데이터베이스 연결 정보
    SQLALCHEMY_TRACK_MODIFICATIONS = False