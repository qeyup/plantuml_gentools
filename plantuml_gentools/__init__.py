import sys

import plantuml

from enum import Enum

Id=0
Objects=[]
class Object():
    def __init__(self, Type, name="", contentIn = None, Color=""):
        global Id
        global Objects

        Id+=1
        self.name = name.replace("\n","\\n")
        self.ID = ("ID_%s" % Id)
        self.type = Type
        self.contanedList = []
        self.Color = Color
        
        if self.name == "":
            self.Code = ("%s %s") % (self.type, self.ID)
        else:
            self.Code = ("%s \"%s\" as %s %s") % (self.type, self.name, self.ID, self.Color)

        if contentIn is None:
            Objects.append(self)
        else:
            contentIn.contanedList.append(self)

Connections=[]
def connect(A, B, Color="", Style="-", Dir="", LConn="<", RConn=">"):
    global Connections

    Conector="%s-%s-%s" % (LConn, Dir, RConn)
    Conector=Conector.replace("-", Style)
    if A is not None and B is not None:
        Connections.append(("%s %s %s %s\n") %(A.ID, Conector, B.ID, Color))

aligns=[]
def AlignObjects(ObjectList, Dir="", Space=0):
    global aligns
    Add="-"
    for i in range(0,Space):
        Add+="-"
    for i in range(len(ObjectList) - 1):
        obj1 = ObjectList[i]
        obj2 = ObjectList[i+1]
        aligns.append(("%s -[hidden]%s%s %s\n") % (obj1.ID, Dir, Add, obj2.ID))

Title=""
def SetTittle(NewTitle):
    global Title
    global FileName
    Title = ("\n\ntitle %s\n\n") % (NewTitle)

def Exit(invert=False, Output=""):
    global Objects
    global FileName

    def GenObjCode(ObjecList, curret_indent=""):
        ObjectCode=""
        for obj in ObjecList:
            ObjectCode +="%s%s" % (curret_indent, obj.Code)
            if len(obj.contanedList) > 0:
                ObjectCode+="{\n"
                ObjectCode+=GenObjCode(obj.contanedList, (("%s\t") % (curret_indent)))
                ObjectCode+="%s}" % curret_indent
            ObjectCode+="\n"
        return ObjectCode

    puml=""
    puml +="@startuml\n"

    puml +="%s" % Title
    
    if invert:
        puml += "left to right direction\n"


    puml += "%s" % GenObjCode(Objects)

    puml += "\n"

    for align in aligns:
        puml += "%s" % align

    puml += "\n"

    for con in Connections:
        puml += "%s" % con


    puml += "@enduml\n"

    if Output=="":
        #print("%s" % puml)

        url = "http://www.plantuml.com/plantuml/svg/" + plantuml.deflate_and_encode(puml)
        print("![image](%s)" % url)
    else:
        f = open(("%s.puml" % (Output)), 'w+')
        f.write(puml)
        f.close()