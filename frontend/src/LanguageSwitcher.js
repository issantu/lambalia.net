import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = ({ className = '' }) => {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Extensive language list restored for global reach
  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'it', name: 'Italiano', flag: '🇮🇹' },
    { code: 'pt', name: 'Português', flag: '🇧🇷' },
    { code: 'ja', name: '日本語', flag: '🇯🇵' },
    { code: 'zh', name: '中文', flag: '🇨🇳' },
    { code: 'ar', name: 'العربية', flag: '🇸🇦' },
    { code: 'ru', name: 'Русский', flag: '🇷🇺' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'ko', name: '한국어', flag: '🇰🇷' }
  ];

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const changeLanguage = (langCode) => {
    i18n.changeLanguage(langCode);
    
    // Update document direction for RTL languages
    if (langCode === 'ar') {
      document.dir = 'rtl';
      document.body.style.fontFamily = 'Arial, sans-serif'; // Better Arabic font support
    } else {
      document.dir = 'ltr';
      document.body.style.fontFamily = '';
    }
    
    // Store language preference
    localStorage.setItem('lambalia-language', langCode);
    
    // Close dropdown after selection
    setIsOpen(false);
  };

  return (
    <div ref={dropdownRef} className={`relative inline-block text-left ${className}`} style={{ zIndex: 50000 }}>
      <div>
        <button
          type="button"
          onClick={toggleDropdown}
          className="inline-flex justify-center items-center px-2 py-1 text-xs font-medium text-gray-600 bg-white border border-gray-200 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-green-500"
          aria-expanded={isOpen}
          aria-haspopup="true"
        >
          <span className="mr-1 text-sm">{currentLanguage.flag}</span>
          <span className="hidden md:inline text-xs">{currentLanguage.name}</span>
          <span className="md:hidden text-xs">{currentLanguage.code.toUpperCase()}</span>
          <svg className={`ml-1 h-3 w-3 transform transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>

        {isOpen && (
          <div 
            className="absolute right-0 mt-1 w-44 rounded-md shadow-2xl bg-white ring-1 ring-black ring-opacity-10 transition-all duration-200 ease-in-out max-h-80 overflow-y-auto border border-gray-200" 
            style={{ 
              zIndex: 99999,
              position: 'absolute',
              top: '100%',
              right: 0
            }}
          >
            <div className="py-1" role="menu" aria-orientation="vertical">
              {languages.map((language) => (
                <button
                  key={language.code}
                  onClick={() => changeLanguage(language.code)}
                  className={`${
                    i18n.language === language.code
                      ? 'bg-green-100 text-green-900'
                      : 'text-gray-700 hover:bg-gray-100'
                  } group flex items-center px-3 py-2 text-xs w-full text-left transition-colors duration-150 focus:outline-none focus:bg-gray-100`}
                  role="menuitem"
                >
                  <span className="mr-2 text-sm">{language.flag}</span>
                  <span className="flex-1">{language.name}</span>
                  {i18n.language === language.code && (
                    <span className="ml-1 text-green-600">
                      <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LanguageSwitcher;