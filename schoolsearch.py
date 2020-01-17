import pandas as pd

def printTeacher(classroom, df2, extra): 
    teachDf = df2.where(classroom == df2["Classroom"]).dropna()
    for index, row in teachDf.iterrows():
        print(f' {row["TLastName"]}{row["TFirstName"]} {extra}')


def studentSearch(cmd, df, df2):
    if len(cmd) < 2:
        return
    stuDf = df.where(cmd[1] == df["StLastName"]).dropna()
    for index, row in stuDf.iterrows():
        if len(cmd) == 2:
            teachDf = df2.where(row["Classroom"] == df2["Classroom"]).dropna()
            for index2, row2 in teachDf.iterrows():
                print(f'{row["StLastName"]}{row["StFirstName"]} Grade {int(row["Grade"])} Classroom {int(row["Classroom"])} {row2["TLastName"]}{row2["TFirstName"]}')
        elif len(cmd) == 3:
           print(f'{row["StLastName"]}{row["StFirstName"]} {int(row["Bus"])}')


def teacherSearch(cmd, df, df2):
    if len(cmd) < 2:
        return
    teachDf = (df2.where(cmd[1] == df2["TLastName"]).dropna()).reset_index()
    if teachDf.empty:
       return
    stuDf = df.where(teachDf.at[0, 'Classroom'] == df["Classroom"]).dropna()
    for index, row in stuDf.iterrows():
        print(f'{row["StLastName"]} {row["StFirstName"]}')
    

def getGradeTeachers(df, df2):
    teachDf = pd.DataFrame()
    for index, row in df.iterrows():
        teachDf = teachDf.append(df2.where(row["Classroom"]== df2["Classroom"]).dropna())
    teachDf = teachDf.drop_duplicates(subset = "TLastName")
    for index, row in teachDf.iterrows():
        print(f'{row["TLastName"]} {row["TFirstName"]}')

def gradeSearchOptions(cmd, df, df2):
    if cmd[0] == 'T':
        getGradeTeachers(df, df2)
        return
    if cmd[0] == 'H':
        df = df.nlargest(1,  ["GPA"])
    elif cmd[0] == 'L':
        df = df.nsmallest(1, ["GPA"])
    for index, row in df.iterrows():
        teachDf = df2.where(row["Classroom"] == df2["Classroom"]).dropna()
        for index2, row2 in teachDf.iterrows():
            print(f'{row["StLastName"]} {row["StFirstName"]} GPA {row["GPA"]} {row2["TLastName"]}{row2["TFirstName"]} Bus {int(row["Bus"])}')

def gradeSearchNoOpt(grade, stuDf):
    for index, row in stuDf.iterrows():
        print(f'{row["StLastName"]} {row["StFirstName"]}')

def gradeSearch(cmd, df, df2):
    cmdLen = len(cmd)
    if cmdLen < 2:
        return
    grade = int(cmd[1])
    stuDf = df.where(grade == df["Grade"]).dropna()
    if cmdLen == 2:
        gradeSearchNoOpt(grade, stuDf)
    elif cmdLen == 3:
        gradeSearchOptions(cmd[2], stuDf, df2)

def busSearch(cmd, df):
    if len(cmd) < 2:
        return
    stuDf = df.where(int(cmd[1]) == df["Bus"]).dropna()
    for index, row in stuDf.iterrows():
        print(f'{row["StLastName"]}{row["StFirstName"]} Grade {int(row["Grade"])} Classroom {int(row["Classroom"])}')

def avgSearch(cmd, df):
    if len(cmd) < 2:
        return
    stuDf = df.where(int(cmd[1]) == df["Grade"]).dropna()
    if stuDf.empty:
       return
    avg = stuDf["GPA"].mean()
    print(f'Grade level {cmd[1]}\nAverage GPA {avg}')

def infoSearch(cmd, df):
    for i in range(7):
        stuDf = df.where(i == df["Grade"]).dropna()
        print(f'Grade {i}: {stuDf.shape[0]} students')

def classroomStudents(classroom, df):
    stuDf = df.where(classroom == df["Classroom"]).dropna()
    for index, row in stuDf.iterrows():
        print(f'{row["StLastName"]}{row["StFirstName"]}')

def classroomTeachers(classroom, df2):
    stuDf = df2.where(classroom == df2["Classroom"]).dropna()
    for index, row in stuDf.iterrows():
        print(f'{row["TLastName"]}{row["TFirstName"]}')

def enrollmentSearch(cmd, df):
    classesDf = df.drop_duplicates(subset='Classroom')
    classesDf = classesDf.sort_values('Classroom')
    for index, row in classesDf.iterrows():
        print(f'Classroom {row["Classroom"]}:')
        classroomStudents(int(row["Classroom"]), df)
        print(f'\n')

def getGradeAnalytics(cmd, df):
    gradesDf = df.drop_duplicates(subset = 'Grade').dropna() 
    gradesDf = gradesDf.sort_values('Grade')
    for index, row in gradesDf.iterrows():
        print(f'Grade {row["Grade"]}')
        getData(cmd, df, row, "Grade")

def getBusAnalytics(cmd, df):
    busDf = df.drop_duplicates(subset = 'Bus').dropna() 
    busDf = busDf.sort_values('Bus')
    for index, row in busDf.iterrows():
        print(f'Bus {row["Bus"]}')
        getData(cmd, df, row, "Bus") 

def getTeacherAnalytics(cmd, df, df2):
    teachDf = df2.sort_values('TLastName')
    for index, row in teachDf.iterrows():
        print(f'{row["TLastName"]} {row["TFirstName"]} :')
        getData(cmd, df, row, "Classroom")


def getData(cmd, df, row, data):
    filtered = df.where(row[data] == df[data]).dropna()
    avg = filtered["GPA"].mean()
    print(f'Average GPA {avg}')
    high = filtered.nlargest(1, ["GPA"]).reset_index()
    print(f'High GPA {high.at[(high.shape[0]-1), "GPA"]}')
    low = filtered.nsmallest(1, ["GPA"]).reset_index()
    print(f'Low GPA {low.at[(high.shape[0]-1), "GPA"]}')
    print("\n")


def dataSearch(cmd, df, df2):
    cmdLen = len(cmd)
    if cmdLen <2:
        return
    elif cmd[1][0] == 'G':
        getGradeAnalytics(cmd, df)
    elif cmd[1][0] == 'B':
        getBusAnalytics(cmd, df)
    elif cmd[1][0] == 'T':
        getTeacherAnalytics(cmd, df, df2)

def classroomSearch(cmd, df, df2):
    cmdLen = len(cmd)
    if cmdLen < 2:
        return
    elif cmdLen ==2:
        classroomStudents(int(cmd[1]), df)
    elif (cmdLen == 3) & (cmd[2][0]=='T'):
        classroomTeachers(int(cmd[1]), df2)

def handleAsk(cmd, df, df2):
    if cmd[0][0] == 'D':
        dataSearch(cmd, df, df2)

    if cmd[0][0] == 'C':
        classroomSearch(cmd, df, df2)
    
    if cmd[0][0] == 'E':
        enrollmentSearch(cmd, df)

    if cmd[0][0] == 'S' :
        studentSearch(cmd, df, df2)

    if cmd[0][0] == 'T' :
        teacherSearch(cmd, df, df2)

    if cmd[0][0] == 'G' :
        gradeSearch(cmd, df, df2)

    if cmd[0][0] == 'B' :
        busSearch(cmd, df)

    if cmd[0][0] == 'A' :
        avgSearch(cmd, df)

    if cmd[0][0] == 'I' :
        infoSearch(cmd, df)
    
def printPrompt():
    print(f"""• D[ata-Analysis] <G[rade]|B[us]|T[eacher]>
    \n• C[lassroom]: <number> [T[eachers]]
    \n• E[nrollment]
    \n• S[tudent]: <lastname> [B[us]]
    \n• T[eacher]: <lastname>
    \n• B[us]: <number>
    \n• G[rade]: <number> [H[igh]|L[ow]|[T[eachers]]]
    \n• A[verage]: <number>
    \n• I[nfo]
    \n• Q[uit]""")


def main():
    #df = pd.read_csv(r'\Users\Nicole Schwartz\Anaconda3\csc365\csc365lab1\students.txt', header=None, names=["StLastName", "StFirstName", "Grade", "Classroom", "Bus", "GPA", "TLastName", "TFirstName"])
    try:
       df = pd.read_csv(r"./list.txt", header=None, names=["StLastName", "StFirstName", "Grade", "Classroom", "Bus", "GPA"])
       df2 = pd.read_csv(r"./teachers.txt", header=None, names=["TLastName", "TFirstName", "Classroom"])
    except FileNotFoundError:
        return
    printPrompt()
    cmd = input(">>")

    while cmd is not "Q":
        if len(cmd) > 0:
            cmd = cmd.split()
            handleAsk(cmd, df, df2)
        printPrompt()
        cmd = input(">>")
    return 

if __name__ == '__main__':
    main()
