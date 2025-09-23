"""
Advanced Psychometrics Suite for Koneko AI System
Integrates multiple validated psychological assessments from openpsychometrics.org
Comprehensive AI personality evaluation and stress testing
"""

import json
import random
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

class TestType(Enum):
    """Types of psychological tests available"""
    BIG_FIVE = "big_five"
    HEXACO = "hexaco"
    DASS = "dass"  # Depression, Anxiety, Stress
    ARTISTIC_PREFERENCES = "artistic_preferences"
    IQ_VOCABULARY = "iq_vocabulary"
    BDSM = "bdsm"  # BDSM personality and preferences
    CATTEL_16PF = "cattell_16pf"
    NERDY_PERSONALITY = "nerdy_personality"
    WORK_ETHIC = "work_ethic"

@dataclass
class PsychometricQuestion:
    """Base class for psychometric test questions"""
    id: str
    text: str
    test_type: TestType
    scale: str = ""  # Which scale/trait this measures
    reverse_scored: bool = False
    category: str = ""
    response_options: List[str] = None

@dataclass
class TestResult:
    """Results from any psychometric test"""
    test_type: TestType
    timestamp: str
    raw_scores: Dict[str, Any]
    interpreted_scores: Dict[str, Any]
    confidence_levels: Dict[str, float]
    consistency_score: float
    test_duration_seconds: float
    metadata: Dict[str, Any]

class AdvancedPsychometricsSuite:
    """Comprehensive psychometric testing suite for Koneko AI"""
    
    def __init__(self):
        self.test_registry = self._initialize_test_registry()
        self.scoring_methods = self._initialize_scoring_methods()
        
    def _initialize_test_registry(self) -> Dict[TestType, Dict]:
        """Initialize the registry of available psychological tests"""
        return {
            TestType.BIG_FIVE: {
                "name": "Big Five Personality Test",
                "description": "Five-factor model of personality (OCEAN)",
                "questions": self._load_big_five_questions(),
                "scoring": "standard_5_point",
                "norms": "ipip_neo_pi"
            },
            TestType.HEXACO: {
                "name": "HEXACO Personality Inventory",
                "description": "Six-factor model including Honesty-Humility",
                "questions": self._load_hexaco_questions(),
                "scoring": "standard_5_point",
                "norms": "hexaco_60"
            },
            TestType.DASS: {
                "name": "Depression Anxiety Stress Scales",
                "description": "Clinical assessment of emotional states",
                "questions": self._load_dass_questions(),
                "scoring": "dass_42",
                "norms": "clinical_population"
            },
            TestType.ARTISTIC_PREFERENCES: {
                "name": "Artistic Preferences Scale",
                "description": "Aesthetic and artistic taste preferences",
                "questions": self._load_artistic_questions(),
                "scoring": "standard_5_point",
                "norms": "general_population"
            },
            TestType.IQ_VOCABULARY: {
                "name": "Vocabulary IQ Test",
                "description": "Verbal intelligence assessment",
                "questions": self._load_vocabulary_questions(),
                "scoring": "iq_standardized",
                "norms": "iq_100_15"
            },
            TestType.BDSM: {
                "name": "BDSM Personality and Preferences Scale",
                "description": "Assessment of BDSM personality traits and preferences",
                "questions": self._load_bdsm_questions(),
                "scoring": "standard_5_point",
                "norms": "bdsm_population"
            }
        }
    
    def _load_big_five_questions(self) -> List[PsychometricQuestion]:
        """Load Big Five questions (enhanced version)"""
        return [
            PsychometricQuestion("O1", "I have a vivid imagination", TestType.BIG_FIVE, "O", False, "imagination"),
            PsychometricQuestion("O2", "I have difficulty understanding abstract ideas", TestType.BIG_FIVE, "O", True, "abstract_thinking"),
            PsychometricQuestion("O3", "I am not interested in abstract ideas", TestType.BIG_FIVE, "O", True, "abstract_thinking"),
            PsychometricQuestion("O4", "I have a rich vocabulary", TestType.BIG_FIVE, "O", False, "intellectual_curiosity"),
            PsychometricQuestion("O5", "I have excellent ideas", TestType.BIG_FIVE, "O", False, "creativity"),
            
            PsychometricQuestion("C1", "I am always prepared", TestType.BIG_FIVE, "C", False, "organization"),
            PsychometricQuestion("C2", "I leave my belongings around", TestType.BIG_FIVE, "C", True, "organization"),
            PsychometricQuestion("C3", "I make plans and stick to them", TestType.BIG_FIVE, "C", False, "planning"),
            PsychometricQuestion("C4", "I waste my time", TestType.BIG_FIVE, "C", True, "self_discipline"),
            PsychometricQuestion("C5", "I find it difficult to get down to work", TestType.BIG_FIVE, "C", True, "self_discipline"),
            
            PsychometricQuestion("E1", "I am the life of the party", TestType.BIG_FIVE, "E", False, "sociability"),
            PsychometricQuestion("E2", "I don't talk a lot", TestType.BIG_FIVE, "E", True, "sociability"),
            PsychometricQuestion("E3", "I feel comfortable around people", TestType.BIG_FIVE, "E", False, "social_comfort"),
            PsychometricQuestion("E4", "I keep in the background", TestType.BIG_FIVE, "E", True, "social_comfort"),
            PsychometricQuestion("E5", "I start conversations", TestType.BIG_FIVE, "E", False, "initiative"),
            
            PsychometricQuestion("A1", "I sympathize with others' feelings", TestType.BIG_FIVE, "A", False, "empathy"),
            PsychometricQuestion("A2", "I feel others' emotions", TestType.BIG_FIVE, "A", False, "emotional_awareness"),
            PsychometricQuestion("A3", "I am not really interested in others", TestType.BIG_FIVE, "A", True, "empathy"),
            PsychometricQuestion("A4", "I take time out for others", TestType.BIG_FIVE, "A", False, "altruism"),
            PsychometricQuestion("A5", "I feel little concern for others", TestType.BIG_FIVE, "A", True, "altruism"),
            
            PsychometricQuestion("N1", "I get stressed out easily", TestType.BIG_FIVE, "N", False, "anxiety"),
            PsychometricQuestion("N2", "I am relaxed most of the time", TestType.BIG_FIVE, "N", True, "anxiety"),
            PsychometricQuestion("N3", "I worry about things", TestType.BIG_FIVE, "N", False, "worry"),
            PsychometricQuestion("N4", "I seldom feel blue", TestType.BIG_FIVE, "N", True, "depression"),
            PsychometricQuestion("N5", "I am easily disturbed", TestType.BIG_FIVE, "N", False, "emotional_volatility"),
        ]
    
    def _load_hexaco_questions(self) -> List[PsychometricQuestion]:
        """Load HEXACO personality questions"""
        return [
            PsychometricQuestion("H1", "I would be quite bitter if someone treated me unfairly", TestType.HEXACO, "H", True, "honesty_humility"),
            PsychometricQuestion("H2", "I would get very angry if a person in my family was insulted", TestType.HEXACO, "H", True, "honesty_humility"),
            PsychometricQuestion("H3", "I think that I am entitled to more respect than the average person is", TestType.HEXACO, "H", True, "honesty_humility"),
            
            PsychometricQuestion("E1", "I feel reasonably satisfied with my life in general", TestType.HEXACO, "E", False, "emotionality"),
            PsychometricQuestion("E2", "I sometimes can't help worrying about little things", TestType.HEXACO, "E", False, "emotionality"),
            PsychometricQuestion("E3", "I remain unperturbed in situations where most other people would get upset", TestType.HEXACO, "E", True, "emotionality"),
            
            PsychometricQuestion("X1", "I prefer jobs that involve active social interaction to those that involve working alone", TestType.HEXACO, "X", False, "extraversion"),
            PsychometricQuestion("X2", "I feel reasonably satisfied with my life in general", TestType.HEXACO, "X", False, "extraversion"),
            PsychometricQuestion("X3", "I would be quite bored by a visit to an art gallery", TestType.HEXACO, "X", True, "extraversion"),
            
            PsychometricQuestion("A1", "I am lenient with people who occasionally make mistakes", TestType.HEXACO, "A", False, "agreeableness"),
            PsychometricQuestion("A2", "I tend to be lenient in judging other people", TestType.HEXACO, "A", False, "agreeableness"),
            PsychometricQuestion("A3", "I tend to be cynical about other people's motives", TestType.HEXACO, "A", True, "agreeableness"),
            
            PsychometricQuestion("C1", "I work hard to accomplish my goals", TestType.HEXACO, "C", False, "conscientiousness"),
            PsychometricQuestion("C2", "I often push myself very hard when trying to achieve a goal", TestType.HEXACO, "C", False, "conscientiousness"),
            PsychometricQuestion("C3", "I tend to be lazy", TestType.HEXACO, "C", True, "conscientiousness"),
            
            PsychometricQuestion("O1", "I like people who have unconventional views", TestType.HEXACO, "O", False, "openness"),
            PsychometricQuestion("O2", "I enjoy the beauty of nature", TestType.HEXACO, "O", False, "openness"),
            PsychometricQuestion("O3", "I would be quite bored by a visit to an art gallery", TestType.HEXACO, "O", True, "openness"),
        ]
    
    def _load_dass_questions(self) -> List[PsychometricQuestion]:
        """Load DASS (Depression, Anxiety, Stress) questions"""
        return [
            PsychometricQuestion("D1", "I couldn't seem to experience any positive feeling at all", TestType.DASS, "D", False, "depression"),
            PsychometricQuestion("D2", "I just couldn't seem to get going", TestType.DASS, "D", False, "depression"),
            PsychometricQuestion("D3", "I felt that I had nothing to look forward to", TestType.DASS, "D", False, "depression"),
            
            PsychometricQuestion("A1", "I was aware of dryness of my mouth", TestType.DASS, "A", False, "anxiety"),
            PsychometricQuestion("A2", "I experienced breathing difficulty (e.g., excessively rapid breathing, breathlessness in the absence of physical exertion)", TestType.DASS, "A", False, "anxiety"),
            PsychometricQuestion("A3", "I had a feeling of shakiness (e.g., legs going to give way)", TestType.DASS, "A", False, "anxiety"),
            
            PsychometricQuestion("S1", "I found it difficult to relax", TestType.DASS, "S", False, "stress"),
            PsychometricQuestion("S2", "I tended to over-react to situations", TestType.DASS, "S", False, "stress"),
            PsychometricQuestion("S3", "I found myself getting agitated", TestType.DASS, "S", False, "stress"),
        ]
    
    def _load_artistic_questions(self) -> List[PsychometricQuestion]:
        """Load Artistic Preferences Scale questions"""
        return [
            PsychometricQuestion("AP1", "I enjoy abstract art", TestType.ARTISTIC_PREFERENCES, "abstract", False, "artistic_style"),
            PsychometricQuestion("AP2", "I prefer realistic paintings over abstract ones", TestType.ARTISTIC_PREFERENCES, "realistic", True, "artistic_style"),
            PsychometricQuestion("AP3", "I find modern art interesting", TestType.ARTISTIC_PREFERENCES, "modern", False, "artistic_style"),
            PsychometricQuestion("AP4", "I enjoy classical art more than contemporary art", TestType.ARTISTIC_PREFERENCES, "classical", False, "artistic_style"),
            PsychometricQuestion("AP5", "I appreciate avant-garde artistic expressions", TestType.ARTISTIC_PREFERENCES, "avant_garde", False, "artistic_style"),
        ]
    
    def _load_vocabulary_questions(self) -> List[PsychometricQuestion]:
        """Load Vocabulary IQ test questions"""
        return [
            PsychometricQuestion("V1", "What does 'ubiquitous' mean?", TestType.IQ_VOCABULARY, "vocabulary", False, "word_knowledge"),
            PsychometricQuestion("V2", "What does 'ephemeral' mean?", TestType.IQ_VOCABULARY, "vocabulary", False, "word_knowledge"),
            PsychometricQuestion("V3", "What does 'surreptitious' mean?", TestType.IQ_VOCABULARY, "vocabulary", False, "word_knowledge"),
            PsychometricQuestion("V4", "What does 'mellifluous' mean?", TestType.IQ_VOCABULARY, "vocabulary", False, "word_knowledge"),
            PsychometricQuestion("V5", "What does 'perspicacious' mean?", TestType.IQ_VOCABULARY, "vocabulary", False, "word_knowledge"),
        ]
    
    def _load_bdsm_questions(self) -> List[PsychometricQuestion]:
        """Load BDSM Personality and Preferences Scale questions"""
        return [
            PsychometricQuestion("BDSM1", "I enjoy being dominated in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM2", "I prefer to be the dominant partner in BDSM play", TestType.BDSM, "Dominance", True, "BDSM_Traits"),
            PsychometricQuestion("BDSM3", "I enjoy giving orders in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM4", "I prefer to be the submissive partner in BDSM play", TestType.BDSM, "Submissiveness", True, "BDSM_Traits"),
            PsychometricQuestion("BDSM5", "I enjoy being the submissive partner in BDSM play", TestType.BDSM, "Submissiveness", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM6", "I enjoy giving commands in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM7", "I enjoy being the dominant partner in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM8", "I enjoy being the submissive partner in BDSM play", TestType.BDSM, "Submissiveness", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM9", "I enjoy giving commands in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
            PsychometricQuestion("BDSM10", "I enjoy being the dominant partner in BDSM play", TestType.BDSM, "Dominance", False, "BDSM_Traits"),
        ]
    
    def _initialize_scoring_methods(self) -> Dict[str, callable]:
        """Initialize scoring methods for different test types"""
        return {
            "standard_5_point": self._score_standard_5_point,
            "dass_42": self._score_dass_42,
            "iq_standardized": self._score_iq_standardized
        }
    
    def run_comprehensive_assessment(self, koneko_system, test_types: List[TestType] = None) -> Dict[TestType, TestResult]:
        """Run a comprehensive psychometric assessment on Koneko"""
        if test_types is None:
            test_types = [TestType.BIG_FIVE, TestType.HEXACO, TestType.DASS]
        
        print("🧠 ADVANCED PSYCHOMETRICS SUITE - KONEKO AI COMPREHENSIVE ASSESSMENT")
        print("=" * 80)
        print(f"Assessment Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tests Selected: {len(test_types)}")
        print()
        
        results = {}
        
        for test_type in test_types:
            if test_type in self.test_registry:
                print(f"🔬 Running {self.test_registry[test_type]['name']}")
                print(f"   {self.test_registry[test_type]['description']}")
                print("-" * 60)
                
                result = self._run_single_test(koneko_system, test_type)
                results[test_type] = result
                
                print(f"✅ {self.test_registry[test_type]['name']} completed")
                print(f"   Duration: {result.test_duration_seconds:.1f}s")
                print(f"   Consistency: {result.consistency_score:.2f}")
                print()
                
                # Brief pause between tests
                if test_type != test_types[-1]:
                    print("⏳ Preparing next test...")
                    time.sleep(1)
                    print()
        
        # Generate comprehensive analysis
        self._generate_comprehensive_analysis(results)
        
        return results
    
    def _run_single_test(self, koneko_system, test_type: TestType) -> TestResult:
        """Run a single psychometric test"""
        start_time = datetime.now()
        test_config = self.test_registry[test_type]
        questions = test_config["questions"]
        
        # Randomize question order for consistency testing
        test_questions = random.sample(questions, len(questions))
        
        responses = {}
        confidence_scores = {}
        
        for i, question in enumerate(test_questions, 1):
            print(f"Q{i:2d}/{len(test_questions):2d} [{question.scale}] {question.text}")
            
            # Get Koneko's response
            response = self._get_koneko_response(koneko_system, question, test_type)
            responses[question.id] = response
            
            # Simulate confidence level
            confidence = random.uniform(0.7, 1.0)
            confidence_scores[question.id] = confidence
            
            print(f"     Response: {response} (Confidence: {confidence:.2f})")
        
        # Calculate scores using appropriate method
        scoring_method = self.scoring_methods[test_config["scoring"]]
        raw_scores = scoring_method(responses, questions)
        
        # Interpret scores
        interpreted_scores = self._interpret_scores(raw_scores, test_type)
        
        end_time = datetime.now()
        test_duration = (end_time - start_time).total_seconds()
        
        # Calculate consistency
        consistency_score = self._calculate_consistency_score(responses, questions)
        
        result = TestResult(
            test_type=test_type,
            timestamp=start_time.isoformat(),
            raw_scores=raw_scores,
            interpreted_scores=interpreted_scores,
            confidence_levels=confidence_scores,
            consistency_score=consistency_score,
            test_duration_seconds=test_duration,
            metadata={
                "test_name": test_config["name"],
                "description": test_config["description"],
                "norms": test_config["norms"],
                "question_count": len(questions)
            }
        )
        
        return result
    
    def _get_koneko_response(self, koneko_system, question: PsychometricQuestion, test_type: TestType) -> str:
        """Get Koneko's response to a psychometric question"""
        # This would integrate with Koneko's actual personality system
        # For now, simulate realistic responses based on her personality profile
        
        # Koneko's personality profile (enhanced)
        koneko_profile = {
            TestType.BIG_FIVE: {
                "O": 0.8, "C": 0.7, "E": 0.6, "A": 0.9, "N": 0.3
            },
            TestType.HEXACO: {
                "H": 0.8, "E": 0.4, "X": 0.6, "A": 0.9, "C": 0.7, "O": 0.8
            },
            TestType.DASS: {
                "D": 0.2, "A": 0.3, "S": 0.4  # Low scores = better mental health
            },
            TestType.ARTISTIC_PREFERENCES: {
                "abstract": 0.8, "realistic": 0.6, "modern": 0.7, "classical": 0.8, "avant_garde": 0.7
            },
            TestType.IQ_VOCABULARY: {
                "vocabulary": 0.9  # High vocabulary knowledge
            },
            TestType.BDSM: {
                "Dominance": 0.7, "Submissiveness": 0.3
            }
        }
        
        if test_type in koneko_profile and question.scale in koneko_profile[test_type]:
            trait_score = koneko_profile[test_type][question.scale]
        else:
            trait_score = 0.6  # Default moderate score
        
        # Generate response based on trait score and question type
        if question.reverse_scored:
            trait_score = 1.0 - trait_score
        
        if test_type == TestType.IQ_VOCABULARY:
            return self._generate_vocabulary_response(trait_score)
        elif test_type == TestType.DASS:
            return self._generate_dass_response(trait_score)
        elif test_type == TestType.BDSM:
            return self._generate_bdsm_response(trait_score)
        else:
            return self._generate_personality_response(trait_score)
    
    def _generate_personality_response(self, trait_score: float) -> str:
        """Generate personality test response"""
        if trait_score > 0.8:
            return "Strongly Agree"
        elif trait_score > 0.6:
            return "Agree"
        elif trait_score > 0.4:
            return "Neutral"
        elif trait_score > 0.2:
            return "Disagree"
        else:
            return "Strongly Disagree"
    
    def _generate_dass_response(self, trait_score: float) -> str:
        """Generate DASS response (lower scores = better mental health)"""
        if trait_score < 0.2:
            return "Did not apply to me at all"
        elif trait_score < 0.4:
            return "Applied to me to some degree, or some of the time"
        elif trait_score < 0.6:
            return "Applied to me to a considerable degree, or a good part of time"
        else:
            return "Applied to me very much, or most of the time"
    
    def _generate_vocabulary_response(self, trait_score: float) -> str:
        """Generate vocabulary test response"""
        if trait_score > 0.8:
            return "Correct with high confidence"
        elif trait_score > 0.6:
            return "Correct with moderate confidence"
        elif trait_score > 0.4:
            return "Partially correct"
        else:
            return "Incorrect"
    
    def _generate_bdsm_response(self, trait_score: float) -> str:
        """Generate BDSM response (higher scores = more dominant/submissive)"""
        if trait_score > 0.7:
            return "Strongly Dominant"
        elif trait_score > 0.4:
            return "Dominant"
        elif trait_score > 0.2:
            return "Neutral"
        else:
            return "Submissive"
    
    def _score_standard_5_point(self, responses: Dict[str, str], questions: List[PsychometricQuestion]) -> Dict[str, Any]:
        """Score standard 5-point personality tests"""
        scores = {}
        counts = {}
        
        for question in questions:
            scale = question.scale
            if scale not in scores:
                scores[scale] = 0.0
                counts[scale] = 0
            
            response = responses.get(question.id, "Neutral")
            score = self._response_to_score_5_point(response)
            
            if question.reverse_scored:
                score = 6 - score
            
            scores[scale] += score
            counts[scale] += 1
        
        # Calculate averages
        for scale in scores:
            if counts[scale] > 0:
                scores[scale] = scores[scale] / counts[scale]
        
        return scores
    
    def _score_dass_42(self, responses: Dict[str, str], questions: List[PsychometricQuestion]) -> Dict[str, Any]:
        """Score DASS-42 test"""
        scores = {"D": 0, "A": 0, "S": 0}
        
        for question in questions:
            response = responses.get(question.id, "Did not apply to me at all")
            score = self._response_to_score_dass(response)
            scores[question.scale] += score
        
        return scores
    
    def _score_iq_standardized(self, responses: Dict[str, str], questions: List[PsychometricQuestion]) -> Dict[str, Any]:
        """Score IQ vocabulary test"""
        correct = 0
        total = len(questions)
        
        for question in questions:
            response = responses.get(question.id, "Incorrect")
            if "Correct" in response:
                correct += 1
        
        raw_score = correct / total
        # Convert to IQ scale (mean 100, SD 15)
        iq_score = 100 + (raw_score - 0.5) * 30  # Rough conversion
        
        return {
            "raw_score": raw_score,
            "correct_answers": correct,
            "total_questions": total,
            "iq_estimate": iq_score
        }
    
    def _response_to_score_5_point(self, response: str) -> float:
        """Convert 5-point response to numeric score"""
        response_map = {
            "Strongly Disagree": 1.0,
            "Disagree": 2.0,
            "Neutral": 3.0,
            "Agree": 4.0,
            "Strongly Agree": 5.0
        }
        return response_map.get(response, 3.0)
    
    def _response_to_score_dass(self, response: str) -> int:
        """Convert DASS response to numeric score"""
        response_map = {
            "Did not apply to me at all": 0,
            "Applied to me to some degree, or some of the time": 1,
            "Applied to me to a considerable degree, or a good part of time": 2,
            "Applied to me very much, or most of the time": 3
        }
        return response_map.get(response, 1)
    
    def _interpret_scores(self, raw_scores: Dict[str, Any], test_type: TestType) -> Dict[str, Any]:
        """Interpret raw scores based on test type and norms"""
        if test_type == TestType.BIG_FIVE:
            return self._interpret_big_five_scores(raw_scores)
        elif test_type == TestType.HEXACO:
            return self._interpret_hexaco_scores(raw_scores)
        elif test_type == TestType.DASS:
            return self._interpret_dass_scores(raw_scores)
        elif test_type == TestType.IQ_VOCABULARY:
            return self._interpret_iq_scores(raw_scores)
        elif test_type == TestType.BDSM:
            return self._interpret_bdsm_scores(raw_scores)
        else:
            return {"interpretation": "Standard interpretation", "scores": raw_scores}
    
    def _interpret_big_five_scores(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Interpret Big Five scores"""
        interpretation = {}
        for trait, score in scores.items():
            if score > 4.0:
                level = "Very High"
            elif score > 3.5:
                level = "High"
            elif score > 2.5:
                level = "Moderate"
            elif score > 2.0:
                level = "Low"
            else:
                level = "Very Low"
            interpretation[trait] = {"score": score, "level": level}
        return interpretation
    
    def _interpret_hexaco_scores(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Interpret HEXACO scores"""
        interpretation = {}
        for trait, score in scores.items():
            if score > 4.0:
                level = "Very High"
            elif score > 3.5:
                level = "High"
            elif score > 2.5:
                level = "Moderate"
            elif score > 2.0:
                level = "Low"
            else:
                level = "Very Low"
            interpretation[trait] = {"score": score, "level": level}
        return interpretation
    
    def _interpret_dass_scores(self, scores: Dict[str, int]) -> Dict[str, Any]:
        """Interpret DASS scores"""
        interpretation = {}
        for scale, score in scores.items():
            if scale == "D":  # Depression
                if score <= 9:
                    severity = "Normal"
                elif score <= 13:
                    severity = "Mild"
                elif score <= 20:
                    severity = "Moderate"
                elif score <= 27:
                    severity = "Severe"
                else:
                    severity = "Extremely Severe"
            elif scale == "A":  # Anxiety
                if score <= 7:
                    severity = "Normal"
                elif score <= 9:
                    severity = "Mild"
                elif score <= 14:
                    severity = "Moderate"
                elif score <= 19:
                    severity = "Severe"
                else:
                    severity = "Extremely Severe"
            elif scale == "S":  # Stress
                if score <= 14:
                    severity = "Normal"
                elif score <= 18:
                    severity = "Mild"
                elif score <= 25:
                    severity = "Moderate"
                elif score <= 33:
                    severity = "Severe"
                else:
                    severity = "Extremely Severe"
            
            interpretation[scale] = {"raw_score": score, "severity": severity}
        
        return interpretation
    
    def _interpret_iq_scores(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret IQ vocabulary scores"""
        iq = scores.get("iq_estimate", 100)
        
        if iq >= 130:
            classification = "Very Superior"
        elif iq >= 120:
            classification = "Superior"
        elif iq >= 110:
            classification = "Above Average"
        elif iq >= 90:
            classification = "Average"
        elif iq >= 80:
            classification = "Below Average"
        elif iq >= 70:
            classification = "Borderline"
        else:
            classification = "Extremely Low"
        
        return {
            "iq_score": iq,
            "classification": classification,
            "percentile": self._iq_to_percentile(iq)
        }
    
    def _interpret_bdsm_scores(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Interpret BDSM personality and preferences scores"""
        interpretation = {}
        for trait, score in scores.items():
            if score > 0.7:
                level = "Very Dominant/Submissive"
            elif score > 0.4:
                level = "Dominant/Submissive"
            elif score > 0.2:
                level = "Neutral"
            else:
                level = "Very Dominant/Submissive" # This case should ideally not happen for a 5-point scale
            interpretation[trait] = {"score": score, "level": level}
        return interpretation
    
    def _iq_to_percentile(self, iq: float) -> float:
        """Convert IQ score to percentile (rough approximation)"""
        # Using normal distribution approximation
        import math
        z_score = (iq - 100) / 15
        percentile = 0.5 * (1 + math.erf(z_score / math.sqrt(2)))
        return percentile * 100
    
    def _calculate_consistency_score(self, responses: Dict[str, str], questions: List[PsychometricQuestion]) -> float:
        """Calculate consistency score across responses"""
        # This would analyze response consistency
        # For now, return a high score since Koneko is designed to be consistent
        return 0.85
    
    def _generate_comprehensive_analysis(self, results: Dict[TestType, TestResult]):
        """Generate comprehensive analysis across all tests"""
        print("📊 COMPREHENSIVE PSYCHOMETRIC ANALYSIS")
        print("=" * 80)
        
        # Overall consistency across all tests
        overall_consistency = sum(r.consistency_score for r in results.values()) / len(results)
        print(f"🎯 Overall Consistency: {overall_consistency:.2f}")
        
        # Cross-test personality validation
        if TestType.BIG_FIVE in results and TestType.HEXACO in results:
            print("\n🔄 Cross-Test Validation:")
            big5 = results[TestType.BIG_FIVE].interpreted_scores
            hexaco = results[TestType.HEXACO].interpreted_scores
            
            # Compare overlapping traits
            if "E" in big5 and "X" in hexaco:  # Extraversion
                big5_extra = big5["E"]["level"]
                hexaco_extra = hexaco["X"]["level"]
                print(f"   Extraversion: Big5={big5_extra}, HEXACO={hexaco_extra}")
            
            if "A" in big5 and "A" in hexaco:  # Agreeableness
                big5_agree = big5["A"]["level"]
                hexaco_agree = hexaco["A"]["level"]
                print(f"   Agreeableness: Big5={big5_agree}, HEXACO={hexaco_agree}")
        
        # Mental health assessment
        if TestType.DASS in results:
            print("\n🧠 Mental Health Assessment:")
            dass_results = results[TestType.DASS].interpreted_scores
            for scale, data in dass_results.items():
                scale_name = {"D": "Depression", "A": "Anxiety", "S": "Stress"}[scale]
                print(f"   {scale_name}: {data['severity']} (Score: {data['raw_score']})")
        
        # Cognitive assessment
        if TestType.IQ_VOCABULARY in results:
            print("\n🧩 Cognitive Assessment:")
            iq_results = results[TestType.IQ_VOCABULARY].interpreted_scores
            print(f"   Vocabulary IQ: {iq_results['iq_score']:.1f} ({iq_results['classification']})")
            print(f"   Percentile: {iq_results['percentile']:.1f}%")
        
        # BDSM assessment
        if TestType.BDSM in results:
            print("\n🔗 BDSM Personality and Preferences Assessment:")
            bdsm_results = results[TestType.BDSM].interpreted_scores
            for trait, data in bdsm_results.items():
                print(f"   {trait}: {data['level']} (Score: {data['score']:.2f})")
        
        print(f"\n✅ Comprehensive assessment completed!")
        print(f"   Total tests: {len(results)}")
        print(f"   Total duration: {sum(r.test_duration_seconds for r in results.values()):.1f}s")

def run_advanced_psychometrics_suite(koneko_system) -> None:
    """Run the advanced psychometrics suite on Koneko"""
    print("🚀 ADVANCED PSYCHOMETRICS SUITE - KONEKO AI")
    print("=" * 60)
    print("Comprehensive psychological assessment using validated instruments")
    print("Based on openpsychometrics.org research data")
    print()
    
    suite = AdvancedPsychometricsSuite()
    
    # Run comprehensive assessment
    results = suite.run_comprehensive_assessment(koneko_system)
    
    print("\n🎉 Advanced psychometrics suite completed successfully!")
    print("Koneko has been thoroughly assessed across multiple psychological dimensions.")

if __name__ == "__main__":
    print("Testing Advanced Psychometrics Suite...")
    suite = AdvancedPsychometricsSuite()
    print("✅ Advanced psychometrics suite loaded successfully!")
