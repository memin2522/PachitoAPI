from marshmallow import Schema, fields, post_dump
from datetime import datetime

class QuestionSchema(Schema):
    question = fields.Str(required=True)

class AnswerSchema(Schema):
    answer = fields.Str(required=True)

class WSAnswerSchema(Schema): 
    type = fields.Constant("answer")
    answer = fields.String(required=True) 
    jobId = fields.String(load_default=None)