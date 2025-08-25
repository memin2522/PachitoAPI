import logging

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas import QuestionSchema, AnswerSchema

blp = Blueprint("Main", __name__)
iaResponse = None
appQuestion = None
hasAnswered = False

@blp.route("/")
class MainOperations(MethodView):
    def get(self):
        return "<h1>This is the main page of the Middleware PachitoIA api. If you see this everything is working correctly</h1>"

@blp.route("/question")
class QuestionOperations(MethodView):

    @blp.arguments(QuestionSchema)
    @blp.response(201, QuestionSchema)
    def post(self, question_data):
        global appQuestion
        if(appQuestion != None):
            appQuestion = question_data
            return appQuestion
        else:
            abort(400, message="There is already a question being procesed") 
    
    @blp.response(201, QuestionSchema)
    def get(self):
        global appQuestion
        if(appQuestion != None):
            response = appQuestion
            appQuestion = None
            return response
        else:
            abort(400, message="There is no question to return") 

@blp.route("/answer")
class AnswerOperations(MethodView):

    @blp.arguments(AnswerSchema)
    @blp.response(201, AnswerSchema)
    def post(self, answer_data):
        iaResponse = answer_data
        return iaResponse
    
    @blp.response(201, AnswerSchema)
    def get(self):
        global iaResponse
        if(iaResponse != None):
            response = iaResponse
            iaResponse = None
            return response
        else:
            abort(400, message="There is no answer to return") 

@blp.route("/health")
def health():
    return "OK", 200