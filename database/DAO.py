from database.DB_connect import DBConnect
from model.pilota import Pilota


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStagione():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct `year` 
                    from seasons s 
                                 """

        cursor.execute(query,)

        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPiloti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct driverId, forename ,surname
                    from drivers 
               """

        cursor.execute(query, )

        for row in cursor:
            result.append(Pilota(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPiloti(anno, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r2.driverId as dr
                    from races r,results r2 
                    where r.raceId =r2.raceId  
                    and year(r.`date`)= %s
                    and r2.`position` is not null
                                    """

        cursor.execute(query,(anno,) )

        for row in cursor:
            result.append(idMap[row["dr"]])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getVittorie(anno, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as dr1, r2.driverId as dr2, count(*) as peso
                    from results r1, results r2, races r 
                    where r.`year`  = %s
                    and r2.raceId = r.raceId  
                    and r1.raceId = r.raceId 
                    and r1.`position` < r2.`position` 
                    and r1.resultId < r2.resultId 
                    group by r1.driverId, r2.driverId
                                        """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append((idMap[row["dr1"]],idMap[row["dr2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result
