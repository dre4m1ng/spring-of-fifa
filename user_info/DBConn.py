from sqlalchemy import create_engine, Column, Integer, String, Text, Float, JSON, DateTime, DECIMAL, Boolean
from sqlalchemy.exc import OperationalError
from sqlalchemy.types import Integer, VARCHAR, CHAR, DECIMAL, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import json
from datetime import datetime

def db_conn(id, password, db_ip, db):
    db_path = f'{id}:{password}@{db_ip}:3306/{db}'

    engine = create_engine(f'mysql://{db_path}')
    
    try:
        # 연결 시도
        with engine.connect():
            print("Database connection successful.")
    except OperationalError as e:
        print(f"Database connection failed. Error: {e}")
    
    return engine

def top10000(top10000_path, engine):
    df = pd.read_parquet(top10000_path)
    df = df[df.notnull().all(axis=1)]

    # price는 'BP'라고 들어간 것이 있어서 VARCHAR로
    dtype = {
        'rankNo' : Integer(),
        'LV' : Integer(),
        'nickName' : VARCHAR(20),
        'rankScore' : DECIMAL(precision=6, scale=2),
        'tier' : CHAR(6),
        'korRankTier' : VARCHAR(7),
        'price' : VARCHAR(20),
        'ouid' : CHAR(32)
    }

    df.to_sql(name='top10000', con=engine, index=False, dtype=dtype, if_exists='replace')
    print('Data loading completed..')

class MatchDetail:
    def matchData(engine, table, input_data):
        # 세션 생성
        Session = sessionmaker(bind=engine)
        session = Session()

        # Base 클래스 생성
        Base = declarative_base()
        
        # MatchData class 정의
        class MatchData(Base):
            __tablename__ = table
            
            matchUid = Column(String, primary_key=True)
            matchId = Column(String)
            matchDate = Column(DateTime)
            matchType = Column(Integer)
            ouid = Column(String)
            seasonId = Column(Integer)
            matchResult = Column(String)
            matchEndType = Column(Integer)
            systemPause = Column(Integer)
            foul = Column(Integer)
            injury = Column(Integer)
            redCards = Column(Integer)
            yellowCards = Column(Integer)
            dribble = Column(Integer)
            cornerKick = Column(Integer)
            possession = Column(Integer)
            offsideCount = Column(Integer)
            averageRating = Column(Integer)
            controller = Column(String)
            shootTotal = Column(Integer)
            effectiveShootTotal = Column(Integer)
            shootOutScore = Column(Integer)
            goalTotal = Column(Integer)
            goalTotalDisplay = Column(Integer)
            ownGoal = Column(Integer)
            shootHeading = Column(Integer)
            goalHeading = Column(Integer)
            shootFreekick = Column(Integer)
            goalFreekick = Column(Integer)
            shootInPenalty = Column(Integer)
            goalInPenalty = Column(Integer)
            shootOutPenalty = Column(Integer)
            goalOutPenalty = Column(Integer)
            shootPenaltyKick = Column(Integer)
            goalPenaltyKick = Column(Integer)
            passTry = Column(Integer)
            passSuccess = Column(Integer)
            shortPassTry = Column(Integer)
            shortPassSuccess = Column(Integer)
            longPassTry = Column(Integer)
            longPassSuccess = Column(Integer)
            bouncingLobPassTry = Column(Integer)
            bouncingLobPassSuccess = Column(Integer)
            drivenGroundPassTry = Column(Integer)
            drivenGroundPassSuccess = Column(Integer)
            throughPassTry = Column(Integer)
            throughPassSuccess = Column(Integer)
            lobbedThroughPassTry = Column(Integer)
            lobbedThroughPassSuccess = Column(Integer)
            blockTry = Column(Integer)
            blockSuccess = Column(Integer)
            tackleTry = Column(Integer)
            tackleSuccess = Column(Integer)
            
        # 딕셔너리를 JSON 형식으로 변환하여 데이터베이스에 저장
        match_row = MatchData(
            matchUid=input_data['matchUid'],
            matchId=input_data['matchId'],
            matchDate=datetime.fromisoformat(input_data['matchDate']),
            matchType=input_data['matchType'],
            ouid=input_data['ouid'],
            seasonId=input_data['seasonId'],
            matchResult=input_data['matchResult'],
            matchEndType=input_data['matchEndType'],
            systemPause=input_data['systemPause'],
            foul=input_data['foul'],
            injury=input_data['injury'],
            redCards=input_data['redCards'],
            yellowCards=input_data['yellowCards'],
            dribble=input_data['dribble'],
            cornerKick=input_data['cornerKick'],
            possession=input_data['possession'],
            offsideCount=input_data['offsideCount'],
            averageRating=input_data['averageRating'],
            controller=input_data['controller'],
            shootTotal=input_data['shootTotal'],
            effectiveShootTotal=input_data['effectiveShootTotal'],
            shootOutScore=input_data['shootOutScore'],
            goalTotal=input_data['goalTotal'],
            goalTotalDisplay=input_data['goalTotalDisplay'],
            ownGoal=input_data['ownGoal'],
            shootHeading=input_data['shootHeading'],
            goalHeading=input_data['goalHeading'],
            shootFreekick=input_data['shootFreekick'],
            goalFreekick=input_data['goalFreekick'],
            shootInPenalty=input_data['shootInPenalty'],
            goalInPenalty=input_data['goalInPenalty'],
            shootOutPenalty=input_data['shootOutPenalty'],
            goalOutPenalty=input_data['goalOutPenalty'],
            shootPenaltyKick=input_data['shootPenaltyKick'],
            goalPenaltyKick=input_data['goalPenaltyKick'],
            passTry=input_data['passTry'],
            passSuccess=input_data['passSuccess'],
            shortPassTry=input_data['shortPassTry'],
            shortPassSuccess=input_data['shortPassSuccess'],
            longPassTry=input_data['longPassTry'],
            longPassSuccess=input_data['longPassSuccess'],
            bouncingLobPassTry=input_data['bouncingLobPassTry'],
            bouncingLobPassSuccess=input_data['bouncingLobPassSuccess'],
            drivenGroundPassTry=input_data['drivenGroundPassTry'],
            drivenGroundPassSuccess=input_data['drivenGroundPassSuccess'],
            throughPassTry=input_data['throughPassTry'],
            throughPassSuccess=input_data['throughPassSuccess'],
            lobbedThroughPassTry=input_data['lobbedThroughPassTry'],
            lobbedThroughPassSuccess=input_data['lobbedThroughPassSuccess'],
            blockTry=input_data['blockTry'],
            blockSuccess=input_data['blockSuccess'],
            tackleTry=input_data['tackleTry'],
            tackleSuccess=input_data['tackleSuccess']
        )

        # 데이터베이스에 추가
        session.add(match_row)
        session.commit()
    
    def shoot(engine, table, input_data):
        # 세션 생성
        Session = sessionmaker(bind=engine)
        session = Session()

        # Base 클래스 생성
        Base = declarative_base()

        class ShootData(Base):
            __tablename__ = table
            
            goalTime = Column(Integer)
            x = Column(DECIMAL)
            y = Column(DECIMAL)
            type = Column(Integer)
            result = Column(Integer)
            spId = Column(String)
            spGrade = Column(Integer)
            spLevel = Column(Integer)
            spIdType = Column(Boolean)
            assist = Column(Boolean)
            assistSpId = Column(String)
            assistX = Column(DECIMAL)
            assistY = Column(DECIMAL)
            hitPost = Column(Boolean)
            inPenalty = Column(Boolean)
            matchUid = Column(String)
            shootUid = Column(String, primary_key=True)
            
        shoot_row = ShootData(
            goalTime=input_data['goalTime'],
            x=input_data['x'],
            y=input_data['y'],
            type=input_data['type'],
            result=input_data['result'],
            spId=input_data['spId'],
            spGrade=input_data['spGrade'],
            spLevel=input_data['spLevel'],
            spIdType=input_data['spIdType'],
            assist=input_data['assist'],
            assistSpId=input_data['assistSpId'],
            assistX=input_data['assistX'],
            assistY=input_data['assistY'],
            hitPost=input_data['hitPost'],
            inPenalty=input_data['inPenalty'],
            matchUid=input_data['matchUid'],
            shootUid=input_data['shootUid']
        )

        # 데이터베이스에 추가
        session.add(shoot_row)
        session.commit()
        
    def player(engine, table, input_data):
        # 세션 생성
        Session = sessionmaker(bind=engine)
        session = Session()

        # Base 클래스 생성
        Base = declarative_base()

        class playerData(Base):
            __tablename__ = table
            
            matchUid = Column(String)
            playerUid = Column(String, primary_key=True)
            spId = Column(String)
            spPosition = Column(Integer)
            spGrade = Column(Integer)
            shoot = Column(Integer)
            effectiveShoot = Column(Integer)
            assist = Column(Integer)
            goal = Column(Integer)
            dribble = Column(Integer)
            intercept = Column(Integer)
            defending = Column(Integer)
            passTry = Column(Integer)
            passSuccess = Column(Integer)
            dribbleTry = Column(Integer)
            dribbleSuccess = Column(Integer)
            ballPossesionTry = Column(Integer)
            ballPossesionSuccess = Column(Integer)
            aerialTry = Column(Integer)
            aerialSuccess = Column(Integer)
            blockTry = Column(Integer)
            block = Column(Integer)
            tackleTry = Column(Integer)
            tackle = Column(Integer)
            yellowCards = Column(Integer)
            redCards = Column(Integer)
            spRating = Column(Float)
            
        player_row = playerData(
            matchUid=input_data['matchUid'],
            playerUid=input_data['playerUid'],
            spId=input_data['spId'],
            spPosition=input_data['spPosition'],
            spGrade=input_data['spGrade'],
            shoot=input_data['shoot'],
            effectiveShoot=input_data['effectiveShoot'],
            assist=input_data['assist'],
            goal=input_data['goal'],
            dribble=input_data['dribble'],
            intercept=input_data['intercept'],
            defending=input_data['defending'],
            passTry=input_data['passTry'],
            passSuccess=input_data['passSuccess'],
            dribbleTry=input_data['dribbleTry'],
            dribbleSuccess=input_data['dribbleSuccess'],
            ballPossesionTry=input_data['ballPossesionTry'],
            ballPossesionSuccess=input_data['ballPossesionSuccess'],
            aerialTry=input_data['aerialTry'],
            aerialSuccess=input_data['aerialSuccess'],
            blockTry=input_data['blockTry'],
            block=input_data['block'],
            tackleTry=input_data['tackleTry'],
            tackle=input_data['tackle'],
            yellowCards=input_data['yellowCards'],
            redCards=input_data['redCards'],
            spRating=input_data['spRating']
        )

        # 데이터베이스에 추가
        session.add(player_row)
        session.commit()