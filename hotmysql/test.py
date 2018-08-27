#-*- coding: utf-8 -*-
import pymysql
import time
def doc_process(str):
    begin = str.find(" ")
    end = str.find("\n")
    return str[ begin+1:end ]

db = pymysql.connect("localhost","root","sam861127","song", charset = "utf8mb4")
cursor = db.cursor()

f = open("lyric.txt", "r")
catch = ""
while True:
    catch = f.readline()
    if catch.find("歌手:") != -1:
        break
singerQ = 0
dor = 0
singer = ""
name = ""
lyric = ""
singer_id = 0
song_id = 0
while True:
    if dor == 1:
        break
    singer = catch
    name = f.readline()
    lyric = ""
    lyric_tem = ""
    while True:
        tem_2 = f.readline()
        if tem_2.find("歌手:") != -1:
            catch = tem_2
            lyric = lyric_tem
            break
        elif tem_2 != "" :
            lyric_tem = lyric
            lyric = lyric + tem_2
        else:
            dor = 1
            break
            
    print(doc_process(singer) + "ss")
    
    sql = "INSERT INTO `hot_song_singer` (`id`, `name`) VALUES (%s, %s)"
    
    cursor.execute("SELECT * FROM `hot_song_singer` WHERE `name` REGEXP %s", doc_process(singer).strip())
    qtem = cursor.fetchone()
    if qtem != None:
        singerQ = qtem[0]
    elif qtem == None:
        singer_id += 1
        singerQ = singer_id
        param1 = (str(singer_id), doc_process(singer).strip())
        cursor.execute(sql, param1)
        db.commit()
    print("singer_id = " + str(singer_id))


    song_id += 1
    sql2 = "INSERT INTO `hot_song` (`id`, `name`, `singer_id`, `lyric`) VALUES (%s, %s, %s, %s)"
    param = (str(song_id), doc_process(name), str(singerQ), lyric)
    
    #try:
    cursor.execute(sql2, param)
    db.commit()
    #except:
        #print("failed to key" + doc_process(name) +"singer:" + str(singer_id))
        #db.rollback()
        #song_id -= 1

db.close()

