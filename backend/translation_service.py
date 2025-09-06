# Translation Service for Lambalia - AI-powered with Google Translate backup
import os
import asyncio
import json
import hashlib
import time
import logging
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Import emergent integrations for AI translation
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Import Google Translate for backup
try:
    from google.cloud import translate_v2 as translate
    from google.oauth2 import service_account
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False
    logging.warning("Google Translate not available - will use AI-only translation")

load_dotenv()

class TranslationService:
    """
    Advanced translation service using AI-powered translation with Google Translate backup
    Supports real-time messaging translation and on-demand content translation
    """
    
    def __init__(self):
        self.emergent_llm_key = os.environ.get('EMERGENT_LLM_KEY')
        self.google_credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        self.google_credentials_json = os.environ.get('GOOGLE_TRANSLATE_CREDENTIALS_JSON')
        
        # Translation clients
        self.ai_chat = None
        self.google_client = None
        
        # Cache for translations (in-memory for now)
        self.translation_cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Usage tracking
        self.usage_stats = {
            'ai_translations': 0,
            'google_translations': 0,
            'cache_hits': 0,
            'total_requests': 0
        }
        
        # Supported languages
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ru': 'Russian',
            'tr': 'Turkish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'no': 'Norwegian',
            'da': 'Danish',
            'fi': 'Finnish',
            'pl': 'Polish',
            'cs': 'Czech',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'mt': 'Maltese',
            'el': 'Greek',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Filipino',
            'sw': 'Swahili',
            'he': 'Hebrew',
            'fa': 'Persian',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'pa': 'Punjabi',
            'or': 'Odia',
            'as': 'Assamese',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Myanmar',
            'km': 'Khmer',
            'lo': 'Lao',
            'ka': 'Georgian',
            'am': 'Amharic',
            'is': 'Icelandic',
            'ga': 'Irish',
            'cy': 'Welsh',
            'eu': 'Basque',
            'ca': 'Catalan',
            'gl': 'Galician',
            'mk': 'Macedonian',
            'sq': 'Albanian',
            'bs': 'Bosnian',
            'sr': 'Serbian',
            'mn': 'Mongolian',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'uz': 'Uzbek',
            'tg': 'Tajik',
            'az': 'Azerbaijani',
            'hy': 'Armenian',
            'be': 'Belarusian',
            'uk': 'Ukrainian',
            'lv': 'Latvian'
        }
    
    async def initialize(self):
        """Initialize translation services"""
        try:
            await self._initialize_ai_translation()
            if GOOGLE_TRANSLATE_AVAILABLE:
                await self._initialize_google_translate()
            logging.info("Translation service initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize translation service: {str(e)}")
            raise
    
    async def _initialize_ai_translation(self):
        """Initialize AI-powered translation using Emergent LLM"""
        if not self.emergent_llm_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        try:
            # Initialize AI chat for translation
            self.ai_chat = LlmChat(
                api_key=self.emergent_llm_key,
                session_id="translation_service",
                system_message="""You are a professional translator that specializes in preserving cultural authenticity while providing accurate translations. 

CRITICAL INSTRUCTIONS:
1. PRESERVE native dish names and cultural terms in their original language
2. Translate descriptions, instructions, and general content
3. When you encounter food names, recipe names, or cultural dishes, keep them in the original language and add the translation in parentheses if helpful
4. For example: "Paella (Spanish rice dish)" not "Spanish Rice Dish"
5. Maintain the emotional tone and cultural context of the original text
6. For cooking instructions, be precise and clear
7. Return ONLY the translated text, no explanations or additional commentary
8. If the text is already in the target language, return it unchanged

Examples:
- "I love making Biryani with my grandmother" → "Me encanta hacer Biryani con mi abuela" (preserving "Biryani")
- "This Coq au Vin recipe is amazing" → "Esta receta de Coq au Vin es increíble" (preserving "Coq au Vin")
"""
            ).with_model("openai", "gpt-4o-mini")
            
            # Test the connection
            test_message = UserMessage(text="Test connection")
            response = await self.ai_chat.send_message(test_message)
            logging.info("AI translation service connected successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize AI translation: {str(e)}")
            raise
    
    async def _initialize_google_translate(self):
        """Initialize Google Translate as backup service"""
        if not GOOGLE_TRANSLATE_AVAILABLE:
            logging.warning("Google Translate dependencies not available")
            return
        
        try:
            if self.google_credentials_path and os.path.exists(self.google_credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.google_credentials_path
                )
                self.google_client = translate.Client(credentials=credentials)
            elif self.google_credentials_json:
                credentials_dict = json.loads(self.google_credentials_json)
                credentials = service_account.Credentials.from_service_account_info(credentials_dict)
                self.google_client = translate.Client(credentials=credentials)
            else:
                logging.warning("No Google Translate credentials found - will use AI-only translation")
                return
            
            # Test connection
            test_result = await asyncio.to_thread(
                self.google_client.translate, "Hello", target_language="es"
            )
            logging.info("Google Translate backup service connected successfully")
            
        except Exception as e:
            logging.warning(f"Google Translate backup not available: {str(e)}")
            self.google_client = None
    
    def _generate_cache_key(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """Generate cache key for translation"""
        key_data = f"{text.strip()}:{target_lang}:{source_lang or 'auto'}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get translation from cache"""
        if cache_key in self.translation_cache:
            cached_item = self.translation_cache[cache_key]
            if time.time() - cached_item['timestamp'] < self.cache_ttl:
                return cached_item['data']
            else:
                del self.translation_cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, translation_data: Dict[str, Any]):
        """Save translation to cache"""
        self.translation_cache[cache_key] = {
            'data': translation_data,
            'timestamp': time.time()
        }
    
    async def translate_with_ai(self, text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
        """Translate text using AI with cultural preservation"""
        try:
            if not self.ai_chat:
                raise Exception("AI translation service not initialized")
            
            # Construct translation prompt
            source_lang_name = self.supported_languages.get(source_language, source_language) if source_language else "auto-detected language"
            target_lang_name = self.supported_languages.get(target_language, target_language)
            
            prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}.

REMEMBER: Preserve native dish names, recipe names, and cultural food terms in their original language.

Text to translate: "{text}"

Provide only the translation:"""
            
            message = UserMessage(text=prompt)
            response = await self.ai_chat.send_message(message)
            
            translated_text = response.strip()
            
            # Detect if the response contains unwanted explanations
            if "translation:" in translated_text.lower() or "here is" in translated_text.lower():
                # Extract just the translation part
                lines = translated_text.split('\n')
                for line in lines:
                    if line.strip() and not any(word in line.lower() for word in ['translation:', 'here is', 'the text', 'translates to']):
                        translated_text = line.strip()
                        break
            
            self.usage_stats['ai_translations'] += 1
            
            return {
                'success': True,
                'translated_text': translated_text,
                'method': 'ai',
                'source_language': source_language,
                'target_language': target_language,
                'character_count': len(text)
            }
            
        except Exception as e:
            logging.error(f"AI translation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'method': 'ai'
            }
    
    async def translate_with_google(self, text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
        """Translate text using Google Translate as backup"""
        try:
            if not self.google_client:
                raise Exception("Google Translate service not available")
            
            result = await asyncio.to_thread(
                self.google_client.translate,
                text,
                target_language=target_language,
                source_language=source_language
            )
            
            self.usage_stats['google_translations'] += 1
            
            return {
                'success': True,
                'translated_text': result['translatedText'],
                'method': 'google',
                'detected_language': result.get('detectedSourceLanguage'),
                'target_language': target_language,
                'character_count': len(text)
            }
            
        except Exception as e:
            logging.error(f"Google Translate failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'method': 'google'
            }
    
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None, preserve_cultural: bool = True) -> Dict[str, Any]:
        """
        Main translation method with AI primary and Google Translate backup
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            preserve_cultural: Whether to preserve cultural dish names (default: True)
        """
        request_id = f"req_{int(time.time() * 1000)}"
        start_time = time.time()
        
        # Input validation
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Empty text provided',
                'request_id': request_id
            }
        
        if target_language not in self.supported_languages:
            return {
                'success': False,
                'error': f'Unsupported target language: {target_language}',
                'request_id': request_id
            }
        
        text = text.strip()
        
        # Check cache first
        cache_key = self._generate_cache_key(text, target_language, source_language)
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result:
            self.usage_stats['cache_hits'] += 1
            self.usage_stats['total_requests'] += 1
            cached_result['cache_hit'] = True
            cached_result['request_id'] = request_id
            cached_result['processing_time_ms'] = (time.time() - start_time) * 1000
            return cached_result
        
        self.usage_stats['total_requests'] += 1
        
        # Try AI translation first (with cultural preservation if requested)
        if preserve_cultural:
            result = await self.translate_with_ai(text, target_language, source_language)
        else:
            # For non-cultural content, try Google first for speed
            result = await self.translate_with_google(text, target_language, source_language)
            if not result['success']:
                result = await self.translate_with_ai(text, target_language, source_language)
        
        # If AI fails, try Google Translate as backup
        if not result['success'] and preserve_cultural:
            logging.warning("AI translation failed, falling back to Google Translate")
            result = await self.translate_with_google(text, target_language, source_language)
        
        # If both fail, return error
        if not result['success']:
            return {
                'success': False,
                'error': 'Both AI and Google Translate services failed',
                'request_id': request_id,
                'processing_time_ms': (time.time() - start_time) * 1000
            }
        
        # Add metadata
        result.update({
            'cache_hit': False,
            'request_id': request_id,
            'processing_time_ms': (time.time() - start_time) * 1000,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Cache successful result
        self._save_to_cache(cache_key, result)
        
        return result
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text using AI or Google Translate"""
        try:
            # Try Google Translate for language detection first (more accurate)
            if self.google_client:
                result = await asyncio.to_thread(self.google_client.detect_language, text)
                return {
                    'success': True,
                    'detected_language': result['language'],
                    'confidence': result['confidence'],
                    'method': 'google'
                }
            
            # Fallback to AI detection
            if self.ai_chat:
                prompt = f"""Detect the language of the following text and respond with ONLY the ISO 639-1 language code (like 'en', 'es', 'fr', etc.):

Text: "{text[:200]}"

Language code:"""
                
                message = UserMessage(text=prompt)
                response = await self.ai_chat.send_message(message)
                detected_lang = response.strip().lower()
                
                # Validate the detected language
                if detected_lang in self.supported_languages:
                    return {
                        'success': True,
                        'detected_language': detected_lang,
                        'confidence': 0.85,  # Estimated confidence for AI detection
                        'method': 'ai'
                    }
            
            return {
                'success': False,
                'error': 'Language detection services not available'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def batch_translate(self, texts: List[str], target_language: str, source_language: Optional[str] = None, preserve_cultural: bool = True) -> Dict[str, Any]:
        """Translate multiple texts in batch"""
        if not texts:
            return {
                'success': False,
                'error': 'No texts provided for translation'
            }
        
        # Process translations concurrently
        tasks = [
            self.translate_text(text, target_language, source_language, preserve_cultural)
            for text in texts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        translations = []
        errors = []
        total_characters = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"Text {i}: {str(result)}")
            elif result['success']:
                translations.append(result)
                total_characters += result.get('character_count', 0)
            else:
                errors.append(f"Text {i}: {result.get('error', 'Unknown error')}")
        
        return {
            'success': len(errors) == 0,
            'translations': translations,
            'total_characters': total_characters,
            'total_texts': len(texts),
            'successful_translations': len(translations),
            'errors': errors
        }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get translation service usage statistics"""
        stats = self.usage_stats.copy()
        if stats['total_requests'] > 0:
            stats['cache_hit_rate'] = round((stats['cache_hits'] / stats['total_requests']) * 100, 2)
            stats['ai_usage_rate'] = round((stats['ai_translations'] / stats['total_requests']) * 100, 2)
            stats['google_usage_rate'] = round((stats['google_translations'] / stats['total_requests']) * 100, 2)
        else:
            stats['cache_hit_rate'] = 0
            stats['ai_usage_rate'] = 0
            stats['google_usage_rate'] = 0
        
        return stats
    
    async def cleanup(self):
        """Cleanup resources"""
        self.translation_cache.clear()
        logging.info("Translation service cleanup completed")

# Global translation service instance
translation_service = None

async def get_translation_service() -> TranslationService:
    """Get or create translation service instance"""
    global translation_service
    if translation_service is None:
        translation_service = TranslationService()
        await translation_service.initialize()
    return translation_service