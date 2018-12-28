import sys
import plantuml
import traceback

# Pending points
# - Alings options


id = 0
class Object():

    def __init__(self, type, name="", color="", top_margin=1, bottom_margin=1, left_margin=10, right_margin=10, include_in=None):
        global id
        id += 1

        self.id = "ID_%i" % id
        self.type = type
        self.name = name
        self.color = color
        self.invert_draw_dir = False
        self.top_margin = top_margin 
        self.bottom_margin = bottom_margin 
        self.left_margin = left_margin 
        self.right_margin = right_margin
        self.align = None

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

    def AlingContentAsRows(self, max_per_row = 0, exclude_objs = None, h_sep = 0, v_sep = 0, force = 5):
        self.align = ["rows", exclude_objs, max_per_row, h_sep, v_sep, force]

    def AlingContentAsColumns(self, max_per_column = 0, exclude_objs = None):
        self.align = ["columns", exclude_objs, max_per_column]

    def AlingContentAsCeter(self, middle_objs = None, exclude_objs = None):
        self.align = ["center", exclude_objs, middle_objs]

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

        def GetAlignList(main_obj):
            obj_groups=[main_obj.include_list]
            
            if main_obj.align is None:
                return obj_groups

            align_mode = main_obj.align[0]

            if align_mode == "rows":
                max_per_row = main_obj.align[2]
                obj_groups = []
                row = []
                j = 0
                for i in range(0,len(main_obj.include_list)):
                    row.append(main_obj.include_list[i])

                    j += 1
                    if j >= max_per_row:
                        obj_groups.append(row)
                        row = []
                        j = 0
                if j > 0:
                    obj_groups.append(row)
                    row = []
                    j = 0

            return obj_groups

        def CodeIterate(object_list, used_object, indent=""):
            code = ""
            for obj in object_list:
                if obj in used_object:
                    print(("Object %s re-used") % (obj.id))
                    continue

                used_object.append(obj)

                code +="%s%s" % (indent, obj.GenObjectCode())
                if len(obj.include_list) > 0:
                    obj_groups = GetAlignList(obj)

                    code+="{\n"
                    xx = 0
                    for group in obj_groups:
                        xx += 1
                        code+="together AA_%s{\n" % xx
                        code+=CodeIterate(group, used_object, (("%s\t") % (indent)))
                        code+="}\n"
                        
                        if xx > 0:
                            code+="AA_%s -[hidden]- AA_%s\n" % (xx-1,xx)
                    code+="%s}" % indent
                code+="\n"
            return code

        def GenConnetionCode(main_obj, objects_list = None):
            code = ""
            for obj, connector, color, invert in main_obj.connection_list:
                if color != "":
                    if not color.startswith("#"):
                        color = ("#%s") %(color)

                if objects_list is not None:
                    if not obj in objects_list:
                        continue
                if not invert:
                    code += (("%s %s %s %s\n") % (main_obj.id, connector, obj.id, color))
                else:
                    code += (("%s %s %s %s\n") % (obj.id, connector, main_obj.id, color))
            return code

        def GenAlingCode(main_obj):
            code = ""
            if main_obj.align is None:
                return code
            align_mode = main_obj.align[0]
            exclude_objs = main_obj.align[1]

            obj_list=[]
            for obj in main_obj.include_list:
                if exclude_objs is not None:
                    if obj in exclude_objs:
                        continue
                obj_list.append(obj)

            if len(obj_list) < 2:
                return code


            if align_mode == "center":
                max_per_row = self.align[2]

                h_row = []
                l_row = []
                for i in range(len(self.include_list)):
                    obj = self.include_list[i]
                    if i < (len(self.include_list)/2):
                        h_row.append(obj)
                    else:
                        l_row.append(obj)

                for i in range(len(h_row)-1):
                    obj1 = h_row[i]
                    obj2 = h_row[i+1]
                    code += "%s -[hidden]- %s\n" % (obj1.id, obj2.id)


            if align_mode == "rows":
                max_per_row = main_obj.align[2]
                h_sep = main_obj.align[3]
                v_sep = main_obj.align[4]
                force = main_obj.align[5]

                rows = []
                row = []
                j = 0
                for i in range(0,len(obj_list)):
                    if exclude_objs is not None:
                        if obj_list[i] in exclude_objs:
                            continue

                    row.append(obj_list[i])

                    j += 1
                    if j >= max_per_row:
                        rows.append(row)
                        row = []
                        j = 0
                if j > 0:
                    rows.append(row)
                    row = []
                    j = 0

                columns = []
                column = []
                if len(rows) > 1:
                    for obj in rows[0]:
                        columns.append([])

                for row in rows:
                    for j in range(0,len(row)):
                        columns[j].append(row[j])

                sep="-"
                for i in range(0,h_sep):
                    sep+="-"

                for row in rows:
                    for i in range(0,len(row)-1):
                        obj1 = row[i]
                        obj2 = row[i+1]
                        
                        obj1_conected=[]
                        for item in obj1.connection_list:
                            obj1_conected.append(item[0])
                        obj2_conected=[]
                        for item in obj2.connection_list:
                            obj2_conected.append(item[0])

                        if obj1 in obj2_conected:
                            continue
                        if obj2 in obj1_conected:
                            continue

                        for x in range (0,force):
                            code += "%s -[hidden]down%s %s\n" % (obj1.id, sep, obj2.id)
                            code += "%s -[hidden]up%s %s\n" % (obj2.id, sep, obj1.id)
                            #code += "%s --> %s\n" % (obj1.id, obj2.id)
                            #code += "%s <|-[hidden]down%s %s\n" % (obj2.id, sep, obj1.id)

                sep="-"
                for i in range(0,v_sep):
                    sep+="-"

                for column in columns:
                    for i in range(0,len(column)-1):
                        obj1 = column[i]
                        obj2 = column[i+1]

                        obj1_conected=[]
                        for item in obj1.connection_list:
                            obj1_conected.append(item[0])
                        obj2_conected=[]
                        for item in obj2.connection_list:
                            obj2_conected.append(item[0])

                        if obj1 in obj2_conected:
                            continue
                        if obj2 in obj1_conected:
                            continue

                        for x in range (0,force):
                            code += "%s -[hidden]right%s %s\n" % (obj1.id, sep, obj2.id)
                            code += "%s -[hidden]left%s %s\n" % (obj2.id, sep, obj1.id)
                            #code += "%s -> %s\n" % (obj1.id, obj2.id)
                            #code += "%s -[hidden]> %s\n" % (obj2.id, obj1.id)

            return code

        code=""

        code +="@startuml\n"

        if self.name != "":
            code +="title %s\n" % self.name

        if self.invert_draw_dir:
            code += "left to right direction\n"

        used_object = []
        used_object.append(self)

        obj_groups = GetAlignList(self)
        xx = 0
        for group in obj_groups:
            xx += 1
            code+="together AA_%s{\n" % xx
            code+=CodeIterate(group, used_object)
            code+="}\n"
            if xx > 1:
                code+="AA_%s -[hidden]- AA_%s\n" % (xx-1,xx)


        code += "\n\n"
        code += "'#================\n"
        code += "'# CONNECTION CODE \n"
        code += "'#================\n"
        code += "\n"
        for obj in used_object:
            code += GenConnetionCode(obj, used_object)
        code += "\n"

        #code += "\n\n"
        #code += "'#===========\n"
        #code += "'# ALIGN CODE \n"
        #code += "'#===========\n"
        #code += "\n"
        #for obj in used_object:
            #code += GenAlingCode(obj)
        #code+="\n"

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
