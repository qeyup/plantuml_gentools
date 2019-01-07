import sys
import plantuml
import traceback

# Pending points
# - Alings grid options


id = 0
class Object():

    def __init__(self, type="together", name="", color="", top_margin=1, bottom_margin=1, left_margin=10, right_margin=10, include_in=None):
        global id
        id += 1

        self.id = "ID_%i" % id
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
        """ Include objects inside the object
        :param include_objs Objects
        """
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

    def Connect(self, connect_objs, color="", style="-", dir=1, lengh=0, l_conn="<", r_conn=">", invert=False, hidden = False, label=""):
        """ Make connectio nbetween the object and the object list.
        :param 
        """
        while dir > 3:
            dir -= 4

        if dir <= 0:
            dir_code="right"
        elif dir == 1:
            dir_code="down"
        elif dir == 2:
            dir_code="left"
            #dir_code="right"
            #invert = not invert
        elif dir == 3:
            dir_code="up"
            #dir_code="down"
            #invert = not invert

        sep="-"
        for i in range(0,lengh):
            sep+="-"


        if hidden:
            connector = "-[hidden]%s%s" % (dir_code, sep)
        else:
            connector="%s-%s%s%s" % (l_conn, dir_code, sep, r_conn)
            connector=connector.replace("-", style)
        
        if type(connect_objs) == list:
            for obj in connect_objs:
                self.connection_list.append([self, obj, connector, color, invert, label])
        else:
            self.connection_list.append([self, connect_objs, connector, color, invert, label])

    def ConnectPair(self, object_list1, object_list2, color="", style="-", dir=1, lengh=0, l_conn="<", r_conn=">", invert=False, hidden = False, label=""):
        """ Include connection between external objects. 
        This connections will be included when the owner object is been included in the diagram.
        """
        while dir > 3:
            dir -= 4

        if dir <= 0:
            dir_code="right"
        elif dir == 1:
            dir_code="down"
        elif dir == 2:
            dir_code="left"
            #dir_code="right"
            #invert = not invert
        elif dir == 3:
            dir_code="up"
            #dir_code="down"
            #invert = not invert

        sep="-"
        for i in range(0,lengh):
            sep+="-"


        if hidden:
            connector = "-[hidden]%s%s" % (dir_code, sep)
        else:
            connector="%s-%s%s%s" % (l_conn, dir_code, sep, r_conn)
            connector=connector.replace("-", style)


        obj_list1 = []
        if type(object_list1) == list:
            obj_list1 = object_list1
        else:
            obj_list1.append(object_list1)

        obj_list2 = []
        if type(object_list2) == list:
            obj_list2 = object_list2
        else:
            obj_list2.append(object_list2)

        for obj1 in obj_list1:
            for obj2 in obj_list2:
                self.connection_list.append([obj1, obj2, connector, color, invert, label])

    def GenConnectionPair(self, objects_list, color="", style="-", dir=1, lengh=0, l_conn="<", r_conn=">", invert=False, hidden = False, label=""):
        """ Generate connections between external objects.
        It could be circular conections o one to each other connection.
        This connections will be included when the owner object is been included in the diagram.
        """
        while dir > 3:
            dir -= 4

        if dir <= 0:
            dir_code="right"
        elif dir == 1:
            dir_code="down"
        elif dir == 2:
            dir_code="left"
            #dir_code="right"
            #invert = not invert
        elif dir == 3:
            dir_code="up"
            #dir_code="down"
            #invert = not invert

        sep="-"
        for i in range(0,lengh):
            sep+="-"


        if hidden:
            connector = "-[hidden]%s%s" % (dir_code, sep)
        else:
            connector="%s-%s%s%s" % (l_conn, dir_code, sep, r_conn)
            connector=connector.replace("-", style)

        for i in range(0,len(objects_list)-1):
            self.connection_list.append([objects_list[i], objects_list[i+1], connector, color, invert, label])

    def GenObjectCode(self):
        """
        :param 
        """
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
            code_line = ("%s \"%s\" as %s") % (self.type, name, self.id)
        else:
            code_line = ("%s %s") % (self.type, self.id)

        if self.color != "":
            if self.color.startswith("#"):
                code_line += (" %s") %(self.color)
            else:
                code_line += (" #%s") %(self.color)

        return code_line

    def GenContainerCode(self):
        """
        :param 
        """
        def CodeIterate(obj, used_object, indent=""):
            code = ""
            if obj in used_object:
                print(("Object %s re-used") % (obj.id))
                return code

            used_object.append(obj)

            code +="%s%s" % (indent, obj.GenObjectCode())
            if len(obj.include_list) > 0:
                code+="{\n"
                for include_obj in obj.include_list:
                    code+=CodeIterate(include_obj, used_object, (("%s\t") % (indent)))
                code+="%s}" % indent
            code+="\n"
            return code

        def GenConnetionCode(main_obj, objects_list = None):
            code = ""
            for obj1, obj2, connector, color, invert, label in main_obj.connection_list:
                if color != "":
                    if not color.startswith("#"):
                        color = ("#%s") %(color)
                if objects_list is not None:
                    if not obj1 in objects_list:
                        continue
                    if not obj2 in objects_list:
                        continue
                if label != "":
                    label = " : %s" % label

                if not invert:
                    code += (("%s %s %s %s %s\n") % (obj1.id, connector, obj2.id, color, label))
                else:
                    code += (("%s %s %s %s %s\n") % (obj.id, connector, main_obj.id, color, label))
            return code

        code=""

        code +="@startuml\n"

        if self.name != "":
            code +="title %s\n" % self.name

        if self.invert_draw_dir:
            code += "left to right direction\n"

        used_object = []
        code+=CodeIterate(self, used_object)
        code+="\n"

        for obj in used_object:
            code += GenConnetionCode(obj, used_object)

        code += "\n"

        code += "@enduml\n"


        code += "\n\n"
        code += "'>=============\n"
        code += "'> SCRIPT CODE \n"
        code += "'>=============\n"
        code += "\n"
        try:
            stack = traceback.extract_stack()
            script_file = stack[0][0]

            with open(script_file, "r") as file:
                for line in file:
                    code += "'> %s" % line

        except:
            pass


        return code

    def GenContainerURL(self, format="png", print_URL=False, print_code=False):
        """
        :param 
        """
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
        """
        :param 
        """
        f = open(("%s.puml" % (file_name)), 'w+')
        f.write(self.GenContainerCode())
        f.close()
