# Generated from FieldPath.g4 by ANTLR 4.7.1
from antlr4 import *

"""
  Copyright (c) 2018 MapR, Inc.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 """
from mapr.ojai.field_logic.Segment import NameSegment, IndexSegment
from mapr.ojai.field_logic.FieldPath import FieldPath


# This class defines a complete listener for a parse tree produced by FieldPathParser.
class FieldPathListener(ParseTreeListener):

    # Enter a parse tree produced by FieldPathParser#parse.
    def enterParse(self, ctx):
        pass

    # Exit a parse tree produced by FieldPathParser#parse.
    def exitParse(self, ctx):
        pass


    # Enter a parse tree produced by FieldPathParser#field_segment.
    def enterField_segment(self, ctx):
        pass

    # Exit a parse tree produced by FieldPathParser#field_segment.
    def exitField_segment(self, ctx):
        pass


    # Enter a parse tree produced by FieldPathParser#name_segment.
    def enterName_segment(self, ctx):
        pass

    # Exit a parse tree produced by FieldPathParser#name_segment.
    def exitName_segment(self, ctx):
        pass


    # Enter a parse tree produced by FieldPathParser#index_segment.
    def enterIndex_segment(self, ctx):
        pass

    # Exit a parse tree produced by FieldPathParser#index_segment.
    def exitIndex_segment(self, ctx):
        pass


