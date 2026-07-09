// src/types/index.ts
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  scans_count: number;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ClassPrediction {
  class_name: string;
  confidence: number;
  risk_level: string;
}

export interface AnalysisResult {
  success: boolean;
  is_valid_image: boolean;
  prediction?: string;
  confidence?: number;
  risk_level?: string;          // <--- THIS IS THE LINE I MISSED BEFORE
  all_predictions?: ClassPrediction[];
  risk_assessment?: string;
  recommendations?: string[];
  error_message?: string;
  image_id?: string;
  analyzed_at?: string;
}

export interface HistoryItem {
  id: string;
  prediction: string;
  confidence: number;
  risk_level: string;
  image_filename: string;
  analyzed_at: string;
}