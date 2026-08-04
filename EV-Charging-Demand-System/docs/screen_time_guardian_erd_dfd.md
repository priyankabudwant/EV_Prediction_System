# Screen Time Guardian - ER Diagram and DFD

Based on `C:\Users\HP\Downloads\last_screen_time_guardian (1).zip`.

## ER Diagram

```mermaid
erDiagram
    USERS ||--o{ USAGE_DATA : logs
    USERS ||--o{ SESSIONS : starts
    USERS ||--o{ FOCUS_SESSIONS : creates
    USERS ||--o{ USER_LIMITS : sets

    USERS {
        string email PK
        string first_name
        string last_name
        string password_hash
        timestamp created_at
    }

    USAGE_DATA {
        int id PK
        string user_email FK
        string application_name
        string timestamp
        string start_time
        int duration
        boolean is_productive
        string category
        timestamp created_at
    }

    SESSIONS {
        int id PK
        string user_email FK
        string session_type
        string start_time
        string end_time
        int duration
        timestamp created_at
    }

    FOCUS_SESSIONS {
        int id PK
        string user_email FK
        string session_id UK
        string start_time
        int duration
        string session_type
        string blocked_apps
        boolean is_active
        timestamp created_at
    }

    USER_LIMITS {
        int id PK
        string user_email FK
        string application_name
        int daily_limit
        timestamp created_at
    }
```

## DFD Level 0 - Context Diagram

```mermaid
flowchart LR
    User[User]
    Tracker[Desktop Tracker]
    System((Screen Time Guardian System))
    DB[(SQLite Database)]

    User -->|Register/Login, view dashboard, set limits, start focus mode| System
    System -->|Analytics, alerts, productivity reports, focus status| User

    Tracker -->|Active app usage, duration, category| System
    System -->|Auth token, focus blocked apps/status| Tracker

    System <--> DB
```

## DFD Level 1 - Main Processes

```mermaid
flowchart TB
    User[User]
    Tracker[Desktop Tracker]

    P1((1. Authentication))
    P2((2. Usage Tracking))
    P3((3. Analytics & Reports))
    P4((4. Distraction Limits))
    P5((5. Focus Mode))
    P6((6. Security & Data Export))

    D1[(Users)]
    D2[(Usage Data)]
    D3[(Sessions)]
    D4[(User Limits)]
    D5[(Focus Sessions)]

    User -->|Registration/Login details| P1
    P1 -->|Token/Profile| User
    P1 <--> D1

    Tracker -->|Application name, start time, duration| P2
    User -->|Start/End tracking session| P2
    P2 --> D2
    P2 --> D3
    P2 -->|Tracking response| Tracker

    User -->|Dashboard, daily history, app analytics request| P3
    P3 -->|Read usage records| D2
    P3 -->|Read sessions| D3
    P3 -->|Charts, totals, productivity score, trends| User

    User -->|Daily app limit settings| P4
    P4 <--> D4
    P4 -->|Limit alerts/preferences| User

    User -->|Start/Stop focus session, blocked apps| P5
    Tracker -->|Focus status check| P5
    P5 <--> D5
    P5 -->|Blocked app list/status| Tracker
    P5 -->|Focus status| User

    User -->|Privacy settings, password change, export request| P6
    P6 -->|Read/update account| D1
    P6 -->|Read export data| D2
    P6 -->|Security response/export JSON| User
```

## Main Data Flow Summary

1. User registers or logs in.
2. Backend stores user details in `users` and returns a simple bearer token.
3. Desktop tracker detects the active application.
4. Tracker sends app name, duration, timestamp, productivity flag, and category to the backend.
5. Backend stores this in `usage_data`.
6. Dashboard and analytics pages read `usage_data` to show totals, trends, top apps, productivity score, and reports.
7. User can set distraction limits in `user_limits`.
8. User can start focus mode, stored in `focus_sessions`.
9. Tracker checks focus status and blocks matching apps during an active focus session.

## SFD - System Flow Diagram

```mermaid
flowchart TD
    Start([Start])
    OpenApp[Open Screen Time Guardian]
    HasAccount{User has account?}
    Register[Register User]
    Login[Login User]
    AuthCheck{Credentials valid?}
    Token[Generate Auth Token]
    Dashboard[Open Dashboard]

    StartTracking{Start tracking?}
    TrackerRun[Run Desktop Tracker]
    DetectApp[Detect Active Application]
    Classify[Classify App as Productive or Distracting]
    SendUsage[Send Usage Data to Backend]
    StoreUsage[(Store in Usage Data)]

    FocusChoice{Focus mode enabled?}
    SetFocus[Set Focus Duration and Blocked Apps]
    StoreFocus[(Store Focus Session)]
    CheckBlocked{Active app is blocked?}
    BlockApp[Close/Block Distracting App]
    ContinueTrack[Continue Monitoring]

    Analytics[Generate Dashboard Analytics]
    ShowReports[Show Reports, Charts, Trends, Productivity Score]
    LimitsChoice{Set daily app limits?}
    SaveLimits[(Store User Limits)]
    Alert[Show Limit Alerts]
    End([End])

    Start --> OpenApp
    OpenApp --> HasAccount
    HasAccount -- No --> Register
    Register --> Login
    HasAccount -- Yes --> Login
    Login --> AuthCheck
    AuthCheck -- No --> Login
    AuthCheck -- Yes --> Token
    Token --> Dashboard

    Dashboard --> StartTracking
    StartTracking -- Yes --> TrackerRun
    StartTracking -- No --> Analytics

    TrackerRun --> DetectApp
    DetectApp --> Classify
    Classify --> SendUsage
    SendUsage --> StoreUsage
    StoreUsage --> FocusChoice

    FocusChoice -- Yes --> SetFocus
    SetFocus --> StoreFocus
    StoreFocus --> CheckBlocked
    CheckBlocked -- Yes --> BlockApp
    BlockApp --> ContinueTrack
    CheckBlocked -- No --> ContinueTrack
    FocusChoice -- No --> ContinueTrack

    ContinueTrack --> DetectApp

    Dashboard --> LimitsChoice
    LimitsChoice -- Yes --> SaveLimits
    SaveLimits --> Alert
    LimitsChoice -- No --> Analytics
    Alert --> Analytics

    Analytics --> ShowReports
    ShowReports --> End
```
