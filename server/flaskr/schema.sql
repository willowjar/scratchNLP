DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  project_name TEXT NOT NULL,
  instructions TEXT NOT NULL,
  variables TEXT,
  lists TEXT,
  stacks TEXT,
  scripts TEXT
);
