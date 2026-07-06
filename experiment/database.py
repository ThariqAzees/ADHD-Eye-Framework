import os
import sqlite3
import json
from typing import List, Dict, Any, Optional

DB_FILE = "experiment.db"

def get_db_path() -> str:
    """Returns the absolute path to the SQLite database file inside the experiment package."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, DB_FILE)

def get_connection() -> sqlite3.Connection:
    """Creates and returns a context-managed connection to the SQLite database with a timeout."""
    conn = sqlite3.connect(get_db_path(), timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes the database schema by creating required tables if they do not exist."""
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(get_db_path()), exist_ok=True)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Studies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studies (
                study_id TEXT PRIMARY KEY,
                study_name TEXT NOT NULL,
                version TEXT NOT NULL,
                calibration_protocol TEXT NOT NULL,
                practice_trials INTEGER NOT NULL,
                task_order TEXT NOT NULL,
                counterbalancing_enabled INTEGER NOT NULL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Participants Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT NOT NULL,
                study_id TEXT NOT NULL,
                age_group TEXT NOT NULL,
                vision_correction TEXT,
                dominant_hand TEXT,
                consent_obtained INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (participant_id, study_id),
                FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE
            )
        """)
        
        # 3. Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                participant_id TEXT NOT NULL,
                study_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT NOT NULL,
                browser TEXT,
                operating_system TEXT,
                screen_resolution TEXT,
                webcam_information TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (participant_id, study_id) REFERENCES participants(participant_id, study_id) ON DELETE CASCADE,
                FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE
            )
        """)
        
        # 4. Events Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                event_category TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()

# --- Studies CRUD ---

def insert_study(study_data: Dict[str, Any]) -> None:
    """Inserts a new study configuration into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO studies (
                study_id, study_name, version, calibration_protocol, 
                practice_trials, task_order, counterbalancing_enabled, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            study_data['study_id'],
            study_data['study_name'],
            study_data['version'],
            study_data['calibration_protocol'],
            study_data['practice_trials'],
            study_data['task_order'],
            1 if study_data['counterbalancing_enabled'] else 0,
            study_data.get('notes')
        ))
        conn.commit()

def get_study(study_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a study configuration by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM studies WHERE study_id = ?", (study_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_studies() -> List[Dict[str, Any]]:
    """Retrieves all study configurations in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM studies ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

# --- Participants CRUD ---

def insert_participant(part_data: Dict[str, Any]) -> None:
    """Inserts a new participant record into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO participants (
                participant_id, study_id, age_group, vision_correction, 
                dominant_hand, consent_obtained
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            part_data['participant_id'],
            part_data['study_id'],
            part_data['age_group'],
            part_data.get('vision_correction'),
            part_data.get('dominant_hand'),
            1 if part_data['consent_obtained'] else 0
        ))
        conn.commit()

def get_participant(participant_id: str, study_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a participant by ID within a specific study."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants WHERE participant_id = ? AND study_id = ?", (participant_id, study_id))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_participants_by_study(study_id: str) -> List[Dict[str, Any]]:
    """Retrieves all participants registered for a study."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants WHERE study_id = ? ORDER BY created_at DESC", (study_id,))
        return [dict(row) for row in cursor.fetchall()]

# --- Sessions CRUD ---

def insert_session(session_data: Dict[str, Any]) -> None:
    """Inserts a new session record into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (
                session_id, participant_id, study_id, start_time, status,
                browser, operating_system, screen_resolution, webcam_information
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data['session_id'],
            session_data['participant_id'],
            session_data['study_id'],
            session_data['start_time'],
            session_data['status'],
            session_data.get('browser'),
            session_data.get('operating_system'),
            session_data.get('screen_resolution'),
            session_data.get('webcam_information')
        ))
        conn.commit()

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a session record by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_session_status(session_id: str, status: str, end_time: Optional[str] = None) -> None:
    """Updates the status and optionally the end_time of a session."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if end_time:
            cursor.execute("UPDATE sessions SET status = ?, end_time = ? WHERE session_id = ?", (status, end_time, session_id))
        else:
            cursor.execute("UPDATE sessions SET status = ? WHERE session_id = ?", (status, session_id))
        conn.commit()

def update_session_device_info(session_id: str, device_data: Dict[str, Any]) -> None:
    """Updates client-side device/browser telemetry metadata for a session."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sessions 
            SET browser = ?, operating_system = ?, screen_resolution = ?, webcam_information = ? 
            WHERE session_id = ?
        """, (
            device_data.get('browser'),
            device_data.get('operating_system'),
            device_data.get('screen_resolution'),
            device_data.get('webcam_information'),
            session_id
        ))
        conn.commit()

def get_all_sessions() -> List[Dict[str, Any]]:
    """Retrieves all sessions across all studies."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, st.study_name 
            FROM sessions s 
            JOIN studies st ON s.study_id = st.study_id 
            ORDER BY s.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

# --- Events CRUD ---

def insert_event(session_id: str, timestamp: str, category: str, event_type: str, payload: Dict[str, Any]) -> None:
    """Inserts a structured interaction event log linked to a session."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Verify if session is closed to satisfy post-session security checks
        cursor.execute("SELECT status FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if row and row['status'] == "SESSION_CLOSED":
            # Session is closed, do not allow further logging
            return
            
        payload_str = json.dumps(payload) if payload else None
        cursor.execute("""
            INSERT INTO events (session_id, timestamp, event_category, event_type, payload)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, timestamp, category, event_type, payload_str))
        conn.commit()

def get_events_by_session(session_id: str) -> List[Dict[str, Any]]:
    """Retrieves all logs/events for a specific session."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d['payload'] = json.loads(d['payload']) if d['payload'] else {}
            result.append(d)
        return result
