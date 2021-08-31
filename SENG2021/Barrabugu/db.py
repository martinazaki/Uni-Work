import os.path
import utils
import flask


def initialize():
    conn = utils.get_db()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE users
        (
            id INTEGER,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NULL, 
            is_sys_admin BOOLEAN NOT NULL DEFAULT false,
            PRIMARY KEY (id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE enrolments
        (
            user_id INTEGER,
            course_id INTEGER,
            team_id INTEGER,
            description VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE course_admins
        (
            user_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE courses
        (
            id INTEGER,
            slug VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL UNIQUE,
            frozen BOOLEAN DEFAULT false,
            team_cap INT NOT NULL DEFAULT 5,
            PRIMARY KEY (id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE teams
        (
            id INTEGER,
            name VARCHAR(255) NOT NULL,
            leader_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (leader_id) REFERENCES students(id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE applications
        (
            id INTEGER,
            target_team_id INTEGER NOT NULL,
            from_student_id INTEGER NOT NULL,
            seen BOOLEAN NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (target_team_id) REFERENCES teams(id),
            FOREIGN KEY (from_student_id) REFERENCES students(id),
            CONSTRAINT unique_applications UNIQUE (target_team_id, from_student_id)
        );
        """
    )
    cur.execute(
        """CREATE TABLE meetings
        (
            id INTEGER,
            course_id INTEGER NOT NULL,
            start_utc DATETIME NOT NULL,
            duration_minutes INTEGER NOT NULL,
            description VARCHAR(1024),
            PRIMARY KEY (id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """
    )
    conn.commit()
    conn.close()
