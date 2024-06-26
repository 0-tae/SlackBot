# Google-Calendar 슬랙봇

자료 조사 : 2023-12-26 ~ 2023-12-29

개발 기간 : 2024-01-02 ~ 2024-01-16

## 서비스 소개

### 개요

오늘의 일정 알림과 휴가 및 이벤트를 등록, 공유할 수 있는 슬랙봇 시스템입니다.

소스코드 : [https://github.com/0-tae/SlackBot.git](https://github.com/0-tae/SlackBot.git)

### 1) 메인 화면

메인 화면은 현재 사용 가능한 모든 기능들이 배치 되어 있으며,

 오늘 휴가자 목록과 일정 목록이 갱신 됩니다.

- 메인 화면 UI

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled.png)

### 2) 휴가 등록

멤버를 선택하여 자신의 캘린더에 휴가를 등록할 수 있습니다.

**연차**일 경우 **날짜의 기간**을, **반차** 혹은 **시간 연차**일 경우 **날짜와 시간**을 입력합니다.

**반차**의 경우, 입력한 시간대에 따라 다르게 기록됩니다 (ex. 시작시간 09:00 일 때, 오전 반차)

선택한 휴가 종류에 따라 아래의 시간 입력란이 변경됩니다. 

제출할 경우, 연동된 구글 캘린더에  추가됩니다.

- 연차 등록 UI
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%201.png)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%202.png)
    

- 반차, 시간 연차 등록 UI
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%203.png)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%204.png)
    

### 3) 이벤트 등록

일정을 입력해서 구글 캘린더에 등록합니다.

**하루 종일** 체크박스를 클릭 할 경우, 아래의 시간 선택란이 사라지고, 날짜만 입력 받을 수 있게 됩니다.

- 이벤트 입력 UI
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%205.png)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%206.png)
    

- 하루 종일 선택 시
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%207.png)
    

### 4) 오늘 일정 알림

슬랙봇으로 부터 오늘의 일정 메시지를 받을 수 있습니다.

시간은 09:00로 설정할 예정이며, 스크린샷은 17시 30분에 설정 하였습니다.

**유저별 알림 상세 설정**은 필요할 경우 기능을 추가할 예정입니다. 

- 일정 알림 메시지
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%208.png)
    

### 5) 일정 새로고침

새로 고침 버튼을 클릭하여 오늘의 일정을 갱신할 수 있습니다.

**연차**일 경우 시간을 명시하지 않고, **반차** 혹은 **시간 연차**일 경우 시간이 명시됩니다.

**특정 날짜의 일정 조회 및 갱신**은 필요할 경우 기능을 추가할 예정입니다. 

- 일정 새로 고침
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%209.png)
    

### 6) 이벤트 전파

**내 일정 전파하기** 버튼을 통해 다른 멤버나 채널에 이벤트를 전파할 수 있습니다. 

이때, 슬랙봇이 이벤트와 날짜를 요약하여 **해당 멤버 및 채널에게 메시지를 보냅니다.**

전파된 일정이 오늘 날짜인 경우, **(오늘)**이 명시됩니다.

**날짜를 선택**하면, 해당 날짜의 **스케줄이 우측 선택란에 모두 갱신** 됩니다.

만약 일정이 없을 경우 **오늘 일정 없음**이 표시 되며, 물론 전파할 수 있습니다.

멤버(복수 선택 가능)나 채널을 선택하여 **전파할 대상을 지정**할 수 있습니다. 

- 일정 전파하기 UI
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2010.png)
    

- 일정이 없을 경우
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2011.png)
    

- 슬랙봇 메시지 전파
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2012.png)
    

### 7) 전파된 일정 내 캘린더에 추가하기

누군가에게 일정을 전파 받았다면, **내 캘린더에 추가하기** 버튼을 통해 해당 일정을 자신의 캘린더에 추가할 수 있습니다.

현재는 별도의 진행 단계는 없고, 버튼을 누르면 바로 추가됩니다.

- 다른 사람의 일정 추가
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2013.png)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2014.png)
    

## 시스템 구성

슬랙봇 시스템의 전체적인 동작 흐름을 설명합니다.

### 시스템 구성 아키텍처

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2015.png)

## 서비스 시퀀스 다이어그램

각 서비스의 동작 흐름을 설명합니다.

### 1) 구글 로그인 연동

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2016.png)

### 2) 휴가 등록

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2017.png)

### 3) 이벤트 등록

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2018.png)

### 4) 새로 고침

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2019.png)

### 5) 이벤트 전파

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2020.png)

### 6) 전파된 이벤트 내 캘린더에 작성

![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2021.png)

## 고민 해봤던 점

- 도메인 필요 → ngrok으로 임시 도메인을 가져와서 해결
- 단 하나의 경로로 들어오는 액션 핸들링 (멀티 쓰레딩? 멀티 프로세싱?)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2022.png)
    
    ![Untitled](Google-Calendar%20%E1%84%89%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%A8%E1%84%87%E1%85%A9%E1%86%BA%20fd07e105dca745f5954426912e790b23/Untitled%2023.png)
    
- view의 생성, 수정을 편하게 하기 위한 코드의 재사용성 향상, JSON 데이터 처리로 인한 휴먼 에러 줄이기

## Todo (확장할 기능, 보완할 부분)

- UI와 안내 텍스트 수정 보완
- 유저별 알림 상세 설정 → DB 연동
- 특정 날짜의 일정 조회
- 자신의 캘린더로 가는 버튼 구현
- slash_command 등록 (ex) /create → 일정 생성 모달폼 띄움)
- 기타 예외 처리
- 기타 배포 관련 작업

- 코드 리뷰 받을 부분
    1. 패키지 분리, view.util, google_calendar_bot_controller, schduler, google api, slacks api의 배치
    2. 외부 API 사용 시, 데이터 전처리는 어디서 해주는지 (google_calendar_api, slackbot_api) 
    3. 캘린더 API를 이용할 때마다, google api의 인스턴스를 request한 유저마다 교체 해주어야 한다. 현재 토큰에 슬랙 유저 식별자를 남겨 토큰을 불러오고(ex. U2943921-token), 유저를 인자로 받아 인스턴스를 교체 중인데, 따로 처리 방법이 있는지? (google_calendar_api)
    4. 캐시를 구현하게 될 경우 식별자를 어떤 걸 사용하는지? (template_manager, modal_manager)
    5. 액션 핸들링(google_calendar_bot_controller)
