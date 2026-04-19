# coding:utf-8
import base64
import numpy as np
import os
import re
from Bio import SeqIO
import pandas as pd
import configparser
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
# 创建一个配置解析器

app = Flask(__name__)
config = configparser.ConfigParser()
config.read(os.getcwd() + '/config.ini')
mysql = config.getboolean('DEFAULT', 'mysql')
debug = config.getboolean('DEFAULT', 'Debug')
# 获取Database部分的'Host'、'User'、'Password'和'Database'选项
host = config.get('Database', 'Host')
user = config.get('Database', 'User')
password = config.get('Database', 'Password')
database = config.get('Database', 'Database')
sql_str = None

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATE_FOLDER'] = 'templates'
# 开启输出底层执行的sql语句
app.config['SQLALCHEMY_ECHO'] = True
# 开启数据库的自动提交功能[一般不使用]
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#db = SQLAlchemy(app)
Bootstrap(app)
CORS(app)

# 配置日志
app.logger.setLevel(logging.INFO)  # 设置日志级别为 INFO
app.logger.info(sql_str)
# 创建一个 handler，用于写入日志文件
file_handler = RotatingFileHandler('../ReconstructionSpatialTranscriptome.log', maxBytes=1024 * 1024 * 100, backupCount=10)
file_handler.setLevel(logging.INFO)

# 再创建一个 handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 定义 handler 的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 给 app.logger 添加 handler
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

#with app.app_context():
#    db.create_all()

def initweb():
    current_directory = os.getcwd()
    current_directory = current_directory + '/'
    app.logger.info(current_directory)
    # try:
    #     os.mkdir(current_directory + "tempblast")
    # except FileExistsError:
    #     print('文件夹已存在')
    #
    # try:
    #     os.mkdir(current_directory + "fastastore")
    # except FileExistsError:
    #     print('文件夹已存在')

# 路由和视图函数
@app.route('/')
@cross_origin()
def index():
    app.logger.info('User accessed the index page.')
    initweb()
    return render_template('index.html')


@app.route('/about')
def about():
    app.logger.info('User accessed the about page.')
    return render_template('about.html')


@app.route('/qc')
def qc():
    app.logger.info('User accessed the qc page.')
    return render_template('qc.html')


if __name__ == '__main__':
    if debug:
        app.run(host='0.0.0.0', debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', debug=False, port=5000)

# pyinstaller -F MainPro.py --add-data 'templates:templates'
