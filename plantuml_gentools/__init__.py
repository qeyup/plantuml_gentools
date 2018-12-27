import sys
import plantuml

# Pending points
# - include code in the output
# - Alings options


id = 0
class Object():

    def __init__(self, type, name="", color="", top_margin=1, bottom_margin=1, left_margin=10, right_margin=10, include_in=None):
        global id
        id += 1

        self.id = id
        self.type = type
        self.name = name
        self.color = color
        self.invert_draw_dir = True
        self.top_margin = top_margin 
        self.bottom_margin = bottom_margin 
        self.left_margin = left_margin 
        self.right_margin = right_margin

        self.include_list = []
        self.included = None

        self.connection_list = []

        if include_in is not None:
            include_in.Include(self)

    def Include(self, include_objs):
        if type(include_objs) == list:
            for obj in include_objs:
                if obj.included is not None:
                    obj.included.include_list.remove(obj)
                self.include_list.append(obj)
                obj.included = self
        else:
            if include_objs.included is not None:
                include_objs.included.include_list.remove(include_objs)
            self.include_list.append(include_objs)
            include_objs.included = self

    def Connect(self, connect_objs, color="", style="-", dir="", l_conn="<", r_conn=">", invert=False):
        connector="%s-%s-%s" % (l_conn, dir, r_conn)
        connector=connector.replace("-", style)
        
        if type(connect_objs) == list:
            for obj in connect_objs:
                self.connection_list.append([obj, connector, color, invert])
        else:
            self.connection_list.append([connect_objs, connector, color, invert])

    def GenObjectCode(self):
        code_line = ""

        top_margin=""
        for i in range(0,self.top_margin):
            top_margin+="\\n"
        bottom_margin=""
        for i in range(0,self.bottom_margin):
            bottom_margin+="\\n"
        left_margin=""
        for i in range(0,self.left_margin):
            left_margin+=" "
        right_margin=""
        for i in range(0,self.right_margin):
            right_margin+=" "

        name = self.name

        name= name.replace("\n", "\\n")
        name = name.replace("\\n", ("%s\\n%s") % (right_margin, left_margin))
        name = "%s%s%s%s%s" % (top_margin, left_margin, name, right_margin, bottom_margin)


        if self.name != "":
            code_line = ("%s \"%s\" as ID_%s") % (self.type, name, self.id)
        else:
            code_line = ("%s ID_%s") % (self.type, self.id)

        if self.color != "":
            if self.color.startswith("#"):
                code_line += (" %s") %(self.color)
            else:
                code_line += (" #%s") %(self.color)

        return code_line

    def GenContainerCode(self):
        def CodeIterate(object_list, used_object, indent=""):
            code = ""
            for obj in object_list:
                if obj in used_object:
                    print(("Object %s re-used") % (obj.id))
                    continue

                used_object.append(obj)

                code +="%s%s" % (indent, obj.GenObjectCode())
                if len(obj.include_list) > 0:
                    code+="{\n"
                    code+=CodeIterate(obj.include_list, used_object, (("%s\t") % (indent)))
                    code+="%s}" % indent
                code+="\n"
            return code

        def GenConnetionCode(main_obj, objects_list = None):
            code = ""
            for obj, connector, color, invert in main_obj.connection_list:
                if objects_list is not None:
                    if not obj in objects_list:
                        continue
                if not invert:
                    code += (("ID_%s %s ID_%s %s\n") % (main_obj.id, connector, obj.id, color))
                else:
                    code += (("ID_%s %s ID_%s %s\n") % (obj.id, connector, main_obj.id, color))
            return code

        code=""
        code +="@startuml\n"

        if self.name != "":
            code +="title %s\n" % self.name

        if self.invert_draw_dir:
            code += "left to right direction\n"

        used_object = []
        used_object.append(self)
        code+=CodeIterate(self.include_list, used_object)
        code+="\n"

        for obj in used_object:
            code += GenConnetionCode(obj, used_object)

        code += "\n"

        code += "@enduml\n"

        return code

    def GenContainerURL(self, format="png", print_URL=False, print_code=False):
        code = self.GenContainerCode()
        url = "http://www.plantuml.com/plantuml/" + format + "/" + plantuml.deflate_and_encode(code)
        if self.name != "":
            url = ("![%s](%s)") % (self.name, url)
        else:
            url = ("![image](%s)") % (url)

        if print_code:
            print(code)
        if print_URL:
            print(url)

        return url

    def SaveContainerPlantUML(self, file_name="out"):
        f = open(("%s.puml" % (file_name)), 'w+')
        f.write(self.GenContainerCode())
        f.close()



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
