from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# headless로 윈도우 창 띄우지 않고 실행하기
OP = Options()
OP.add_argument("--headless")

# webdriver, url
browser = webdriver.Chrome(options=OP)
url = 'https://fconline.nexon.com/datacenter'
browser.get(url)

# csv 파일 경로를 input으로 받기
csv_file_path = input("CSV 파일 경로를 입력하거라: ")
# csv 파일을 데이터프레임으로 읽어오기
df_spid = pd.read_csv(csv_file_path)
# 데이터프레임을 list로 변환하기
name_list_csv = df_spid.values.tolist()
# 행 개수 조회
name_list_csv_num = len(name_list_csv)


df = pd.DataFrame(columns=['Season_Class', 'Name', 'Position', 'Birth', 'Height', 'Weight', 'Physical', 'Skill', 'Foot', 'Season', 'Nation', 'Speed_M', 'Soot_M', 'Pass_M', 'Dribble_M', 'Defance_M', 'Physical_M', 'Sprint_Speed', 'Acceleration', 'Finishing', 'Soot_Power', 'Long_Shots', 'Positioning', 'Volley', 'Penalty_Kick', 'Short_Pass', 'Vision',
                  'Crossing', 'Long_Pass', 'Free_Kick', 'Curve', 'Dribbling', 'Ball_Control', 'Agility', 'Balance', 'Reaction', 'Defensive_Awareness', 'Tackle', 'Interceptions', 'Heading_Accuracy', 'Sliding_Tackle', 'Standing_Tackle', 'Stamina', 'Aggression', 'Jumping', 'Calmness', 'GK_Diving', 'GK_Handling', 'GK_Kicking', 'GK_Reflexes', 'GK_Positioning'])

failed_names = []  # 실패한 선수 이름을 저장할 리스트

for name in name_list_csv:
    # 선수 이름 입력
    browser.find_element(By.XPATH, '//*[@id="searchName"]').send_keys(name)
    print(f'{name}', "크롤링 시작")

    # 검색 버튼 클릭
    browser.find_element(
        By.XPATH, '//*[@id="form1"]/div[1]/div[3]/button[1]').click()

    # 최대 3번 시도
    for _ in range(3):
        try:
            # 기다리기
            tr_wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="divPlayerList"]/div[@class="tr"]')))

            # 검색 결과 수 가져오기
            n = len(browser.find_elements(
                By.XPATH, '//*[@id="divPlayerList"]/div[@class="tr"]'))

            for i in tqdm(range(1, n + 1)):
                # 스크롤 이동
                a = browser.find_element(
                    By.XPATH, f'//*[@id="divPlayerList"]/div[{i}]')
                ActionChains(browser).scroll_to_element(a).perform()

                browser.find_element(
                    By.XPATH, f'//*[@id="divPlayerList"]/div[{i}]/div[1]/div/div[6]/a').click()
                time.sleep(0.3)

                # 요소 찾기
                info_wrap = browser.find_element(
                    By.XPATH, '//*[@id="playerPreview"]/div/div/div[1]/div[2]')
                info_split = info_wrap.text.split('\n')
                info_split_emp = info_split[2].split(" ")
                season_class = info_wrap.find_element(
                    By.XPATH, '//*[@id="playerPreview"]/div/div/div[1]/div[2]/div[1]/div[1]/img').get_attribute('src')
                player_stat_1 = browser.find_element(
                    By.XPATH, '//*[@id="playerPreview"]/div/div/div[2]').text.split('\n')
                player_stat_2 = browser.find_element(
                    By.XPATH, '//*[@id="playerPreview"]/div/div/div[3]').text.split('\n')
                player_stat_3 = browser.find_element(
                    By.XPATH, f'//*[@id="divPlayerList"]/div[{i}]').text.split('\n')

                # 특성 빈 리스트
                img_alt_list = []
                # span 요소의 개수 확인
                skill_wrap = browser.find_elements(
                    By.XPATH, '//*[@id="playerPreview"]/div/div/div[1]/div[2]/div[5]/span')
                num_skill_wrap = len(skill_wrap)

                # 각 span 요소의 img 속성값을 가져오기
                for j in range(1, num_skill_wrap + 1):
                    img_element = browser.find_element(
                        By.XPATH, f'//*[@id="playerPreview"]/div/div/div[1]/div[2]/div[5]/span[{j}]/img')
                    img_alt = img_element.get_attribute('alt')
                    img_alt_list.append(img_alt)

                # data에 넣기
                data = {
                    'Season_Class': [season_class.split('/')[-1][:-4]],
                    'Name': [info_split[0]],
                    'Position': [info_split[1]],
                    'Birth': [info_split_emp[0]],
                    'Height': [info_split_emp[2]],
                    'Weight': [info_split_emp[3]],
                    'Physical': [info_split_emp[4]],
                    'Skill': [info_split_emp[5]],
                    'Foot': [' '.join(info_split_emp[6:9])],
                    'Season': [info_split_emp[9]],
                    'Nation': [info_split[3]],
                    'Skill_Wrap': [img_alt_list[:]],
                    'Speed_M': [player_stat_1[1]],
                    'Soot_M': [player_stat_1[3]],
                    'Pass_M': [player_stat_1[5]],
                    'Dribble_M': [player_stat_1[7]],
                    'Defance_M': [player_stat_1[9]],
                    'Physical_M': [player_stat_1[11]],
                    'Sprint_Speed': [player_stat_2[1]],
                    'Acceleration': [player_stat_2[3]],
                    'Finishing': [player_stat_2[5]],
                    'Soot_Power': [player_stat_2[7]],
                    'Long_Shots': [player_stat_2[9]],
                    'Positioning': [player_stat_2[11]],
                    'Volley': [player_stat_2[13]],
                    'Penalty_Kick': [player_stat_2[15]],
                    'Short_Pass': [player_stat_2[17]],
                    'Vision': [player_stat_2[19]],
                    'Crossing': [player_stat_2[21]],
                    'Long_Pass': [player_stat_2[23]],
                    'Free_Kick': [player_stat_2[25]],
                    'Curve': [player_stat_2[27]],
                    'Dribbling': [player_stat_2[29]],
                    'Ball_Control': [player_stat_2[31]],
                    'Agility': [player_stat_2[33]],
                    'Balance': [player_stat_2[35]],
                    'Reaction': [player_stat_2[37]],
                    'Defensive_Awareness': [player_stat_2[39]],
                    'Tackle': [player_stat_2[41]],
                    'Interceptions': [player_stat_2[43]],
                    'Heading_Accuracy': [player_stat_2[45]],
                    'Sliding_Tackle': [player_stat_2[47]],
                    'Standing_Tackle': [player_stat_2[49]],
                    'Stamina': [player_stat_2[51]],
                    'Aggression': [player_stat_2[53]],
                    'Jumping': [player_stat_2[55]],
                    'Calmness': [player_stat_2[57]],
                    'GK_Diving': [player_stat_2[59]],
                    'GK_Handling': [player_stat_2[61]],
                    'GK_Kicking': [player_stat_2[63]],
                    'GK_Reflexes': [player_stat_2[65]],
                    'GK_Positioning': [player_stat_2[67]],
                    'Salary': [player_stat_3[3]],
                    'BP': [player_stat_3[-3]]
                }

                df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
                # 미리보기 눌러서 끄기
                browser.find_element(
                    By.XPATH, f'//*[@id="divPlayerList"]/div[{i}]/div[1]/div/div[6]/a').click()

            print(f'{name}', f'{n}'"번 돌았습니다.")

            # 검색창 비우기
            browser.find_element(By.XPATH, '//*[@id="searchName"]').clear()

            break  # 성공 시 반복문 종료
        except NoSuchElementException as e : 
            # 요소가 나타나지 않으면 1분 대기 후 재시도
            print(f"{e}, 요소가 나타나지 않습니다. 1분 대기 후 재시도합니다.")
            time.sleep(60)
            continue
    else:
        print("3번 시도했지만 실패했습니다.")
        failed_names.append(name)  # 실패한 선수의 이름을 리스트에 추가
        continue  # 실패 시 다음 선수로 넘어가기

# 실패한 선수의 이름을 df화하여 csv 파일로 저장
df_failed_names = pd.DataFrame(failed_names, columns=['Failed_Name'])
df_failed_names.to_csv(f'{csv_file_path}_fail.csv',
                       index=False, encoding="utf-8-sig")
# 성공한 선수의 이름을 csv 파일로 저장
df.to_csv(f'{csv_file_path}_output.csv', index=False, encoding="utf-8-sig")
