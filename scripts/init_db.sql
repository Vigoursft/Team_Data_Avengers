CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  display_name TEXT NOT NULL,
  primary_role TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS achievements (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  role TEXT NOT NULL,
  raw_text TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS star_stories (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  achievement_id INT REFERENCES achievements(id),
  situation TEXT, 
  task TEXT, 
  action TEXT, 
  result TEXT,
  full_text TEXT,
  tokens_input INT DEFAULT 0,
  tokens_output INT DEFAULT 0,
  model_used TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS interview_questions (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  achievement_id INT REFERENCES achievements(id),
  role TEXT,
  question_text TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS interview_answers (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  question_id INT REFERENCES interview_questions(id),
  answer_text TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  answer_id INT REFERENCES interview_answers(id),
  rubric JSONB,
  summary TEXT,
  suggestions TEXT,
  tokens_input INT DEFAULT 0,
  tokens_output INT DEFAULT 0,
  model_used TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS token_usage (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  feature TEXT,                              -- 'STAR', 'QUESTIONS', 'FEEDBACK'
  model_used TEXT,
  prompt_tokens INT,
  completion_tokens INT,
  total_tokens INT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_token_usage_created ON token_usage(created_at);
CREATE INDEX IF NOT EXISTS idx_token_usage_feature ON token_usage(feature);