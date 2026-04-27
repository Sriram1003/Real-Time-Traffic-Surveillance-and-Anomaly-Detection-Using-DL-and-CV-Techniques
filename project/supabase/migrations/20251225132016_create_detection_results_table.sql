/*
  # Create detection results table

  1. New Tables
    - `detection_results`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key to auth.users)
      - `video_name` (text)
      - `total_vehicles` (integer)
      - `detection_metrics` (jsonb with vehicle counts and metrics)
      - `created_at` (timestamp)
  
  2. Security
    - Enable RLS on `detection_results` table
    - Add policy for authenticated users to read their own results
    - Add policy for authenticated users to create results
    - Add policy for authenticated users to delete their own results
*/

CREATE TABLE IF NOT EXISTS detection_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  video_name text NOT NULL,
  total_vehicles integer NOT NULL DEFAULT 0,
  detection_metrics jsonb NOT NULL DEFAULT '{"cars": 0, "bikes": 0, "trucks": 0, "buses": 0}',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE detection_results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own detection results"
  ON detection_results
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own detection results"
  ON detection_results
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own detection results"
  ON detection_results
  FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS detection_results_user_id_idx ON detection_results(user_id);
CREATE INDEX IF NOT EXISTS detection_results_created_at_idx ON detection_results(created_at);
