-- 1. Les Utilisateurs
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    body_weight REAL NOT NULL,
    height REAL NOT NULL,
    birthdate DATE NOT NULL
);

-- 2. Le Catalogue
CREATE TABLE Muscles (
    muscle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    faisceau TEXT
);

CREATE TABLE Exercices (
    exercice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    type TEXT CHECK(type IN ('barre', 'haltere', 'poids_corps')) NOT NULL
);

CREATE TABLE Exercices_Cible (
    exercice_id INTEGER,
    muscle_id INTEGER,
    role TEXT CHECK(role IN ('principal', 'secondaire')) NOT NULL,
    PRIMARY KEY (exercice_id, muscle_id),
    FOREIGN KEY (exercice_id) REFERENCES Exercices(exercice_id) ON DELETE CASCADE,
    FOREIGN KEY (muscle_id) REFERENCES Muscles(muscle_id) ON DELETE CASCADE
);

-- 3. La Planification
CREATE TABLE Splits (
    split_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE Seances_Planifiees (
    seance_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    split_id INTEGER NOT NULL,
    nom TEXT,
    FOREIGN KEY (split_id) REFERENCES Splits(split_id) ON DELETE CASCADE
);

CREATE TABLE Programmes_Exercices (
    programme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seance_plan_id INTEGER NOT NULL,
    exercice_id INTEGER NOT NULL,
    objectif_series INTEGER NOT NULL,
    FOREIGN KEY (seance_plan_id) REFERENCES Seances_Planifiees(seance_plan_id) ON DELETE CASCADE,
    FOREIGN KEY (exercice_id) REFERENCES Exercices(exercice_id) ON DELETE CASCADE
);

-- 4. L'Historique
CREATE TABLE Workout_Logs (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    seance_plan_id INTEGER NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (seance_plan_id) REFERENCES Seances_Planifiees(seance_plan_id) ON DELETE SET NULL
);

CREATE TABLE Sets_Realises (
    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercice_id INTEGER NOT NULL,
    numero_serie INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    charge REAL NOT NULL,
    rir INTEGER NOT NULL,
    FOREIGN KEY (workout_id) REFERENCES Workout_Logs(workout_id) ON DELETE CASCADE,
    FOREIGN KEY (exercice_id) REFERENCES Exercices(exercice_id) ON DELETE CASCADE
);