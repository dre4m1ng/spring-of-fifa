from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm
from nexon_api import Fconline


def ranker_cwl(save_path, api_key):
    """
    FConline 홈페이지에서 공식경기 랭킹을 기져오는 모듈

    Args:
        save_path (str): 저장경로
        api_key (str): nexon API key

    Returns:
        df: .parquet 형태의 포멧으로 save_path 위치에 데이터 저장
    """
    # 데이터 저장을 위한 현재시간
    now = datetime.now()
    cur_time = now.strftime('%y%m%d%H')
    parquet_file_path = f'{save_path}/{cur_time}_user_info.parquet'

    # chrome driver option setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    # linux 환경에서 필요한 option
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Chrome 드라이버 생성
    browser = webdriver.Chrome(options=chrome_options)

    # 접속할 웹페이지 URL
    url = 'https://fconline.nexon.com/datacenter/rank'

    # 웹페이지 열기
    browser.get(url)

    # 랭커 유저 리스트
    user_rank_num, user_lvs, user_names, user_prices, user_rank_scores, user_ranks = [
    ], [], [], [], [], []

    # 반복 횟수 설정
    current_iter = 0
    total_iter = 50

    while current_iter < total_iter:
        for i in range(2, 12):
            # 페이지 로딩시간
            time.sleep(1)
            # 요소를 찾을때 까지 대기
            user_info_wait = WebDriverWait(
                browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]/div[1]/div/div[2]')))
            WebDriverWait(
                user_info_wait, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'tr')))
            WebDriverWait(
                user_info_wait, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.td.rank_coach span.ico_rank img')))

            # 요소 찾기
            user_info = user_info_wait.find_elements(By.CLASS_NAME, 'tr')
            user_ranks_url = user_info_wait.find_elements(
                By.CSS_SELECTOR, 'span.td.rank_coach span.ico_rank img')
            for user in user_info:
                info = user.text.split('\n')
                user_rank_num.append(info[0])
                user_lvs.append(info[1])
                user_names.append(info[2])
                user_prices.append(info[3].split(' ')[0])
                user_rank_scores.append(info[4])
            for user_rank in user_ranks_url:
                src = user_rank.get_attribute('src').split('/')[-1][4:-4]
                user_ranks.append(src)
            if i == 11:
                next_list_wait = WebDriverWait(
                    browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="inner"]/div[2]/div/a[3]')))
                browser.execute_script("arguments[0].click();", next_list_wait)
                break

            # 요소를 찾을 때까지 대기
            next_page_xpath = f'//*[@id="inner"]/div[2]/div/ul/li[{i}]/a'
            next_page_wait = WebDriverWait(
                browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, next_page_xpath)))

            # JavaScript를 사용하여 스크롤합니다.
            browser.execute_script("arguments[0].click();", next_page_wait)

        # 반복 횟수 증가
        tqdm.write(f"Processing iteration {current_iter + 1}/{total_iter}")
        current_iter += 1

    pbar = tqdm(range(len(user_names)))

    # rank mapping
    kor_rank = ['슈퍼챔피언스', '슈퍼챌린저', '챌린저1부', '챌린저2부',
                '챌린저3부', '월드클래스1부', '월드클래스2부', '월드클래스3부', '프로1부']
    kor_rank_dict = dict(zip(sorted(list(set(user_ranks))), kor_rank))
    fc = Fconline(api_key)
    ouid_ls = []
    for i in pbar:
        ouid_ls.append(fc.ouid(user_names[i]))

    # df으로 저장
    df = pd.DataFrame({
        'rankNo': user_rank_num,
        'LV': user_lvs,
        'nickName': user_names,
        'rankScore': user_rank_scores,
        'tier': user_ranks,
        'price': user_prices,
        'ouid': ouid_ls
    })

    df['korRankTier'] = df['tier'].map(kor_rank_dict)
    df = df.dropna()
    df.to_parquet(parquet_file_path, engine='pyarrow', index=False)
    f_date = datetime.now().strftime('%y/%M/%d T%H:%m:%S')
    return print(f"{f_date} 파일 적재 완료.")
