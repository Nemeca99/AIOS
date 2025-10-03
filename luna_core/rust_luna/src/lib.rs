use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::SystemTime;
use uuid::Uuid;
use regex::Regex;
use chrono::{DateTime, Utc};

/// Represents a Luna response with personality traits
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct LunaResponse {
    #[pyo3(get, set)]
    pub response: String,
    #[pyo3(get, set)]
    pub personality_trait: String,
    #[pyo3(get, set)]
    pub karma_score: f64,
    #[pyo3(get, set)]
    pub timestamp: f64,
    #[pyo3(get, set)]
    pub metadata: HashMap<String, String>,
}

#[pymethods]
impl LunaResponse {
    #[new]
    fn new(response: String, personality_trait: String, karma_score: f64) -> Self {
        Self {
            response,
            personality_trait,
            karma_score,
            timestamp: SystemTime::now()
                .duration_since(SystemTime::UNIX_EPOCH)
                .unwrap()
                .as_secs_f64(),
            metadata: HashMap::new(),
        }
    }
}

/// Represents a learning session result
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct LearningSessionResult {
    #[pyo3(get)]
    pub total_questions: usize,
    #[pyo3(get)]
    pub total_responses: usize,
    #[pyo3(get)]
    pub average_karma: f64,
    #[pyo3(get)]
    pub session_duration: f64,
    #[pyo3(get)]
    pub responses: Vec<LunaResponse>,
}

#[pymethods]
impl LearningSessionResult {
    #[new]
    fn new(total_questions: usize, total_responses: usize, average_karma: f64, session_duration: f64) -> Self {
        Self {
            total_questions,
            total_responses,
            average_karma,
            session_duration,
            responses: Vec::new(),
        }
    }
}

/// Main Luna Rust implementation
#[pyclass]
pub struct RustLunaCore {
    responses: Vec<LunaResponse>,
    total_interactions: u64,
    karma_history: Vec<f64>,
    personality_traits: HashMap<String, f64>,
}

#[pymethods]
impl RustLunaCore {
    #[new]
    fn new() -> Self {
        Self {
            responses: Vec::new(),
            total_interactions: 0,
            karma_history: Vec::new(),
            personality_traits: HashMap::new(),
        }
    }

    /// Generate a response with personality traits
    fn generate_response(&mut self, question: String, personality_trait: String, karma_score: f64) -> LunaResponse {
        self.total_interactions += 1;
        
        let response = LunaResponse::new(
            format!("Luna's response to: {}", question),
            personality_trait.clone(),
            karma_score
        );
        
        // Update personality traits
        let current_trait_value = self.personality_traits.get(&personality_trait).unwrap_or(&0.5);
        let new_trait_value = (current_trait_value + karma_score) / 2.0;
        self.personality_traits.insert(personality_trait, new_trait_value.clamp(0.0, 1.0));
        
        // Store response and karma
        self.responses.push(response.clone());
        self.karma_history.push(karma_score);
        
        response
    }

    /// Run a learning session with multiple questions
    fn run_learning_session(&mut self, questions: Vec<String>, traits: Vec<String>) -> LearningSessionResult {
        let start_time = SystemTime::now();
        
        if questions.len() != traits.len() {
            return LearningSessionResult::new(0, 0, 0.0, 0.0);
        }
        
        let mut responses = Vec::new();
        let mut total_karma = 0.0;
        
        for (question, personality_trait) in questions.iter().zip(traits.iter()) {
            // Generate karma score based on question complexity and trait
            let karma_score = self.calculate_karma_score(question, personality_trait);
            let response = self.generate_response(question.clone(), personality_trait.clone(), karma_score);
            
            total_karma += karma_score;
            responses.push(response);
        }
        
        let session_duration = start_time
            .duration_since(SystemTime::now())
            .unwrap_or_default()
            .as_secs_f64();
        
        let average_karma = if responses.is_empty() { 0.0 } else { total_karma / responses.len() as f64 };
        
        let mut result = LearningSessionResult::new(
            questions.len(),
            responses.len(),
            average_karma,
            session_duration
        );
        result.responses = responses;
        
        result
    }

    /// Calculate karma score based on question analysis
    fn calculate_karma_score(&self, question: &str, personality_trait: &str) -> f64 {
        let mut score = 0.5; // Base score
        
        // Analyze question complexity
        let word_count = question.split_whitespace().count();
        score += (word_count as f64 / 100.0).min(0.2); // Up to 0.2 bonus for complexity
        
        // Analyze emotional content
        let emotional_words = ["love", "hate", "happy", "sad", "angry", "excited", "worried"];
        let emotional_count = emotional_words.iter()
            .filter(|word| question.to_lowercase().contains(*word))
            .count();
        score += (emotional_count as f64 * 0.1).min(0.3); // Up to 0.3 bonus for emotion
        
        // Trait-specific adjustments
        match personality_trait {
            "openness" => score += 0.1,
            "conscientiousness" => score += 0.05,
            "extraversion" => score += 0.15,
            "agreeableness" => score += 0.1,
            "neuroticism" => score -= 0.05,
            _ => {}
        }
        
        score.clamp(0.0, 1.0)
    }

    /// Analyze emotional tone of text
    fn analyze_emotional_tone(&self, text: &str) -> String {
        let positive_words = ["happy", "good", "great", "wonderful", "amazing", "love", "joy"];
        let negative_words = ["sad", "bad", "terrible", "awful", "hate", "angry", "fear"];
        
        let positive_count = positive_words.iter()
            .filter(|word| text.to_lowercase().contains(*word))
            .count();
        let negative_count = negative_words.iter()
            .filter(|word| text.to_lowercase().contains(*word))
            .count();
        
        if positive_count > negative_count {
            "positive".to_string()
        } else if negative_count > positive_count {
            "negative".to_string()
        } else {
            "neutral".to_string()
        }
    }

    /// Classify question type
    fn classify_question_type(&self, question: &str) -> String {
        if question.contains("?") {
            "question".to_string()
        } else if question.contains("!") {
            "exclamation".to_string()
        } else if question.len() > 100 {
            "complex".to_string()
        } else {
            "simple".to_string()
        }
    }

    /// Get personality trait scores
    fn get_personality_traits(&self) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            let traits = PyDict::new(py);
            for (personality_trait, value) in &self.personality_traits {
                traits.set_item(personality_trait, value)?;
            }
            Ok(traits.into())
        })
    }

    /// Get system statistics
    fn get_stats(&self) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            let stats = PyDict::new(py);
            stats.set_item("total_interactions", self.total_interactions)?;
            stats.set_item("total_responses", self.responses.len())?;
            stats.set_item("average_karma", self.calculate_average_karma())?;
            stats.set_item("personality_traits", self.personality_traits.len())?;
            Ok(stats.into())
        })
    }

    /// Calculate average karma score
    fn calculate_average_karma(&self) -> f64 {
        if self.karma_history.is_empty() {
            0.0
        } else {
            self.karma_history.iter().sum::<f64>() / self.karma_history.len() as f64
        }
    }

    /// Get all responses
    fn get_all_responses(&self) -> Vec<LunaResponse> {
        self.responses.clone()
    }

    /// Clear all data
    fn clear_all(&mut self) {
        self.responses.clear();
        self.total_interactions = 0;
        self.karma_history.clear();
        self.personality_traits.clear();
    }
}

/// Python module definition
#[pymodule]
fn aios_luna_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<LunaResponse>()?;
    m.add_class::<LearningSessionResult>()?;
    m.add_class::<RustLunaCore>()?;
    Ok(())
}
